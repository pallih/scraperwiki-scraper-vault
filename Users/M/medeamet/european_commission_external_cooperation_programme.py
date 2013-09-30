import scraperwiki
import urllib2, urllib
from scraperwiki import datastore

from lxml import etree

url = 'http://ec.europa.eu/europeaid/work/funding/beneficiaries/index.cfm?lang=EN&mode=SM&type=grant&order=false&direc=false&paging.offset=1&paging.len=5000'
urldata = {
    'lang': 'EN',
    'method': 'doQueryGrants',
    'year': '2007',
    'makeGrants': '-1',
    'region': '-1',
    'amount': '-1',
    'organisation': '',
    'doSearch': 'true',
    'doMode': 'SM',
}

idfn = lambda s: s
def comma_int(s):
    if not s:
        return None
    return int(s.replace(',', ''))

def empty_int(s):
    if not s:
        return None
    return int(s)

def percent(s):
    if not s:
        return None
    assert s.endswith(' %')
    return float(s[:-2])/100

columns = (
        ('contract_number', idfn),
        ('title', idfn),
        ('dac_code', empty_int),
        ('theme', idfn),
        ('organisation', idfn),
        ('org_nationality', idfn),
        ('country_region', idfn),
        ('action_location', idfn),
        ('amount', comma_int),
        ('ec_financing', percent),
        ('total_cost', comma_int),
        ('duration', idfn),
)

def strip(e):
    if e.text is None:
        return ''
    return e.text.strip()

for year in (2007, 2008, 2009):
    urldata['year'] = str(year)
    f = urllib2.urlopen(url, data=urllib.urlencode(urldata))
    parser = etree.HTMLParser()
    root = etree.parse(f, parser)

    for row in root.findall("//tr[@id='currencies']"):
        data = dict((name, convert(strip(cell))) for (name, convert), cell in zip(columns, row))
        assert len(data) == len(columns)
        data['year'] = year
        datastore.save(unique_keys=['contract_number'], data=data)


import scraperwiki
import urllib2, urllib
from scraperwiki import datastore

from lxml import etree

url = 'http://ec.europa.eu/europeaid/work/funding/beneficiaries/index.cfm?lang=EN&mode=SM&type=grant&order=false&direc=false&paging.offset=1&paging.len=5000'
urldata = {
    'lang': 'EN',
    'method': 'doQueryGrants',
    'year': '2007',
    'makeGrants': '-1',
    'region': '-1',
    'amount': '-1',
    'organisation': '',
    'doSearch': 'true',
    'doMode': 'SM',
}

idfn = lambda s: s
def comma_int(s):
    if not s:
        return None
    return int(s.replace(',', ''))

def empty_int(s):
    if not s:
        return None
    return int(s)

def percent(s):
    if not s:
        return None
    assert s.endswith(' %')
    return float(s[:-2])/100

columns = (
        ('contract_number', idfn),
        ('title', idfn),
        ('dac_code', empty_int),
        ('theme', idfn),
        ('organisation', idfn),
        ('org_nationality', idfn),
        ('country_region', idfn),
        ('action_location', idfn),
        ('amount', comma_int),
        ('ec_financing', percent),
        ('total_cost', comma_int),
        ('duration', idfn),
)

def strip(e):
    if e.text is None:
        return ''
    return e.text.strip()

for year in (2007, 2008, 2009):
    urldata['year'] = str(year)
    f = urllib2.urlopen(url, data=urllib.urlencode(urldata))
    parser = etree.HTMLParser()
    root = etree.parse(f, parser)

    for row in root.findall("//tr[@id='currencies']"):
        data = dict((name, convert(strip(cell))) for (name, convert), cell in zip(columns, row))
        assert len(data) == len(columns)
        data['year'] = year
        datastore.save(unique_keys=['contract_number'], data=data)


