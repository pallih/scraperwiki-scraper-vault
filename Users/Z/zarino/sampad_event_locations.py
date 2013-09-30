import scraperwiki
import requests
import lxml.html
import re

def geocode_postcode(postcode):
    import urllib2, json
    try:
        resp = scraperwiki.scrape('http://mapit.mysociety.org/postcode/%s.json' % urllib2.quote(postcode))
    except urllib2.HTTPError:
        return (None, None)
    else:
        obj = json.loads(resp)
        if obj['wgs84_lat'] and obj['wgs84_lon']:
            return (obj['wgs84_lat'], obj['wgs84_lon'])
        else:
            return (None,None)
    
html = requests.get('http://www.sampad.org.uk/events/')
dom = lxml.html.fromstring(html.text)
total_pages = int(dom.cssselect('.pagination li')[-2].text_content())

for i in range(1,total_pages+1):
    print 'Scraping events page', i
    urls_to_scrape = []
    events = []
    html = requests.get('http://www.sampad.org.uk/events/?page=' + str(i))
    dom = lxml.html.fromstring(html.text)
    for li in dom.cssselect('.event-group li'):
        a = li.cssselect('.unit>a')[0]
        if li.get('class'):
            t = re.sub(r'-', ' ', li.get('class').split(' ')[0])
        else:
            t = None
        html2 = requests.get('http://www.sampad.org.uk' + a.get('href'))
        dom2 = lxml.html.fromstring(html2.text)
        for a2 in dom2.cssselect('#date-venue-info a'):
            postcode_check = re.findall(r'addr=([^&]+)', a2.get('href'))
            if postcode_check:
                postcode = postcode_check[0]
                (lat,lng) = geocode_postcode(postcode)
            else:
                postcode = lat = lng = None
            event = {
                'title': dom2.cssselect('#main-content h1')[0].text,
                'date': dom2.cssselect('#date-venue-info h2')[0].text.strip(),
                'price': dom2.cssselect('#date-venue-info p')[0].text.strip(),
                'location': dom2.cssselect('#date-venue-info p')[1].text.strip(),
                'postcode': postcode,
                'image_url': dom2.cssselect('#main-image')[0].get('src'),
                'type': t,
                'url': a.get('href'),
                'lat': lat,
                'lng': lng
            }
            events.append(event)
    scraperwiki.sqlite.save(['url'], events, 'events')
import scraperwiki
import requests
import lxml.html
import re

def geocode_postcode(postcode):
    import urllib2, json
    try:
        resp = scraperwiki.scrape('http://mapit.mysociety.org/postcode/%s.json' % urllib2.quote(postcode))
    except urllib2.HTTPError:
        return (None, None)
    else:
        obj = json.loads(resp)
        if obj['wgs84_lat'] and obj['wgs84_lon']:
            return (obj['wgs84_lat'], obj['wgs84_lon'])
        else:
            return (None,None)
    
html = requests.get('http://www.sampad.org.uk/events/')
dom = lxml.html.fromstring(html.text)
total_pages = int(dom.cssselect('.pagination li')[-2].text_content())

for i in range(1,total_pages+1):
    print 'Scraping events page', i
    urls_to_scrape = []
    events = []
    html = requests.get('http://www.sampad.org.uk/events/?page=' + str(i))
    dom = lxml.html.fromstring(html.text)
    for li in dom.cssselect('.event-group li'):
        a = li.cssselect('.unit>a')[0]
        if li.get('class'):
            t = re.sub(r'-', ' ', li.get('class').split(' ')[0])
        else:
            t = None
        html2 = requests.get('http://www.sampad.org.uk' + a.get('href'))
        dom2 = lxml.html.fromstring(html2.text)
        for a2 in dom2.cssselect('#date-venue-info a'):
            postcode_check = re.findall(r'addr=([^&]+)', a2.get('href'))
            if postcode_check:
                postcode = postcode_check[0]
                (lat,lng) = geocode_postcode(postcode)
            else:
                postcode = lat = lng = None
            event = {
                'title': dom2.cssselect('#main-content h1')[0].text,
                'date': dom2.cssselect('#date-venue-info h2')[0].text.strip(),
                'price': dom2.cssselect('#date-venue-info p')[0].text.strip(),
                'location': dom2.cssselect('#date-venue-info p')[1].text.strip(),
                'postcode': postcode,
                'image_url': dom2.cssselect('#main-image')[0].get('src'),
                'type': t,
                'url': a.get('href'),
                'lat': lat,
                'lng': lng
            }
            events.append(event)
    scraperwiki.sqlite.save(['url'], events, 'events')
