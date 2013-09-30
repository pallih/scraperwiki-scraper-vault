import datetime as dt
import dateutil.parser
from StringIO import StringIO

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter as ff
import numpy

import scraperwiki
from scraperwiki import dumpMessage, sqlite, utils


def sec2minsec(x, i):
    m = int(x/60)
    s = int(x%60)
    return '%(m)02d:%(s)02d' % {'m':m,'s':s}

scraperwiki.sqlite.attach("parkrun")
data = scraperwiki.sqlite.execute(           
    '''select time, race, racedate from parkrun.swdata'''
    )

races = {}
for time, race, racedate in data['data']:
    races.setdefault(dateutil.parser.parse(racedate), []).append(time)

dates = []
winners = []
means = []
medians = []
spreads = []

for race in sorted(races):
    times = races[race]

    winners.append(numpy.min(times))
    means.append(numpy.average(times))
    medians.append(numpy.median(times))
    spreads.append(numpy.std(times))
    dates.append(race.date())

x = mpl.dates.date2num(dates)
winners = numpy.array(winners)
medians = numpy.array(medians)
spreads = numpy.array(spreads)
 
fig = plt.figure()
ax = fig.add_subplot(111)
ax.yaxis.set_major_formatter(ff(sec2minsec))
plt.xlabel("Date of Parkrun")
plt.ylabel("Time (min:sec)")

ax.plot_date(x, winners, 'ro', label="Winning time")
ax.errorbar(x, medians, yerr=spreads, label="Median time (and spread)")

fig.autofmt_xdate()

legend = plt.legend()


format = "png"
imagedata = StringIO()
plt.savefig(imagedata, format=format, dpi=96)
utils.httpresponseheader("Content-Type", "image/%s" % format)
dumpMessage({"content": imagedata.getvalue().encode("base64"), "message_type": "console", "encoding":"base64"})


import datetime as dt
import dateutil.parser
from StringIO import StringIO

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter as ff
import numpy

import scraperwiki
from scraperwiki import dumpMessage, sqlite, utils


def sec2minsec(x, i):
    m = int(x/60)
    s = int(x%60)
    return '%(m)02d:%(s)02d' % {'m':m,'s':s}

scraperwiki.sqlite.attach("parkrun")
data = scraperwiki.sqlite.execute(           
    '''select time, race, racedate from parkrun.swdata'''
    )

races = {}
for time, race, racedate in data['data']:
    races.setdefault(dateutil.parser.parse(racedate), []).append(time)

dates = []
winners = []
means = []
medians = []
spreads = []

for race in sorted(races):
    times = races[race]

    winners.append(numpy.min(times))
    means.append(numpy.average(times))
    medians.append(numpy.median(times))
    spreads.append(numpy.std(times))
    dates.append(race.date())

x = mpl.dates.date2num(dates)
winners = numpy.array(winners)
medians = numpy.array(medians)
spreads = numpy.array(spreads)
 
fig = plt.figure()
ax = fig.add_subplot(111)
ax.yaxis.set_major_formatter(ff(sec2minsec))
plt.xlabel("Date of Parkrun")
plt.ylabel("Time (min:sec)")

ax.plot_date(x, winners, 'ro', label="Winning time")
ax.errorbar(x, medians, yerr=spreads, label="Median time (and spread)")

fig.autofmt_xdate()

legend = plt.legend()


format = "png"
imagedata = StringIO()
plt.savefig(imagedata, format=format, dpi=96)
utils.httpresponseheader("Content-Type", "image/%s" % format)
dumpMessage({"content": imagedata.getvalue().encode("base64"), "message_type": "console", "encoding":"base64"})


