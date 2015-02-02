#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
from datetime import datetime, timedelta

from tabulate import tabulate
from pyorbital import orbital

# --------------------------------------------------------------------------- #
# Read command line arguments
argv = sys.argv
if len(argv) < 2:
    print "Usage: python orbit.py <TLE_FILENAME>"

TLE_FILENAME = argv[1]
CALC_START = datetime.utcnow()
CALC_PERIOD = 120
CALC_RESOLUTION = 6
OBSERVATOR = (51.049754, 13.757227, 92.0)

# --------------------------------------------------------------------------- #
orbit = orbital.Orbital(os.path.basename(TLE_FILENAME)[0:-4], TLE_FILENAME)

# --------------------------------------------------------------------------- #
# calculate all positions
calculated = []
startTimestamp = time.mktime(CALC_START.timetuple())
startDatetime = CALC_START
incTimestamp = CALC_RESOLUTION
incDatetime = timedelta(seconds=CALC_RESOLUTION)
endTimestamp = startTimestamp + CALC_PERIOD
nowDatetime = CALC_START
nowTimestamp = startTimestamp
while nowTimestamp < endTimestamp:
    coordSpherical = orbit.get_lonlatalt(nowDatetime)
    coordObserver = orbit.get_observer_look(nowDatetime, *OBSERVATOR)
    calculated.append({
        'spherical': coordSpherical,
        'observer': coordObserver,
        'time': nowDatetime,
    })
    nowTimestamp += incTimestamp
    nowDatetime += incDatetime

# --------------------------------------------------------------------------- #
# print in table

table = []
tableHeader = [\
    'TIME',
    'AZ',
    'ELV',
    'LNG',
    'LAT',
    'ALT'
]
for each in calculated:
    table.append([\
        each['time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        each['observer'][0], # azimuth
        each['observer'][1], # elevation
        each['spherical'][0], # longitude
        each['spherical'][1], # latitude
        each['spherical'][2], # altitude
    ])

print ""
print "Observer Location: Latitude %10.5f Longitude %10.5f Altitude %10.5f(m)." % OBSERVATOR
print tabulate(table, headers=tableHeader)
print "All times are in UTC."
print ""
