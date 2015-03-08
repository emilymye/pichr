from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from pichr.models import *
from pichr.forms import *
from pichr.solver import analyze

def index(request):
    return search(request)

def search(request):

    payload = {
        'title': 'Search PICHR'
    }
    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            # injuries = Injury.objects.filter(location)
            type_f = [o.pk for o in InjuryType.objects.all()]
            loc_f = [l.pk for l in InjuryLocation.objects.all()]
            filters = form.cleaned_data

            q_text = ""
            if filters["injury_type"] != None and filters["injury_type"].sctid != 19130008:
                tpe = filters["injury_type"]

                type_f = [tpe.sctid]
                q_text = " with type %s" % tpe.name

            if filters["location"] != None:
                loc = filters["location"]
                q_text += " affecting the %s" % loc.name.lower()
                loc_f = [desc['sctid'] for desc in loc.descendants.all().values("sctid").distinct()]
                loc_f.append(loc.sctid)

            injuries = list(Injury.objects.filter(
                injury_location__sctid__in=loc_f,
                injury_type__sctid__in=type_f
            ))

            payload["results"] = analyze(injuries, q_text)
            return render(request, "results.html", payload)
        
    else:
        payload['form'] = SearchForm()

    return render(request, "search.html", payload)

