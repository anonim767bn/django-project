from rest_framework import serializers
from django.db.models import Model
from .models import Tournament, Match, Team, Place
from typing import Type


def get_serializer(model_: Type[Model]) -> Type[serializers.ModelSerializer]:
    class Serializer(serializers.ModelSerializer):
        owner = serializers.ReadOnlyField(source='owner.username')

        class Meta:
            model = model_
            fields = '__all__'

    return Serializer


TournamentSerializer: Type[serializers.ModelSerializer] = \
    get_serializer(Tournament)
MatchSerializer: Type[serializers.ModelSerializer] = \
    get_serializer(Match)
TeamSerializer: Type[serializers.ModelSerializer] = \
    get_serializer(Team)
PlaceSerializer: Type[serializers.ModelSerializer] = \
    get_serializer(Place)
