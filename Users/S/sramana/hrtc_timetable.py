"""Timetable for buses operated by Himachal Road Transport Corporation (HRTC)
"""
from datetime import datetime
import time
import pickle
import scraperwiki
import lxml.html
import requests

base_url = 'http://hrtc.gov.in/hrtc/db/'
sources = []
destinations = []

var = scraperwiki.sqlite.get_var('crawled')
if var:
    crawled = pickle.loads(var)
else:
    crawled = set()

def clean(rec):
    for k,v in rec.items():
        v = ' '.join(v.split())
        v = v.replace('--', '')
        v = v.replace(' Kms', '')

        if k == 'service_type':
            v = v.replace(']', '')

        if k == 'fare_in_rupees_from_source' and v:
            v = v.split()[1]

        if k in ['arrival_time', 'departure_time']:
            v = v.replace(' PM', '')
            v = v.replace(' AM', '')

        rec[k] = v


def get_sources_and_destinations():
    url = base_url + 'route.asp'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for option in root.cssselect('select[name=from] option'):
        id = option.get('value')
        if id == "0":
            continue
        sources.append(id)

    for option in root.cssselect('select[name=to] option'):
        id = option.get('value')
        if id == "0":
            continue
        destinations.append(id)


def get_schedules():
    for source in sources:
        for destination in destinations:
            if source == 'AMBALA' and destination == 'GURGAON':
                continue 
            if source == destination:
                continue

            if (source, destination) in crawled:
                continue
            crawled.add((source, destination))

            #time.sleep(1)
            print "Fetching schedules from", source, "to", destination
            url = base_url + 'dispdatan.asp'
            params = {'from':source,
                      'to':destination,
                      'c1':0,
                      'B1':'Search'}
            html = requests.post(url, data=params).content
            root = lxml.html.fromstring(html)
            links = [a.get('href') for a in root.cssselect('a')]
            links = sorted(set(links))

            data = []
            for link in links:
                if link in crawled:
                    print link, "already crawled"
                    continue

                crawled.add(link)
                print "Fetching route", link
                url = base_url + link
                html = scraperwiki.scrape(url)
                root = lxml.html.fromstring(html)
                rows = root.cssselect('#AutoNumber1 tr')

                rows.pop(-1) # Last row is dummy
                row1 = rows.pop(0) # Service details
                row2 = rows.pop(0) # Table headers
                service = str(row1.text_content())

                for row in rows:
                    cells = [td.text_content() for td in row.cssselect('td')]
                    rec = dict()
                    rec['stop_name'] = cells[0]
                    rec['arrival_time'] = cells[1]
                    rec['departure_time'] = cells[2]
                    rec['distance_in_km_from_source'] = cells[3]
                    rec['fare_in_rupees_from_source'] = cells[4]

                    rec['service_number'] = link.split('=')[-1]
                    rec['service_name'] = service.split('[')[0]
                    rec['service_type'] = service.split('[')[-1]

                    clean(rec)
                    rec['updated_on'] = datetime.now()
                    data.append(rec)

            scraperwiki.sqlite.save(data=data, unique_keys=['service_number', 'stop_name', 'departure_time'])
            scraperwiki.sqlite.save_var('crawled', pickle.dumps(crawled))


get_sources_and_destinations()
get_schedules()
"""Timetable for buses operated by Himachal Road Transport Corporation (HRTC)
"""
from datetime import datetime
import time
import pickle
import scraperwiki
import lxml.html
import requests

base_url = 'http://hrtc.gov.in/hrtc/db/'
sources = []
destinations = []

var = scraperwiki.sqlite.get_var('crawled')
if var:
    crawled = pickle.loads(var)
else:
    crawled = set()

def clean(rec):
    for k,v in rec.items():
        v = ' '.join(v.split())
        v = v.replace('--', '')
        v = v.replace(' Kms', '')

        if k == 'service_type':
            v = v.replace(']', '')

        if k == 'fare_in_rupees_from_source' and v:
            v = v.split()[1]

        if k in ['arrival_time', 'departure_time']:
            v = v.replace(' PM', '')
            v = v.replace(' AM', '')

        rec[k] = v


def get_sources_and_destinations():
    url = base_url + 'route.asp'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for option in root.cssselect('select[name=from] option'):
        id = option.get('value')
        if id == "0":
            continue
        sources.append(id)

    for option in root.cssselect('select[name=to] option'):
        id = option.get('value')
        if id == "0":
            continue
        destinations.append(id)


def get_schedules():
    for source in sources:
        for destination in destinations:
            if source == 'AMBALA' and destination == 'GURGAON':
                continue 
            if source == destination:
                continue

            if (source, destination) in crawled:
                continue
            crawled.add((source, destination))

            #time.sleep(1)
            print "Fetching schedules from", source, "to", destination
            url = base_url + 'dispdatan.asp'
            params = {'from':source,
                      'to':destination,
                      'c1':0,
                      'B1':'Search'}
            html = requests.post(url, data=params).content
            root = lxml.html.fromstring(html)
            links = [a.get('href') for a in root.cssselect('a')]
            links = sorted(set(links))

            data = []
            for link in links:
                if link in crawled:
                    print link, "already crawled"
                    continue

                crawled.add(link)
                print "Fetching route", link
                url = base_url + link
                html = scraperwiki.scrape(url)
                root = lxml.html.fromstring(html)
                rows = root.cssselect('#AutoNumber1 tr')

                rows.pop(-1) # Last row is dummy
                row1 = rows.pop(0) # Service details
                row2 = rows.pop(0) # Table headers
                service = str(row1.text_content())

                for row in rows:
                    cells = [td.text_content() for td in row.cssselect('td')]
                    rec = dict()
                    rec['stop_name'] = cells[0]
                    rec['arrival_time'] = cells[1]
                    rec['departure_time'] = cells[2]
                    rec['distance_in_km_from_source'] = cells[3]
                    rec['fare_in_rupees_from_source'] = cells[4]

                    rec['service_number'] = link.split('=')[-1]
                    rec['service_name'] = service.split('[')[0]
                    rec['service_type'] = service.split('[')[-1]

                    clean(rec)
                    rec['updated_on'] = datetime.now()
                    data.append(rec)

            scraperwiki.sqlite.save(data=data, unique_keys=['service_number', 'stop_name', 'departure_time'])
            scraperwiki.sqlite.save_var('crawled', pickle.dumps(crawled))


get_sources_and_destinations()
get_schedules()
