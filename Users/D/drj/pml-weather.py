# David Jones, Climate Code Foundation, 2010-11-17
# Plymouth Marine Laboratory Weather.

# One file of data per day; this is for 2003-11-28:
# http://www.westernchannelobservatory.org.uk/pml_weather_station/data/031128_met.dat
# Days from 2003-03-28 to current.

# Some files are dodgy:
# http://www.westernchannelobservatory.org.uk/pml_weather_station/data/090903_met.dat
#   Borked date field.  Subsequent day also.
# http://www.westernchannelobservatory.org.uk/pml_weather_station/data/090825_met.dat
#   Bit 6 of a byte has been flipped (in transmission?) turning a time field of '49'
#   into 't9' which causes an exception in our code.
# http://www.westernchannelobservatory.org.uk/pml_weather_station/data/100928_met.dat
#   Contains a bogus temperature of -39.88 (as does 2010-08-31)
# Currently the borked date and the bit flip cause the entire day to be rejected.  For
#   now, this is acceptable.  The obviously bogus temperature however, slips through.


prefix = 'http://www.westernchannelobservatory.org.uk/pml_weather_station/data/'

import datetime
import itertools
import sys
# http://docs.python.org/library/traceback.html
import traceback
import urllib

import scraperwiki

start = datetime.date(2003, 3,28)
if 0: start = datetime.date(2010, 9, 22)
aday = datetime.timedelta(1)
today = datetime.date.today()
# We scan from start to limit.  Unwise to get today's or yesterday's data, as they may not be complete.
limit = today - aday
if 0: limit = datetime.date(2009,10, 1)

# Any dates in this list will be scraped,
# even if they've been done recently.
# Mostly useful for debugging a particular problem.
priority = ['2010-09-28']
priority = []

def scrapeall():
    print "Dates from %s to %s (excluding latter)" % (start, limit)
    resultofday = {}
    day = start
    while day < limit:
        touched = metaget(day)
        toucheddate = datetime.date(*map(int, touched.split('-')))
        if (str(day) in priority or
          today - toucheddate > datetime.timedelta(6)):
            notskip(day)
            result = try_scrape(day)
            resultofday[str(day)] = result
            if result in ['good', 'qc', 'missing']:
                metatouch(day)
        else:
            skip(day)
        day += aday
    count = dict((key,len(list(items))) for key,items in
        itertools.groupby(sorted(resultofday.values())))
    print "Found %s files" % count

def metaget(day):
    """Get the last touched date for this day's data,
    from the scraperwiki metadata store.
    """
    key = "touch%s" % day.isoformat()
    result = scraperwiki.metadata.get(key, "1900-01-01")
    return result

def metatouch(day):
    """Touch the day with today's date, updating the scraperwiki
    metadata store.
    """
    key = "touch%s" % day.isoformat()
    try:
        # This is unreliable, so we try:except: it.
        scraperwiki.metadata.save(key, str(today))
    except Exception,err:
        print "metadata.save", key, str(err)


skipped = []
def notskip(day):
    global skipped
    s = ''
    if skipped:
        s = "until "
    print s + str(day)
    skipped = []

def skip(day):
    global skipped
    if not skipped:
        print "skipping", day
    skipped.append(day)
    if len(skipped) > 30:
        print "and up to", day
        skipped = []

def try_scrape(day):
    try:
        return scrape1(day)
    except:
        traceback.print_exc(file=sys.stdout)
        return 'except'

def scrape1(day):
    # Date in form YYMMDD
    frag = "%02d%02d%02d" % (day.year%100, day.month, day.day)
    url = prefix + frag + '_met.dat'
    try:
        content = urllib.urlopen(url)
    except IOError:
        print "No data at %s" % url
        return 'missing'
    rows = list(content)
    if not rows:
        print "No data in %s" % url
        return 'missing'
    # Early files are 8 column format, later files are 9 column format.
    # And just after lunch on 2004-08-24, we see a 10 column format.
    # column holding date field
    datecol = 8
    if len(rows[0].split(',')) == 8:
        datecol = 7
    dates = set(row.split(',')[datecol].strip() for row in rows)
    if len(dates) > 1:
        print "Multiple dates found, %s, in file %s" % (dates, url)
        return 'suspect'
    recorddate, = dates
    recorddate = map(int, recorddate.split('/'))
    # Y2K1 fix and US to UK ordering.
    # Early files have date in form MM/DD/YY,
    # later files use YYYY/MM/DD
    if recorddate[0] < 100:
        recorddate = (recorddate[2]+2000,recorddate[0],recorddate[1])
    recorddate = datetime.date(*recorddate)
    if recorddate != day:
        print "Date %s found in file %s" % (recorddate, url)
        return 'suspect'
    # Quality Control Checks
    # Must have at least 24 readings in a 24-hour period...
    if len(rows) < 24:
        print "Only %d rows in %s" % (len(rows), url)
        return 'qc'
    # Must have at least one reading in every hour...
    timecol = datecol - 1 # column holding time field
    tempcol = 4
    # dictionary that maps times (key) to temperatures (value)
    ttdict = dict((row[timecol].strip(), float(row[tempcol]))
        for row in [r.split(',') for r in rows])
    hours = set(int(time.split(':')[0]) for time in ttdict)
    if hours != set(range(24)):
        print "Only %d hours in %s" % (len(hours), url)
        return 'qc'
    # Convert times to number of seconds (since 00:00:00),
    # ordered list of (sec,temp) pairs.
    sectemp = sorted((((h*60+m)*60+s,temp) for (h,m,s),temp in
        ((map(int, t.split(':')),tem) for t,tem in ttdict.items())))
    sectimes,temps = zip(*sectemp)
    # And find the largest gap between observation times.
    diffs = [b-a for a,b in zip(sectimes, sectimes[1:])]
    if max(diffs) > 3600:
        print "Large gap in %s" % url
        return 'qc'
    temps = median_filter(temps)
    tmin = min(temps)
    tmax = max(temps)
    
    baserecord = dict(id="uk_pml")
    isodate = recorddate.isoformat()
    tmind = {'element':'tminD', isodate:tmin}
    tmind.update(baserecord)
    tmaxd = {'element':'tmaxD', isodate:tmax}
    tmaxd.update(baserecord)
    scraperwiki.datastore.save(['id','element'], tmind)
    scraperwiki.datastore.save(['id','element'], tmaxd)
    return 'good'

def median_filter(seq):
    """Apply a (3 point) median filter to the sequence and
    return a fresh list.  Each item of the returned list is
    the median item of the corresponding 3 items in the original
    sequence; the returned list is 2 items shorter."""
    
    assert len(seq) >= 3
    return [sorted(triple)[1] for triple in zip(seq, seq[1:], seq[2:])]

scrapeall()
