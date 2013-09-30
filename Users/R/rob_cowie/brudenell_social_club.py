# -*- coding: utf-8 -*-

"""
Brudenell Social Club scraper
"""

from datetime import datetime
from itertools import repeat
from os import path
import lxml.html
import scraperwiki


ROOT_URL = "http://www.brudenellsocialclub.co.uk/Event"


def element_classes(element):
    """List of an elements classes"""
    return element.attrib.get('class', '').split(' ') or []


def scrape_item(item_elem):
    data = {}
    data['link'] = path.join(PICTUREHOUSES_URL, item_elem.cssselect('.left.a a')[0].attrib['href'].lstrip('/'))
    print data['link']
    data['title'] = item_elem.cssselect('.left.b .movielink')[0].text
    data['description'] = data['title']
    try:
        dt_elem = item_elem[2].cssselect('a')[0]
    except IndexError:
        return None
    if 'epoch' in dt_elem.attrib:
        #data['date'] = datetime.fromtimestamp(float(dt_elem.attrib['epoch'])).strftime('%a, %d %b %Y %H:%M:%S')
        data['date'] = datetime.fromtimestamp(float(dt_elem.attrib['epoch']))
    else:
        return None ## ditch those without date
    return data


def extract_events(url):
    src = scraperwiki.scrape(url)
    root = lxml.html.fromstring(src)
    listings = root.cssselect('.largelist .item')
    listings = [scrape_item(item) for item in listings]
    listings = [listing for listing in listings if listing]
    return listings


def event_months(start_month, start_year, stop_month=None, stop_year=None):
    """Yield (year, month) tuples from start month and year"""
    years = count(start_year)
    months = cycle(xrange(1, 13))
    ## advance to current month
    for i in xrange(start_month - 1):
        months.next()

    for year in years:
        for month in months:
            if month == stop_month and year == stop_year:
                raise StopIteration()
            yield month, year
            if month == 12:
                break




def main():
    now = datetime.utcnow()
    for month, year in event_months(now.month, now.year):
        url = ROOT_URL ## TODO: Add params. Is requests available?
        events = extract_events(HACKNEY_ATTIC_URL)
        try:
            ## Delete future events (so that they are dropped if removed from source)
            scraperwiki.sqlite.execute("DELETE FROM brudenell_events WHERE date >= 'now'")
        except scraperwiki.sqlite.SqliteError, e:
            print str(e)
        for event in events:
            scraperwiki.sqlite.save(['link', 'date'], event, table_name='brudenell_events')

main()
# -*- coding: utf-8 -*-

"""
Brudenell Social Club scraper
"""

from datetime import datetime
from itertools import repeat
from os import path
import lxml.html
import scraperwiki


ROOT_URL = "http://www.brudenellsocialclub.co.uk/Event"


def element_classes(element):
    """List of an elements classes"""
    return element.attrib.get('class', '').split(' ') or []


def scrape_item(item_elem):
    data = {}
    data['link'] = path.join(PICTUREHOUSES_URL, item_elem.cssselect('.left.a a')[0].attrib['href'].lstrip('/'))
    print data['link']
    data['title'] = item_elem.cssselect('.left.b .movielink')[0].text
    data['description'] = data['title']
    try:
        dt_elem = item_elem[2].cssselect('a')[0]
    except IndexError:
        return None
    if 'epoch' in dt_elem.attrib:
        #data['date'] = datetime.fromtimestamp(float(dt_elem.attrib['epoch'])).strftime('%a, %d %b %Y %H:%M:%S')
        data['date'] = datetime.fromtimestamp(float(dt_elem.attrib['epoch']))
    else:
        return None ## ditch those without date
    return data


def extract_events(url):
    src = scraperwiki.scrape(url)
    root = lxml.html.fromstring(src)
    listings = root.cssselect('.largelist .item')
    listings = [scrape_item(item) for item in listings]
    listings = [listing for listing in listings if listing]
    return listings


def event_months(start_month, start_year, stop_month=None, stop_year=None):
    """Yield (year, month) tuples from start month and year"""
    years = count(start_year)
    months = cycle(xrange(1, 13))
    ## advance to current month
    for i in xrange(start_month - 1):
        months.next()

    for year in years:
        for month in months:
            if month == stop_month and year == stop_year:
                raise StopIteration()
            yield month, year
            if month == 12:
                break




def main():
    now = datetime.utcnow()
    for month, year in event_months(now.month, now.year):
        url = ROOT_URL ## TODO: Add params. Is requests available?
        events = extract_events(HACKNEY_ATTIC_URL)
        try:
            ## Delete future events (so that they are dropped if removed from source)
            scraperwiki.sqlite.execute("DELETE FROM brudenell_events WHERE date >= 'now'")
        except scraperwiki.sqlite.SqliteError, e:
            print str(e)
        for event in events:
            scraperwiki.sqlite.save(['link', 'date'], event, table_name='brudenell_events')

main()
