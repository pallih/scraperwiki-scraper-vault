import scraperwiki
import datetime
import demjson
import hashlib
import operator
from geopy import distance 

def loadUrl(key, url):
    result = scraperwiki.scrape(url)
    digest = hashlib.sha512(result).hexdigest()
    if digest == scraperwiki.sqlite.get_var(key, None):
        return None
    
    scraperwiki.sqlite.save_var(key, digest)
    return result

def getNewBuses(buses_json):
    if buses_json is None:
        return []
    buses = demjson.decode(buses_json)
    try:
        old_ids = [id['id'] for id in scraperwiki.sqlite.select("id from buses")]
    except scraperwiki.sqlite.SqliteError, e:
        old_ids = []

    buses = filter(lambda x: int(x['id']) not in old_ids, buses)
    print "Found %s new buses. Loading..." % (len(buses))

    # field nome (name) has dangling spaces at the end, clean it up
    for bus in buses:
        bus['id'] = int(bus['id'])
        bus['nome'] = bus['nome'].strip()
        (bus['codigo'],bus['sentido']) = bus['codigo'].split('-')
        bus['sentido'] = int(bus['sentido'])
        bus['data'] = datetime.datetime.utcnow()

    return buses

def getDistance(point1, point2):
    return distance.distance(point1, point2)

def getLatLon(bus):
    id = str(bus['id'])
    latlon_json = loadUrl("route-" + id, "http://www.poatransporte.com.br/php/facades/process.php?a=il&p=" + id)
    #latlon_json = scraperwiki.scrape("http://www.poatransporte.com.br/php/facades/process.php?a=il&p=" + id)

    if latlon_json is None:
        return bus['latlon']

    latlon = demjson.decode(latlon_json)

    # keep only the latlon data as a tuple
    keys = sorted(filter(lambda x: x.isdigit(), latlon), key=int)
    return [(latlon[k]['lat'],latlon[k]['lng']) for k in keys]

def calculateDistance(latlon):
    length = len(latlon)

    # need at minimum 2 points
    if length < 2: return 0

    dist = distance.distance(latlon[0], latlon[1])
    for i in range(1, length-1):
        dist += distance.distance(latlon[i], latlon[i+1])

    return dist


buses_url = "http://www.poatransporte.com.br/php/facades/process.php?a=nc&p=%&t=o"
buses = getNewBuses(scraperwiki.scrape(buses_url))

for bus in buses:
    latlon = getLatLon(bus)
    dist = calculateDistance(latlon)

    print "%d\t%s\t%.3f" % (bus['id'], bus['codigo'], dist.km)
    bus['rota'] = ' '.join([i[0] + ',' + i[1] for i in latlon])
    bus['distancia'] = round(dist.km,3)
    scraperwiki.sqlite.save(['id'], bus, "buses")import scraperwiki
import datetime
import demjson
import hashlib
import operator
from geopy import distance 

def loadUrl(key, url):
    result = scraperwiki.scrape(url)
    digest = hashlib.sha512(result).hexdigest()
    if digest == scraperwiki.sqlite.get_var(key, None):
        return None
    
    scraperwiki.sqlite.save_var(key, digest)
    return result

def getNewBuses(buses_json):
    if buses_json is None:
        return []
    buses = demjson.decode(buses_json)
    try:
        old_ids = [id['id'] for id in scraperwiki.sqlite.select("id from buses")]
    except scraperwiki.sqlite.SqliteError, e:
        old_ids = []

    buses = filter(lambda x: int(x['id']) not in old_ids, buses)
    print "Found %s new buses. Loading..." % (len(buses))

    # field nome (name) has dangling spaces at the end, clean it up
    for bus in buses:
        bus['id'] = int(bus['id'])
        bus['nome'] = bus['nome'].strip()
        (bus['codigo'],bus['sentido']) = bus['codigo'].split('-')
        bus['sentido'] = int(bus['sentido'])
        bus['data'] = datetime.datetime.utcnow()

    return buses

def getDistance(point1, point2):
    return distance.distance(point1, point2)

def getLatLon(bus):
    id = str(bus['id'])
    latlon_json = loadUrl("route-" + id, "http://www.poatransporte.com.br/php/facades/process.php?a=il&p=" + id)
    #latlon_json = scraperwiki.scrape("http://www.poatransporte.com.br/php/facades/process.php?a=il&p=" + id)

    if latlon_json is None:
        return bus['latlon']

    latlon = demjson.decode(latlon_json)

    # keep only the latlon data as a tuple
    keys = sorted(filter(lambda x: x.isdigit(), latlon), key=int)
    return [(latlon[k]['lat'],latlon[k]['lng']) for k in keys]

def calculateDistance(latlon):
    length = len(latlon)

    # need at minimum 2 points
    if length < 2: return 0

    dist = distance.distance(latlon[0], latlon[1])
    for i in range(1, length-1):
        dist += distance.distance(latlon[i], latlon[i+1])

    return dist


buses_url = "http://www.poatransporte.com.br/php/facades/process.php?a=nc&p=%&t=o"
buses = getNewBuses(scraperwiki.scrape(buses_url))

for bus in buses:
    latlon = getLatLon(bus)
    dist = calculateDistance(latlon)

    print "%d\t%s\t%.3f" % (bus['id'], bus['codigo'], dist.km)
    bus['rota'] = ' '.join([i[0] + ',' + i[1] for i in latlon])
    bus['distancia'] = round(dist.km,3)
    scraperwiki.sqlite.save(['id'], bus, "buses")import scraperwiki
import datetime
import demjson
import hashlib
import operator
from geopy import distance 

def loadUrl(key, url):
    result = scraperwiki.scrape(url)
    digest = hashlib.sha512(result).hexdigest()
    if digest == scraperwiki.sqlite.get_var(key, None):
        return None
    
    scraperwiki.sqlite.save_var(key, digest)
    return result

def getNewBuses(buses_json):
    if buses_json is None:
        return []
    buses = demjson.decode(buses_json)
    try:
        old_ids = [id['id'] for id in scraperwiki.sqlite.select("id from buses")]
    except scraperwiki.sqlite.SqliteError, e:
        old_ids = []

    buses = filter(lambda x: int(x['id']) not in old_ids, buses)
    print "Found %s new buses. Loading..." % (len(buses))

    # field nome (name) has dangling spaces at the end, clean it up
    for bus in buses:
        bus['id'] = int(bus['id'])
        bus['nome'] = bus['nome'].strip()
        (bus['codigo'],bus['sentido']) = bus['codigo'].split('-')
        bus['sentido'] = int(bus['sentido'])
        bus['data'] = datetime.datetime.utcnow()

    return buses

def getDistance(point1, point2):
    return distance.distance(point1, point2)

def getLatLon(bus):
    id = str(bus['id'])
    latlon_json = loadUrl("route-" + id, "http://www.poatransporte.com.br/php/facades/process.php?a=il&p=" + id)
    #latlon_json = scraperwiki.scrape("http://www.poatransporte.com.br/php/facades/process.php?a=il&p=" + id)

    if latlon_json is None:
        return bus['latlon']

    latlon = demjson.decode(latlon_json)

    # keep only the latlon data as a tuple
    keys = sorted(filter(lambda x: x.isdigit(), latlon), key=int)
    return [(latlon[k]['lat'],latlon[k]['lng']) for k in keys]

def calculateDistance(latlon):
    length = len(latlon)

    # need at minimum 2 points
    if length < 2: return 0

    dist = distance.distance(latlon[0], latlon[1])
    for i in range(1, length-1):
        dist += distance.distance(latlon[i], latlon[i+1])

    return dist


buses_url = "http://www.poatransporte.com.br/php/facades/process.php?a=nc&p=%&t=o"
buses = getNewBuses(scraperwiki.scrape(buses_url))

for bus in buses:
    latlon = getLatLon(bus)
    dist = calculateDistance(latlon)

    print "%d\t%s\t%.3f" % (bus['id'], bus['codigo'], dist.km)
    bus['rota'] = ' '.join([i[0] + ',' + i[1] for i in latlon])
    bus['distancia'] = round(dist.km,3)
    scraperwiki.sqlite.save(['id'], bus, "buses")