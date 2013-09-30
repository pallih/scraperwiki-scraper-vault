# Scrapes http://indiawaterportal.org/met_data/
# for min and max temperature over a century

import scraperwiki
from lxml import etree
import csv
from cStringIO import StringIO

PRECIPITATION = "1"
MIN_TEMP = "2"
AVE_TEMP = "3"
MAX_TEMP = "4"

base = "http://www.indiawaterportal.org/met_data/"

data = scraperwiki.scrape(base)

doc = etree.HTML(data)
years = doc.xpath('//select[@name="toYear"]/option[@value != "0"]/@value')
MIN_YEAR = years[0]
MAX_YEAR = years[-1]

options = doc.xpath('//select[@name="state"]/option[@value != "0"]')
states = dict((el.get('value'), el.text) for el in options)

def extract_data(state, district, type):
        url = "%sdata/csv/%s/%s/%s/%s/%s" % (base, state, district, type, MIN_YEAR, MAX_YEAR)
        data = scraperwiki.scrape(url)
        f = StringIO(data)
        f.readline() # blank first line
        f.readline() # header row
        reader = csv.reader(f, dialect=csv.excel_tab)
        tempdata = {}
        for row in reader:
            year = row[0]
            for month in range(1, 13):
                value = row[month]
                key = '%s%02d' % (year, month)
                tempdata[key] = value
        return tempdata

state_districts = {}
for state in states:
    url = "%sdata/state/%s" % (base, state)
    data = scraperwiki.scrape(url)
    doc = etree.HTML(data)
    options = doc.xpath('//option[@value != "0"]')
    districts = dict((el.get('value'), el.text) for el in options)
    state_districts[state] = districts
    for district in districts:
        tmin = extract_data(state, district, MIN_TEMP)
        tmax = extract_data(state, district, MAX_TEMP)
        prec = extract_data(state, district, PRECIPITATION)
        name = "India/%s/%s" % (states[state], districts[district])
        print name
        print tmin
        print tmax
        print prec
        scraperwiki.datastore.save(['name'], dict(name=name, tmin=tmin, tmax=tmax, prec=prec))
# Scrapes http://indiawaterportal.org/met_data/
# for min and max temperature over a century

import scraperwiki
from lxml import etree
import csv
from cStringIO import StringIO

PRECIPITATION = "1"
MIN_TEMP = "2"
AVE_TEMP = "3"
MAX_TEMP = "4"

base = "http://www.indiawaterportal.org/met_data/"

data = scraperwiki.scrape(base)

doc = etree.HTML(data)
years = doc.xpath('//select[@name="toYear"]/option[@value != "0"]/@value')
MIN_YEAR = years[0]
MAX_YEAR = years[-1]

options = doc.xpath('//select[@name="state"]/option[@value != "0"]')
states = dict((el.get('value'), el.text) for el in options)

def extract_data(state, district, type):
        url = "%sdata/csv/%s/%s/%s/%s/%s" % (base, state, district, type, MIN_YEAR, MAX_YEAR)
        data = scraperwiki.scrape(url)
        f = StringIO(data)
        f.readline() # blank first line
        f.readline() # header row
        reader = csv.reader(f, dialect=csv.excel_tab)
        tempdata = {}
        for row in reader:
            year = row[0]
            for month in range(1, 13):
                value = row[month]
                key = '%s%02d' % (year, month)
                tempdata[key] = value
        return tempdata

state_districts = {}
for state in states:
    url = "%sdata/state/%s" % (base, state)
    data = scraperwiki.scrape(url)
    doc = etree.HTML(data)
    options = doc.xpath('//option[@value != "0"]')
    districts = dict((el.get('value'), el.text) for el in options)
    state_districts[state] = districts
    for district in districts:
        tmin = extract_data(state, district, MIN_TEMP)
        tmax = extract_data(state, district, MAX_TEMP)
        prec = extract_data(state, district, PRECIPITATION)
        name = "India/%s/%s" % (states[state], districts[district])
        print name
        print tmin
        print tmax
        print prec
        scraperwiki.datastore.save(['name'], dict(name=name, tmin=tmin, tmax=tmax, prec=prec))
