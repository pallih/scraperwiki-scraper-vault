import dateutil.parser
import random

import requests
import scraperwiki

from lxml.html import fromstring


# Retrieve air pollution data from Regione Liguria
#
# The steps are as follows
# 1. choose a year
# 2. get a list of all polluting agents available for that year
# 3. get a list of all monitoring stations for each polluting agent (sensors)
# 4. retrieve data for all combinations of sensors and stations
# 5. parse data (a very simple tabular format)
# 6. store data

# This is the only endpoint to query for all:
# - list of monitoring stations
# - list of sensors available at each station (varies from year to year)
# - actual data

URL = 'http://www.cartografiarl.regione.liguria.it/SiraQualAria/script/Pub2AccessoDatiAriaPost.asp'


def query_data(year, start, end, station, sensor):
    
    # date query parameters (inclusive)
    # e.g. if you only need one day they should be the same value

    iniz = "%s/%s" % (start, year)
    fine = "%s/%s" % (end, year)
    
    payload = {
        'Iniz': iniz,
        'Fine': fine,
        'Azione': 'ESTRAZ_LEGGI',
        'CodRete': '',
        'CodTema': 'PUNTI',
        'Anno': year,
        'IdTema': '',
        'CodParam': sensor,
        #'SiglaParam': 'Benzene - adsorbimento continuo, gc/fid', # it is NOT retrieved automatically
        'Separatore': ',',
        'IdRichiesta': '',
        'IdRichiestaCarto': '',
        'IdEstraz': 'DE',
        'IdRete': '',
        'CodUbic': station,
        #'DesUbic': 'Piazza Garibaldi - Busalla', # is retrieved automatically from CodUbic above
        'DatiSuFile': 'false',
        'ChkDatiSuFile': '',}
    
    headers = {'Referer': URL} # if this is not set, the query will return no response (these guys are clever)
    
    r = requests.post(URL, data=payload, headers=headers)

    store = [] # used to store data before saving to

    root = fromstring(r.text)
    for tr in root.cssselect("#VALORI TABLE TR"):
        tds = tr.cssselect("td")
        tds = [td.text_content() for td in tds]
        try:
            start = dateutil.parser.parse(tds[0], dayfirst=True)
            end = dateutil.parser.parse(tds[1], dayfirst=True)
            value = float(tds[2])
        except ValueError:
            pass
        else:
            validato = True if tds[3].strip() == 'Si' else False
            certificato = True if tds[4].strip() == 'Si' else False
            data = {
                'start_time': start,
                'end_time': end,
                'value':value,
                'validato': validato,
                'certificato': certificato,
                'postazione_code': station,
                'sensor_code': sensor,
                }
            store.append(data)
    scraperwiki.sqlite.save(["sensor_code", "postazione_code", "start_time", "end_time"], store)

    # save unique info about sensor and station
    stored = [ {"sensor_code": sensor, "postazione_code": station, "year": year} ]
    scraperwiki.sqlite.save(["sensor_code", "postazione_code", "year"], stored, table_name="stored")

# this check avoids scraping stuff we already did
# but it is very time-consuming so we need to disable it
#stored = scraperwiki.sqlite.select("distinct sensor_code, postazione_code, SUBSTR(start_time, 1, 4) as year from `swdata`")
#for v in stored:
#    v['year'] = int(v['year'])

def update_scraped_sensors():
    '''Brings a secondary ``stored`` table up to date.

    Run only if there are missing data in the secondary ``stored`` table.'''

    stored = scraperwiki.sqlite.select("distinct sensor_code, postazione_code, SUBSTR(start_time, 1, 4) as year from `swdata`")
    for v in stored:
        v['year'] = int(v['year'])
    scraperwiki.sqlite.save(["sensor_code", "postazione_code", "year"], stored, table_name="stored")

def stats():
    '''Basic counts for the stored data.'''

    stored = scraperwiki.sqlite.select("sensor_code, postazione_code, year from stored")
    print(len(stored))

def run():
    '''Main runner for the scraper.'''

    scraperwiki.sqlite.attach("ambiente_in_liguria_-_aria", "src")
    origin = scraperwiki.sqlite.select("sensor_code, postazione_code, year from src.swdata where year = 2012")
    #stored = scraperwiki.sqlite.select("sensor_code, postazione_code, year from stored")
    #unscraped = [v for v in origin if v not in stored]
    sample = random.sample(origin, 10)
    for s in sample:
        last = scraperwiki.sqlite.select("max(end_time) as last from swdata where sensor_code = '%s' and postazione_code = '%s'" % (s['sensor_code'], s['postazione_code']))
        print(last[0]['last'][5:10])
        #query_data(s['year'], "01/01", "31/12", s['postazione_code'], s['sensor_code'])

run()
stats()