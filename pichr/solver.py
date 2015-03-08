from pichr.models import *

import numpy as np
import json


def analyze(injuries, qtext): 
    n = len(injuries)
    summary = "We found %d injuries%s." % (n, qtext)
    
    days, era_diff, fastball_diff = [], [], []
    for i, injury in enumerate(injuries):
        r = injury.recovery 
        days.append(r.duration)
        era_diff.append(r.postERA - r.preERA)
        fastball_diff.append(r.postFastball - r.preFastball)

    era_pts = zip(days, era_diff)
    fastball_pts = zip(days, fastball_diff)

    days = np.array(days)
    days.sort()
    histogram = np.histogram(days, bins=4)

    summary += "Recovery times ranged from %d to %d days, with an average of %.1f days." % (
        min(days), max(days), days.mean()
    )

    return { 
        "days": days,
        "summary": summary, 
        "injuries": injuries,
        "era_pts": json.dumps(era_pts),
        "fastball_pts": json.dumps(fastball_pts),
    }