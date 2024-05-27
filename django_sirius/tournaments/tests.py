from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from tournaments.models import Tournament, Team, Place, Match
from django.urls import reverse
from django.db.utils import IntegrityError


def add_setup(cls: type) -> type:
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='12345', )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    cls.setUp = setUp
    return cls

class TeamTestCase(APITestCase):
    def test_create_team(self):
        response = self.client.post(
            reverse('team-list'), {'title': 'team1', 'founding': '2000-01-01'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn(response.data['id'], [str(team.id)
                      for team in Team.objects.all()], )

    def test_future_founding_date(self):
        response = self.client.post(
            reverse('team-list'), {'title': 'team1', 'founding': '3000-01-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_past_founding_date(self):
        response = self.client.post(
            reverse('team-list'), {'title': 'team1', 'founding': '2000-01-01'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_empty_title(self):
        response = self.client.post(
            reverse('team-list'), {'title': '', 'founding': '2000-01-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_founding(self):
        response = self.client.post(
            reverse('team-list'), {'title': 'team1', 'founding': ''})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@add_setup
class TournamentTestCase(APITestCase):
    def test_start_later_then_end(self):
        with self.assertRaises(IntegrityError):
            self.client.post(reverse(
                'tournament-list'), {'title': 'tournament1', 'start': '2022-01-01', 'end': '2021-01-01'})


@add_setup
class PlaceTestCase(APITestCase):
    def test_create_place(self):
        response = self.client.post(
            reverse('place-list'), {'title': 'place1', 'address': 'address1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
