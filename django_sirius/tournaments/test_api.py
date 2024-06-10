from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from tournaments.models import Tournament, Team, Place, Match
from django.urls import reverse
from django.db.utils import IntegrityError
from typing import Callable
from rest_framework.test import APIClient


def add_null_field_test(path: str, field_name: str, creation_attrs: dict) -> Callable:
    def decorator(cls) -> type:
        def test_null_fields(self):
            creation_attrs_copy = creation_attrs.copy()
            creation_attrs_copy[field_name] = ''
            response = self.client.post(reverse(path), creation_attrs_copy)
            self.assertEqual(response.status_code, 400, )
            self.assertIn(field_name, response.data)
        setattr(cls, f'test_null_{field_name}', test_null_fields)
        return cls
    return decorator


def add_permission_test(path: str, creation_attrs: dict) -> Callable:
    def decorator(cls) -> type:
        def test_permission(self):
            response = self.client.post(reverse(path), creation_attrs)
            id = response.data['id']
            self.client2 = APIClient()
            self.user2 = User.objects.create_user(
                'testuser2', password='12345', )
            self.token2 = Token.objects.create(user=self.user2)
            self.client2.credentials(
                HTTP_AUTHORIZATION='Token ' + self.token2.key)
            response = self.client2.get(f'{reverse(path)}{id}/')
            self.assertEqual(response.status_code, 200)
            response = self.client2.put(
                f'{reverse(path)}{id}/', creation_attrs)
            self.assertEqual(response.status_code, 403)
        setattr(cls, 'test_permission', test_permission)
        return cls
    return decorator


def add_test_created(model, path: str, creation_attrs: dict) -> Callable:
    def decorator(cls) -> type:
        def test_created(self):
            response = self.client.post(reverse(path), creation_attrs)
            self.assertEqual(response.status_code, 201)
            self.assertIn('id', response.data)
            self.assertIn(response.data['id'], [str(obj.id)
                          for obj in model.objects.all()])
        setattr(cls, 'test_created', test_created)
        return cls
    return decorator


class SetUpMixin(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='12345', )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


@add_permission_test('api:team-list', {'title': 'team1', 'founding': '2000-01-01'})
@add_test_created(Team, 'api:team-list', {'title': 'team1', 'founding': '2000-01-01'})
@add_null_field_test('api:team-list', 'title', {'title': '', 'founding': '2000-01-01'})
@add_null_field_test('api:team-list', 'founding', {'title': 'team1', 'founding': ''})
class TeamTestCase(SetUpMixin):

    def test_future_founding_date(self):
        response = self.client.post(
            reverse('api:team-list'), {'title': 'team1', 'founding': '3000-01-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_past_founding_date(self):
        response = self.client.post(
            reverse('api:team-list'), {'title': 'team1', 'founding': '2000-01-01'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@add_permission_test('api:tournament-list', {'title': 'tournament1', 'start': '2021-01-01', 'end': '2022-01-01'})
@add_test_created(Tournament, 'api:tournament-list', {'title': 'tournament1', 'start': '2021-01-01', 'end': '2022-01-01'})
@add_null_field_test('api:tournament-list', 'title', {'title': '', 'start': '2021-01-01', 'end': '2022-01-01'})
@add_null_field_test('api:tournament-list', 'start', {'title': 'tournament1', 'start': '', 'end': '2022-01-01'})
@add_null_field_test('api:tournament-list', 'end', {'title': 'tournament1', 'start': '2021-01-01', 'end': ''})
class TournamentTestCase(SetUpMixin):
    def test_start_later_then_end(self):
        with self.assertRaises(IntegrityError):
            self.client.post(reverse(
                'api:tournament-list'), {'title': 'tournament1', 'start': '2022-01-01', 'end': '2021-01-01'})


@add_permission_test('api:place-list', {'title': 'place1', 'address': 'address1'})
@add_test_created(Place, 'api:place-list', {'title': 'place1', 'address': 'address1'})
@add_null_field_test('api:place-list', 'title', {'title': '', 'address': 'address1'})
class PlaceTestCase(SetUpMixin):
    def test_create_place(self):
        response = self.client.post(
            reverse('api:place-list'), {'title': 'place1', 'address': 'address1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@add_null_field_test('api:match-list', 'match_date_time', {'match_date_time': ''})
class MatchTestCase(SetUpMixin):
    def setUp(self):
        super().setUp()
        self.team1_id = self.client.post(reverse('api:team-list'), {
            'title': 'team1', 'founding': '2000-01-01'}).data['id']
        self.team2_id = self.client.post(reverse('api:team-list'), {
            'title': 'team2', 'founding': '2000-01-01'}).data['id']
        self.place_id = self.client.post(reverse('api:place-list'), {
            'title': 'place', 'address': 'city'}).data['id']
        self.place_id = self.client.post(reverse('api:place-list'), {
            'title': 'place', 'address': 'city'}).data['id']
        self.tournament_id = self.client.post(reverse('api:tournament-list'), {
            'title': 'tournament', 'start': '2020-01-01', 'end': '2020-01-10'}).data['id']

    def test_create_match(self):
        response = self.client.post(reverse('api:match-list'), {
            'tournament': self.tournament_id,
            'team1': self.team1_id,
            'team2': self.team2_id,
            'place': self.place_id,
            'match_date_time': '2021-01-01 12:00:00'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_team1_ne_team2(self):
        with self.assertRaises(IntegrityError):
            response = self.client.post(reverse('api:match-list'), {
                'tournament': self.tournament_id,
                'team1': self.team1_id,
                'team2': self.team1_id,
                'place': self.place_id,
                'match_date_time': '2021-01-01 12:00:00'
            })
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
