from django.contrib import admin
from .models import Tournament, Team, Match, TournamentTeam

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','description', 'start', 'end')
    readonly_fields = ('id',)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'founding')
    readonly_fields = ('id',)


class MatchAdmin(admin.ModelAdmin):
    list_display = ('id','team1_id', 'team2_id', 'tournament_id', 'place', 'match_date_time')
    readonly_fields = ('id',)



admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(TournamentTeam)