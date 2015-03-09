from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from pichr.models import *
from pichr.forms import *
from pichr.analysis import analyze

def index(request):
    return search(request)


def search(request):
    payload = { }
    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():

            filters = form.cleaned_data
            injuries = []

            query = ""
            
            if filters["injury"] is not None:
                inj = filters["injury"]
                injuries = list(Recovery.objects.filter(sct_injury_id=inj.sctid))
                query = inj.name
            else:
                type_f = [o.pk for o in SCTMorphology.objects.all()]
                loc_f = [l.pk for l in SCTBodyStructure.objects.all()]

                query = "general injury"

                if filters["injury_type"] is not None and \
                   filters["injury_type"].sctid != 19130008:
                    tpe = filters["injury_type"]
                    type_f = [tpe.sctid]
                    query = "%s" % tpe.name.lower()

                if filters["location"] is not None:
                    loc = filters["location"]
                    query += " of %s" % loc.sctname.lower()
                    loc_f = [desc['sctid'] for desc in loc.descendants.all().values("sctid").distinct()]
                    loc_f.append(loc.sctid)

                injuries = list(Recovery.objects.filter(
                    sct_injury__finding_site__sctid__in=loc_f,
                    sct_injury__morphology__sctid__in=type_f
                ))

            payload["query_injury"] = query.lower()
            payload["results"] = analyze(injuries, query)

            return render(request, "results.html", payload)
        
    else:
        payload['form'] = SearchForm()

    return render(request, "search.html", payload)

