"""
    Script to scrape daily climate data for a number of weather stations
    from http://www.dwd.de/
    License: Public Domain. No rights reserved.

    Original from: https://github.com/marians/dwd-climate-data-scraper

"""

import scraperwiki
import mechanize
import urllib
import re
import time
import sys
from BeautifulSoup import BeautifulSoup
import simplejson as json
import random

def shuffle(l):
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]

def main():
    articles = []
    BASE_URL = "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_windowLabel=T82002&_state=maximized&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland"
    br = mechanize.Browser()
    br.set_handle_robots(False)

    #print '========== 1. Seite ==============================='
    br.open(BASE_URL)

    #print '========== 2. Seite ==============================='
    br.follow_link(text_regex=r".*Klimadaten\s+Deutschland.*")
    assert br.viewing_html()


    #print '========== 3. Seite ==============================='
    br.follow_link(text_regex=r".*Messstationen.*")
    assert br.viewing_html()

    #print '========== 4. Seite ==============================='
    listpage_response = br.follow_link(text_regex=r".*Tageswerte.*")
    assert br.viewing_html()
    soup = BeautifulSoup(listpage_response.read())
    options = soup.findAll('option')
    # Read all station IDs and location names
    stations = {}
    for option in options:
        #print option['value'], " - ", option.string.encode('iso-8859-1')
        lmatch = re.match(r"^[0-9]{5}\s+(.+)$", option.string)
        #print lmatch
        if re.match(r"^[0-9]{5}$", option['value']):
            stations[option['value']] = lmatch.group(1)
    #print stations
    if len(stations) == 0:
        print "Error: No stations found."
        sys.exit(1)
    
    # randomize stations to increase chances of getting complete data
    # over multiple runs
    station_ids = shuffle(stations.keys())

    # iterate over stations
    #allrows = []
    url = 'http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_windowLabel=T82002&_urlType=action&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland'
    for station in station_ids:
        print "Reading values for station ", station, " - ", stations[station].encode('iso-8859-1')
        post_params = {
            'Hidden-Variable tageswerte': 'tageswerte',
            'T82002gsbDocumentPath': 'Content/Oeffentlichkeit/KU/Formulare/KU2__KlDaten__Akt/KlDaten__Akt__tk__klimadatenForm,templateId=processForm.html',
            '_nfpb': 'true',
            '_pageLabel': '_dwdwww_klima_umwelt_klimadaten_deutschland',
            'anzeigen': 'Anzeigen',
            'input_': '',
            'pageLocale': 'de',
            'resourceId': '675382',
            'stationen': station}

        post_response = br.open(url, urllib.urlencode(post_params))
        assert br.viewing_html()
        body = post_response.read()

        # use this headers expression in order to confirm that the data has the expected format
        headers_regex = re.compile(r"STAT\s+JJJJMMDD\s+QN\s+TG\s+TN\s+TM\s+TX\s+RFM\s+FM\s+FX\s+SO\s+NM\s+RR\s+PM")
        if not headers_regex.search(body):
            print "Error: Data not in expected format - or header line not found."
            sys.exit(1)
        else:
            values_regex = re.compile(r"([0-9]{5})\s+([0-9]{8})\s+([0-9]{1,2})\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)")
            matches = re.findall(values_regex, body)
            #print matches
            rows = []
            for row in matches:
                # station_id
                # date                        in format YYYYMMDD
                # quality_level               = QN  = Qualitaetsniveau der Daten
                # temperature_5cm_min         = TG  = Minimum der Temperatur in 5 cm ueber dem Erdboden (Grad C)
                # temperature_200cm_min       = TN  = Minimum der Temperatur in 2 m ueber dem Erdboden (Grad C)
                # temperature_200cm_average   = TM  = Mittel der Temperatur in 2 m ueber dem Erdboden (Grad C)
                # temperature_200cm_max       = TX  = Maximum der Temperatur in 2 m ueber dem Erdboden (Grad C)
                # relative_humidity           = RFM = Mittel der relativen Feuchte (%)
                # wind_force_average          = FM  = Mittel der Windstaerke (Bft)
                # wind_speed_max              = FX  = Maximum der Windgeschwindigkeit (Spitzenboee) (m/sec)
                # sunshine_duration           = SO  = Summe der Sonnenscheindauer (Stunden)
                # cloud_amount_average        = NM  = Mittel des Bedeckungsgrades (Achtel)
                # precipitation_height        = RR  = Niederschlagshoehe (mm)
                # barometric_pressure_average = PM  = Mittel des Luftdruckes in Stationshoehe (hpa)
                row = {'station_id': int(row[0]),
                    'date': row[1],
                    'quality_level': int(row[2]),
                    'temperature_5cm_min': row[3],
                    'temperature_200cm_min': row[4],
                    'temperature_200cm_average': row[5],
                    'temperature_200cm_max': row[6],
                    'relative_humidity': row[7],
                    'wind_force_average': row[8],
                    'wind_speed_max': row[9],
                    'sunshine_duration': row[10],
                    'cloud_amount_average': row[11],
                    'precipitation_height': row[12],
                    'barometric_pressure_average': row[13]
                }
                rows.append(row)
            scraperwiki.sqlite.save(unique_keys=["station_id", "date"], data=rows)
        time.sleep(1)
    #f = open('klimadaten.json', 'w')
    #f.write(json.dumps(allrows))
    #f.close()
    #print len(allrows), " rows written to klimadaten.json"


main()
"""
    Script to scrape daily climate data for a number of weather stations
    from http://www.dwd.de/
    License: Public Domain. No rights reserved.

    Original from: https://github.com/marians/dwd-climate-data-scraper

"""

import scraperwiki
import mechanize
import urllib
import re
import time
import sys
from BeautifulSoup import BeautifulSoup
import simplejson as json
import random

def shuffle(l):
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]

def main():
    articles = []
    BASE_URL = "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_windowLabel=T82002&_state=maximized&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland"
    br = mechanize.Browser()
    br.set_handle_robots(False)

    #print '========== 1. Seite ==============================='
    br.open(BASE_URL)

    #print '========== 2. Seite ==============================='
    br.follow_link(text_regex=r".*Klimadaten\s+Deutschland.*")
    assert br.viewing_html()


    #print '========== 3. Seite ==============================='
    br.follow_link(text_regex=r".*Messstationen.*")
    assert br.viewing_html()

    #print '========== 4. Seite ==============================='
    listpage_response = br.follow_link(text_regex=r".*Tageswerte.*")
    assert br.viewing_html()
    soup = BeautifulSoup(listpage_response.read())
    options = soup.findAll('option')
    # Read all station IDs and location names
    stations = {}
    for option in options:
        #print option['value'], " - ", option.string.encode('iso-8859-1')
        lmatch = re.match(r"^[0-9]{5}\s+(.+)$", option.string)
        #print lmatch
        if re.match(r"^[0-9]{5}$", option['value']):
            stations[option['value']] = lmatch.group(1)
    #print stations
    if len(stations) == 0:
        print "Error: No stations found."
        sys.exit(1)
    
    # randomize stations to increase chances of getting complete data
    # over multiple runs
    station_ids = shuffle(stations.keys())

    # iterate over stations
    #allrows = []
    url = 'http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_windowLabel=T82002&_urlType=action&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland'
    for station in station_ids:
        print "Reading values for station ", station, " - ", stations[station].encode('iso-8859-1')
        post_params = {
            'Hidden-Variable tageswerte': 'tageswerte',
            'T82002gsbDocumentPath': 'Content/Oeffentlichkeit/KU/Formulare/KU2__KlDaten__Akt/KlDaten__Akt__tk__klimadatenForm,templateId=processForm.html',
            '_nfpb': 'true',
            '_pageLabel': '_dwdwww_klima_umwelt_klimadaten_deutschland',
            'anzeigen': 'Anzeigen',
            'input_': '',
            'pageLocale': 'de',
            'resourceId': '675382',
            'stationen': station}

        post_response = br.open(url, urllib.urlencode(post_params))
        assert br.viewing_html()
        body = post_response.read()

        # use this headers expression in order to confirm that the data has the expected format
        headers_regex = re.compile(r"STAT\s+JJJJMMDD\s+QN\s+TG\s+TN\s+TM\s+TX\s+RFM\s+FM\s+FX\s+SO\s+NM\s+RR\s+PM")
        if not headers_regex.search(body):
            print "Error: Data not in expected format - or header line not found."
            sys.exit(1)
        else:
            values_regex = re.compile(r"([0-9]{5})\s+([0-9]{8})\s+([0-9]{1,2})\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)")
            matches = re.findall(values_regex, body)
            #print matches
            rows = []
            for row in matches:
                # station_id
                # date                        in format YYYYMMDD
                # quality_level               = QN  = Qualitaetsniveau der Daten
                # temperature_5cm_min         = TG  = Minimum der Temperatur in 5 cm ueber dem Erdboden (Grad C)
                # temperature_200cm_min       = TN  = Minimum der Temperatur in 2 m ueber dem Erdboden (Grad C)
                # temperature_200cm_average   = TM  = Mittel der Temperatur in 2 m ueber dem Erdboden (Grad C)
                # temperature_200cm_max       = TX  = Maximum der Temperatur in 2 m ueber dem Erdboden (Grad C)
                # relative_humidity           = RFM = Mittel der relativen Feuchte (%)
                # wind_force_average          = FM  = Mittel der Windstaerke (Bft)
                # wind_speed_max              = FX  = Maximum der Windgeschwindigkeit (Spitzenboee) (m/sec)
                # sunshine_duration           = SO  = Summe der Sonnenscheindauer (Stunden)
                # cloud_amount_average        = NM  = Mittel des Bedeckungsgrades (Achtel)
                # precipitation_height        = RR  = Niederschlagshoehe (mm)
                # barometric_pressure_average = PM  = Mittel des Luftdruckes in Stationshoehe (hpa)
                row = {'station_id': int(row[0]),
                    'date': row[1],
                    'quality_level': int(row[2]),
                    'temperature_5cm_min': row[3],
                    'temperature_200cm_min': row[4],
                    'temperature_200cm_average': row[5],
                    'temperature_200cm_max': row[6],
                    'relative_humidity': row[7],
                    'wind_force_average': row[8],
                    'wind_speed_max': row[9],
                    'sunshine_duration': row[10],
                    'cloud_amount_average': row[11],
                    'precipitation_height': row[12],
                    'barometric_pressure_average': row[13]
                }
                rows.append(row)
            scraperwiki.sqlite.save(unique_keys=["station_id", "date"], data=rows)
        time.sleep(1)
    #f = open('klimadaten.json', 'w')
    #f.write(json.dumps(allrows))
    #f.close()
    #print len(allrows), " rows written to klimadaten.json"


main()
"""
    Script to scrape daily climate data for a number of weather stations
    from http://www.dwd.de/
    License: Public Domain. No rights reserved.

    Original from: https://github.com/marians/dwd-climate-data-scraper

"""

import scraperwiki
import mechanize
import urllib
import re
import time
import sys
from BeautifulSoup import BeautifulSoup
import simplejson as json
import random

def shuffle(l):
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]

def main():
    articles = []
    BASE_URL = "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_windowLabel=T82002&_state=maximized&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland"
    br = mechanize.Browser()
    br.set_handle_robots(False)

    #print '========== 1. Seite ==============================='
    br.open(BASE_URL)

    #print '========== 2. Seite ==============================='
    br.follow_link(text_regex=r".*Klimadaten\s+Deutschland.*")
    assert br.viewing_html()


    #print '========== 3. Seite ==============================='
    br.follow_link(text_regex=r".*Messstationen.*")
    assert br.viewing_html()

    #print '========== 4. Seite ==============================='
    listpage_response = br.follow_link(text_regex=r".*Tageswerte.*")
    assert br.viewing_html()
    soup = BeautifulSoup(listpage_response.read())
    options = soup.findAll('option')
    # Read all station IDs and location names
    stations = {}
    for option in options:
        #print option['value'], " - ", option.string.encode('iso-8859-1')
        lmatch = re.match(r"^[0-9]{5}\s+(.+)$", option.string)
        #print lmatch
        if re.match(r"^[0-9]{5}$", option['value']):
            stations[option['value']] = lmatch.group(1)
    #print stations
    if len(stations) == 0:
        print "Error: No stations found."
        sys.exit(1)
    
    # randomize stations to increase chances of getting complete data
    # over multiple runs
    station_ids = shuffle(stations.keys())

    # iterate over stations
    #allrows = []
    url = 'http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_windowLabel=T82002&_urlType=action&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland'
    for station in station_ids:
        print "Reading values for station ", station, " - ", stations[station].encode('iso-8859-1')
        post_params = {
            'Hidden-Variable tageswerte': 'tageswerte',
            'T82002gsbDocumentPath': 'Content/Oeffentlichkeit/KU/Formulare/KU2__KlDaten__Akt/KlDaten__Akt__tk__klimadatenForm,templateId=processForm.html',
            '_nfpb': 'true',
            '_pageLabel': '_dwdwww_klima_umwelt_klimadaten_deutschland',
            'anzeigen': 'Anzeigen',
            'input_': '',
            'pageLocale': 'de',
            'resourceId': '675382',
            'stationen': station}

        post_response = br.open(url, urllib.urlencode(post_params))
        assert br.viewing_html()
        body = post_response.read()

        # use this headers expression in order to confirm that the data has the expected format
        headers_regex = re.compile(r"STAT\s+JJJJMMDD\s+QN\s+TG\s+TN\s+TM\s+TX\s+RFM\s+FM\s+FX\s+SO\s+NM\s+RR\s+PM")
        if not headers_regex.search(body):
            print "Error: Data not in expected format - or header line not found."
            sys.exit(1)
        else:
            values_regex = re.compile(r"([0-9]{5})\s+([0-9]{8})\s+([0-9]{1,2})\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)")
            matches = re.findall(values_regex, body)
            #print matches
            rows = []
            for row in matches:
                # station_id
                # date                        in format YYYYMMDD
                # quality_level               = QN  = Qualitaetsniveau der Daten
                # temperature_5cm_min         = TG  = Minimum der Temperatur in 5 cm ueber dem Erdboden (Grad C)
                # temperature_200cm_min       = TN  = Minimum der Temperatur in 2 m ueber dem Erdboden (Grad C)
                # temperature_200cm_average   = TM  = Mittel der Temperatur in 2 m ueber dem Erdboden (Grad C)
                # temperature_200cm_max       = TX  = Maximum der Temperatur in 2 m ueber dem Erdboden (Grad C)
                # relative_humidity           = RFM = Mittel der relativen Feuchte (%)
                # wind_force_average          = FM  = Mittel der Windstaerke (Bft)
                # wind_speed_max              = FX  = Maximum der Windgeschwindigkeit (Spitzenboee) (m/sec)
                # sunshine_duration           = SO  = Summe der Sonnenscheindauer (Stunden)
                # cloud_amount_average        = NM  = Mittel des Bedeckungsgrades (Achtel)
                # precipitation_height        = RR  = Niederschlagshoehe (mm)
                # barometric_pressure_average = PM  = Mittel des Luftdruckes in Stationshoehe (hpa)
                row = {'station_id': int(row[0]),
                    'date': row[1],
                    'quality_level': int(row[2]),
                    'temperature_5cm_min': row[3],
                    'temperature_200cm_min': row[4],
                    'temperature_200cm_average': row[5],
                    'temperature_200cm_max': row[6],
                    'relative_humidity': row[7],
                    'wind_force_average': row[8],
                    'wind_speed_max': row[9],
                    'sunshine_duration': row[10],
                    'cloud_amount_average': row[11],
                    'precipitation_height': row[12],
                    'barometric_pressure_average': row[13]
                }
                rows.append(row)
            scraperwiki.sqlite.save(unique_keys=["station_id", "date"], data=rows)
        time.sleep(1)
    #f = open('klimadaten.json', 'w')
    #f.write(json.dumps(allrows))
    #f.close()
    #print len(allrows), " rows written to klimadaten.json"


main()
"""
    Script to scrape daily climate data for a number of weather stations
    from http://www.dwd.de/
    License: Public Domain. No rights reserved.

    Original from: https://github.com/marians/dwd-climate-data-scraper

"""

import scraperwiki
import mechanize
import urllib
import re
import time
import sys
from BeautifulSoup import BeautifulSoup
import simplejson as json
import random

def shuffle(l):
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]

def main():
    articles = []
    BASE_URL = "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_windowLabel=T82002&_state=maximized&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland"
    br = mechanize.Browser()
    br.set_handle_robots(False)

    #print '========== 1. Seite ==============================='
    br.open(BASE_URL)

    #print '========== 2. Seite ==============================='
    br.follow_link(text_regex=r".*Klimadaten\s+Deutschland.*")
    assert br.viewing_html()


    #print '========== 3. Seite ==============================='
    br.follow_link(text_regex=r".*Messstationen.*")
    assert br.viewing_html()

    #print '========== 4. Seite ==============================='
    listpage_response = br.follow_link(text_regex=r".*Tageswerte.*")
    assert br.viewing_html()
    soup = BeautifulSoup(listpage_response.read())
    options = soup.findAll('option')
    # Read all station IDs and location names
    stations = {}
    for option in options:
        #print option['value'], " - ", option.string.encode('iso-8859-1')
        lmatch = re.match(r"^[0-9]{5}\s+(.+)$", option.string)
        #print lmatch
        if re.match(r"^[0-9]{5}$", option['value']):
            stations[option['value']] = lmatch.group(1)
    #print stations
    if len(stations) == 0:
        print "Error: No stations found."
        sys.exit(1)
    
    # randomize stations to increase chances of getting complete data
    # over multiple runs
    station_ids = shuffle(stations.keys())

    # iterate over stations
    #allrows = []
    url = 'http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_windowLabel=T82002&_urlType=action&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland'
    for station in station_ids:
        print "Reading values for station ", station, " - ", stations[station].encode('iso-8859-1')
        post_params = {
            'Hidden-Variable tageswerte': 'tageswerte',
            'T82002gsbDocumentPath': 'Content/Oeffentlichkeit/KU/Formulare/KU2__KlDaten__Akt/KlDaten__Akt__tk__klimadatenForm,templateId=processForm.html',
            '_nfpb': 'true',
            '_pageLabel': '_dwdwww_klima_umwelt_klimadaten_deutschland',
            'anzeigen': 'Anzeigen',
            'input_': '',
            'pageLocale': 'de',
            'resourceId': '675382',
            'stationen': station}

        post_response = br.open(url, urllib.urlencode(post_params))
        assert br.viewing_html()
        body = post_response.read()

        # use this headers expression in order to confirm that the data has the expected format
        headers_regex = re.compile(r"STAT\s+JJJJMMDD\s+QN\s+TG\s+TN\s+TM\s+TX\s+RFM\s+FM\s+FX\s+SO\s+NM\s+RR\s+PM")
        if not headers_regex.search(body):
            print "Error: Data not in expected format - or header line not found."
            sys.exit(1)
        else:
            values_regex = re.compile(r"([0-9]{5})\s+([0-9]{8})\s+([0-9]{1,2})\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)\s+([-\.0-9]+)")
            matches = re.findall(values_regex, body)
            #print matches
            rows = []
            for row in matches:
                # station_id
                # date                        in format YYYYMMDD
                # quality_level               = QN  = Qualitaetsniveau der Daten
                # temperature_5cm_min         = TG  = Minimum der Temperatur in 5 cm ueber dem Erdboden (Grad C)
                # temperature_200cm_min       = TN  = Minimum der Temperatur in 2 m ueber dem Erdboden (Grad C)
                # temperature_200cm_average   = TM  = Mittel der Temperatur in 2 m ueber dem Erdboden (Grad C)
                # temperature_200cm_max       = TX  = Maximum der Temperatur in 2 m ueber dem Erdboden (Grad C)
                # relative_humidity           = RFM = Mittel der relativen Feuchte (%)
                # wind_force_average          = FM  = Mittel der Windstaerke (Bft)
                # wind_speed_max              = FX  = Maximum der Windgeschwindigkeit (Spitzenboee) (m/sec)
                # sunshine_duration           = SO  = Summe der Sonnenscheindauer (Stunden)
                # cloud_amount_average        = NM  = Mittel des Bedeckungsgrades (Achtel)
                # precipitation_height        = RR  = Niederschlagshoehe (mm)
                # barometric_pressure_average = PM  = Mittel des Luftdruckes in Stationshoehe (hpa)
                row = {'station_id': int(row[0]),
                    'date': row[1],
                    'quality_level': int(row[2]),
                    'temperature_5cm_min': row[3],
                    'temperature_200cm_min': row[4],
                    'temperature_200cm_average': row[5],
                    'temperature_200cm_max': row[6],
                    'relative_humidity': row[7],
                    'wind_force_average': row[8],
                    'wind_speed_max': row[9],
                    'sunshine_duration': row[10],
                    'cloud_amount_average': row[11],
                    'precipitation_height': row[12],
                    'barometric_pressure_average': row[13]
                }
                rows.append(row)
            scraperwiki.sqlite.save(unique_keys=["station_id", "date"], data=rows)
        time.sleep(1)
    #f = open('klimadaten.json', 'w')
    #f.write(json.dumps(allrows))
    #f.close()
    #print len(allrows), " rows written to klimadaten.json"


main()
