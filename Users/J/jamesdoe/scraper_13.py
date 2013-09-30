import resource
import scraperwiki
import lxml.html
import sys
import re
import urllib2
import simplejson
from pprint import pprint
import json  

# data = json.load(json_data)


url = 'http://www.flavorus.com/wafform.aspx?_act=eventcalendarwidget&AJAX=1&FetchEvents=1&_pky=&start=1372557129&end=1388563199'
source = scraperwiki.scrape(url)
decoded_data = json.loads(source)
 
for event in decoded_data:
    event_url = event["url"]
    event_url = event_url.replace("javascript: self.parent.location.href='", "");
    event_url = event_url.replace("';", "")

    html = scraperwiki.scrape(event_url)
    root = lxml.html.fromstring(html)

    try:
        venue_details = root.cssselect(".event-page-location")[0]
    except (IndexError):
        venue_details = ""

    try:
        venue_address = venue_details.cssselect(".m-t-10 h5+p")[0].text_content()
        venue_url = venue_details.cssselect("h5 a")[0].attrib.get('href')
        venue_name = venue_details.cssselect("h5 a")[0].text_content()
        venue_directions_url = venue_details.cssselect(".m-t-10 .float-r a")[0].attrib.get('href')
    except (IndexError,AttributeError):
        venue_directions_url = ""
        venue_address = ""
        venue_url = ""
        venue_directions_url = ""

    try:
        event_image = root.cssselect(".event-images-box a")[0].attrib.get('href')
    except (IndexError):
        event_image = ""
    try:
        description = root.cssselect(".event-details")[0].text_content()
    except (IndexError):
        description = ""

    data = {
        "day" : event["day"],
        "id" : event["id"],
        "month" : event["month"],
        "start" : event["start"],
        "startdateonly" : event["startdateonly"],
        "title" : event["title"],
        "url" : event_url,
        "year" : event["year"],
        "venueName" : venue_name,
        "venueAddress" : venue_address,
        "venueDirectionsURL" : venue_directions_url,
        "eventImage" : event_image,
        "description" : description,
        "source" : "flavorus"
    }
        
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)import resource
import scraperwiki
import lxml.html
import sys
import re
import urllib2
import simplejson
from pprint import pprint
import json  

# data = json.load(json_data)


url = 'http://www.flavorus.com/wafform.aspx?_act=eventcalendarwidget&AJAX=1&FetchEvents=1&_pky=&start=1372557129&end=1388563199'
source = scraperwiki.scrape(url)
decoded_data = json.loads(source)
 
for event in decoded_data:
    event_url = event["url"]
    event_url = event_url.replace("javascript: self.parent.location.href='", "");
    event_url = event_url.replace("';", "")

    html = scraperwiki.scrape(event_url)
    root = lxml.html.fromstring(html)

    try:
        venue_details = root.cssselect(".event-page-location")[0]
    except (IndexError):
        venue_details = ""

    try:
        venue_address = venue_details.cssselect(".m-t-10 h5+p")[0].text_content()
        venue_url = venue_details.cssselect("h5 a")[0].attrib.get('href')
        venue_name = venue_details.cssselect("h5 a")[0].text_content()
        venue_directions_url = venue_details.cssselect(".m-t-10 .float-r a")[0].attrib.get('href')
    except (IndexError,AttributeError):
        venue_directions_url = ""
        venue_address = ""
        venue_url = ""
        venue_directions_url = ""

    try:
        event_image = root.cssselect(".event-images-box a")[0].attrib.get('href')
    except (IndexError):
        event_image = ""
    try:
        description = root.cssselect(".event-details")[0].text_content()
    except (IndexError):
        description = ""

    data = {
        "day" : event["day"],
        "id" : event["id"],
        "month" : event["month"],
        "start" : event["start"],
        "startdateonly" : event["startdateonly"],
        "title" : event["title"],
        "url" : event_url,
        "year" : event["year"],
        "venueName" : venue_name,
        "venueAddress" : venue_address,
        "venueDirectionsURL" : venue_directions_url,
        "eventImage" : event_image,
        "description" : description,
        "source" : "flavorus"
    }
        
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)import resource
import scraperwiki
import lxml.html
import sys
import re
import urllib2
import simplejson
from pprint import pprint
import json  

# data = json.load(json_data)


url = 'http://www.flavorus.com/wafform.aspx?_act=eventcalendarwidget&AJAX=1&FetchEvents=1&_pky=&start=1372557129&end=1388563199'
source = scraperwiki.scrape(url)
decoded_data = json.loads(source)
 
for event in decoded_data:
    event_url = event["url"]
    event_url = event_url.replace("javascript: self.parent.location.href='", "");
    event_url = event_url.replace("';", "")

    html = scraperwiki.scrape(event_url)
    root = lxml.html.fromstring(html)

    try:
        venue_details = root.cssselect(".event-page-location")[0]
    except (IndexError):
        venue_details = ""

    try:
        venue_address = venue_details.cssselect(".m-t-10 h5+p")[0].text_content()
        venue_url = venue_details.cssselect("h5 a")[0].attrib.get('href')
        venue_name = venue_details.cssselect("h5 a")[0].text_content()
        venue_directions_url = venue_details.cssselect(".m-t-10 .float-r a")[0].attrib.get('href')
    except (IndexError,AttributeError):
        venue_directions_url = ""
        venue_address = ""
        venue_url = ""
        venue_directions_url = ""

    try:
        event_image = root.cssselect(".event-images-box a")[0].attrib.get('href')
    except (IndexError):
        event_image = ""
    try:
        description = root.cssselect(".event-details")[0].text_content()
    except (IndexError):
        description = ""

    data = {
        "day" : event["day"],
        "id" : event["id"],
        "month" : event["month"],
        "start" : event["start"],
        "startdateonly" : event["startdateonly"],
        "title" : event["title"],
        "url" : event_url,
        "year" : event["year"],
        "venueName" : venue_name,
        "venueAddress" : venue_address,
        "venueDirectionsURL" : venue_directions_url,
        "eventImage" : event_image,
        "description" : description,
        "source" : "flavorus"
    }
        
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)import resource
import scraperwiki
import lxml.html
import sys
import re
import urllib2
import simplejson
from pprint import pprint
import json  

# data = json.load(json_data)


url = 'http://www.flavorus.com/wafform.aspx?_act=eventcalendarwidget&AJAX=1&FetchEvents=1&_pky=&start=1372557129&end=1388563199'
source = scraperwiki.scrape(url)
decoded_data = json.loads(source)
 
for event in decoded_data:
    event_url = event["url"]
    event_url = event_url.replace("javascript: self.parent.location.href='", "");
    event_url = event_url.replace("';", "")

    html = scraperwiki.scrape(event_url)
    root = lxml.html.fromstring(html)

    try:
        venue_details = root.cssselect(".event-page-location")[0]
    except (IndexError):
        venue_details = ""

    try:
        venue_address = venue_details.cssselect(".m-t-10 h5+p")[0].text_content()
        venue_url = venue_details.cssselect("h5 a")[0].attrib.get('href')
        venue_name = venue_details.cssselect("h5 a")[0].text_content()
        venue_directions_url = venue_details.cssselect(".m-t-10 .float-r a")[0].attrib.get('href')
    except (IndexError,AttributeError):
        venue_directions_url = ""
        venue_address = ""
        venue_url = ""
        venue_directions_url = ""

    try:
        event_image = root.cssselect(".event-images-box a")[0].attrib.get('href')
    except (IndexError):
        event_image = ""
    try:
        description = root.cssselect(".event-details")[0].text_content()
    except (IndexError):
        description = ""

    data = {
        "day" : event["day"],
        "id" : event["id"],
        "month" : event["month"],
        "start" : event["start"],
        "startdateonly" : event["startdateonly"],
        "title" : event["title"],
        "url" : event_url,
        "year" : event["year"],
        "venueName" : venue_name,
        "venueAddress" : venue_address,
        "venueDirectionsURL" : venue_directions_url,
        "eventImage" : event_image,
        "description" : description,
        "source" : "flavorus"
    }
        
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)