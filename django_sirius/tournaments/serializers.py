"""Serializers for the tournaments app."""
from typing import Type

from django.db.models import Model
from rest_framework import serializers

from .models import Match, Place, Team, Tournament


def get_serializer(
    just_model: Type[Model],
) -> Type[serializers.ModelSerializer]:
    """Get a serializer for a model.

    Args:
        just_model (Type[Model]): The model.

    Returns:
        Type[serializers.ModelSerializer]: Serializer for the model.
    """
    class Serializer(serializers.ModelSerializer):
        owner = serializers.ReadOnlyField(source='owner.username')

        class Meta:
            model = just_model
            fields = '__all__'

    return Serializer


TournamentSerializer = get_serializer(Tournament)
MatchSerializer = get_serializer(Match)
TeamSerializer = get_serializer(Team)
PlaceSerializer = get_serializer(Place)
