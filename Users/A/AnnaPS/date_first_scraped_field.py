# It would be nice to have a "date_first_scraped" field that persisted between runs.
# This would make it possible to create an RSS feed and add new items as they appear. 
# This scraper shows one way to create such a field... is there a better way?
from datetime import datetime
import simplejson
import urllib2
import scraperwiki

DATA_URL = 'http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=date_first_scraped_field&query=select%20*%20from%20swdata'
existing_records = urllib2.urlopen(DATA_URL).read()
existing_records = simplejson.loads(existing_records)

record = {}
for i in range(0,1000):
    match_found = False
    record['num'] = i
    record['date_first_scraped'] = datetime.utcnow() 
    for i,x in enumerate(existing_records):
        if x['num']==record['num']:
            scraperwiki.sqlite.save(['num'], existing_records[i]) 
            match_found = True
            break
    if not match_found:
        scraperwiki.sqlite.save(['num'], record)