from scraperwiki import swimport
from scraperwiki.sqlite import attach, select, get_var, save_var, save, execute, commit, show_tables
from urllib2 import urlopen
from urllib import urlencode
from json import loads, dumps
from time import sleep
from unidecode import unidecode
from geopy import geocoders, distance
import re

MAX_KM_FROM_PROVINCE = 600
MAX_KM_FROM_COUNTRY = 10000
COUNTRY_COORDS = (-28.5, 24.5) #Currently, we're assuming that South Africa is always the country.

COLUMNS = {
  # Full address
  'full-address': '`Address`',

  # Town-country
  'town-country': '`Town` || ", " || `Country` ',

  # Province-country
  'province-country': '`Province` || ", " || `Country`',

  # Town-province-country
  'town-province-country': '`Town` || ", " || `Province` || ", " || `Country`',

  # Postcode-country
  'postcode-country': '`Postal_Code` || ", " || `Country`'
}

PREVIOUS_SCRAPER = 'geocode_all_mix_scrapers_1'

def geocode():
    if "scraped" not in show_tables():
        d = swimport('csv2sw').read.csv('https://views.scraperwiki.com/run/combine_mix_scraper_spreadsheets/?date='+str(time()))
        save([], d, 'scraped')
        execute('DELETE FROM `scraped` WHERE `Country` != "South Africa"')
        commit()

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
                d = []
                break
            else:
                d = loads(json)
                break
        
        return d

    @staticmethod
    def convert_coords(coords):
        try:
            return tuple(map(float, coords))
        except TypeError:
            raise TypeError("coords could not be converted to a tuple of latitude and longitude numbers.")

    def geocode(self, address, exactly_one = True):
        d = self.load(unidecode(address))
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

    try:
        PREVIOUS_SCRAPER
    except:
        execute("""
    CREATE TABLE `geocode` (
      `address-geocode` TEXT,
      `latitude-geocode` REAL,
      `longitude-geocode` REAL,
    
      `number-of-matches` text,
    
      `service` TEXT,
      `address-input` TEXT
    )""")
    else:
        attach(PREVIOUS_SCRAPER)
        save([], select('* FROM `geocode`'), 'geocode')

    execute("CREATE UNIQUE INDEX geocode_key ON `geocode` (`address-input`, `service`);")

    execute('''
CREATE TABLE `branch_address` (
  `address-column` TEXT,
  `address-input` TEXT,
  `entityRecord` INTEGER,
  FOREIGN KEY(entityRecord) REFERENCES scraped(rowid)
)''')
    execute("CREATE UNIQUE INDEX branch_key ON `branch_address` (`entityRecord`, `address-column`);")
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
    `scraped`
  ''' % COLUMNS[column], column)
        commit()
        execute('''
INSERT INTO `branch_address` (
  `entityRecord`,
  `address-column`,
  `address-input`
) SELECT
    `rowid`, 
    ? as "address-column",
    %s as "address-input"
  FROM
    `scraped`
  ''' % COLUMNS[column], column)
        commit()
    execute('DELETE FROM `address` WHERE `address-input` IS NULL')
    commit()
"""
    execute('''
CREATE TABLE `entity-geocode` (
 `address-geocode` TEXT,
 `latitude-geocode` REAL,
 `longitude-geocode` REAL,
 `number-of-matches` text,
 `service` TEXT,

 `address-input` TEXT,

 `address-column` TEXT,
 `entityRecord` INTEGER,
)
''')

    commit()
    d = select('''
* FROM `geocode`
CROSS JOIN `branch_address` ON (
  `branch_address`.`address-input` = `geocode`.`address-input`
)
''')
    save([], d, 'entity-geocode')
"""

def choose():
    execute('DROP TABLE IF EXISTS `entity-geocode`')
    for entityRecord in [row['rowid'] for row in select('rowid FROM `scraped`')]:
        d = select('''
  `latitude-geocode`, `longitude-geocode`
FROM `branch_address`
JOIN `geocode` ON (
  `branch_address`.`address-input` = `geocode`.`address-input`
) WHERE (
  `address-column` = "province-country" AND
  `service` = "nominatim" AND
  `entityRecord` = ?
)''', entityRecord)
        if 0 == len(d):
            # No province
            d2 = select('''
  `entityRecord`, `latitude-geocode`, `longitude-geocode`
FROM `branch_address`
JOIN `geocode` ON (
  `branch_address`.`address-input` = `geocode`.`address-input`
) WHERE (
  `address-column` = "full-address" AND
  `service` = "google" AND
  `entityRecord` = ?
)''', entityRecord)
            if len(d2) == 0:
                continue
            row = d2[0]

            if row['latitude-geocode'] == None:
                kilometers_from_country = None
            else:
                kilometers_from_country = distance.distance(
                    (row['latitude-geocode'], row['longitude-geocode']),
                    COUNTRY_COORDS
                ).km

            if kilometers_from_country < MAX_KM_FROM_COUNTRY:
                best_address = {
                    "entityRecord": row['entityRecord'],
                    "service": "google",
                    "address-column": "full-address"
                }
            else:
                best_address = {
                    "entityRecord": row['entityRecord'],
                    "service": None,
                    "address-column": None
                }

        else:
            # Yes province

            # This should be pretty accurate, but not that precise.
            province_coords = (d[0]['latitude-geocode'], d[0]['longitude-geocode'])

            best_address = {
                "entityRecord": entityRecord,
                "service": "nominatim",
                "address-column": "province-country"
            }
            # Ordered from worst to best.
            for address_type, service in [
                ('postcode-country', 'nominatim'),
                ('postcode-country', 'google'),
                ('postcode-country', 'geonames'),
                ('full-address', 'google'),
                ('town-country', 'nominatim'),
                ('town-country', 'google'),
                ('town-country', 'geonames'),
                ('town-province-country', 'nominatim'),
                ('town-province-country', 'google'),
                ('town-province-country', 'geonames')
            ]:
                d2 = select('''
  `entityRecord`, `address-column`, `service`, `latitude-geocode`, `longitude-geocode`
FROM `branch_address`
JOIN `geocode` ON
  `branch_address`.`address-input` = `geocode`.`address-input`
WHERE (
  `address-column` = ? AND
  `service` = ? AND
  `entityRecord` = ?
)''', [address_type, service, entityRecord])
                if len(d2) == 0:
                    continue
                row = d2[0]
    
                if row['latitude-geocode'] == None:
                    kilometers_from_province = None
                else:
                    kilometers_from_province = distance.distance(
                        (row['latitude-geocode'], row['longitude-geocode']),
                        province_coords
                    ).km
    
                if kilometers_from_province < MAX_KM_FROM_PROVINCE:
                    best_address = {
                        "entityRecord": row['entityRecord'],
                        "service": service,
                        "address-column": address_type
                    }

        save(['entityRecord'], best_address, 'branch_best-address', verbose = False)

def clear():
    execute('DROP TABLE address')
    execute('DROP TABLE branch_address')
    execute('DROP TABLE geocode')

def joinbest():
  d = select('''
  `Date_data_was_extracted`
, `Name_of_data_source`
, `Type_of_source`
, `URL_of_data_source`
, `Location_type`

, `Address`
, `Fax`
, `Email`
, `Telephone`

, `License_number`
--, `License_date`

, `Name_of_entity`
, `Type_of_entity`

, `Country`
, `Postal_code`
, `Province`
, `Sub-district`
, `Town`
, `Street_address`

, `latitude-geocode` 
, `longitude-geocode` 
FROM `branch_best-address`
JOIN `branch_address` ON (
  `branch_best-address`.`entityRecord` = `branch_address`.`entityRecord` AND
  `branch_best-address`.`address-column`= `branch_address`.`address-column`
)
JOIN `geocode` ON (
  `geocode`.`service` = `branch_best-address`.`service` AND
 `geocode`.`address-input` = `branch_address`.`address-input`
)
JOIN `scraped` ON
  `scraped`.`rowid` = `branch_best-address`.`entityRecord`
''')
  execute('DROP TABLE IF EXISTS `final`')
  save([], d, 'final')

geocode()
print "Finished geocoding"
print "Joining"

#execute('DROP TABLE IF EXISTS `branch_best-address`')
#choose()

joinbest()
print "Finished joining"
#SELECT `address-column`, `service`, count(*) as "number-geocoded" FROM `accuracy` WHERE (`address-geocode` IS NOT NULL) GROUP BY `address-column`, `service`

print '''
-- Address types
select count(*), `address-column` from `branch_best-address` group by `address-column`

-- Join the best geocode results.
SELECT
  `Date_data_was_extracted`
, `Name_of_data_source`
, `Type_of_source`
, `URL_of_data_source`
, `Location_type`

, `Address`
, `Fax`
, `Email`
, `Telephone`

, `License_number`
--, `License_date`

, `Name_of_entity`
, `Type_of_entity`

, `Country`
, `Postal_code`
, `Province`
, `Sub-district`
, `Town`
, `Street_address`

, `latitude-geocode` 
, `longitude-geocode` 
FROM `branch_best-address`
JOIN `branch_address` ON (
  `branch_best-address`.`entityRecord` = `branch_address`.`entityRecord` AND
  `branch_best-address`.`address-column`= `branch_address`.`address-column`
)
JOIN `geocode` ON (
  `geocode`.`service` = `branch_best-address`.`service` AND
 `geocode`.`address-input` = `branch_address`.`address-input`
)
JOIN `scraped` ON
  `scraped`.`rowid` = `branch_best-address`.`entityRecord`

-- The others
SELECT
  `Date_data_was_extracted`
, `Name_of_data_source`
, `Type_of_source`
, `URL_of_data_source`
, `Location_type`

, `Address`
, `Fax`
, `Email`
, `Telephone`

, `License_number`
--, `License_date`

, `Name_of_entity`
, `Type_of_entity`

, `Country`
, `Postal_code`
, `Province`
, `Sub-district`
, `Town`
, `Street_address`

, NULL AS `latitude-geocode` 
, NULL AS `longitude-geocode` 
from `scraped` where rowid in (SELECT entityRecord from `branch_best-address` where `address-column` is null) limit 1

'''