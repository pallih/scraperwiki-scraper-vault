# it may be each page containing a link to the last inserted sciopero
HOMEPAGE = 'http://www.commissionegaranziasciopero.it/'

import re
# it is the pattern used to extract the id of a sciopero from its details url
id_p = re.compile(r'id=(?P<id>\d+)')
prov = re.compile(r'\(\w+\)')

# it is the url used to request the details of a sciopero
sciopero_prefix = 'http://www.commissionegaranziasciopero.it/dettaglioSciopero?id=%s&tipo=tr'

# it is the waiting time (in seconds) after each request
SLEEP_TIME = 0.1

class GeoSleep():
    def __init__(self):
        self.time = 0
    def reset(self):
        self.time = 0
    def increment(self):
        self.time += 1
geo_sleep = GeoSleep()

# required to save data
import scraperwiki
from scraperwiki import CPUTimeExceededError

# required to parse html
from bs4 import BeautifulSoup

# required to make http calls
import requests

# datatypes
import time
from datetime import datetime

from geopy import geocoders
geo = geocoders.Google(domain='maps.google.it')
gn = geocoders.GeoNames()

def interventi_0_fun(value):
    ret = {}
    if hasattr(value, 'a') and value.a and value.a['href']:
        ret['interventi_pdf'] = value.a['href']
    if hasattr(value, 'span') and hasattr(value.span, 'text'):
        interventi = value.span.text
        interventi = re.sub('\s+', ' ', interventi)
        ret['Interventi'] = interventi
    #if not ret:
    #    print value
    #from pprint import pprint; pprint(ret)
    return ret

def interventi_1_fun(value):
    print 'i1: %s' % value
    ret = {}
    if value.a and 'href' in value.a:
        ret['interventi_pdf'] = value.a['href']
    if hasattr(value, 'text'):
        ret['interventi'] = value.text
    #if 'interventi_pdf' not in ret:
    #    print value
    return ret

ad_hoc = {
    'interventi' : [interventi_0_fun, interventi_1_fun],
}

def resolve_place(place):
    """
    looks for place in cache,
    otherwise make a query to google,
    if it fails make the same query to geonames,
    if success save the place in cache and returns
    """

    place = re.sub(prov, '', place)
    place = place.strip()

    try:
        rs = scraperwiki.sqlite.select("name, lat, long FROM geo_cache WHERE key = ?", (place))
        if len(rs) > 0:
            name = rs[0]['name']
            lat = float(rs[0]['lat'])
            lng = float(rs['0']['long'])

            return (name, (lat, lng))
    except:
        # geo_cache is empty
        pass

    print "Sleeping for %s seconds (geo api)" % geo_sleep.time
    time.sleep(geo_sleep.time)

    try:
        codes = geo.geocode('%s, IT' % place, exactly_one=False)
        geo_sleep.reset()
    except geocoders.google.GQueryError:
        # fallback
        codes = gn.geocode('%s, IT' % place, exactly_one=False)
    except geocoders.google.GTooManyQueriesError:
        # fallback
        codes = gn.geocode('%s, IT' % place, exactly_one=False)
        geo_sleep.increment()
    
    if codes:
        ret = codes[0]
    else:
        codes = ('?', (None, None))
    
    data = {
        'key': place,
        'name': ret[0],
        'lat': float(ret[1][0]),
        'long': float(ret[1][1]),
    }
    scraperwiki.sqlite.save(unique_keys=['key'], data=data, table_name="geo_cache")

    return (data['name'], (data['lat'], data['long']))

def parse_sciopero(s, id):
    """
    This function, given an html representing a sciopero and its id (from the webpage of its details),
    parse the page and finds the interesting data about a sciopero.
    It returns a dict containing the parsed data.
    """

    soup = BeautifulSoup(s, 'lxml')
    
    etichette = soup.find_all('span', {'class': "etichetta"})
    valori = soup.find_all('span', {'class': "valore"})

    sciopero = {'id': id}

    for k, v in zip(etichette, valori):
        k = k.text.strip()
        raw_v = v
        v = v.text.strip()

        if not k:
            continue
        if not v:
            continue
        
        if k.lower() in ad_hoc:
            #print 'ad_hoc'
            for fun in ad_hoc[k.lower()]:
                values = fun(raw_v)
                if values:
                    sciopero.update(values)
                    break
            continue
            
        k = k.encode('ascii', 'ignore') #sqlite doesn't seem to accept "strange" characters as a column name
        v = v.encode('utf-8')
        
        # ad-hoc fields
        if k.lower() == 'organizzazioni sindacali':
            if ', ' in v:
                v = re.split(',\s*', v)

        elif 'data' in k.lower():
            try:
                y, m, d = v.split('-')
                v = datetime(int(y), int(m), int(d)).date()
            except ValueError:
                continue
        elif k.lower() in ['comune', 'localit'] and v not in ['*']:
            #print k, v
            place, coord = resolve_place(v)
            sciopero['place'] = place
            sciopero['lat'], sciopero['long'] = coord

        sciopero[k] = v

    return sciopero

def find_id_range():
    """
    This function scrape the home page of the website, looking for the interval of sciopero scraping.
    The lower limit is the higest (or last inserted) id in the database, or the lowest id in the homepage in case of update.
    The upper limit is the highest id in the homepage.
    It seems to be a good interval, since the home page returns always all the sciopero from today untill the end of the database, ordered by date.
    """
    resp = requests.get(HOMEPAGE)

    soup = BeautifulSoup(resp.content, 'lxml')

    _min = find_first_id()    
    _max = 1

    for a in soup.find_all("a"):
        for m in id_p.finditer(a['href']):
            id = int(m.group('id'))
            _min = min(id, _min)
            _max = max(id, _max)    

    return _min, _max

def find_first_id():
    """
    returns the highest id in the database, or 1 if it's empty
    """
    try:
        rs = scraperwiki.sqlite.select("MAX(id) FROM swdata")
        if len(rs) == 0:
            # if the table is empty
            return 1
        return int(rs[0]['MAX(id)'])
    except:
        # if the table is empty
        return 1

def find_last_id(): # deprecated: see find_id_range()
    """
    This function scrape the home page of the website, looking for the highest id for the sciopero.
    This is required to define the upper limit after which stop the scraper.
    It is a good way, since the home page returns always the last inserted sciopero.
    """
    resp = requests.get(HOMEPAGE)

    soup = BeautifulSoup(resp.content, 'lxml')
    
    _max = 1
    for a in soup.find_all("a"):
        for m in id_p.finditer(a['href']):
            id = int(m.group('id'))
            _max = max(id, _max)

    return _max

def test_sciopero_scraper(id):
    # for testing purpose
    resp = requests.get(sciopero_prefix % str(id))
    return parse_sciopero(resp.content, id)

def sciopero_scraper():
    """
    This function is used to generate the requests for URL containing data.
    It's a generator which returns always a sciopero dict, with at least its id.
    """
    min_id, max_id = find_id_range()
    #print max_id

    print 'scraping from %d to %d' % (min_id, max_id)

    for i in xrange(min_id, max_id):
        try:
            resp = requests.get(sciopero_prefix % str(i))
        except Exception as e:
            print type(e)
            print e
            print dir(e)
            exit()
        print "Sleeping for %s seconds (requests)" % (SLEEP_TIME or 0)
        time.sleep(SLEEP_TIME or 0)

        if resp.status_code == 500 or 'HTTP Status 500' in resp.text:
            continue
        
        #print '%s%s' % (sciopero_prefix, str(i))
        yield parse_sciopero(resp.content, i)

"""
# script di bonifica
import json

rs = scraperwiki.sqlite.select('* FROM swdata')
for row in rs:
    if 'Organizzazioni Sindacali' in row and row['Organizzazioni Sindacali'] and row['Organizzazioni Sindacali'][0] == '[' and row['Organizzazioni Sindacali'][-1] == ']':
        print row['Organizzazioni Sindacali']
        py_data = row['Organizzazioni Sindacali']
        py_data = eval(py_data)
        row['Organizzazioni Sindacali'] = json.dumps(py_data)
        scraperwiki.sqlite.save(["id"], row)
        
exit(0)
"""

"""
from pprint import pprint
pprint(test_sciopero_scraper(133))
"""

# body:
try:
    #print scraperwiki.sqlite.table_info(name="swdata")
    for sciopero in sciopero_scraper():
        if len(sciopero) > 1:
            scraperwiki.sqlite.save(unique_keys=["id"], data=sciopero)
except CPUTimeExceededError:
    print 'the execution must be re-executed to complete the scraping'# it may be each page containing a link to the last inserted sciopero
HOMEPAGE = 'http://www.commissionegaranziasciopero.it/'

import re
# it is the pattern used to extract the id of a sciopero from its details url
id_p = re.compile(r'id=(?P<id>\d+)')
prov = re.compile(r'\(\w+\)')

# it is the url used to request the details of a sciopero
sciopero_prefix = 'http://www.commissionegaranziasciopero.it/dettaglioSciopero?id=%s&tipo=tr'

# it is the waiting time (in seconds) after each request
SLEEP_TIME = 0.1

class GeoSleep():
    def __init__(self):
        self.time = 0
    def reset(self):
        self.time = 0
    def increment(self):
        self.time += 1
geo_sleep = GeoSleep()

# required to save data
import scraperwiki
from scraperwiki import CPUTimeExceededError

# required to parse html
from bs4 import BeautifulSoup

# required to make http calls
import requests

# datatypes
import time
from datetime import datetime

from geopy import geocoders
geo = geocoders.Google(domain='maps.google.it')
gn = geocoders.GeoNames()

def interventi_0_fun(value):
    ret = {}
    if hasattr(value, 'a') and value.a and value.a['href']:
        ret['interventi_pdf'] = value.a['href']
    if hasattr(value, 'span') and hasattr(value.span, 'text'):
        interventi = value.span.text
        interventi = re.sub('\s+', ' ', interventi)
        ret['Interventi'] = interventi
    #if not ret:
    #    print value
    #from pprint import pprint; pprint(ret)
    return ret

def interventi_1_fun(value):
    print 'i1: %s' % value
    ret = {}
    if value.a and 'href' in value.a:
        ret['interventi_pdf'] = value.a['href']
    if hasattr(value, 'text'):
        ret['interventi'] = value.text
    #if 'interventi_pdf' not in ret:
    #    print value
    return ret

ad_hoc = {
    'interventi' : [interventi_0_fun, interventi_1_fun],
}

def resolve_place(place):
    """
    looks for place in cache,
    otherwise make a query to google,
    if it fails make the same query to geonames,
    if success save the place in cache and returns
    """

    place = re.sub(prov, '', place)
    place = place.strip()

    try:
        rs = scraperwiki.sqlite.select("name, lat, long FROM geo_cache WHERE key = ?", (place))
        if len(rs) > 0:
            name = rs[0]['name']
            lat = float(rs[0]['lat'])
            lng = float(rs['0']['long'])

            return (name, (lat, lng))
    except:
        # geo_cache is empty
        pass

    print "Sleeping for %s seconds (geo api)" % geo_sleep.time
    time.sleep(geo_sleep.time)

    try:
        codes = geo.geocode('%s, IT' % place, exactly_one=False)
        geo_sleep.reset()
    except geocoders.google.GQueryError:
        # fallback
        codes = gn.geocode('%s, IT' % place, exactly_one=False)
    except geocoders.google.GTooManyQueriesError:
        # fallback
        codes = gn.geocode('%s, IT' % place, exactly_one=False)
        geo_sleep.increment()
    
    if codes:
        ret = codes[0]
    else:
        codes = ('?', (None, None))
    
    data = {
        'key': place,
        'name': ret[0],
        'lat': float(ret[1][0]),
        'long': float(ret[1][1]),
    }
    scraperwiki.sqlite.save(unique_keys=['key'], data=data, table_name="geo_cache")

    return (data['name'], (data['lat'], data['long']))

def parse_sciopero(s, id):
    """
    This function, given an html representing a sciopero and its id (from the webpage of its details),
    parse the page and finds the interesting data about a sciopero.
    It returns a dict containing the parsed data.
    """

    soup = BeautifulSoup(s, 'lxml')
    
    etichette = soup.find_all('span', {'class': "etichetta"})
    valori = soup.find_all('span', {'class': "valore"})

    sciopero = {'id': id}

    for k, v in zip(etichette, valori):
        k = k.text.strip()
        raw_v = v
        v = v.text.strip()

        if not k:
            continue
        if not v:
            continue
        
        if k.lower() in ad_hoc:
            #print 'ad_hoc'
            for fun in ad_hoc[k.lower()]:
                values = fun(raw_v)
                if values:
                    sciopero.update(values)
                    break
            continue
            
        k = k.encode('ascii', 'ignore') #sqlite doesn't seem to accept "strange" characters as a column name
        v = v.encode('utf-8')
        
        # ad-hoc fields
        if k.lower() == 'organizzazioni sindacali':
            if ', ' in v:
                v = re.split(',\s*', v)

        elif 'data' in k.lower():
            try:
                y, m, d = v.split('-')
                v = datetime(int(y), int(m), int(d)).date()
            except ValueError:
                continue
        elif k.lower() in ['comune', 'localit'] and v not in ['*']:
            #print k, v
            place, coord = resolve_place(v)
            sciopero['place'] = place
            sciopero['lat'], sciopero['long'] = coord

        sciopero[k] = v

    return sciopero

def find_id_range():
    """
    This function scrape the home page of the website, looking for the interval of sciopero scraping.
    The lower limit is the higest (or last inserted) id in the database, or the lowest id in the homepage in case of update.
    The upper limit is the highest id in the homepage.
    It seems to be a good interval, since the home page returns always all the sciopero from today untill the end of the database, ordered by date.
    """
    resp = requests.get(HOMEPAGE)

    soup = BeautifulSoup(resp.content, 'lxml')

    _min = find_first_id()    
    _max = 1

    for a in soup.find_all("a"):
        for m in id_p.finditer(a['href']):
            id = int(m.group('id'))
            _min = min(id, _min)
            _max = max(id, _max)    

    return _min, _max

def find_first_id():
    """
    returns the highest id in the database, or 1 if it's empty
    """
    try:
        rs = scraperwiki.sqlite.select("MAX(id) FROM swdata")
        if len(rs) == 0:
            # if the table is empty
            return 1
        return int(rs[0]['MAX(id)'])
    except:
        # if the table is empty
        return 1

def find_last_id(): # deprecated: see find_id_range()
    """
    This function scrape the home page of the website, looking for the highest id for the sciopero.
    This is required to define the upper limit after which stop the scraper.
    It is a good way, since the home page returns always the last inserted sciopero.
    """
    resp = requests.get(HOMEPAGE)

    soup = BeautifulSoup(resp.content, 'lxml')
    
    _max = 1
    for a in soup.find_all("a"):
        for m in id_p.finditer(a['href']):
            id = int(m.group('id'))
            _max = max(id, _max)

    return _max

def test_sciopero_scraper(id):
    # for testing purpose
    resp = requests.get(sciopero_prefix % str(id))
    return parse_sciopero(resp.content, id)

def sciopero_scraper():
    """
    This function is used to generate the requests for URL containing data.
    It's a generator which returns always a sciopero dict, with at least its id.
    """
    min_id, max_id = find_id_range()
    #print max_id

    print 'scraping from %d to %d' % (min_id, max_id)

    for i in xrange(min_id, max_id):
        try:
            resp = requests.get(sciopero_prefix % str(i))
        except Exception as e:
            print type(e)
            print e
            print dir(e)
            exit()
        print "Sleeping for %s seconds (requests)" % (SLEEP_TIME or 0)
        time.sleep(SLEEP_TIME or 0)

        if resp.status_code == 500 or 'HTTP Status 500' in resp.text:
            continue
        
        #print '%s%s' % (sciopero_prefix, str(i))
        yield parse_sciopero(resp.content, i)

"""
# script di bonifica
import json

rs = scraperwiki.sqlite.select('* FROM swdata')
for row in rs:
    if 'Organizzazioni Sindacali' in row and row['Organizzazioni Sindacali'] and row['Organizzazioni Sindacali'][0] == '[' and row['Organizzazioni Sindacali'][-1] == ']':
        print row['Organizzazioni Sindacali']
        py_data = row['Organizzazioni Sindacali']
        py_data = eval(py_data)
        row['Organizzazioni Sindacali'] = json.dumps(py_data)
        scraperwiki.sqlite.save(["id"], row)
        
exit(0)
"""

"""
from pprint import pprint
pprint(test_sciopero_scraper(133))
"""

# body:
try:
    #print scraperwiki.sqlite.table_info(name="swdata")
    for sciopero in sciopero_scraper():
        if len(sciopero) > 1:
            scraperwiki.sqlite.save(unique_keys=["id"], data=sciopero)
except CPUTimeExceededError:
    print 'the execution must be re-executed to complete the scraping'