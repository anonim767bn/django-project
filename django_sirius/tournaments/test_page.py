from django.contrib.auth.models import User
from django.test import TestCase
from .models import Tournament, Team, Place, Match
from django.utils import timezone
import datetime
from typing import Callable
from django.urls import reverse


def add_test_page(page_name: str, used_templates: tuple = ('base.html',),
                  entity_attr: str | None = None) -> Callable:
    def decorator(cls) -> type:
        def test_page(self):
            response = self.client.get(
                reverse(page_name) if not(entity_attr)
                else reverse(page_name, args=[getattr(self, entity_attr).id])
            )
            self.assertEqual(response.status_code, 200)
            for template in used_templates:
                self.assertTemplateUsed(response, template)
        setattr(cls, f'test_page_{page_name}', test_page)
        return cls
    return decorator


@add_test_page('main_page', ('main.html',), None)
@add_test_page('tournaments', ('list.html',), None)
@add_test_page('teams', ('list.html',), None)
@add_test_page('places', ('list.html',), None)
@add_test_page('matches', ('list.html',), None)
@add_test_page('tournament', ('entity.html',), 'tournament')
@add_test_page('team', ('entity.html',), 'team1')
@add_test_page('place', ('entity.html',), 'place')
@add_test_page('match', ('entity.html',), 'match')
@add_test_page('login', ('login.html',), None)
@add_test_page('register', ('register.html',), None)
class TestPage(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='12345')
        self.tournament = Tournament.objects.create(
            title='tournament',
            owner=self.user,
            start='2021-01-01',
            end='2021-01-02'
        )
        self.team1 = Team.objects.create(
            title='team', owner=self.user, founding='2021-01-01'
        )
        self.team2 = Team.objects.create(
            title='team', owner=self.user, founding='2021-01-01'
        )
        self.place = Place.objects.create(title='place', owner=self.user)
        date_time = timezone.make_aware(datetime.datetime(2021, 1, 1))
        self.match = Match.objects.create(
            tournament=self.tournament,
            team1=self.team1,
            team2=self.team2,
            place=self.place,
            owner=self.user,
            match_date_time=date_time
        )
