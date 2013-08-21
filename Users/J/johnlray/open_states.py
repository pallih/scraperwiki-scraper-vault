import scraperwiki

html = scraperwiki.scrape("http://openstates.org/api/v1/legislators/?state=ak&active=false&apikey=20bea8ddcf0d4aedaff70cb6d60c4176")

print html

import json
import urllib2
import pprint

url = "http://openstates.org/api/v1/legislators/?state=ak&active=false&apikey=20bea8ddcf0d4aedaff70cb6d60c4176"
data = json.load(urllib2.urlopen(url))

scraperwiki.sqlite.save(
    unique_keys=['leg_id'],
    data=data,
    table_name="swdata",
    verbose=2
    )

