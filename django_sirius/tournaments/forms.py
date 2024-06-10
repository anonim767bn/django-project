from django import forms
from django.db.models import Model
from .models import Tournament, Match, Place, Team
from typing import Type


def get_form(model_: Type[Model], fields_: str = '__all__', exclude_: list = ['owner', 'id']) -> Type[forms.ModelForm]:
    class Form(forms.ModelForm):
        class Meta:
            model = model_
            fields = fields_
            exclude = exclude_

    return Form


TournamentForm: Type[forms.ModelForm] = get_form(Tournament, exclude_=['owner', 'id', 'teams'])
MatchForm: Type[forms.ModelForm] = get_form(Match)
PlaceForm: Type[forms.ModelForm] = get_form(Place)
TeamForm: Type[forms.ModelForm] = get_form(Team, exclude_=['owner', 'id', 'tournaments'])
