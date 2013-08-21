import scraperwiki
import json
import re

from scraperwiki.sqlite import save

from lxml import html
from urllib import urlopen

import datetime
import time

def remove_html_tags(x):
    exp = re.compile(r'<[^<]*?>')
    clean_x = exp.sub('', x)
    return clean_x


url="https://www.eventbrite.com/json/event_search?app_key=M2CIAOV4Y4WSOY27VX&within=15&within_unit=M&city=Birmingham&latitude=52.486243&longitude=-1.890401&max=100"

response = urlopen (url)

jsonresponse = json.loads (response.read())

print jsonresponse

HALF_HOUR = 1000 * 60 * 30

def parsedate(evil_date):
  offset = evil_date.find(' GMT')
  date = evil_date[:offset]
  modifier_symbol = evil_date[offset+4:]
  modifier_hour = int(evil_date[offset+4:offset+6])
  modifier_minute = int(evil_date[offset+6:offset+8])
  parsed = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
  delta = datetime.timedelta(hours=modifier_hour, minutes=modifier_minute)
  final = None
  if modifier_symbol == '-':
    final = parsed - delta
  else:
    final = parsed + delta
  return int(float(final.strftime('%s.%f')) * 1000)

for item in jsonresponse['events'][1:]: # [] means dictionary
    print item['event']

#    save([], {"eventid": item['event']['id'],"date": item['event']['start_date']})
#     ,"title":                  item['event'].get('title', None)
    result = {
    "id":                      item['event'].get('id', '')
    ,"title":                  item['event'].get('title', '')
    ,"description":            remove_html_tags(item['event'].get('description',''))
    ,"category":             item['event'].get('category', '')
    ,"start_date":             item['event'].get('start_date', '')
    ,"end_date":               item['event'].get('end_date', '')
    ,"num_attendee_rows":      item['event'].get('num_attendee_rows', '')
    ,"url":                    item['event'].get('url', '')
    ,"logo":                   item['event'].get('logo', '')
    ,"timezone_offset":        item['event'].get('timezone_offset', '')
                               
    ,"venue_name":             item['event']['venue'].get('name', '')
    ,"venue_city":             item['event']['venue'].get('city', '')
    ,"venue_country":          item['event']['venue'].get('country', '')
    ,"venue_region":           item['event']['venue'].get('region', '')
    ,"venue_longitude":        item['event']['venue'].get('longitude', '')
    ,"venue_postal_code":      item['event']['venue'].get('postal_code', '')
    ,"venue_address_2":        item['event']['venue'].get('address_2', '')
    ,"venue_address":          item['event']['venue'].get('address', '')
    ,"venue_latitude":         item['event']['venue'].get('latitude', '')
    ,"venue_longitude":        item['event']['venue'].get('longitude', '')
    ,"venue_country_code":     item['event']['venue'].get('country_code', '')
    ,"venue_id":               item['event']['venue'].get('id', '')
    ,"venue_Lat-Long":         item['event']['venue'].get('Lat-Long', '')
                               
    ,"organizer_url":          item['event']['organizer'].get('url', '')
    ,"organizer_id":           item['event']['organizer'].get('id', '')
    ,"organizer_description":  item['event']['organizer'].get('description', '')
    ,"organizer_name":         item['event']['organizer'].get('name', '')
    ,"organizer_long_description": item['event']['organizer'].get('long_description', '')
   
    }

    output = dict()
    output['id'] = 'eventbrite:' + str(result['id'])
    output['source'] = 'eventbrite'
    output['url'] = result['url']
    output['title'] = result['title']
    output['description'] = result['description']
    output['start'] = parsedate(result['start_date'] + ' ' + result['timezone_offset'])
    output['end'] = parsedate(result['end_date'] + ' ' + result['timezone_offset'])
    if output['start'] == output['end']:
       output['end'] = output['start'] + HALF_HOUR
    output['venue'] = result['venue_name']
    output['city'] = result['venue_city']
    output['location'] = '\n'.join(filter(lambda x: x != '', [result['venue_name'], result['venue_address'], result['venue_address_2'], result['venue_city'], result['venue_region'], result['venue_postal_code'], result['venue_country']]))
    output['geo'] = [result['venue_latitude'], result['venue_longitude']]
    output['categories'] = result['category'].split(',')
    output['modified'] = int(time.time() * 1000)
    result['fourteen_json'] = json.dumps(output)
    
    save([], result)


