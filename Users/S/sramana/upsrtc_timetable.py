"""Timetable of buses operated by Uttar Pradesh State Road Transport Corporation (UPSRTC)
"""
from datetime import datetime
import re
import scraperwiki
import lxml.html

base_url = 'http://www.upsrtc.com/online/query/'
services = dict()


def find_by_text(element, selector, text):
    for a in element.cssselect(selector):
        if text in a.text_content():
            return a


def clean(items):
    cleaned = []
    for item in items:
        # Remove non-ascii characters
        item = unicode(item).encode("ascii", "ignore")

        # Remove escaped html characters like &nbsp;
        item = re.sub(r'&\S+;', '', item)

        # Remove extra whitespace
        item = ' '.join(item.split())

        # Change NULL to empty string
        item = item or ''

        # Convert to int if numeric
        try:
            item = int(item)
        except Exception:
            pass

        cleaned.append(item)

    return cleaned


def get_services():
    url = base_url + 'ser_sch_query.asp'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    options = root.cssselect('form[name=frm2] select option')
    for option in options:
        id = option.get('value')
        service_number = option.text_content()
        services[id] = service_number


def get_schedules():
    for service in sorted(services):
        print "Processing", service
        url = base_url + 'QueryByServiceNo.asp'
        params = dict(selSerNo=service)

        try:
            html = scraperwiki.scrape(url, params)
        except Exception as e:
            print "Exception while processing", service
            print e
            continue

        root = lxml.html.fromstring(html)
        table = find_by_text(root, '.tt table', 'Service Name')
        meta_row = find_by_text(table, 'tr', 'Service Name')
        meta_data = [b.text_content() for b in meta_row.cssselect('b')]
        rows = table.cssselect('tr')
        del rows[0:5] # First five rows have just meta-data
        del rows[-1] # Last row is empty

        data = []
        for row in rows:
            cells = [td.text_content() for td in row.cssselect('td')]
            cells = clean(cells)
            meta_data = clean(meta_data)
            rec = dict()
            rec['service_number'] = meta_data[0]
            rec['service_name'] = meta_data[1]
            rec['service_type'] = meta_data[2]
            rec['stop_name'] = cells[0]
            rec['arrival_time'] = cells[1][:5].replace('origi','')
            rec['departure_time'] = cells[2][:5]
            rec['distance_in_km_from_source'] = cells[3]
            rec['fare_in_rupees_from_source'] = cells[4]
            rec['crawled_on'] = datetime.now()

            data.append(rec)

        scraperwiki.sqlite.save(data=data, unique_keys=['service_number', 'stop_name', 'departure_time'])


get_services()
get_schedules()
