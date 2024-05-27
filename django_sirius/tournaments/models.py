from django.db import models
from uuid import uuid4
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


def check_founding(dt: date) -> None:
    if dt > date.today():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'founding': dt}
        )


class UUIDmixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=True)

    class Meta:
        abstract = True


class OwnerMixin(models.Model):
    owner = models.ForeignKey(User, verbose_name=_(
        'user'), on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Team(UUIDmixin, OwnerMixin):
    title = models.TextField(_('title'), null=False, blank=False)
    founding = models.DateField(
        _('founding'), null=False, blank=False, validators=[check_founding])
    tournaments = models.ManyToManyField(
        'Tournament', verbose_name=_('tournaments'), through='TournamentTeam')

    class Meta:
        db_table = 'team'
        ordering = ['founding']
        verbose_name = _('team')
        verbose_name_plural = _('teams')

    def __str__(self) -> str:
        return f'command {self.title} founded {self.founding}'


class Tournament(UUIDmixin, OwnerMixin):
    title = models.TextField(_('title'), null=False, blank=False)
    description = models.TextField(_('description'), null=True, blank=True)
    start = models.DateField(_('start'), null=False, blank=False)
    end = models.DateField(_('end'), null=False, blank=False)
    teams = models.ManyToManyField(
        'Team', verbose_name=_('teams'), through='TournamentTeam')

    def __str__(self):
        return f' tournament {self.title} from {self.start} to {self.end}'

    class Meta:
        db_table = 'tournament'
        ordering = ['start']
        verbose_name = _('tournament')
        verbose_name_plural = _('tournaments')
        constraints = [
            models.CheckConstraint(
                check=models.Q(start__lte=models.F('end')),
                name='start_lte_end'
            )
        ]


class TournamentTeam(UUIDmixin, OwnerMixin):
    tournament = models.ForeignKey(Tournament, verbose_name=_(
        'tournament id'), on_delete=models.CASCADE)
    team = models.ForeignKey(Team, verbose_name=_(
        'team id'), on_delete=models.CASCADE)

    class Meta:
        db_table = 'tournament_team'
        ordering = ['tournament']
        verbose_name = _('relationship tournament team')
        verbose_name_plural = _('relationships tournament teams')
        unique_together = (
            ('tournament', 'team')
        )


class Place(UUIDmixin, OwnerMixin):
    title = models.TextField(_('title'), null=False, blank=False)
    address = models.TextField(_('address'), null=False, blank=False)

    class Meta:
        db_table = 'place'
        ordering = ['title']
        verbose_name = _('place')
        verbose_name_plural = _('places')

    def __str__(self):
        return f'place {self.title} address {self.address}'


class Match(UUIDmixin, OwnerMixin):
    tournament_id = models.ForeignKey(
        Tournament,
        verbose_name=_('tournament id'),
        on_delete=models.CASCADE,
    )
    team1_id = models.ForeignKey(
        Team,
        verbose_name=_('team 1'),
        on_delete=models.CASCADE,
        related_name='mathces_as_team_1',
    )
    team2_id = models.ForeignKey(
        Team,
        verbose_name=_('team 2'),
        on_delete=models.CASCADE,
        related_name='mathces_as_team_2',
    )

    place_id = models.ForeignKey(
        Place,
        verbose_name=_('place'),
        on_delete=models.CASCADE,
    )
    match_date_time = models.DateTimeField(
        _('match date and time'), null=False, blank=False)

    class Meta:
        db_table = 'match'
        ordering = ['match_date_time']
        verbose_name = _('match')
        verbose_name_plural = _('matches')
        unique_together = (
            ('tournament_id', 'team1_id', 'team2_id', 'match_date_time', 'place_id')
        )
        constraints = [
            models.CheckConstraint(check=~models.Q(
                team1_id=models.F('team2_id')), name='team1_ne_team2')
        ]
