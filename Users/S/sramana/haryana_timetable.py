"""Timetable of buses operated by Haryana Road Transport Corporation
"""

from datetime import datetime
import re
import scraperwiki
import lxml.html

base_url = 'http://hartrans.gov.in/roadways/time_tablelist.asp'
per_page = 50
max = 10000


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


def get_schedules():
    for i in range(max/per_page):
        # We could have requested all pages at once, but the website is choking.
        url = base_url + '?RecPerPage=%s&start=%s' % (per_page, i*per_page+1)
        print url
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        #from IPython import embed
        #embed()
        table = root.cssselect('table #ewlistmain')[0]
        rows = table.cssselect('tr')
        del rows[0] # First row is header

        data = []
        for row in rows:
            cells = [td.text_content() for td in row.cssselect('td')]
            cells = clean(cells)
            rec = dict()

            rec['source'] = cells[0]
            rec['departure_time'] = cells[1].replace(' hrs', '').replace('.', ':')
            rec['destination'] = cells[2]
            rec['via'] = cells[3]
            fare = cells[4].replace('Rs.', '')
            distance = cells[5].replace('Km', '')
            rec['fare_in_rupees'] = int(float(fare)) if fare else None
            rec['distance_in_km'] = int(float(distance)) if distance else None
            rec['service_type'] = cells[6]
            rec['crawled_on'] = datetime.now()

            data.append(rec)

        scraperwiki.sqlite.save(data=data, unique_keys=['source', 'destination', 'via', 'departure_time', 'service_type'])


get_schedules()
"""Timetable of buses operated by Haryana Road Transport Corporation
"""

from datetime import datetime
import re
import scraperwiki
import lxml.html

base_url = 'http://hartrans.gov.in/roadways/time_tablelist.asp'
per_page = 50
max = 10000


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


def get_schedules():
    for i in range(max/per_page):
        # We could have requested all pages at once, but the website is choking.
        url = base_url + '?RecPerPage=%s&start=%s' % (per_page, i*per_page+1)
        print url
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        #from IPython import embed
        #embed()
        table = root.cssselect('table #ewlistmain')[0]
        rows = table.cssselect('tr')
        del rows[0] # First row is header

        data = []
        for row in rows:
            cells = [td.text_content() for td in row.cssselect('td')]
            cells = clean(cells)
            rec = dict()

            rec['source'] = cells[0]
            rec['departure_time'] = cells[1].replace(' hrs', '').replace('.', ':')
            rec['destination'] = cells[2]
            rec['via'] = cells[3]
            fare = cells[4].replace('Rs.', '')
            distance = cells[5].replace('Km', '')
            rec['fare_in_rupees'] = int(float(fare)) if fare else None
            rec['distance_in_km'] = int(float(distance)) if distance else None
            rec['service_type'] = cells[6]
            rec['crawled_on'] = datetime.now()

            data.append(rec)

        scraperwiki.sqlite.save(data=data, unique_keys=['source', 'destination', 'via', 'departure_time', 'service_type'])


get_schedules()
