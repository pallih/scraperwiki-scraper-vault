from scraperwiki.sqlite import attach, select, get_var, save_var, save, execute, commit, show_tables
from urllib2 import urlopen
from urllib import urlencode
from json import loads, dumps
from time import sleep
from unidecode import unidecode
from geopy import geocoders, distance

attach("capitec_bank")

COLUMNS = {
  # Full address
  'full-address': 'address',

  # Town-country
  'town-country': 'branchName || ", South Africa"',

  # Province-country
  'province-country': 'provinceName || ", South Africa"',

  # Town-province-country
  'town-province-country': 'branchName || ", " || provinceName || ", South Africa"',

  # Postcode-country
  'postcode-country': 'postcode || ", " || "South Africa"'
}

def geocode():
    if "address" not in show_tables():
        initialize()

    while select('count(*) AS "c" FROM `address` WHERE `finished` = 0')[0]['c'] > 0:
        address = select("`address-column`, `address-input` FROM `address` WHERE `finished` = 0 LIMIT 1")[0]
        #print address
        if select('count(*) AS "c" FROM `geocode` WHERE `address-input` = ?', [address['address-input']])[0]['c'] == 0:
            d = all_services(address['address-input'])
            for row in d:
                row['address-input'] = address['address-input']
            save([], d, 'geocode')
        params = (address['address-column'], address['address-input'])
        execute("UPDATE `address` SET `finished` = 1 WHERE (`address-column` = ? AND `address-input` = ?)", params )
        commit()

class Nominatim:
    GEOCODE_URL = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&json_callback=&%s'

    def geocode_url(self, address):
        return self.GEOCODE_URL % urlencode({'q': address})

    def load(self, address):
        url = self.geocode_url(address)
        while True:
            try:
                json = urlopen(url).read()
            except:
                sleep(90)
            else:
                break
        d = loads(json)
        return d

    @staticmethod
    def convert_coords(coords):
        try:
            return tuple(map(float, coords))
        except TypeError:
            raise TypeError("coords could not be converted to a tuple of latitude and longitude numbers.")

    def geocode(self, address, exactly_one = True):
        d = self.load(address)
        if len(d) > 0:
            return [ ( match["display_name"], self.convert_coords([match[u'lat'], match[u'lon']]) ) for match in d ]
        else:
            return None

GEOCODERS = {
  # Tuples of geocoder, args, kwargs
  "google": (geocoders.Google, [], {"domain": "maps.google.co.za"}),
#  "yahoo": (geocoders.Yahoo, ["APP_ID"], {}),
  "nominatim": (Nominatim, [], {}),
# "geocoder.us": (geocoders.GeocoderDotUS, [], {}), # Non-commercial only and mainly US
  "geonames": (geocoders.GeoNames, [], {}),
# "semantic-mediawiki": (geocoders.SemanticMediaWiki, ["http://wiki.case.edu/%s"], {"attributes": ['Coordinates'], "relations": ['Located in']})
}

def all_services(raw_address):
    d = []
    #print raw_address
    for service in GEOCODERS:
        #print service
        s = GEOCODERS[service]
        g = s[0](*s[1], **s[2])

        while True:
            try:
                matches = g.geocode(raw_address, exactly_one = False)
            except geocoders.google.GQueryError:
                matches = None
                break
            except UnicodeEncodeError:
                raw_address = unidecode(raw_address)
            else:
                break

        if matches == None:
            d.append({
              "service": service,
              "number-of-matches": 0
            })
        else:
            address_geocode, (lat, lng) = matches[0]
            d.append({
              "address-geocode": address_geocode,
              "latitude-geocode": float(lat),
              "longitude-geocode": float(lng),
              "service": service,
              "number-of-matches": len(matches)
            })
    return d

def initialize():
    execute("""
CREATE TABLE `address` (
  `address-column` text,
  `address-input` text,
  `finished` integer
)""")
    execute("CREATE UNIQUE INDEX column ON `address` (`address-column`,`address-input`);")
    execute("""
CREATE TABLE `geocode` (
  `address-geocode` TEXT,
  `latitude-geocode` REAL,
  `longitude-geocode` REAL,

  `number-of-matches` text,

  `service` TEXT,
  `address-input` TEXT
)""")
    execute("CREATE UNIQUE INDEX geocode_key ON `geocode` (`address-input`, `service`);")

    execute('''
CREATE TABLE `branch_address` (
  `branchId` TEXT,
  `address-column` TEXT,
  `address-input` TEXT,
  `latitude-scrape` REAL,
  `longitude-scrape` REAL
)''')
    execute("CREATE UNIQUE INDEX branch_key ON `branch_address` (`branchId`, `address-column`);")
    commit()

    for column in COLUMNS:
        execute('''
INSERT INTO `address` (
  `address-column`,
  `address-input`,
  `finished`
) SELECT DISTINCT
    ? as "address-column",
    %s as "address-input",
    0 as "finished"
  FROM
    `branches`
  ''' % COLUMNS[column], column)
        commit()
        execute('''
INSERT INTO `branch_address` (
  `branchId`,
  `address-column`,
  `address-input`,
  `latitude-scrape`,
  `longitude-scrape`
) SELECT
    `branchId`, 
    ? as "address-column",
    %s as "address-input",
    `latitude`,
    `longitude`
  FROM
    `branches`
  ''' % COLUMNS[column], column)
        commit()
    execute('DELETE FROM `address` WHERE `address-input` IS NULL')
    commit()

def join():
    execute('DROP TABLE IF EXISTS `accuracy`')
    commit()
    d = select('''
* FROM `geocode`
LEFT JOIN `branch_address` ON (
  `branch_address`.`address-input` = `geocode`.`address-input`
)
''')
    for row in d:
        if row['address-geocode'] == None:
            row['kilometers_off'] = None
        else:
            row['kilometers_off'] = distance.distance(
                (row['latitude-scrape'], row['longitude-scrape']),
                (row['latitude-geocode'], row['longitude-geocode'])
            ).km
        for key in ['latitude-scrape', 'longitude-scrape', 'latitude-geocode', 'longitude-geocode', 'address-input']:
            del(row[key])
    save([], d, 'accuracy')

geocode()
print "Finished geocoding"
print "Joining"
join()
print "Finished joining"
#SELECT `address-column`, `service`, count(*) as "number-geocoded" FROM `accuracy` WHERE (`address-geocode` IS NOT NULL) GROUP BY `address-column`, `service`from scraperwiki.sqlite import attach, select, get_var, save_var, save, execute, commit, show_tables
from urllib2 import urlopen
from urllib import urlencode
from json import loads, dumps
from time import sleep
from unidecode import unidecode
from geopy import geocoders, distance

attach("capitec_bank")

COLUMNS = {
  # Full address
  'full-address': 'address',

  # Town-country
  'town-country': 'branchName || ", South Africa"',

  # Province-country
  'province-country': 'provinceName || ", South Africa"',

  # Town-province-country
  'town-province-country': 'branchName || ", " || provinceName || ", South Africa"',

  # Postcode-country
  'postcode-country': 'postcode || ", " || "South Africa"'
}

def geocode():
    if "address" not in show_tables():
        initialize()

    while select('count(*) AS "c" FROM `address` WHERE `finished` = 0')[0]['c'] > 0:
        address = select("`address-column`, `address-input` FROM `address` WHERE `finished` = 0 LIMIT 1")[0]
        #print address
        if select('count(*) AS "c" FROM `geocode` WHERE `address-input` = ?', [address['address-input']])[0]['c'] == 0:
            d = all_services(address['address-input'])
            for row in d:
                row['address-input'] = address['address-input']
            save([], d, 'geocode')
        params = (address['address-column'], address['address-input'])
        execute("UPDATE `address` SET `finished` = 1 WHERE (`address-column` = ? AND `address-input` = ?)", params )
        commit()

class Nominatim:
    GEOCODE_URL = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&json_callback=&%s'

    def geocode_url(self, address):
        return self.GEOCODE_URL % urlencode({'q': address})

    def load(self, address):
        url = self.geocode_url(address)
        while True:
            try:
                json = urlopen(url).read()
            except:
                sleep(90)
            else:
                break
        d = loads(json)
        return d

    @staticmethod
    def convert_coords(coords):
        try:
            return tuple(map(float, coords))
        except TypeError:
            raise TypeError("coords could not be converted to a tuple of latitude and longitude numbers.")

    def geocode(self, address, exactly_one = True):
        d = self.load(address)
        if len(d) > 0:
            return [ ( match["display_name"], self.convert_coords([match[u'lat'], match[u'lon']]) ) for match in d ]
        else:
            return None

GEOCODERS = {
  # Tuples of geocoder, args, kwargs
  "google": (geocoders.Google, [], {"domain": "maps.google.co.za"}),
#  "yahoo": (geocoders.Yahoo, ["APP_ID"], {}),
  "nominatim": (Nominatim, [], {}),
# "geocoder.us": (geocoders.GeocoderDotUS, [], {}), # Non-commercial only and mainly US
  "geonames": (geocoders.GeoNames, [], {}),
# "semantic-mediawiki": (geocoders.SemanticMediaWiki, ["http://wiki.case.edu/%s"], {"attributes": ['Coordinates'], "relations": ['Located in']})
}

def all_services(raw_address):
    d = []
    #print raw_address
    for service in GEOCODERS:
        #print service
        s = GEOCODERS[service]
        g = s[0](*s[1], **s[2])

        while True:
            try:
                matches = g.geocode(raw_address, exactly_one = False)
            except geocoders.google.GQueryError:
                matches = None
                break
            except UnicodeEncodeError:
                raw_address = unidecode(raw_address)
            else:
                break

        if matches == None:
            d.append({
              "service": service,
              "number-of-matches": 0
            })
        else:
            address_geocode, (lat, lng) = matches[0]
            d.append({
              "address-geocode": address_geocode,
              "latitude-geocode": float(lat),
              "longitude-geocode": float(lng),
              "service": service,
              "number-of-matches": len(matches)
            })
    return d

def initialize():
    execute("""
CREATE TABLE `address` (
  `address-column` text,
  `address-input` text,
  `finished` integer
)""")
    execute("CREATE UNIQUE INDEX column ON `address` (`address-column`,`address-input`);")
    execute("""
CREATE TABLE `geocode` (
  `address-geocode` TEXT,
  `latitude-geocode` REAL,
  `longitude-geocode` REAL,

  `number-of-matches` text,

  `service` TEXT,
  `address-input` TEXT
)""")
    execute("CREATE UNIQUE INDEX geocode_key ON `geocode` (`address-input`, `service`);")

    execute('''
CREATE TABLE `branch_address` (
  `branchId` TEXT,
  `address-column` TEXT,
  `address-input` TEXT,
  `latitude-scrape` REAL,
  `longitude-scrape` REAL
)''')
    execute("CREATE UNIQUE INDEX branch_key ON `branch_address` (`branchId`, `address-column`);")
    commit()

    for column in COLUMNS:
        execute('''
INSERT INTO `address` (
  `address-column`,
  `address-input`,
  `finished`
) SELECT DISTINCT
    ? as "address-column",
    %s as "address-input",
    0 as "finished"
  FROM
    `branches`
  ''' % COLUMNS[column], column)
        commit()
        execute('''
INSERT INTO `branch_address` (
  `branchId`,
  `address-column`,
  `address-input`,
  `latitude-scrape`,
  `longitude-scrape`
) SELECT
    `branchId`, 
    ? as "address-column",
    %s as "address-input",
    `latitude`,
    `longitude`
  FROM
    `branches`
  ''' % COLUMNS[column], column)
        commit()
    execute('DELETE FROM `address` WHERE `address-input` IS NULL')
    commit()

def join():
    execute('DROP TABLE IF EXISTS `accuracy`')
    commit()
    d = select('''
* FROM `geocode`
LEFT JOIN `branch_address` ON (
  `branch_address`.`address-input` = `geocode`.`address-input`
)
''')
    for row in d:
        if row['address-geocode'] == None:
            row['kilometers_off'] = None
        else:
            row['kilometers_off'] = distance.distance(
                (row['latitude-scrape'], row['longitude-scrape']),
                (row['latitude-geocode'], row['longitude-geocode'])
            ).km
        for key in ['latitude-scrape', 'longitude-scrape', 'latitude-geocode', 'longitude-geocode', 'address-input']:
            del(row[key])
    save([], d, 'accuracy')

geocode()
print "Finished geocoding"
print "Joining"
join()
print "Finished joining"
#SELECT `address-column`, `service`, count(*) as "number-geocoded" FROM `accuracy` WHERE (`address-geocode` IS NOT NULL) GROUP BY `address-column`, `service`