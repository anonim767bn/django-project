"""Tests for API."""
from typing import Callable

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from tournaments.models import Place, Team, Tournament

from .config import TEST_PASSWORD

STR_MATCH_DATE_TIME = 'match_date_time'
STR_START = 'start'
STR_END = 'end'
STR_ADDRESS = 'address'
STR_ID = 'id'
STR_TITLE = 'title'
STR_FOUNDING = 'founding'
TEAM_LIST = 'api:team-list'
TOURNAMENT_LIST = 'api:tournament-list'
PLACE_LIST = 'api:place-list'


def add_null_field_test(
    path: str,
    field_name: str,
    creation_attrs: dict,
) -> Callable:
    """Add null field test to class.

    Args:
        path (str): path.
        field_name (str): field that shouldn't be null.
        creation_attrs (dict): attributes for creation.

    Returns:
        Callable: decorator.
    """
    def decorator(cls) -> type:
        def test_null_fields(self):
            creation_attrs_copy = creation_attrs.copy()
            creation_attrs_copy[field_name] = ''
            response = self.client.post(reverse(path), creation_attrs_copy)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field_name, response.data)

        setattr(cls, f'test_null_{field_name}', test_null_fields)
        return cls

    return decorator


def add_permission_test(
    path: str,
    creation_attrs: dict,
) -> Callable:
    """Add permission test to class.

    Args:
        path (str): path.
        creation_attrs (dict): attributes for creation.

    Returns:
        Callable: decorator.
    """
    def decorator(cls) -> type:
        def test_permission(self):
            response = self.client.post(reverse(path), creation_attrs)
            id_ = response.data[STR_ID]
            self.client2 = APIClient()
            self.user2 = User.objects.create_user(
                'testuser2', password=TEST_PASSWORD,
            )
            self.token2 = Token.objects.create(user=self.user2)
            token2_key = self.token2.key
            self.client2.credentials(
                HTTP_AUTHORIZATION=f'Token {token2_key}',
            )
            reverse_path = reverse(path)
            response = self.client2.get(f'{reverse_path}{id_}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response = self.client2.put(
                f'{reverse_path}{id_}/',
                creation_attrs,
            )
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        cls.test_permission = test_permission
        return cls

    return decorator


def add_test_created(model: type, path: str, creation_attrs: dict) -> Callable:
    """Add creation test to class.

    Args:
        model (type): model class.
        path (str): path.
        creation_attrs (dict): attributes for creation.

    Returns:
        Callable: decorator.
    """
    def decorator(cls) -> type:
        def test_created(self):
            response = self.client.post(reverse(path), creation_attrs)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn(STR_ID, response.data)
            self.assertIn(
                response.data[STR_ID],
                [str(object_.id) for object_ in model.objects.all()],
            )

        cls.test_created = test_created
        return cls

    return decorator


class SetUpMixin(APITestCase):
    """Mixin to add setup for test cases."""

    def setUp(self):
        """Set up for test case."""
        self.user = User.objects.create_user(
            'testuser',
            password=TEST_PASSWORD,
        )
        self.token = Token.objects.create(user=self.user)
        token_key = self.token.key
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token_key}',
        )


@add_permission_test(
    TEAM_LIST,
    {
        STR_TITLE: 'teeam_1',
        STR_FOUNDING: '2000-01-02',
    },
)
@add_test_created(
    Team,
    TEAM_LIST,
    {
        STR_TITLE: 'teeam1',
        STR_FOUNDING: '2000-03-01',
    },
)
@add_null_field_test(
    TEAM_LIST,
    STR_TITLE,
    {
        STR_TITLE: '',
        STR_FOUNDING: '2000-01-05',
    },
)
@add_null_field_test(
    TEAM_LIST,
    STR_FOUNDING,
    {
        STR_TITLE: 'teeam1',
        STR_FOUNDING: '',
    },
)
class TeamTestCase(SetUpMixin):
    """Test case for Team model."""

    def test_future_founding_date(self):
        """Test future founding date."""
        response = self.client.post(
            reverse(TEAM_LIST),
            {STR_TITLE: 'teeam1', STR_FOUNDING: '3000-01-01'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_past_founding_date(self):
        """Test past founding date."""
        response = self.client.post(
            reverse(TEAM_LIST),
            {STR_TITLE: 'teeeam1', STR_FOUNDING: '2001-01-01'},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@add_permission_test(
    TOURNAMENT_LIST,
    {
        STR_TITLE: 'tournameent1',
        STR_START: '2021-01-02',
        STR_END: '2022-01-02',
    },
)
@add_test_created(
    Tournament,
    TOURNAMENT_LIST,
    {
        STR_TITLE: 'touurnament1',
        STR_START: '2021-01-03',
        STR_END: '2022-01-03',
    },
)
@add_null_field_test(
    TOURNAMENT_LIST,
    STR_TITLE,
    {STR_TITLE: '', STR_START: '2021-01-06', STR_END: '2023-01-01'},
)
@add_null_field_test(
    TOURNAMENT_LIST,
    STR_START,
    {STR_TITLE: 'tournament1', STR_START: '', STR_END: '2022-01-01'},
)
@add_null_field_test(
    TOURNAMENT_LIST,
    STR_END,
    {STR_TITLE: 'tournament1', STR_START: '2021-08-01', STR_END: ''},
)
class TournamentTestCase(SetUpMixin):
    """Test case for Tournament model."""

    def test_start_later_then_end(self):
        """Test start date later than end date."""
        with self.assertRaises(IntegrityError):
            self.client.post(
                reverse(TOURNAMENT_LIST),
                {
                    STR_TITLE: 'tournament1',
                    STR_START: '2022-01-01',
                    STR_END: '2019-01-01',
                },
            )


@add_permission_test(
    PLACE_LIST,
    {STR_TITLE: 'place1', STR_ADDRESS: 'addresstest1'},
)
@add_test_created(
    Place,
    PLACE_LIST,
    {STR_TITLE: 'place1', STR_ADDRESS: 'address1'},
)
@add_null_field_test(
    PLACE_LIST,
    STR_TITLE,
    {STR_TITLE: '', STR_ADDRESS: 'addresstest1'},
)
class PlaceTestCase(SetUpMixin):
    """Test case for Place model."""

    def test_create_place(self):
        """Test create place."""
        response = self.client.post(
            reverse(PLACE_LIST),
            {STR_TITLE: 'place1', STR_ADDRESS: 'address1'},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@add_null_field_test(
    'api:match-list',
    STR_MATCH_DATE_TIME,
    {STR_MATCH_DATE_TIME: ''},
)
class MatchTestCase(SetUpMixin):
    """Test case for Match model."""

    def setUp(self):
        """Set up for MatchTestCase."""
        super().setUp()
        self.team1_id = self.client.post(
            reverse(TEAM_LIST),
            {STR_TITLE: 'team_1', STR_FOUNDING: '2000-01-01'},
        ).data[STR_ID]
        self.team2_id = self.client.post(
            reverse(TEAM_LIST),
            {STR_TITLE: 'team2', STR_FOUNDING: '2000-01-01'},
        ).data[STR_ID]
        self.place_id = self.client.post(
            reverse(PLACE_LIST),
            {STR_TITLE: 'place', STR_ADDRESS: 'city'},
        ).data[STR_ID]
        self.tournament_id = self.client.post(
            reverse(TOURNAMENT_LIST),
            {
                STR_TITLE: 'tournament',
                STR_START: '2020-01-01',
                STR_END: '2020-01-10',
            },
        ).data[STR_ID]

    def test_create_match(self):
        """Test create match."""
        response = self.client.post(
            reverse('api:match-list'),
            {
                'tournament': self.tournament_id,
                'team1': self.team1_id,
                'team2': self.team2_id,
                'place': self.place_id,
                STR_MATCH_DATE_TIME: '2021-01-01 12:00:00',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_team1_ne_team2(self):
        """Test that team_1 and team_2 are different."""
        with self.assertRaises(IntegrityError):
            response = self.client.post(
                reverse('api:match-list'),
                {
                    'tournament': self.tournament_id,
                    'team1': self.team1_id,
                    'team2': self.team1_id,
                    'place': self.place_id,
                    STR_MATCH_DATE_TIME: '2021-01-01 12:00:00',
                },
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
