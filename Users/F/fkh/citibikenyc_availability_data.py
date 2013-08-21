import scraperwiki
import json
import sys
import datetime

now = datetime.datetime.now()

source = scraperwiki.scrape("http://api.citybik.es/citibikenyc.json") 

feed = json.loads(source)

for row in feed:
    data = {
    'location': row['name'],
    'id': row['id'],
    'timestamp': row['timestamp'],
    'bikes': row['bikes'],
    'free': row['free']
    }
    scraperwiki.sqlite.save(unique_keys=['timestamp', 'id'], data=data)
    

'''
{"name": "W 52 St & 11 Av", 
"idx": 0,
"timestamp": "2013-06-02T17:39:08.689861", 
"number": 72, "free": 15, "bikes": 19, "coordinates": "", "address": "W 52 St & 11 Av", "lat": 40767272, "lng": -73993928, "id": 0}
'''

