"""Test pages."""
import datetime
from typing import Callable, Optional

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from .config import TEST_PASSWORD
from .models import Match, Place, Team, Tournament

LIST_HTML_TEMPLATE = 'list.html'
ENTITY_HTML_TEMPLATE = 'entity.html'


def add_test_page(
    page_name: str,
    used_templates: Optional[tuple] = ('base.html',),
    entity_attr: str | None = None,
) -> Callable:
    """Adding a test page to a class.

    Args:
        page_name (str): The name of the page.
        used_templates (tuple, optional): The templates used by the page.\
            Defaults to ('base.html',).
        entity_attr (str | None, optional): The entity attribute.\
            Defaults to None.

    Returns:
        Callable: The decorator.
    """
    def decorator(cls) -> type:
        def test_page(self):
            response = self.client.get(
                reverse(
                    viewname=page_name,
                    args=[getattr(self, entity_attr).id],
                ),
            ) if entity_attr else self.client.get(reverse(page_name))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            for template in used_templates:
                self.assertTemplateUsed(response, template)
        setattr(cls, f'test_page_{page_name}', test_page)
        return cls
    return decorator


@add_test_page('main_page', ('main.html',), None)
@add_test_page('tournaments', (LIST_HTML_TEMPLATE,), None)
@add_test_page('teams', (LIST_HTML_TEMPLATE,), None)
@add_test_page('places', (LIST_HTML_TEMPLATE,), None)
@add_test_page('matches', (LIST_HTML_TEMPLATE,), None)
@add_test_page('tournament', (ENTITY_HTML_TEMPLATE,), 'tournament')
@add_test_page('team', (ENTITY_HTML_TEMPLATE,), 'team1')
@add_test_page('place', (ENTITY_HTML_TEMPLATE,), 'place')
@add_test_page('match', (ENTITY_HTML_TEMPLATE,), 'match')
@add_test_page('login', ('login.html',), None)
@add_test_page('register', ('register.html',), None)
class TestPage(TestCase):
    """Test pages."""

    def setUp(self):
        """Set up."""
        self.user = User.objects.create_user(
            'testuser',
            password=TEST_PASSWORD,
        )
        self.tournament = Tournament.objects.create(
            title='tournament',
            owner=self.user,
            start='2021-01-01',
            end='2021-01-02',
        )
        self.team1 = Team.objects.create(
            title='team', owner=self.user, founding='2021-01-01',
        )
        self.team2 = Team.objects.create(
            title='team', owner=self.user, founding='2021-01-01',
        )
        self.place = Place.objects.create(title='place', owner=self.user)
        year = 2021
        date_time = timezone.make_aware(datetime.datetime(year, 1, 1))
        self.match = Match.objects.create(
            tournament=self.tournament,
            team1=self.team1,
            team2=self.team2,
            place=self.place,
            owner=self.user,
            match_date_time=date_time,
        )
