# Scrape climate data from Environment Canada
# David Jones, Climate Code Foundation, 2011-09

# List of suspect stations/data:
# CAE1016992_ year 1977 is present but has no useful data
# CAE2400400_ contains many bogus missing months (eg 1944-01)

# The pages (stations) to scrape come from another scraper:
# http://scraperwiki.com/scrapers/can-weather-stations/
# (which may currently not be scraping all the stations)

# Scrapes are prioritised based on date since last scraped and an
# estimate of the amount of new data we would find.

# Note: Currently location data (lat/lon) is scraped from the CSV file,
# but in the CSV file the location is only stored to 2 decimal degrees.
# (for WMO stations) There is more precise location data (seconds of arc)
# in Canada's WMO Volume A report:
# http://www.climate.weatheroffice.gc.ca/prods_servs/wmo_volumea_e.html
# Also of note from the Volume A report, several stations listed in
# Volume A have WMO identifiers, but that WMO identifier is not listed
# for that station in the CSV file that this scraper accesses
# (for example 71178 BONAVISTA , 71949 FARO).
# The _web display_ for each station also appears to contain
# location information more precisely (also to seconds of arc).

# http://docs.python.org/release/2.6.6/library/csv.html
import csv
import itertools
# http://docs.python.org/release/2.6.6/library/json.html
import json
import math
import re
import time
# http://docs.python.org/release/2.6.6/library/urllib.html
import urllib

import scraperwiki

# Schema.  Not really, haha.
scraperwiki.sqlite.execute("""
create table if not exists series
(id text, element text, monthmin text, monthmax text, yearmin integer, yearmax integer, monthcount integer)
""")
scraperwiki.sqlite.execute("""
create table if not exists obs
(id text, element text, year integer, month integer, v text, f text)
""")
scraperwiki.sqlite.execute("""
create index if not exists obs_id on obs(id)
""")
# To optimise the "show me stations with more than 20 years on tmeanM obs" query:
# select * from (select id,count(*) as n from obs where element='tmeanM' group by id) where n >= 240;
scraperwiki.sqlite.execute("""
create index if not exists obs_element_id on obs(element,id)
""")
if 0: scraperwiki.sqlite.execute("""
insert into series select id,element,monthmin,monthmax,yearmin,yearmax,monthcount from meta
where element in ('tmeanM', 'tminM', 'tmaxM')
""")
if 0: scraperwiki.sqlite.execute("""
delete from meta where element in ('tmeanM', 'tminM', 'tmaxM')
""")
if 0: scraperwiki.sqlite.execute("""
create table metacopy as select * from meta
""")
if 0: scraperwiki.sqlite.execute("""
delete from series where id = "<built-in function id>"
""")
if 0: scraperwiki.sqlite.execute("""
drop table meta
""")
if 0: scraperwiki.sqlite.execute("""
create table meta as select id, `Station Name`, `WMO Identifier`, Latitude, Longitude, touched, webid, source, Province, Elevation, `Climate Identifier`, `TC Identifier`, element, null as session, rowmin, rowmax, clocked, clockedsave
from metacopy
""")
if 0: scraperwiki.sqlite.execute("""drop table metacopy""")
scraperwiki.sqlite.commit()

# Schema convert
def schemaconvert_old():
    """Convert from "one year per row" to "one month per row"."""

    data = []
    for row in scraperwiki.sqlite.execute("""select
    d.id,d.year,d.element,d.M01,d.M02,d.M03,d.M04,d.M05,d.M06,d.M07,d.M08,d.M09,d.M10,d.M11,d.M12,
    f.M01,f.M02,f.M03,f.M04,f.M05,f.M06,f.M07,f.M08,f.M09,f.M10,f.M11,f.M12
     from swdata as d join swdata as f on d.id = f.id and d.year = f.year and d.element||'flag' = f.element""")['data']:
        for m in range(12):
            o = dict(zip(['id', 'year', 'element'], row))
            d = row[3:15]
            f = row[15:27]
            if d[m] is not None:
                o['v'] = d[m]
                o['f'] = f[m]
                o['month'] = m+1
                data.append(o)
    print data
    scraperwiki.sqlite.save(['id', 'element', 'year', 'month'], data, table_name='obs')

def schemaconvert():
    for m in range(12):
        month = m+1
        M = 'M%02d' % month
        scraperwiki.sqlite.execute("""insert into obs
select d.id,d.element,d.year,%d as month, d.%s as v,f.%s as f from swdata as d join swdata as f using (id,year)
where d.element||'flag' == f.element and v is not null""" % (month,M,M))
        scraperwiki.sqlite.commit()

if 0: scraperwiki.sqlite.execute("""drop table if exists obs""")
if 0: schemaconvert()

if 0: exit(0)

url_template="http://www.climate.weatheroffice.gc.ca/climateData/bulkdata_e.html?timeframe=3&Prov=XX&StationID=%s&Year=2010&Month=1&Day=1&format=csv&type=mly"

# List of stations.
# See the scraper: http://scraperwiki.com/scrapers/can-weather-stations/
stations_db = 'can-weather-stations'

def isotime(t=None):
    """Return the current time formatted according to ISO 8601 with 3 decimal digits."""
    # Slightly tricky implementation.  strftime won't do decimals, and there's a
    # hack we have to do in the last 0.5 milliseconds of every second.
    if t is None:
        t = time.time()
    s = '%.3f' % (t%1)
    if s.startswith('1'):
        t += 0.0005
    s = '%.3f' % (t%1)
    assert s.startswith('0')
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(t))+s[1:]

# Copied from http://scraperwiki.com/scrapers/can-mayo-t/
# (but I have since deleted that scraper)
# Deliberately rely on isotime() being called once when this function
# is compiled.
def scrape1csv(csvfile, source, webid, session=isotime()):
    """*csvfile* should be a file opened by csv.reader()."""
    
    t0 = time.clock()
    # Amount of time spent during sqlite.save()
    clockedsave = 0.0
    # Collect the metadata
    meta = {}
    for row in csvfile:
        if not row:
            break
        # The first row of the file starts with a Byte-Order-Mark in utf-8.
        if row[0].startswith('\xef\xbb\xbf'):
            row[0] = row[0][3:].replace('"', '')
        # Ah... unicode.  Station with webid 43165 is
        # named Rivière du Loup.  Yay Quebec.
        # iso-8859-1 is a guess, but it works for that station.
        meta[row[0]] = unicode(row[1], 'iso-8859-1')
    #print meta
    # Make an identifier for this station.  "CA" denotes Canada (3166 country code),
    # "E" is for Environment.
    id11 = "CAE" + meta['Climate Identifier']
    assert len(id11) <= 11
    # extend to 11 characters
    id11 = (id11 + '_'*11)[:11]
    meta.update(dict(id=id11, session=session, touched=isotime(), source=source, webid=webid, element="meta"))
    #print meta
    #clockedsave += clocksave(['id', 'element'], meta, table_name='meta')
    
    # Skip the legend (to the next blank line)
    while csvfile.next():
        pass
    
    # Find out the column indexes by scanning the row of column names.
    columns = csvfile.next()
    #print columns
    yi = columns.index('Year')
    mi = columns.index('Month')
    mini = [i for i,s in enumerate(columns) if s.startswith('Mean Min Temp (')][0]
    maxi = [i for i,s in enumerate(columns) if s.startswith('Mean Max Temp (')][0]
    meani = [i for i,s in enumerate(columns) if s.startswith('Mean Temp (')][0]
    # Earliest row found, regardless of met variables present.
    rowmin = '9999-99'
    # Latest row found, regardless of met variables present.
    rowmax = '0000-00'
    # The data dictionary.  tmean["YYYY-MM"] is the monthly mean temperature,
    # when present.
    tmean = {}
    tmin = {}
    tmax = {}
    for row in csvfile:
        year = int(row[yi])
        month = int(row[mi])
        isoym = key(year, month)
        rowmin = min(rowmin, isoym)
        rowmax = max(rowmax, isoym)
        for i,d in [(meani,tmean), (mini,tmin), (maxi,tmax)]:
            t = row[i]
            flag = row[i+1]
            if flag not in 'BEMIST*':
                print "Strange flag value:", row
            if not t or flag == 'M':
                continue
            # Removed conversion to float(), 2011-09-13
            # so that decimal places are preserved.
            # t = float(t)
            d[(year,month)] = (t,flag)
    rows = []
    for s,element in [(tmean,'tmeanM'), (tmin,'tminM'), (tmax,'tmaxM')]:
        # Each *s* is the dictionary of obs for one element.
        # The key is a (year,month) tuple, the value is a (temp,flag) tuple.
        for (y,m),(d,f) in s.iteritems():
            single = dict(id=id11, element=element, year=y, month=m, v=d, f=f)
            rows.append(single)
    clockedsave += clocksave(['id', 'element', 'year', 'month'], rows, table_name='obs')

    report = []
    # computed metadata for each station series (date ranges of valid data, and so on).
    series = []
    for s,element in [(tmean,'tmeanM'), (tmin,'tminM'), (tmax,'tmaxM')]:
        if s:
            d = dict(id=id11,
                element=element,
                yearmin=min(s)[0],
                yearmax=max(s)[0],
                monthmin=key(*min(s)),
                monthmax=key(*max(s)),
                monthcount=len(s))
            series.append(d)
            report.append('%(element)s %(monthmin)s/%(monthmax)s' % d)
        else:
            report.append('%s No Data' % element)
    clockedsave += clocksave(['id', 'element'], series, table_name='series')
    meta['rowmin'] = rowmin
    meta['rowmax'] = rowmax
    # Resave the metadata (with some bookkeeping records updated).
    # (perhaps we ought to separate metadata into station metadata (gathered from
    # the CSV files etc) and scraper metadata (facts about when the scraper was
    # last run, etc).
    t1 = time.clock()
    meta['clocked'] = t1-t0
    meta['clockedsave'] = clockedsave
    metaclock = clocksave(['id', 'element'], meta, table_name='meta')
    datarange = '; '.join(report)
    print isotime(), id11, datarange, "CPU =", meta['clocked'], "(%f)" % clockedsave, "t1 =", t1

def clocksave(*l, **k):
    """As scraperwiki.sqlite.save(), but returns the number of CPU seconds,
    measured by time.clock(), used."""
    t0 = time.clock()
    scraperwiki.sqlite.save(*l, **k)
    t1 = time.clock()
    return t1-t0
    
def key(y, m):
    """Construct key, of the form "YYYY-MM" for the
    year and month.  *m* is 1-based."""

    return "%04d-%02d" % (y,m)

def dekey(k):
    """Deconstruct key, of the form "YYYY-MM" into an integer (year,month) pair."""
    return map(int, re.match(r'(\d+)-(\d+)', k).groups())


today = isotime()
print "Today is", today
import datetime
todaydt = datetime.date(*map(int, today[:10].split('-')))

touched_data = scraperwiki.sqlite.select("webid,touched from meta where webid is not null")
touched_dict = dict((r['webid'],r['touched']) for r in touched_data)
print len(touched_dict), "touch records"
def days_ago(webid):
    """Return number of days since we last scraped this station.
    """
       
    if webid not in touched_dict:
        # Means we've never scraped the CSV with the current code
        return 60
    touched = touched_dict[webid]
    if not touched:
        return 60
    touched = datetime.date(*map(int, touched[:10].split('-')))
    ago = (todaydt - touched).days
    return ago

scraperwiki.sqlite.attach('can-weather-stations', 's')
missing_data = scraperwiki.sqlite.select("""
webid,julianday(mmax)-julianday(rmax) as r,julianday(rmin)-julianday(mmin) as l from
(select s.swdata.webid as webid,substr(s.swdata.mlyRange,1,10) as mmin,substr(s.swdata.mlyRange,12) as mmax, meta.rowmin||"-01" as rmin,meta.rowmax||"-01" as rmax from s.swdata join meta on meta.webid = s.swdata.webid and meta.element = 'meta')
""")
# Gives the number of missing days (!) for each station.
missing_dict = dict((r['webid'],max(0,r['l'])+max(0,r['r'])) for r in missing_data)
def missing_months(station):
    """Return the number of missing months; based on rowmin and rowmax
    collected in this scraper, and mlyRange scraped in can-weather-stations.
    It attempts to estimate the number of months
    that might be added by scraping the station.  For various reasons not
    accurate.
    """
    
    webid = station['webid']
    # We return 0 for a station with no mlyRange.
    return math.ceil(missing_dict.get(webid, 0) / 30.0)

def scrapelist(stations):
    for station in stations:
        webid = station['webid']
        station['ago'] = days_ago(webid)
        station['missing'] = missing_months(station)
        station['priority'] = prioritise(station)
    stations.sort(key=lambda x: x['priority'], reverse=True)
    for station in stations:
        print isotime(), station['webid'], station['ago'], station['priority']
        webid = station['webid']
        url = url_template % webid
        csvfile = csv.reader(urllib.urlopen(url))
        scrape1csv(csvfile, source=url, webid=webid)

def prioritise(station):
    """Compute a priority for a station.  Stations are prioritised so
    that stations never visited come first, followed by stations in
    reverse order of how recently they have been visited (so older
    stations are visited first).  Stations we expect to have data have a
    significant priority over those that don't.

    The priority has two parts; it is a tuple (T,A).
    *T* is the number of days since the page was touched, with a bonus
    of 10 if there is missing data, and a super bonus of 90 if there is
    a large amount of missing data, and we haven't touched it very
    recently.
    *A* is the amount of missing data.
    Larger tuples, lexicographically ordered, are higher priority."""

    T = station['ago']
    A = station['missing']
    if A > 200 and T > 1: # About 17 years
        T += 90
    if A:
        T += 10


    return (T,A)

# Just so that we get a nice screenshot on ScraperWiki
urllib.urlopen("http://www.climate.weatheroffice.gc.ca/climateData/canada_e.html")

def all_stations_from(db):
    """Yield a stream of all the results from the specified
    sqlite database."""

    print db
    scraperwiki.sqlite.attach(db, 'meta')
    for row in scraperwiki.sqlite.select("* from meta.swdata;"):
        yield row

stations = list(all_stations_from(stations_db))
stations = [item for item in stations if item.get('webid')]
import random
random.shuffle(stations)
ids = [item['webid'] for item in stations]
print ' '.join(ids)
print len(ids), "pages to scrape"
 
scrapelist(stations)

print "Scraped"