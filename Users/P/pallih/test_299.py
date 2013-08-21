import scraperwiki

url = 'https://dl.dropbox.com/s/4nldn4sndoc3v6e/events.json?dl=1'
url2 = 'https://dl.dropbox.com/s/t4buz8otvjy9spu/events2.json?dl=1'

stuff = scraperwiki.scrape(url)


import json


import csv

data = json.loads(stuff)

counter = 0

for item in data['events']:
    record = {}
    for k, v in data['events'][item].iteritems():
        
        record['counter'] = counter
        record[k] = v
    scraperwiki.sqlite.save(unique_keys=['counter'], data=record, table_name="swdata", verbose=2)
    counter = counter +1

    
        
        


