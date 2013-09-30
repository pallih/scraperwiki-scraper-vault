# Cambridge Botanical Gardens Temperatures
# David Jones, Climate Code Foundation, 2011-11-23
#
# This is a scrape of http://scraperwiki.com/scrapers/foi_botanical_gardens/
# that has the same data, but in a slightly different format.

import json
import urllib

import scraperwiki

apiprefix = "http://api.scraperwiki.com/api/1.0/datastore/getdata" 
target="foi_botanical_gardens"

def getall(name):
    """Get all the data from a scraper."""

    offset = 0
    limit = 500

    while offset < 10000:
        url = "%s?format=json&name=%s&offset=%d&limit=%s" %(
            apiprefix, name, offset, limit)
        result = json.load(urllib.urlopen(url))
        for row in result:
            yield row
        offset += len(result)
        if len(result) < limit:
            break
    print "got %d records" % offset

def store(seq):
    commondict = dict(id='uk_cbg')
    for row in seq:
        for element in ['tmin', 'tmax']:
            if element not in row:
                continue
            d = {row['Date']:row[element], 'element':element+'D'}
            d.update(commondict)
            scraperwiki.datastore.save(['id', 'element'], d, silent=True)

store(getall(target))
# Cambridge Botanical Gardens Temperatures
# David Jones, Climate Code Foundation, 2011-11-23
#
# This is a scrape of http://scraperwiki.com/scrapers/foi_botanical_gardens/
# that has the same data, but in a slightly different format.

import json
import urllib

import scraperwiki

apiprefix = "http://api.scraperwiki.com/api/1.0/datastore/getdata" 
target="foi_botanical_gardens"

def getall(name):
    """Get all the data from a scraper."""

    offset = 0
    limit = 500

    while offset < 10000:
        url = "%s?format=json&name=%s&offset=%d&limit=%s" %(
            apiprefix, name, offset, limit)
        result = json.load(urllib.urlopen(url))
        for row in result:
            yield row
        offset += len(result)
        if len(result) < limit:
            break
    print "got %d records" % offset

def store(seq):
    commondict = dict(id='uk_cbg')
    for row in seq:
        for element in ['tmin', 'tmax']:
            if element not in row:
                continue
            d = {row['Date']:row[element], 'element':element+'D'}
            d.update(commondict)
            scraperwiki.datastore.save(['id', 'element'], d, silent=True)

store(getall(target))
