from django import forms
from pichr.models import *

class SearchForm(forms.Form):
    injury_type = forms.ModelChoiceField(
        queryset=InjuryType.objects.all(),
        empty_label=None,
        required=False
    )

    location = forms.ModelChoiceField(
        queryset=InjuryLocation.objects.filter(root=True),
        empty_label="All Areas",
        required=False
    )

    