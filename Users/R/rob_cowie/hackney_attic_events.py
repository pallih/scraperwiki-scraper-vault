# -*- coding: utf-8 -*-

"""
title
link
description
date
"""

from datetime import datetime
from os import path
import lxml.html
import scraperwiki


PICTUREHOUSES_URL = "http://www.picturehouses.co.uk"
HACKNEY_ATTIC_URL = "http://www.picturehouses.co.uk/cinema/Hackney_Picturehouse/Attic/Hackney_Attic_Events/"


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


def main():
    events = extract_events(HACKNEY_ATTIC_URL)
    try:
        ## Delete future events (so that they are dropped if removed from source)
        scraperwiki.sqlite.execute("DELETE FROM hackney_attic_events WHERE date >= 'now'")
    except scraperwiki.sqlite.SqliteError, e:
        print str(e)
    for event in events:
        scraperwiki.sqlite.save(['link', 'date'], event, table_name='hackney_attic_events')

main()
# -*- coding: utf-8 -*-

"""
title
link
description
date
"""

from datetime import datetime
from os import path
import lxml.html
import scraperwiki


PICTUREHOUSES_URL = "http://www.picturehouses.co.uk"
HACKNEY_ATTIC_URL = "http://www.picturehouses.co.uk/cinema/Hackney_Picturehouse/Attic/Hackney_Attic_Events/"


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


def main():
    events = extract_events(HACKNEY_ATTIC_URL)
    try:
        ## Delete future events (so that they are dropped if removed from source)
        scraperwiki.sqlite.execute("DELETE FROM hackney_attic_events WHERE date >= 'now'")
    except scraperwiki.sqlite.SqliteError, e:
        print str(e)
    for event in events:
        scraperwiki.sqlite.save(['link', 'date'], event, table_name='hackney_attic_events')

main()
