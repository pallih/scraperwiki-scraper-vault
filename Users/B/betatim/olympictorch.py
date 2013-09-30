import scraperwiki

import json
import pprint
import urllib
import urllib2


def get_json(url):
    req = urllib2.Request(url)

    req.add_header("User-Agent", "Mozilla")
    req.add_header("Host", "mappingdata.london2012.com")
    req.add_header("Accept", "*/*")

    r = urllib2.urlopen(req)
    text = r.read()

    return json.loads(text)

events_url = "http://mappingdata.london2012.com/torchevents/byarea"
params = {'datasetId': 'TorchRoute-59da3655-1856-4244-b225-38b8420421db',
          'top': '61.53228',
          'left': '-16.91897',
          'bottom': '43.59495',
          'right': '13.66697',
          'zoomLevel': '11',
          }
all_events_url = (events_url + "?" + urllib.urlencode(params) + "&" +
                  urllib.urlencode({'eventTypes': 1}) + "&" +
                  urllib.urlencode({'eventTypes': 2}) + "&" +
                  urllib.urlencode({'eventTypes': 3}) + "&" +
                  urllib.urlencode({'eventTypes': 5})
           )

event_details_url ="http://mappingdata.london2012.com/torchevents/eventdetails?entityid=%s&datasetId=TorchRoute-59da3655-1856-4244-b225-38b8420421db"

events = get_json(all_events_url)

for event in events:
    try:
        event_details = get_json(event_details_url%(event['entityId'] + "S"))
    
    # For some events we get a 404 if we use the extra "S" which gives us more
    # details for an event. Retry without it, and give up otherwise
    except urllib2.HTTPError, e:
        if e.code == 404:
            event_details = get_json(event_details_url%(event['entityId']))
        
    if event_details['entityId'].endswith("S"):
        event_details['entityId'] = event_details['entityId'][:-1]

    scraperwiki.sqlite.save(['entityId'], event_details)

import scraperwiki

import json
import pprint
import urllib
import urllib2


def get_json(url):
    req = urllib2.Request(url)

    req.add_header("User-Agent", "Mozilla")
    req.add_header("Host", "mappingdata.london2012.com")
    req.add_header("Accept", "*/*")

    r = urllib2.urlopen(req)
    text = r.read()

    return json.loads(text)

events_url = "http://mappingdata.london2012.com/torchevents/byarea"
params = {'datasetId': 'TorchRoute-59da3655-1856-4244-b225-38b8420421db',
          'top': '61.53228',
          'left': '-16.91897',
          'bottom': '43.59495',
          'right': '13.66697',
          'zoomLevel': '11',
          }
all_events_url = (events_url + "?" + urllib.urlencode(params) + "&" +
                  urllib.urlencode({'eventTypes': 1}) + "&" +
                  urllib.urlencode({'eventTypes': 2}) + "&" +
                  urllib.urlencode({'eventTypes': 3}) + "&" +
                  urllib.urlencode({'eventTypes': 5})
           )

event_details_url ="http://mappingdata.london2012.com/torchevents/eventdetails?entityid=%s&datasetId=TorchRoute-59da3655-1856-4244-b225-38b8420421db"

events = get_json(all_events_url)

for event in events:
    try:
        event_details = get_json(event_details_url%(event['entityId'] + "S"))
    
    # For some events we get a 404 if we use the extra "S" which gives us more
    # details for an event. Retry without it, and give up otherwise
    except urllib2.HTTPError, e:
        if e.code == 404:
            event_details = get_json(event_details_url%(event['entityId']))
        
    if event_details['entityId'].endswith("S"):
        event_details['entityId'] = event_details['entityId'][:-1]

    scraperwiki.sqlite.save(['entityId'], event_details)

