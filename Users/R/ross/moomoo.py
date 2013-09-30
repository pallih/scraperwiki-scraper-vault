import os, cgi, sys
import json
from datetime import timedelta, datetime
import requests
import scraperwiki

print "Hello"
sys.exit(0)

weather_types = [
"Clear night", "Sunny day", "Partly cloudy (night)", "Partly cloudy (day)",
"Not used", "Mist", "Fog", "Cloudy", "Overcast", "Light rain shower (night)",
"Light rain shower (day)", "Drizzle", "Light rain", "Heavy rain shower (night)",
"Heavy rain shower (day)", "Heavy rain", "Sleet shower (night)", "Sleet shower (day)",
"Sleet", "Hail shower (night)", "Hail shower (day)", "Hail", "Light snow shower (night)", "Light snow shower (day)",
"Light snow", "Heavy snow shower (night)", "Heavy snow shower (day)", "Heavy snow", "Thunder shower (night)", "Thunder shower (day)","Thunder",
]


env = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
API_KEY = env['API_KEY']

SVC_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/all?res=hourly&key={key}"
url = SVC_URL.format(key=API_KEY)

response = requests.get(url)
if response.status_code != 200:
    sys.exit(0)
content = json.loads(response.content)

locations = []
items = []

for loc in content["SiteRep"]["DV"]["Location"]:
    location = dict(id=loc['i'], lat=float(loc['lat']), lon=float(loc['lon']),
                          name=loc['name'], country=loc['country'], 
                          continent=loc['continent'])
    locations.append(location)

    # It's either a list, or it isn't.  Having a value change between dict and
    # list is crappy.
    data = loc['Period']
    if isinstance(data, dict):
        data = [data]

    for p in data:
        # Something wrong with this JSON where some of the Period lists are not []
        if isinstance(p, unicode):
            print 'PANIC'
            continue

        dt = p['value']
        for r in p['Rep']:
            if isinstance(r, unicode):
                print content
                scraperwiki.sqlite.save(['errortime'],{'errortime':datetime.now().date(), 'error': "WOMBLES"}, table_name='scraper_errors')
                continue
            item = {}
            item['when'] = dt[:-1]
            item['wind_gust'] = int(r.get('G','0'))
            item['temperature'] = float(r.get('T','0'))
            item['visibility'] = int(r.get('V','0'))
            item['wind_direction'] = r.get('D','')
            item['wind_speed'] = int(r.get('S','0'))
            item['weather_type'] = weather_types[int(r.get('W','0'))] 
            item['pressure'] = int(r.get('P','0'))
            t = timedelta(minutes=int(r.get('$', '0')))
            d = datetime(1,1,1) + t
            item['time'] = "%02d:%02d" % (d.hour, d.minute)
            item['location'] = location['name']
            items.append(item)

scraperwiki.sqlite.save(['name'], locations, table_name='locations')
scraperwiki.sqlite.save(['time', 'when', 'location'], items, table_name='observations')
import os, cgi, sys
import json
from datetime import timedelta, datetime
import requests
import scraperwiki

print "Hello"
sys.exit(0)

weather_types = [
"Clear night", "Sunny day", "Partly cloudy (night)", "Partly cloudy (day)",
"Not used", "Mist", "Fog", "Cloudy", "Overcast", "Light rain shower (night)",
"Light rain shower (day)", "Drizzle", "Light rain", "Heavy rain shower (night)",
"Heavy rain shower (day)", "Heavy rain", "Sleet shower (night)", "Sleet shower (day)",
"Sleet", "Hail shower (night)", "Hail shower (day)", "Hail", "Light snow shower (night)", "Light snow shower (day)",
"Light snow", "Heavy snow shower (night)", "Heavy snow shower (day)", "Heavy snow", "Thunder shower (night)", "Thunder shower (day)","Thunder",
]


env = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
API_KEY = env['API_KEY']

SVC_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/all?res=hourly&key={key}"
url = SVC_URL.format(key=API_KEY)

response = requests.get(url)
if response.status_code != 200:
    sys.exit(0)
content = json.loads(response.content)

locations = []
items = []

for loc in content["SiteRep"]["DV"]["Location"]:
    location = dict(id=loc['i'], lat=float(loc['lat']), lon=float(loc['lon']),
                          name=loc['name'], country=loc['country'], 
                          continent=loc['continent'])
    locations.append(location)

    # It's either a list, or it isn't.  Having a value change between dict and
    # list is crappy.
    data = loc['Period']
    if isinstance(data, dict):
        data = [data]

    for p in data:
        # Something wrong with this JSON where some of the Period lists are not []
        if isinstance(p, unicode):
            print 'PANIC'
            continue

        dt = p['value']
        for r in p['Rep']:
            if isinstance(r, unicode):
                print content
                scraperwiki.sqlite.save(['errortime'],{'errortime':datetime.now().date(), 'error': "WOMBLES"}, table_name='scraper_errors')
                continue
            item = {}
            item['when'] = dt[:-1]
            item['wind_gust'] = int(r.get('G','0'))
            item['temperature'] = float(r.get('T','0'))
            item['visibility'] = int(r.get('V','0'))
            item['wind_direction'] = r.get('D','')
            item['wind_speed'] = int(r.get('S','0'))
            item['weather_type'] = weather_types[int(r.get('W','0'))] 
            item['pressure'] = int(r.get('P','0'))
            t = timedelta(minutes=int(r.get('$', '0')))
            d = datetime(1,1,1) + t
            item['time'] = "%02d:%02d" % (d.hour, d.minute)
            item['location'] = location['name']
            items.append(item)

scraperwiki.sqlite.save(['name'], locations, table_name='locations')
scraperwiki.sqlite.save(['time', 'when', 'location'], items, table_name='observations')
import os, cgi, sys
import json
from datetime import timedelta, datetime
import requests
import scraperwiki

print "Hello"
sys.exit(0)

weather_types = [
"Clear night", "Sunny day", "Partly cloudy (night)", "Partly cloudy (day)",
"Not used", "Mist", "Fog", "Cloudy", "Overcast", "Light rain shower (night)",
"Light rain shower (day)", "Drizzle", "Light rain", "Heavy rain shower (night)",
"Heavy rain shower (day)", "Heavy rain", "Sleet shower (night)", "Sleet shower (day)",
"Sleet", "Hail shower (night)", "Hail shower (day)", "Hail", "Light snow shower (night)", "Light snow shower (day)",
"Light snow", "Heavy snow shower (night)", "Heavy snow shower (day)", "Heavy snow", "Thunder shower (night)", "Thunder shower (day)","Thunder",
]


env = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
API_KEY = env['API_KEY']

SVC_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/all?res=hourly&key={key}"
url = SVC_URL.format(key=API_KEY)

response = requests.get(url)
if response.status_code != 200:
    sys.exit(0)
content = json.loads(response.content)

locations = []
items = []

for loc in content["SiteRep"]["DV"]["Location"]:
    location = dict(id=loc['i'], lat=float(loc['lat']), lon=float(loc['lon']),
                          name=loc['name'], country=loc['country'], 
                          continent=loc['continent'])
    locations.append(location)

    # It's either a list, or it isn't.  Having a value change between dict and
    # list is crappy.
    data = loc['Period']
    if isinstance(data, dict):
        data = [data]

    for p in data:
        # Something wrong with this JSON where some of the Period lists are not []
        if isinstance(p, unicode):
            print 'PANIC'
            continue

        dt = p['value']
        for r in p['Rep']:
            if isinstance(r, unicode):
                print content
                scraperwiki.sqlite.save(['errortime'],{'errortime':datetime.now().date(), 'error': "WOMBLES"}, table_name='scraper_errors')
                continue
            item = {}
            item['when'] = dt[:-1]
            item['wind_gust'] = int(r.get('G','0'))
            item['temperature'] = float(r.get('T','0'))
            item['visibility'] = int(r.get('V','0'))
            item['wind_direction'] = r.get('D','')
            item['wind_speed'] = int(r.get('S','0'))
            item['weather_type'] = weather_types[int(r.get('W','0'))] 
            item['pressure'] = int(r.get('P','0'))
            t = timedelta(minutes=int(r.get('$', '0')))
            d = datetime(1,1,1) + t
            item['time'] = "%02d:%02d" % (d.hour, d.minute)
            item['location'] = location['name']
            items.append(item)

scraperwiki.sqlite.save(['name'], locations, table_name='locations')
scraperwiki.sqlite.save(['time', 'when', 'location'], items, table_name='observations')
import os, cgi, sys
import json
from datetime import timedelta, datetime
import requests
import scraperwiki

print "Hello"
sys.exit(0)

weather_types = [
"Clear night", "Sunny day", "Partly cloudy (night)", "Partly cloudy (day)",
"Not used", "Mist", "Fog", "Cloudy", "Overcast", "Light rain shower (night)",
"Light rain shower (day)", "Drizzle", "Light rain", "Heavy rain shower (night)",
"Heavy rain shower (day)", "Heavy rain", "Sleet shower (night)", "Sleet shower (day)",
"Sleet", "Hail shower (night)", "Hail shower (day)", "Hail", "Light snow shower (night)", "Light snow shower (day)",
"Light snow", "Heavy snow shower (night)", "Heavy snow shower (day)", "Heavy snow", "Thunder shower (night)", "Thunder shower (day)","Thunder",
]


env = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
API_KEY = env['API_KEY']

SVC_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/all?res=hourly&key={key}"
url = SVC_URL.format(key=API_KEY)

response = requests.get(url)
if response.status_code != 200:
    sys.exit(0)
content = json.loads(response.content)

locations = []
items = []

for loc in content["SiteRep"]["DV"]["Location"]:
    location = dict(id=loc['i'], lat=float(loc['lat']), lon=float(loc['lon']),
                          name=loc['name'], country=loc['country'], 
                          continent=loc['continent'])
    locations.append(location)

    # It's either a list, or it isn't.  Having a value change between dict and
    # list is crappy.
    data = loc['Period']
    if isinstance(data, dict):
        data = [data]

    for p in data:
        # Something wrong with this JSON where some of the Period lists are not []
        if isinstance(p, unicode):
            print 'PANIC'
            continue

        dt = p['value']
        for r in p['Rep']:
            if isinstance(r, unicode):
                print content
                scraperwiki.sqlite.save(['errortime'],{'errortime':datetime.now().date(), 'error': "WOMBLES"}, table_name='scraper_errors')
                continue
            item = {}
            item['when'] = dt[:-1]
            item['wind_gust'] = int(r.get('G','0'))
            item['temperature'] = float(r.get('T','0'))
            item['visibility'] = int(r.get('V','0'))
            item['wind_direction'] = r.get('D','')
            item['wind_speed'] = int(r.get('S','0'))
            item['weather_type'] = weather_types[int(r.get('W','0'))] 
            item['pressure'] = int(r.get('P','0'))
            t = timedelta(minutes=int(r.get('$', '0')))
            d = datetime(1,1,1) + t
            item['time'] = "%02d:%02d" % (d.hour, d.minute)
            item['location'] = location['name']
            items.append(item)

scraperwiki.sqlite.save(['name'], locations, table_name='locations')
scraperwiki.sqlite.save(['time', 'when', 'location'], items, table_name='observations')
