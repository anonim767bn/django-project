"""Forms for the tournaments app."""
from typing import Optional, Type

from django import forms
from django.db.models import Model

from .models import Match, Place, Team, Tournament


def get_form(
    just_model: Type[Model],
    just_fields: Optional[str] = '__all__',
    just_exclude: Optional[tuple] = ('owner', 'id'),
) -> Type[forms.ModelForm]:
    """Get a form for a model.

    Args:
        just_model (Type[Model]): Model.
        just_fields (str, optional): fields. Defaults to '__all__'.
        just_exclude (list, optional): exclude. Defaults to ['owner', 'id'].

    Returns:
        Type[forms.ModelForm]: Form for the model.
    """
    class Form(forms.ModelForm):
        class Meta:
            model = just_model
            fields = just_fields
            exclude = just_exclude

    return Form


TournamentForm: Type[forms.ModelForm] = get_form(
    Tournament,
    just_exclude=['owner', 'id', 'teams'],
)
MatchForm: Type[forms.ModelForm] = get_form(Match)
PlaceForm: Type[forms.ModelForm] = get_form(Place)
TeamForm: Type[forms.ModelForm] = get_form(
    Team,
    just_exclude=['owner', 'id', 'tournaments'],
)
