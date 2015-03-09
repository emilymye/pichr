from pichr.models import *

import numpy as np
import json

from operator import itemgetter, attrgetter


def plot_information(labels, yERA, yFast, x):
    labelsNP, x, yERA, yFast = np.array(labels), np.array(x), np.array(yERA), np.array(yFast)
    pt_lists = []

    print labels
    for l in range(4):
        idx = np.where(labelsNP==l)
        if not idx:
            pt_lists.append([[], []])
        else:
            pt_lists.append([ zip(x[idx], yERA[idx]), zip(x[idx], yFast[idx]) ])

    return pt_lists

def analyze(cases, query):
    eraD, fastD, labels, weights, durations = [], [], [], [], []
    caseList = []

    for rec in cases:
        diffERA = rec.diffERA()
        diffFast = rec.diffFastball()
        dur = rec.duration
        sctinj = rec.sct_injury
        label, weight = rec.labels()

        eraD.append(diffERA)
        fastD.append(diffFast)
        durations.append(dur)
        labels.append(label)
        weights.append(weight)

        caseList.append({
            "injury": rec,
            "playerName": rec.player.name,
            "playerTeam": rec.player.team,
            "name": rec.sct_injury.name,
            "location": rec.sct_injury.finding_site.name,
            "days": dur,
            "eraD": "%0.2f" % diffERA,
            "fastD": "%0.2f" % diffFast,
            "label": label,
            "weight": weight,
            "offseason": "Yes" if rec.offseason else "No"
        })

    counts = list(np.bincount(labels))

    highRankInjuries = [rec for rec in caseList if rec["weight"] > 3 ]
    midHighDays = np.array([i['days'] for i in highRankInjuries if i["offseason"] == "No"])
    offHighDays = np.array([i['days'] for i in highRankInjuries if i["offseason"] == "Yes"])
    m0, m1 = midHighDays.mean(), offHighDays.mean()
    v0, v1 = midHighDays.std(), offHighDays.std()

    days = np.array(durations) 
    reinjuryDays = days[np.where(np.array(labels)==1)]

    limit = reinjuryDays.mean() if reinjuryDays.any() else 0

    

    lbs = plot_information(labels, eraD, fastD, durations)
    
    return {
        "injuries": sorted(highRankInjuries,key=itemgetter('weight','days'), reverse=True),
        "totalcnt": len(cases),
        "cnt": counts[0],
        "mean": "%.d " % m0,
        "variance": "%d " % v0,
        "cntOff": counts[2],
        "meanOff": "%d " % m1,
        "varianceOff": "%d " % v1,
        "cntRe": counts[1],
        "cntReTotal": counts[1] + counts[2],
        "min": "%d" % limit, 
        "max": "%d" % (2 * m0 - limit),
        "eraD": eraD,
        "fastD": fastD,
        "plot_data": json.dumps(lbs)
    }
