# -*- coding: utf-8 -*-

"""
    Aggregator for precipitation data from Northrhine-Westphalia (Nordrhein-Westfalen), Germany

    Source: Landesamt für Umwelt, Natur und Verbraucherschutz Nordrhein-Westfalen
"""

import scraperwiki
import mechanize
import re, sys, random
from datetime import datetime
from BeautifulSoup import BeautifulSoup
import scrapemark
import xlrd
import urllib2 as urllib

def shuffle(l):
    """Sort a list in random order"""
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]

def get_stations():
    """Get meta data about the precipitation sensor stations"""
    url = 'http://luadb.lds.nrw.de/LUA/wiski/pegel.php?stationsname_n=GueterslohWWK2&ersterAufruf=aktuelle%2BWerte'
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    assert br.viewing_html()
    stations = []
    for line in br.response().read().split("\n"):
        #print line
        match = re.match(r"\s*d\.add\([0-9]+,\s*[0-9]+,\s*'([^\']+)',\s*'pegel\.php\?stationsname_n=[^&]+&ersterAufruf=aktuelle%2BWerte'\);\s*", line)
        if match is not None:
            #print match.group(1)
            stations.append(match.group(1))
    #print "Number of stations found:", len(stations)
    return stations

def get_values_for_station_and_day(station, date):
    datestring = date.strftime('%d.%m.%Y')
    now = datetime.today()
    url = 'http://luadb.lds.nrw.de/LUA/wiski/pegel.php?stationsname_n='+ station +'&meindatum='+ datestring +'&tabellet=Tabelle'
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    assert br.viewing_html()
    data = scrapemark.scrape("""
            {*
            <td class='messwerte'>{{ [values].datetime }}</td> 
            <td class='messwerte'>{{ [values].value|float }}&nbsp;</td>
            *}
        """,
        br.response().read())
    if 'values' in data:
        datasets = []
        #print data['values']
        for row in data['values']:
            #print station, row['datetime'], ("%.2f" % row['value'])
            # datetime string can be "DD.MM HH:MM" or "HH:MM"
            match1 = re.match(r"([0-9]{2})\.([0-9]{2})\s+([0-9]{2}):([0-9]{2})", row['datetime'])
            match2 = re.match(r"([0-9]{2}):([0-9]{2})", row['datetime'])
            year = None
            if match1 is not None:
                day = match1.group(1)
                month = match1.group(2)
                year = now.year
                hour = match1.group(3)
                minute = match1.group(4)
                if now.day == 1 and now.month == 1 and day == 31 and month == 12:
                    year = year - 1
            elif match2 is not None:
                day = date.day
                month = date.month
                year = date.year
                hour = match2.group(1)
                minute = match2.group(2)
            if year is not None:
                mez_timestamp = int(datetime(int(year), int(month), int(day), int(hour), int(minute)).strftime('%s'))
                utc_timestamp = mez_timestamp - 3600
                utcdate = datetime.fromtimestamp(utc_timestamp);
                datasets.append({
                    'station': station,
                    'datetime_utc': utcdate.strftime('%Y-%m-%d %H:%S'),
                    'value': ("%.2f" % row['value'])
                })
        scraperwiki.sqlite.save(unique_keys=['datetime_utc', 'station'], data=datasets, table_name="raindata")
        return len(datasets)

stations = get_stations()
stations = shuffle(stations)
for dayshift in range(0,1):
    thedate = datetime.fromtimestamp( int(datetime.today().strftime('%s')) - (86400 * dayshift))
    print "Getting data for", thedate.strftime('%Y-%m-%d')
    for station in stations:
        num = get_values_for_station_and_day(station, thedate)
    print num, "records fetched for date", thedate.strftime('%Y-%m-%d')
