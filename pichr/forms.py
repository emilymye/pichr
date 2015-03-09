from django import forms
from pichr.models import *

class SearchForm(forms.Form):
    injury_type = forms.ModelChoiceField(
        queryset=SCTMorphology.objects.all(),
        empty_label=None,
        required=False
    )

    injObects = SCTInjury.objects.all().values("finding_site__sctid")
    
    idset = [inj['finding_site__sctid'] for inj in injObects]
    location = forms.ModelChoiceField(
        queryset=SCTBodyStructure.objects.filter(sctid__in=idset),
        empty_label="All Areas",
        required=False
    )

    injury = forms.ModelChoiceField(
        queryset=SCTInjury.objects.all(),
        empty_label="Choose a specific injury",
        required=False
    )