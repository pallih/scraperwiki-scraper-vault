"""
scraperwiki script 'translink_metro_stops' for deriving
Translink N.I. Metro bus stops and coordinates
"""
import scraperwiki

import re

# The Map Title gives the service id and direction
rx_route = re.compile(
    r'<span id="ctl00_MainRegion_MainContentRegion_lblServiceDescription">'
    r'Metro Service (?P<service>\w+) - (?P<info>.+?)</span>'
)
# The javascript Map pin and tooltip
rx_marker = re.compile(
    r"var marker_subgurim_(?P<id>.+?) = "
    r"new GMarker\(new GLatLng\((?P<lat>.+?),(?P<lng>.+?)\).+?"
    r"<b>Bus Stop</b><br/>(?P<stop>.*?)<br/>(?P<routes>.*?)</div>'\); }\);"
)
# The tooltip parts
rx_routes = re.compile(
    r'<a href="(?P<href>.*?)">(?P<name>.+?)</a>'
)

def tidy(s):
    return s.replace('&nbsp;', ' ').replace('&apos;', "'")

def strip_route(s):
    for word in ['metro', 'ulsterbus', 'service']:
        s = s.replace(word, '')
    return s.strip()

def make_map_url(id):
    return 'http://www.translink.co.uk/Timetables/Route-Map/?serviceid=%s' % id

scrape = scraperwiki.scrape
store = scraperwiki.sqlite.save
debug = False

# we get the map SERVICE_IDS by manual inspection
# - a minority of map views consistently give 500 errors, eg. Route 1A
SERVICE_IDS = frozenset([
    3, 4, 7, 8, 9, 11, 12,
    31, 32, 33, 34, 35, 36, 37, 38,
    40, 41, 42, 43, 44, 45, 46, 49,
    50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
    60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
    70, 71, 72, 73, 74, 75, 77, 78,
    80, 81, 82, 83, 84, 85, 87, 89,
    107, 109, 110, 111,
    122, 127, 128,
    131, 132, 134,
    144, 146, 147,
    151, 152, 153, 154, 158, 159,
    168, 169, 170, 173, 174, 175, 176,
    184, 185,
])

if debug:
    SERVICE_IDS = frozenset([
        3, 4,
    ])

UNIQUE_KEYS = ['service', 'direction', 'sequence']

# for every map and every "pin" (representing a stop) on the map
# create a data row and save to the datastore
for id in sorted(SERVICE_IDS):
    url = make_map_url(id)
    print 'scraping url: %s' % url
    html = scrape(url)
    route_info = rx_route.search(html)
    if not route_info:
        continue
    route_info = route_info.groupdict()
    service = route_info['service']
    info = (route_info.get('info') or '').strip()
    direction = ''
    print service, direction, info
    # The map page gives the service number but not whether it's
    # for the inbound or outbound direction, so we have to figure
    # this out from the route information - a route beginning with
    # 'Belfast' is outbound etc.
    if info.endswith('Belfast'):
        direction = 'Inbound'
    elif info.startswith('Belfast'):
        direction = 'Outbound'
    for i, match in enumerate(rx_marker.finditer(html)):
        groups = match.groupdict()
        stop = tidy(groups['stop'])
        stopname, comma, road = stop.rpartition(',')
        stopname = stopname or road
        row = {
            'service': service,
            'direction': direction,
            'sequence': i,
            'lat': groups['lat'],
            'lng': groups['lng'],
            'name': stopname.strip(),
            'road': road.strip(),
        }
        metro_routes = []
        ulsterbus_routes = []
        for match in rx_routes.finditer(groups['routes']):
            groups = match.groupdict()
            route = tidy(groups['name']).lower()
            if 'metro' in route:
                metro_routes.append(strip_route(route))
            elif 'ulsterbus' in route:
                ulsterbus_routes.append(strip_route(route))
        row['metro'] = '|'.join(metro_routes)
        row['ulsterbus'] = '|'.join(ulsterbus_routes)
        store(unique_keys=UNIQUE_KEYS, data=row)

"""
scraperwiki script 'translink_metro_stops' for deriving
Translink N.I. Metro bus stops and coordinates
"""
import scraperwiki

import re

# The Map Title gives the service id and direction
rx_route = re.compile(
    r'<span id="ctl00_MainRegion_MainContentRegion_lblServiceDescription">'
    r'Metro Service (?P<service>\w+) - (?P<info>.+?)</span>'
)
# The javascript Map pin and tooltip
rx_marker = re.compile(
    r"var marker_subgurim_(?P<id>.+?) = "
    r"new GMarker\(new GLatLng\((?P<lat>.+?),(?P<lng>.+?)\).+?"
    r"<b>Bus Stop</b><br/>(?P<stop>.*?)<br/>(?P<routes>.*?)</div>'\); }\);"
)
# The tooltip parts
rx_routes = re.compile(
    r'<a href="(?P<href>.*?)">(?P<name>.+?)</a>'
)

def tidy(s):
    return s.replace('&nbsp;', ' ').replace('&apos;', "'")

def strip_route(s):
    for word in ['metro', 'ulsterbus', 'service']:
        s = s.replace(word, '')
    return s.strip()

def make_map_url(id):
    return 'http://www.translink.co.uk/Timetables/Route-Map/?serviceid=%s' % id

scrape = scraperwiki.scrape
store = scraperwiki.sqlite.save
debug = False

# we get the map SERVICE_IDS by manual inspection
# - a minority of map views consistently give 500 errors, eg. Route 1A
SERVICE_IDS = frozenset([
    3, 4, 7, 8, 9, 11, 12,
    31, 32, 33, 34, 35, 36, 37, 38,
    40, 41, 42, 43, 44, 45, 46, 49,
    50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
    60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
    70, 71, 72, 73, 74, 75, 77, 78,
    80, 81, 82, 83, 84, 85, 87, 89,
    107, 109, 110, 111,
    122, 127, 128,
    131, 132, 134,
    144, 146, 147,
    151, 152, 153, 154, 158, 159,
    168, 169, 170, 173, 174, 175, 176,
    184, 185,
])

if debug:
    SERVICE_IDS = frozenset([
        3, 4,
    ])

UNIQUE_KEYS = ['service', 'direction', 'sequence']

# for every map and every "pin" (representing a stop) on the map
# create a data row and save to the datastore
for id in sorted(SERVICE_IDS):
    url = make_map_url(id)
    print 'scraping url: %s' % url
    html = scrape(url)
    route_info = rx_route.search(html)
    if not route_info:
        continue
    route_info = route_info.groupdict()
    service = route_info['service']
    info = (route_info.get('info') or '').strip()
    direction = ''
    print service, direction, info
    # The map page gives the service number but not whether it's
    # for the inbound or outbound direction, so we have to figure
    # this out from the route information - a route beginning with
    # 'Belfast' is outbound etc.
    if info.endswith('Belfast'):
        direction = 'Inbound'
    elif info.startswith('Belfast'):
        direction = 'Outbound'
    for i, match in enumerate(rx_marker.finditer(html)):
        groups = match.groupdict()
        stop = tidy(groups['stop'])
        stopname, comma, road = stop.rpartition(',')
        stopname = stopname or road
        row = {
            'service': service,
            'direction': direction,
            'sequence': i,
            'lat': groups['lat'],
            'lng': groups['lng'],
            'name': stopname.strip(),
            'road': road.strip(),
        }
        metro_routes = []
        ulsterbus_routes = []
        for match in rx_routes.finditer(groups['routes']):
            groups = match.groupdict()
            route = tidy(groups['name']).lower()
            if 'metro' in route:
                metro_routes.append(strip_route(route))
            elif 'ulsterbus' in route:
                ulsterbus_routes.append(strip_route(route))
        row['metro'] = '|'.join(metro_routes)
        row['ulsterbus'] = '|'.join(ulsterbus_routes)
        store(unique_keys=UNIQUE_KEYS, data=row)

