# -*- coding: UTF8 -*-
"""
Scraperwiki script - translink_ni_timetables

First scrape the index pages to find each individual service, then follow
and scrape the service link to get the timetable data.
"""

from itertools import groupby, izip, count, chain

import lxml.html
import requests
import scraperwiki

###########################################################################
# CONSTANTS
###########################################################################
TRANSLINK_URL = 'http://www.translink.co.uk'
METRO_URL = TRANSLINK_URL + '/Metro/Metro-Timetables'
metro_index_fmt = METRO_URL + '/Metro-%s-Timetables/'
TRANSLINK_METRO_INDEX_URLS = [
    metro_index_fmt % i for i in range(1, 10)
] + [
    metro_index_fmt % '910',
] + [
    metro_index_fmt % i for i in range(11, 13)
] + [
    METRO_URL + '/All-Other-Metro-Timetables/'
]
# JS/POST-based pagination hides second page of links in a few cases
# Add the ones that can't be obtained with a GET to this EXTRAS list
TRANSLINK_METRO_EXTRAS = [METRO_URL + X for X in [
    '/All-Other-Metro-Timetables/Metro-Service-650A-Inbound/',
    '/Metro-910-Timetables/Metro-Service-10F-Inbound/',
    '/Metro-910-Timetables/Metro-Service-10F-Outbound/',
    '/Metro-910-Timetables/Metro-Service-10G-Inbound/',
    '/Metro-910-Timetables/Metro-Service-10H-Inbound/',
    '/Metro-910-Timetables/Metro-Service-10H-Outbound/',
    '/Metro-910-Timetables/Metro-Service-10X-Inbound/',
    '/Metro-910-Timetables/Metro-Service-10X-Outbound/',
    '/Metro-2-Timetables/Metro-Service-2G-Inbound/',
    '/Metro-2-Timetables/Metro-Service-2G-Outbound/',
    '/Metro-2-Timetables/Metro-Service-2H-Inbound/',
    '/Metro-2-Timetables/Metro-Service-2H-Outbound/',
]]
TRANSLINK_ULSTERBUS_INDEX = TRANSLINK_URL + '/Timetables/Ulsterbus-Timetables/'
TRANSLINK_GOLDLINE_INDEX = TRANSLINK_URL + '/Timetables/Goldline-Timetables/'
TRANSLINK_ENTERPRISE_INDEX = TRANSLINK_URL + '/Timetables/Enterprise-Timetables/'

TRANSLINK_ID = 'translinkni'
TRANSLINK_NAME = 'Translink N.I.'
METRO_ID = 'METRO'
METRO_NAME = 'Translink N.I. (Metro)'
ULSTERBUS_ID = 'ULB'
GOLDLINE_ID = 'GLE'
ENTERPRISE_ID = 'ENT'
NIRAIL_ID = 'NIR'

BUS_ROUTE_TYPE = 3
RAIL_ROUTE_TYPE = 2
DIRECTIONCODES = {'inbound': 1, 'outbound': 0}
TRIPDATAJOINER = '|'
TRIPDATAPARTJOINER = '#'

# we want to save the per-stop schedule for every stop on every route
UNIQUE_KEYS = [
    'agency_id', 'operator_id', 'route_id', 'stop_sequence',
]
DEBUG = True

if DEBUG:
    TRANSLINK_METRO_INDEX_URLS = [
        metro_index_fmt % 1,
        metro_index_fmt % 2,
    ]

###########################################################################
# UTILS
###########################################################################
scrape = scraperwiki.scrape
store = scraperwiki.sqlite.save
parse = lxml.html.fromstring

def strip(s):
    return (' '.join(s.split('&nbsp;'))).strip()

def determine_route(text):
    begin = end = 'UNKNOWN'
    if text:
        text = text.upper()
        if text.endswith('(AIRPORT EXPRESS 300)'):
            text = text[:-len('(AIRPORT EXPRESS 300)')].strip()
        route = text.split('-')
        begin = strip(route[0])
        end = strip(route[-1])
        if end == 'INBOUND' or end == 'OUTBOUND' or end.endswith('RAIL SERVICE'):
            if len(route) > 2:
                end = strip(route[-2])
            else:
                end = begin
    return begin, end


def valid_metro_route_url(url):
    return url.startswith(
        '/Metro/Metro-Timetables/'
    ) and url.endswith('bound/')

def valid_ulsterbus_route_url(url):
    return url.startswith(
        '/Timetables/Ulsterbus-Timetables/'
    ) and url.endswith('bound/')

def valid_goldline_route_url(url):
    return url.startswith(
        '/Timetables/Goldline-Timetables/'
    ) and url.endswith('bound/')

def valid_enterprise_route_url(url):
    return url.startswith(
        '/Timetables/Enterprise-Timetables/'
    ) and url.endswith('bound/')

def iter_scrape_route(operatorid, routetype, url):
    """
    The core scraping function - not pretty but at least it's all
    in the one place. If the timetable HTML were to change, this
    is the function that would need to be updated.
    """
    html = parse(scrape(url))
    body = html.find('.//div[@id="MainBody"]')
    srvname = strip(html.find('.//div[@id="ltw"]').text).upper()
    srv_parts = srvname.split()
    if srv_parts[-1] == 'INBOUND' or srv_parts[-1] == 'OUTBOUND':
        srv_parts = srv_parts[:-1]
    srvno = srv_parts[-1]
    direction = url[url.rfind('-')+1:].rstrip('/').title()
    try:
        direction_id = DIRECTIONCODES[direction.lower()]
    except KeyError:
        direction_id = None
    srvname = '%s (%s)' % (srvname, direction)
    route = body.find(
        './/div[@class="lower_timetables_details_top_title"]'
    ).text
    begin, end = determine_route(route)
    srvid = '%s-%s' % (operatorid, srvno)
    if direction_id is not None:
        route_id = '%s-%s' % (srvid, direction)
    else:
        route_id = srvid
    route_info = {
        'agency_id': TRANSLINK_ID,
        'operator_id': operatorid,
        'service_id': srvid,
        'route_id': route_id,
        'route_url': url,
        'route_type': routetype,
        'route_long_name': srvname,
        'route_short_name': srvno,
        'route_begin': begin,
        'route_end': end,
        'route_direction': direction_id,
    }
    container = body.find('.//div[@id="timetableContainer"]')
    if container is None:
        print "%s - no data" % route_id
        return
    print route_id
    tables = container.findall('table')
    def iter_tables():
        tripidx = count(1)
        stop_sequence = []
        for i, table in enumerate(tables):
            if not i % 2:
                # every other table is a timetable TODO - verify
                continue
            rows = iter(table.findall('tr'))
            service_nos = timeframes = None
            for r in rows:
                label = strip(r[0].text)
                if label == 'Service:':
                    service_nos = [strip(td.text) for td in r[1:]]
                elif label == 'Days of operation:':
                    timeframes = [strip(td.text) for td in r[1:]]
                    break
            assert len(service_nos) == len(timeframes)
            tripids = [str(tripidx.next()) for x in service_nos]
            datarows = []
            for row in rows:
                # ignore rows that aren't stop time rows
                label = strip(row[0].text)
                if label and label[-1] != ':':
                    datarows.append((label, row))
            for i, (stop, r) in enumerate(datarows):
                if i < len(stop_sequence):
                    # we must have the same stops in each table
                    warn = "inconsistent stop sequence - %s" % stop
                    assert stop_sequence[i] == stop, warn
                else:
                    # first time round
                    stop_sequence.append(stop)
                times = [strip(td.text) for td in r[1:]]
                times = [
                    TRIPDATAPARTJOINER.join(t) for t in izip(
                        tripids, service_nos, timeframes, times
                    )
                ]
                warn = "found meta character in timetable data"
                for t in times:
                    assert t.count(TRIPDATAPARTJOINER) == 3, warn
                yield i, stop, times
    sortkey = lambda X: (X[0], X[1])
    stop_times = sorted(iter_tables(), key=sortkey)
    for key, group in groupby(stop_times, key=sortkey):
        info = dict(route_info)
        alltimes = []
        for item in group:
            alltimes.extend(item[2])
        info['stop_sequence'], info['stop_name'] = key
        info['schedule'] = TRIPDATAJOINER.join(alltimes)
        yield info

###########################################################################
# SCRAPERS
###########################################################################
def scrape_metro():
    """
    There is one index page for each of the main Metro routes - Metro 1
    to Metro 12, then a further 'All other services' page containing the
    remaining services. We need to scrape the index pages to find the
    individual timetable pages, then pass the page url to `iter_scrape_route`.
    A few of the index pages are paginated like the Ulsterbus index, but
    we special case the ones we can't find directly in the METRO_EXTRAS
    list.
    """
    done_routes = set()
    for index_url in TRANSLINK_METRO_INDEX_URLS:
        html = parse(scrape(index_url))
        for link in html.iterlinks():
            url = link[2]
            if valid_metro_route_url(url) and url not in done_routes:
                href = TRANSLINK_URL + url
                for row in iter_scrape_route(METRO_ID, BUS_ROUTE_TYPE, href):
                    yield row
                done_routes.add(url)
    for href in TRANSLINK_METRO_EXTRAS:
        for row in iter_scrape_route(METRO_ID, BUS_ROUTE_TYPE, href):
            yield row

def scrape_ulsterbus():
    """
    For Ulsterbus there is a single index page containing the links
    to the individual service timetables. This index page is
    paginated - 5 pages with <= 100 items on each page. The paginator
    employs 'JS to form POST' buttons, so we need to mimic the
    individual POSTS here.
    """
    fmt = (
        'ctl00$MainRegion$MainContentRegion$MainBodyRegion'
        '$ctl00$rptPageList$ctl00$ctl03$ctl01$ctl%02d'
    )
    for x in [5, 7, 9, 11, 13]:
        done_routes = set()
        payload = {
            '__EVENTTARGET': fmt % x,
            '__EVENTARGUMENT': '',
        }
        response = requests.post(TRANSLINK_ULSTERBUS_INDEX, data=payload)
        html = parse(response.content)
        for link in html.iterlinks():
            url = link[2]
            if valid_ulsterbus_route_url(url) and url not in done_routes:
                href = TRANSLINK_URL + url
                for row in iter_scrape_route(ULSTERBUS_ID, BUS_ROUTE_TYPE, href):
                    yield row
                done_routes.add(url)

def scrape_goldline():
    done_routes = set()
    html = parse(scrape(TRANSLINK_GOLDLINE_INDEX))
    for link in html.iterlinks():
        url = link[2]
        if valid_goldline_route_url(url) and url not in done_routes:
            href = TRANSLINK_URL + url
            for row in iter_scrape_route(GOLDLINE_ID, BUS_ROUTE_TYPE, href):
                yield row
            done_routes.add(url)

def scrape_enterprise():
    done_routes = set()
    html = parse(scrape(TRANSLINK_ENTERPRISE_INDEX))
    for link in html.iterlinks():
        url = link[2]
        if valid_enterprise_route_url(url) and url not in done_routes:
            href = TRANSLINK_URL + url
            for row in iter_scrape_route(ENTERPRISE_ID, RAIL_ROUTE_TYPE, href):
                yield row
            done_routes.add(url)

iterables = [
    #scrape_metro(),
    #scrape_ulsterbus(),
    #scrape_goldline(),
    scrape_enterprise(),
]

for row in chain(*iterables):
    if DEBUG:
        print row
    else:
        store(unique_keys=UNIQUE_KEYS, data=row)

