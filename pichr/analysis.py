from pichr.models import *

import numpy as np
import json
import math

from operator import itemgetter, attrgetter

def plot_information(labels, allERA, allFast, allDays):
    labelsNP = np.array(labels)
    allERA, allFast, allDays = np.array(allERA), np.array(allFast), np.array(allDays)
    
    days, eras, fasts, pt_lists =[], [], [], []
    for l in range(4):
        idx = np.where(labelsNP==l)
        if not idx:
            days.append([])
            eras.append([])
            fasts.append([])
            pt_lists.append([[], []])
        else:
            dayl, eral, fastl = allDays[idx].tolist(), allERA[idx].tolist(), allFast[idx].tolist()
            days.append([dayl])
            eras.append([eral])
            fasts.append([fastl])
            pt_lists.append([ zip(dayl, eral), zip(dayl, fastl) ])



    return days, eras, fasts, pt_lists


def get_high_rank_cases(cases):
    high_case_data = {}

    all_cases_sorted = sorted([(case, case["weight"], -1 * case['days']) for case in cases], key=itemgetter(1,2),reverse=True)
    
    high_cases = [c for (c,w,d) in all_cases_sorted[:10]]
    print [w for (c,w,d) in all_cases_sorted[:10]]
    return high_cases


def get_label_stats(cases, days, eras, fasts):
    data = {}

    for l in range(4):
        ldays = np.array(days[l])
        if ldays.size > 0:
            lera, lfast = np.array(eras[l]), np.array(fasts[l])

            data["l%d" % l] = ldays.size
            data["m%dstr" % l] = "%d"%ldays.mean()
            data["s%dstr" % l] = "%d"%ldays.std()
            data["m%d" % l] = ldays.mean()
            data["s%d" % l] = ldays.std()
            data["mERA%d" % l] = lera.mean()
            data["mERA%d" % l] = lfast.mean()
            if ldays.size == 1:
                data["l%dsingle" % l] = True

    data["total_reinj"] = (data["l1"] if "l1" in data else 0) + \
                          (data['l3'] if 'l3' in data else 0)

    return data


def get_meta_case(case):
    diffERA, diffFast = case.diffERA(), case.diffFastball()
    dur = case.duration
    label, weight = case.labels()

    return diffERA, diffFast, dur, label, weight, {
        "case": case,
        #labels for view
        "playerName": case.player.name,
        "playerTeam": case.player.team,
        "injury": case.sct_injury.name,
        "injury_loc": case.sct_injury.finding_site.name,
        "eraD": "%0.2f" % diffERA,
        "fastD": "%0.2f" % diffFast,
        #filterable stats
        "days": case.duration,
        "label": label,
        "weight": weight,
        "offseason": "Yes" if case.offseason else "No"
    }


def predict_range(days, high_cases, label_stats):
    days = np.array(days)
    rng = { }
    prange = [0,1000]

    if len(days) == 1: 
        return rng

    mean_d, std_d = days.mean(), days.std()
    bounds = (mean_d - 2*std_d, mean_d + 2 * std_d)

    high_case_results = []

    if high_cases:
        mid_good_cases = [hc for hc in high_cases if hc["weight"] > 3 and not hc['case'].offseason]
        mid_high_cases = [hc for hc in high_cases if not hc['case'].offseason]

        if mid_good_cases:
            high_case_results = mid_good_cases
        else:
            rng['uncertain'] = True
            if mid_high_cases: 
                high_case_results = mid_high_cases

        if high_case_results:
            days = [hc['days'] for hc in high_case_results]
            m, s = np.array(days).mean(), np.array(days).std()
            prange = [m - s, m + s]

    elif 'l0' in label_stats:
        m, s = label_stats['m0'], label_stats['s0']
        prange = [m - s, m + s]

        if 'l1' in label_stats:
            mbad, sbad = label_stats['m1'], label_stats['s1']
            prange[0] = max(m-s, mbad + sbad)
            if prange[1] < prange[0]:
                prange[1] = prange[0] + (sbad if sbad > 0 else 50)


    prange[0] = max(0, bounds[0], prange[0])
    prange[1] = min(1000, bounds[1], prange[1])

    rng['min'] = "%d" % (math.floor(float(prange[0])/10) * 10)
    rng['max'] = "%d" % (math.ceil(float(prange[1])/10) * 10)
    
    return rng, high_case_results


def analyze(cases):
    if not cases:
        return None

    eraD, fastD, labels, weights, durations = [], [], [], [], []
    procedures, locations = {}, {}
    cases_meta = []

    for case in cases:
        diffERA, diffFast, dur, label, weight, metacase = get_meta_case(case)
        eraD.append(diffERA)
        fastD.append(diffFast)
        durations.append(dur)
        labels.append(label)
        weights.append(weight)
        cases_meta.append(metacase)

        locID = case.sct_injury.finding_site.sctid
        if locID in locations: locations[locID] += 1
        else: locations[locID] = 1
        proc = case.procedure
        if proc:
            proc_id = proc.sctid
            if proc.sctid in procedures: procedures[proc_id]+=1
            else: procedures[proc_id]=1

    counts = list(np.bincount(labels))

    days, eras, fasts, lbs = plot_information(labels, eraD, fastD, durations)         # Plot information

    stats = get_label_stats(cases_meta, days, eras, fasts)              # Stats per label

    high_case_data = get_high_rank_cases(cases_meta)               # High-ranked case data

    prange, high_cases = predict_range(durations, high_case_data, stats)                   # Predicted range of days
    
    return {
        "total_cnt": len(cases),
        "high_cases": high_cases,
        "counts": counts,
        "stats": stats,
        "range": prange,
        "plot_data": json.dumps(lbs)
    }
