"""Admin module for tournaments app."""
from django.contrib import admin

from .models import Match, Place, Team, Tournament, TournamentTeam

ID = 'id'


class TournamentAdmin(admin.ModelAdmin):
    """Tournament admin."""

    list_display = (ID, 'title', 'description', 'start', 'end')
    readonly_fields = (ID,)


class TeamAdmin(admin.ModelAdmin):
    """Team admin."""

    list_display = (ID, 'title', 'founding')
    readonly_fields = (ID,)


class MatchAdmin(admin.ModelAdmin):
    """Team admin."""

    list_display = (
        ID,
        'team1_id',
        'team2_id',
        'tournament_id',
        'place_id',
        'match_date_time',
    )
    readonly_fields = (ID,)


class TournamentTeamAdmin(admin.ModelAdmin):
    """TournamentTeam admin."""

    list_display = (ID, 'tournament_id', 'team_id')
    readonly_fields = (ID,)


class PlaceAdmin(admin.ModelAdmin):
    """Place admin."""

    list_display = (ID, 'title', 'address')
    readonly_fields = (ID,)


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(TournamentTeam, TournamentTeamAdmin)
admin.site.register(Place, PlaceAdmin)
