from rest_framework import serializers
from .models import Tournament, Match, Team, Place


def get_serializer(model_):
    class Serializer(serializers.ModelSerializer):
        owner = serializers.ReadOnlyField(source='owner.username')

        class Meta:
            model = model_
            fields = '__all__'
    return Serializer

TournamentSerializer = get_serializer(Tournament)
MatchSerializer = get_serializer(Match)
TeamSerializer = get_serializer(Team)
PlaceSerializer = get_serializer(Place)