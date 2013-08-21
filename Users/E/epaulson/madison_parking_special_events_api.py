# Blank Python
sourcescraper = 'madison_wi_special_event_parking'
import dateutil.parser
try: import simplejson as json
except ImportError: import json

import scraperwiki 
scraperwiki.utils.httpresponseheader('Content-Type', 'application/json')         
scraperwiki.sqlite.attach("madison_wi_special_event_parking")

data = scraperwiki.sqlite.select(
   '''* from swdata'''
)


res = scraperwiki.sqlite.execute('select * from scraperstats')

results = {}
results['LastScraped'] =  dateutil.parser.parse(res['data'][0][0]).isoformat()
results['CacheUntil'] = dateutil.parser.parse(res['data'][0][1]).isoformat()
results['ParkingSpecialEvents'] = data


print json.dumps(results)
