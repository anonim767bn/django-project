"""Models for tournaments app."""
from datetime import date
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

STR_TITLE = 'title'
STR_TOURNAMENT = 'tournament'


def check_founding(dt: date) -> None:
    """Check if date is bigger than current date.

    Args:
        dt (date): date to check.

    Raises:
        ValidationError: if date is bigger than current date.
    """
    if dt > date.today():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'founding': dt},
        )


class UUIDmixin(models.Model):
    """Mixin for models with UUID primary key."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=True,
    )

    class Meta:
        abstract = True


class OwnerMixin(models.Model):
    """Mixin for models with owner field."""

    owner = models.ForeignKey(
        User,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class Team(UUIDmixin, OwnerMixin):
    """Team model."""

    title = models.TextField(_(STR_TITLE), null=False, blank=False)
    founding = models.DateField(
        _('founding'),
        null=False,
        blank=False,
        validators=[check_founding],
    )
    tournaments = models.ManyToManyField(
        'Tournament',
        verbose_name=_('tournaments'),
        through='TournamentTeam',
    )

    class Meta:
        db_table = 'team'
        ordering = ['founding']
        verbose_name = _('team')
        verbose_name_plural = _('teams')

    def __str__(self) -> str:
        """Get string representation of the Team.

        Returns:
            str: in format 'title'.
        """
        return f'{self.title}'


class Tournament(UUIDmixin, OwnerMixin):
    """Tournament model."""

    title = models.TextField(_(STR_TITLE), null=False, blank=False)
    description = models.TextField(_('description'), null=True, blank=True)
    start = models.DateField(_('start'), null=False, blank=False)
    end = models.DateField(_('end'), null=False, blank=False)
    teams = models.ManyToManyField(
        'Team',
        verbose_name=_('teams'),
        through='TournamentTeam',
    )

    def __str__(self) -> str:
        """Get string representation of the Tournament.

        Returns:
            str: in format 'title'.
        """
        return f'{self.title}'

    class Meta:
        db_table = STR_TOURNAMENT
        ordering = ['start']
        verbose_name = _(STR_TOURNAMENT)
        verbose_name_plural = _('tournaments')
        constraints = [
            models.CheckConstraint(
                check=models.Q(start__lte=models.F('end')),
                name='start_lte_end',
            ),
        ]


class TournamentTeam(UUIDmixin, OwnerMixin):
    """Tournament-team relationship model."""

    tournament = models.ForeignKey(
        Tournament,
        verbose_name=_('tournament id'),
        on_delete=models.CASCADE,
    )
    team = models.ForeignKey(
        Team,
        verbose_name=_('team id'),
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'tournament_team'
        ordering = [STR_TOURNAMENT]
        verbose_name = _('relationship tournament team')
        verbose_name_plural = _('relationships tournament teams')
        unique_together = (
            (STR_TOURNAMENT, 'team')
        )


class Place(UUIDmixin, OwnerMixin):
    """Place model."""

    title = models.TextField(_(STR_TITLE), null=False, blank=False)
    address = models.TextField(_('address'), null=False, blank=False)

    class Meta:
        db_table = 'place'
        ordering = [STR_TITLE]
        verbose_name = _('place')
        verbose_name_plural = _('places')

    def __str__(self) -> str:
        """Get string representation of the Place.

        Returns:
            str: in format 'title'.
        """
        return f'{self.title}'


class Match(UUIDmixin, OwnerMixin):
    """Match model."""

    tournament = models.ForeignKey(
        Tournament,
        verbose_name=_('tournament id'),
        on_delete=models.CASCADE,
    )
    team1 = models.ForeignKey(
        Team,
        verbose_name=_('team 1'),
        on_delete=models.CASCADE,
        related_name='mathces_as_team_1',
    )
    team2 = models.ForeignKey(
        Team,
        verbose_name=_('team 2'),
        on_delete=models.CASCADE,
        related_name='mathces_as_team_2',
    )

    place = models.ForeignKey(
        Place,
        verbose_name=_('place'),
        on_delete=models.CASCADE,
    )
    match_date_time = models.DateTimeField(
        _('match date and time'),
        null=False,
        blank=False,
    )

    class Meta:
        db_table = 'match'
        ordering = ['match_date_time']
        verbose_name = _('match')
        verbose_name_plural = _('matches')
        unique_together = (
            (
                'tournament_id',
                'team1_id',
                'team2_id',
                'match_date_time',
                'place_id',
            ),
        )
        constraints = [
            models.CheckConstraint(
                check=~models.Q(
                    team1_id=models.F('team2_id'),
                ),
                name='team1_ne_team2',
            ),
        ]

    def __str__(self) -> str:
        """Get string representation of the Match.

        Returns:
            str: in format 'team1 vs team2'.
        """
        team1 = self.team1.title
        team2 = self.team2.title
        return f'{team1} vs {team2}'
