# Scrape a list of Canada Weather Stations from Environment Canada
# David Jones, Climate Code Foundation

import datetime
# http://docs.python.org/release/2.6.6/library/json.html
import json
import re
# http://docs.python.org/release/2.6.6/library/urlparse.html
import urlparse

import scraperwiki

# http://www.crummy.com/software/BeautifulSoup/documentation.html
from BeautifulSoup import BeautifulSoup

url="http://www.climate.weatheroffice.gc.ca/climateData/canada_e.html"
searchpage="http://www.climate.weatheroffice.gc.ca/advanceSearch/searchHistoricData_e.html"
url="http://www.climate.weatheroffice.gc.ca/advanceSearch/searchHistoricDataStations_e.html?searchType=stnProv&timeframe=1&lstProvince=All&optLimit=yearRange&StartYear=1840&EndYear=2010&selRowPerPage=All&cmdProvSubmit=Search"

# Create a view that shows extra daily data on left (l) and right (r) of station record.
scraperwiki.sqlite.execute("""Create view if not exists missing_days as
select webid,d,m,julianday(substr(m,1,10))-julianday(substr(d,1,10)) as l,julianday(substr(d,12))-julianday(substr(m,12)) as r from (select mlyRange as m,dlyRange as d,webid from swdata)
""")
scraperwiki.sqlite.commit()

def scrapesoup(soup):
    """Scrape all the stations from the soup."""

    count=0

    # Every StationID appears as the value attribute of
    # an input element with "name='StationID'".  Its
    # preceding siblings contain date ranges for the
    # hourly, daily, and monthly series; the name of
    # the station is the first td element of the enclosing
    # tr.

    for element in soup.findAll('input', attrs=dict(name='StationID')):
        webid = element['value']
        siblings = element.findPreviousSiblings('input')
        parenttr = element.findParent('tr')
        stationname = parenttr.find('td').string
        d = dict(webid=webid, name=stationname)
        for s in siblings:
            if s['name'] in ['mlyRange', 'dlyRange', 'hlyRange']:
                key = s['name']
                v = iso_date_range(s['value'])
                d[key] = v
        scraperwiki.sqlite.save(['webid'], d)
        count +=1
    return count

def scrapere(s):
    """Scrape using good old regular expression."""

    count = 0
    for t in re.findall(r'<td.*?>(.*?)<.*?((?:<input.*?){3}StationID.*?)/>', s, flags=re.DOTALL):
        # t will typically be some tuple like this:
        """
('ALERT A', '<input type="hidden" name="hlyRange" value="1988-04-01|2011-09-06" /><input type="hidden" name="dlyRange" value="N/A" /><input type="hidden" name="mlyRange" value="N/A" /><input type="hidden" name="StationID" value="7559" ')
"""
        # We only want to name,value parts.
        name,rest = t
        print t
        # Assuming ISO-8859-1 is correct (at least on 2011-09-08 it was), but lazy.
        d = dict(name=unicode(name, 'iso-8859-1'))
        for el in re.split(r'>\s*<', rest):
            key = re.search(r'name="(\w+)"', el).group(1)
            value = re.search(r'value="(.*?)"', el).group(1)
            if key in ['mlyRange', 'dlyRange', 'hlyRange']:
                value = iso_date_range(value)
            if key == 'StationID':
                key = 'webid'
            d[key] = value
        scraperwiki.sqlite.save(['webid'], d)
        count += 1
    return count        


search="http://www.climate.weatheroffice.gc.ca/advanceSearch/searchHistoricDataStations_e.html?searchType=stnProv&timeframe=1&lstProvince=PPPP&optLimit=yearRange&StartYear=1840&EndYear=2010&Month=12&Day=28&Year=2010&selRowPerPage=All&cmdProvSubmit=Search"
def scrape_provinces(provinces):
    """*provinces* is a list of (4 character) province codes.
    Scrape each of the search result pages for each province.
    """

    import random
    random.shuffle(provinces)
    # There is a province called ''; searching on it gets all the stations,
    # including some in the OTHR province which it is not possible to find
    # otherwise.  It takes ages, so we'll sort that province to the end.
    provinces.sort(key=lambda x: x == '')
    for code in provinces:
        print "Province", code
        code = code.replace(' ', '+')
        url = search.replace('PPPP', code)
        html = scraperwiki.scrape(url)
#        soup = BeautifulSoup(html)
#        stations = scrapesoup(soup)
        stations = scrapere(html)
        print "  found", stations, "stations"

def iso_date_range(v):
    """Canonicalize *v*, a date range, to be in ISO 8601 format:
    "YYYY-MM-DD/YYYY-MM-DD".
    """

    if re.match('^(\d+-\d+-\d+[|]?){2}', v):
        v = '/'.join(datetime.date(*map(int, date.split('-'))).isoformat() for
            date in v.split('|'))
    return v

def provinces_from_search(url):
    """Extract the provinces from the search page."""
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    # All the province codes appear inside a 'select' element
    # that has id="lstProvince"; each province appears as
    # an 'option' element inside that, with its 'value' attribute
    # as the 4 character province code, and the full name of the province
    # as the content.
    el = soup.find('select', id="lstProvince")
    res = []
    for p in el.findAll('option'):
        code = p['value']
        if code == 'ANY':
            continue
        res.append(code)
    return res

provinces = provinces_from_search(searchpage)
print "Found", len(provinces), "provinces:", ' '.join(provinces)

scrape_provinces(provinces)

print "Scraped"

# Scrape a list of Canada Weather Stations from Environment Canada
# David Jones, Climate Code Foundation

import datetime
# http://docs.python.org/release/2.6.6/library/json.html
import json
import re
# http://docs.python.org/release/2.6.6/library/urlparse.html
import urlparse

import scraperwiki

# http://www.crummy.com/software/BeautifulSoup/documentation.html
from BeautifulSoup import BeautifulSoup

url="http://www.climate.weatheroffice.gc.ca/climateData/canada_e.html"
searchpage="http://www.climate.weatheroffice.gc.ca/advanceSearch/searchHistoricData_e.html"
url="http://www.climate.weatheroffice.gc.ca/advanceSearch/searchHistoricDataStations_e.html?searchType=stnProv&timeframe=1&lstProvince=All&optLimit=yearRange&StartYear=1840&EndYear=2010&selRowPerPage=All&cmdProvSubmit=Search"

# Create a view that shows extra daily data on left (l) and right (r) of station record.
scraperwiki.sqlite.execute("""Create view if not exists missing_days as
select webid,d,m,julianday(substr(m,1,10))-julianday(substr(d,1,10)) as l,julianday(substr(d,12))-julianday(substr(m,12)) as r from (select mlyRange as m,dlyRange as d,webid from swdata)
""")
scraperwiki.sqlite.commit()

def scrapesoup(soup):
    """Scrape all the stations from the soup."""

    count=0

    # Every StationID appears as the value attribute of
    # an input element with "name='StationID'".  Its
    # preceding siblings contain date ranges for the
    # hourly, daily, and monthly series; the name of
    # the station is the first td element of the enclosing
    # tr.

    for element in soup.findAll('input', attrs=dict(name='StationID')):
        webid = element['value']
        siblings = element.findPreviousSiblings('input')
        parenttr = element.findParent('tr')
        stationname = parenttr.find('td').string
        d = dict(webid=webid, name=stationname)
        for s in siblings:
            if s['name'] in ['mlyRange', 'dlyRange', 'hlyRange']:
                key = s['name']
                v = iso_date_range(s['value'])
                d[key] = v
        scraperwiki.sqlite.save(['webid'], d)
        count +=1
    return count

def scrapere(s):
    """Scrape using good old regular expression."""

    count = 0
    for t in re.findall(r'<td.*?>(.*?)<.*?((?:<input.*?){3}StationID.*?)/>', s, flags=re.DOTALL):
        # t will typically be some tuple like this:
        """
('ALERT A', '<input type="hidden" name="hlyRange" value="1988-04-01|2011-09-06" /><input type="hidden" name="dlyRange" value="N/A" /><input type="hidden" name="mlyRange" value="N/A" /><input type="hidden" name="StationID" value="7559" ')
"""
        # We only want to name,value parts.
        name,rest = t
        print t
        # Assuming ISO-8859-1 is correct (at least on 2011-09-08 it was), but lazy.
        d = dict(name=unicode(name, 'iso-8859-1'))
        for el in re.split(r'>\s*<', rest):
            key = re.search(r'name="(\w+)"', el).group(1)
            value = re.search(r'value="(.*?)"', el).group(1)
            if key in ['mlyRange', 'dlyRange', 'hlyRange']:
                value = iso_date_range(value)
            if key == 'StationID':
                key = 'webid'
            d[key] = value
        scraperwiki.sqlite.save(['webid'], d)
        count += 1
    return count        


search="http://www.climate.weatheroffice.gc.ca/advanceSearch/searchHistoricDataStations_e.html?searchType=stnProv&timeframe=1&lstProvince=PPPP&optLimit=yearRange&StartYear=1840&EndYear=2010&Month=12&Day=28&Year=2010&selRowPerPage=All&cmdProvSubmit=Search"
def scrape_provinces(provinces):
    """*provinces* is a list of (4 character) province codes.
    Scrape each of the search result pages for each province.
    """

    import random
    random.shuffle(provinces)
    # There is a province called ''; searching on it gets all the stations,
    # including some in the OTHR province which it is not possible to find
    # otherwise.  It takes ages, so we'll sort that province to the end.
    provinces.sort(key=lambda x: x == '')
    for code in provinces:
        print "Province", code
        code = code.replace(' ', '+')
        url = search.replace('PPPP', code)
        html = scraperwiki.scrape(url)
#        soup = BeautifulSoup(html)
#        stations = scrapesoup(soup)
        stations = scrapere(html)
        print "  found", stations, "stations"

def iso_date_range(v):
    """Canonicalize *v*, a date range, to be in ISO 8601 format:
    "YYYY-MM-DD/YYYY-MM-DD".
    """

    if re.match('^(\d+-\d+-\d+[|]?){2}', v):
        v = '/'.join(datetime.date(*map(int, date.split('-'))).isoformat() for
            date in v.split('|'))
    return v

def provinces_from_search(url):
    """Extract the provinces from the search page."""
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    # All the province codes appear inside a 'select' element
    # that has id="lstProvince"; each province appears as
    # an 'option' element inside that, with its 'value' attribute
    # as the 4 character province code, and the full name of the province
    # as the content.
    el = soup.find('select', id="lstProvince")
    res = []
    for p in el.findAll('option'):
        code = p['value']
        if code == 'ANY':
            continue
        res.append(code)
    return res

provinces = provinces_from_search(searchpage)
print "Found", len(provinces), "provinces:", ' '.join(provinces)

scrape_provinces(provinces)

print "Scraped"

