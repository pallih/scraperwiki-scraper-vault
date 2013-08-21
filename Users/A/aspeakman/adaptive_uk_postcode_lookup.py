# adaptive database cache for UK postcode lookups from the Web
# switches between various priority ordered sources to do postcode lookup
# and caches any results in the local database

import scraperwiki
import urllib2, urllib
import time
import json
import sys
import re
from datetime import datetime
from datetime import timedelta

util = scraperwiki.utils.swimport("utility_library")
locat = scraperwiki.utils.swimport("location_library")

DEBUG = False
CACHE_EXPIRY = (datetime.now() - timedelta(days=275)).strftime('%Y-%m-%dT%H:%M:%S') # 9 months

def run(test_query = None):
    try:
        query = scraperwiki.utils.GET()
    except:
        query = {}
    if query and 'test' in query and test_query:
        query = test_query
    format = query.get('fmt', 'xml')
    options = 'location'
    if not format or format == 'rss' or format == 'atom' or format == 'object':
        format = 'xml'
    if format == 'jsonp' or format == 'json':
        options = query.get('callback')
    if format == 'json' and query.get('callback'):
        util.set_content('jsonp')
    elif format:
        util.set_content(format)
    result = { }
    postcode = query.get('postcode')
    if postcode:
        postcode = locat.postcode_norm(postcode)  
    elif query.get('lat') and (query.get('lng') or query.get('lon')):
        lng =  query['lng'] if query.get('lng') else query['lon']
        plookup = locat.postcode_reverse(lng, query['lat'])
        if plookup and plookup.get('postcode'):
            postcode = locat.postcode_norm(plookup['postcode'])
    if postcode: # note any postcode is now in normalised form
        specified_source = query.get('source') # specify a specific source if you want to override the default list
        existing_source = None
        ideal_source = locat.get_postcode_best_source(postcode) # ideal source is the first in the default list
        stale = None
        if specified_source:
            result = None # if source is specified, we always replace the cache entry
            if DEBUG: print "Source specified (", specified_source, ") skipping cache lookup"
        else:
            result = cache_fetch(postcode) # is this query result already in the database cache?
            if result:
                existing_source = result['source']
                if result['date_cached'] < CACHE_EXPIRY:
                    stale = True
                    if DEBUG: print "Found stale cache entry from", existing_source
                else:
                    stale = False
                    if DEBUG: print "Found fresh cache entry from", existing_source
            else:
                if DEBUG: print "Nothing in cache"
        # try to get data afresh if existing entry does not exist or is not from the most preferred source or is stale
        if not result or existing_source <> ideal_source or stale: 
            new_result = locat.geocode_postcode(postcode, existing_source, specified_source)
            if new_result:
                new_result['matched'] = locat.postcode_norm(new_result['postcode'])
                new_result['postcode'] = postcode # always key on the original normalised postcode, not the returned match which can be different e.g. partial
                new_result['fetch_count'] = 0
                new_result['date_cached'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                cache_put(new_result) # put the new result in the cache
                result = new_result            
    if not result:
        result = { 'error': 'Query parameters not recognised', 'query': query }
    print util.data_output(result, format, options)

# query the database cache table
# postcode to be supplied normalised with a single space separator
def cache_fetch(postcode):
    try:
        sql = "* from postcodes where postcode = '" + postcode + "'"
        results = scraperwiki.sqlite.select(sql)
        output = results [0]
        try:
            count = int(output['fetch_count']) + 1
        except:
            count = 1
        sql = "update postcodes set fetch_count = " + str(count) + " where postcode = '" + postcode + "'"
        scraperwiki.sqlite.execute(sql)
        scraperwiki.sqlite.commit()
        return output
    except:
        pass
    return None

def cache_put(data):
    if data.get('postcode'):
        scraperwiki.sqlite.save(unique_keys=['postcode'], data=data, table_name='postcodes', verbose=0)
    
source = None
fmt = 'xml'
#test_query = { 'postcode': 'cb11 4er', 'fmt': fmt, 'source': source  }
#test_query = { 'postcode': 'NE66 3XQ', 'fmt': fmt, 'source': source  }
#test_query = { 'lng': '-1.6', 'lat': '55.5', 'fmt': fmt, 'source': source  }
#test_query = { 'postcode': 'wc1e 6bt', 'fmt': fmt, 'source': source  }
#test_query = { 'postcode': 'ld3 9rr', 'fmt': fmt, 'source': source  }
#test_query = { 'postcode': 'WC1H 8JF', 'fmt': fmt, 'source': source  }
test_query = { 'postcode': 'n16 ', 'fmt': fmt, 'source': source  }

run (test_query)

#sys.exit()


