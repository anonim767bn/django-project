from django.db import models
from uuid import uuid4
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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


class Team(UUIDmixin):
    title = models.TextField(_('title'), null=True, blank=True)
    founding = models.DateField(
        _('founding'), null=True, blank=True, validators=[check_founding])
    tournaments = models.ManyToManyField(
        'Tournament', verbose_name=_('tournaments'), through='TournamentTeam')

    class Meta:
        db_table = '"tournament"."team"'
        ordering = ['founding']
        verbose_name = _('team')
        verbose_name_plural = _('teams')

    def __str__(self) -> str:
        return self.title


class Tournament(UUIDmixin):
    title = models.TextField(_('title'), null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    start = models.DateField(_('start'), null=True, blank=True)
    end = models.DateField(_('end'), null=True, blank=True)
    teams = models.ManyToManyField(
        'Team', verbose_name=_('teams'), through='TournamentTeam')

    def __str__(self):
        return self.title

    class Meta:
        db_table = '"tournament"."tournament"'
        ordering = ['start']
        verbose_name = _('tournament')
        verbose_name_plural = _('tournaments')
        constraints = [
            models.CheckConstraint(
                check=models.Q(start__lte=models.F('end')),
                name='start_lte_end'
            )
        ]


class TournamentTeam(models.Model):
    tournament = models.ForeignKey(Tournament, verbose_name=_(
        'tournament id'), on_delete=models.CASCADE)
    team = models.ForeignKey(Team, verbose_name=_(
        'team id'), on_delete=models.CASCADE)

    class Meta:
        db_table = '"tournament"."tournament_team"'
        ordering = ['tournament']
        verbose_name = _('relationship tournament team')
        verbose_name_plural = _('relationships tournament teams')
        unique_together = (
            ('tournament', 'team')
        )


class Match(UUIDmixin):
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

    place = models.TextField('place', null=True, blank=True)
    match_date_time = models.DateTimeField(
        _('match date and time'), null=True, blank=True)

    class Meta:
        db_table = '"tournament"."match"'
        ordering = ['match_date_time']
        verbose_name = _('match')
        verbose_name_plural = _('matches')
        unique_together = (
            ('tournament_id', 'team1_id', 'team2_id', 'match_date_time')
        )
        constraints = [
            models.CheckConstraint(check=~models.Q(
                team1_id=models.F('team2_id')), name='team1_ne_team2')
        ]
