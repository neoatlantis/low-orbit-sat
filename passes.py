#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
from datetime import datetime

from tabulate import tabulate
from pyorbital import orbital

# --------------------------------------------------------------------------- #
satCache = {}
tleList = os.listdir('./tlefiles')
for each in tleList:
    fullpath = os.path.join('tlefiles', each)
    if not os.path.isfile(fullpath):
        continue
    if not each.endswith('.tle'):
        continue
    satName = each[0:-4].lower()
    satCache[satName] = orbital.Orbital(satName, fullpath)

# --------------------------------------------------------------------------- #

OBSERVATOR = (51.049754, 13.757227, 92.0)
NOWTIME = datetime.utcnow()
EMAX_MINIMAL = 10.0 # minimal max-elevation for calculating satellite passes
PASS_PERIOD = 24 # hours for calculating next passes

# --------------------------------------------------------------------------- #
# calculate all passes of all satellites
calculated = []

OBSERV_PARAM = (OBSERVATOR[1], OBSERVATOR[0], OBSERVATOR[2])
for satName in satCache:
    sat = satCache[satName]
    passes = sat.get_next_passes(NOWTIME, PASS_PERIOD, *OBSERV_PARAM)
    for p in passes:
        entry = {}
        rise, fall, emax = p
        risePos = sat.get_observer_look(rise, *OBSERV_PARAM)
        fallPos = sat.get_observer_look(fall, *OBSERV_PARAM)
        emaxPos = sat.get_observer_look(emax, *OBSERV_PARAM)
        if emaxPos[1] < EMAX_MINIMAL:
            continue

        entry['rise'] = {
            'time': rise,
            'azimuth': risePos[0],
            'elevation': risePos[1]
        }
        entry['fall'] = {
            'time': fall,
            'azimuth': fallPos[0],
            'elevation': fallPos[1]
        }
        entry['emax'] = {
            'time': emax,
            'azimuth': emaxPos[0],
            'elevation': emaxPos[1]
        }
        entry['name'] = satName
        calculated.append(entry)

# --------------------------------------------------------------------------- #
# sort calculated results and print in table
def criteria(entry):
    dt = entry['rise']['time']
    return time.mktime(dt.timetuple())
sortedPasses = sorted(calculated, key=criteria)

def toInstruction(x):
    return x['time'].strftime('%Y-%m-%d %H:%M:%S.%f') + \
        " (%5.1f, %4.1f)" % (x['azimuth'], x['elevation'])

table = []
tableHeader = [\
    'Satellite Name',
    'Ascend(Azimuth, Elevation)',
    'Elevation Max(Azimuth, Elevation)',
    'Descend(Azimuth, Elevation)'
]
for entry in sortedPasses:
    table.append([\
        entry['name'].upper(),
        toInstruction(entry['rise']),
        toInstruction(entry['emax']),
        toInstruction(entry['fall'])
    ])

print ""
print "Observer Location: Latitude %10.5f Longitude %10.5f Altitude %10.5f(m)." % OBSERVATOR
print "Time at calculation: %s UTC, predication for %d hours." %\
    (NOWTIME.strftime('%Y-%m-%d %H:%M:%S.%f'), PASS_PERIOD)
print tabulate(table, headers=tableHeader)
print "All times are in UTC."
print ""
