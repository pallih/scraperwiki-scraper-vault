# TO DO
# * Add some error metric, probably based on latitude and longitude.
# * Consider place type.
# * Run more data.
import operator
from scraperwiki.sqlite import attach, select, get_var, save_var, save, execute, commit
from urllib2 import urlopen
from urllib import urlencode
from json import loads, dumps
attach('capitec_bank')
from time import sleep
from unidecode import unidecode

GEOCODE_URL = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&json_callback=&%s'

COLUMNS = [
  # Null
#  'address',

  # Main effects
#  'branchName',
#  'provinceName',

  # Second-order
#  'branchName || ", South Africa"',
  'provinceName || ", South Africa"',
#  'branchName || ", " || provinceName',

  # All
#  'branchName || ", " || provinceName || ", South Africa"'
]

def main():
  if get_var('columns_to_do') == None:
    columns = COLUMNS
  else:
    columns = loads(get_var('columns_to_do'))

  while len(columns) > 0:
    column = columns[0]
    d = load_data(column)
    out = []
    for row in d:
      p = Place(row[column], (row['latitude'], row['longitude']) )
      row_geocode = p.geocode()
      row_geocode.update({
        "address-column":column,
        "branchId": row['branchId']
      })
      out = row_geocode
      sleep(3)
      save([], out, 'geocoded')
    columns.remove(column)

    if len(columns) == 0:
      save_var('columns_to_do',None)
    else:
      save_var('columns_to_do',dumps(columns))

def geocode_url(address):
  return GEOCODE_URL % urlencode({'q': address})

def load_data(column):
  d=select('''
  `branchId`,
   %s,
  `latitude`, `longitude`
FROM
  `branches`
WHERE
  `date-scraped` = (
    SELECT
      max(`date-scraped`)
    FROM
      `branches`
    )
  ''' % column)
  if column == 'address':
    for row in d:
      row[column] = unidecode(row[column])
  return d

class Place:
  GEOCODE_INFO_COLS = ('place_id', 'osm_id', 'type')
  def __init__(self, address, coords = None):
    "Initialize with the string address and, optionally, the (latitude, longitude) tuple."
    if type(address) in (str, unicode):
      self.address_gold = address
    else:
      raise TypeError("address must be a string.")

    if len(coords) != 2:
      raise TypeError("coords must have a length of 2.")

    self.coords_gold = self.convert_coords(coords)

  @staticmethod
  def convert_coords(coords):
    try:
      return tuple(map(float, coords))
    except TypeError:
      raise TypeError("coords could not be converted to a tuple of latitude and longitude numbers.")

  def load(self):
    url = geocode_url(self.address_gold)
    while True:
      try:
        json = urlopen(url).read()
      except:
        sleep(90)
      else:
        break
    d = loads(json)
    return d

  def geocode(self):
    d = self.load()

    self.match_count = len(d)
    if self.match_count > 0:
      "Take the first match."
      match = d[0]
      self.address_geocode = match['display_name']
      self.geocode_info = {k:match[k] for k in self.GEOCODE_INFO_COLS}
      self.coords_geocode = self.convert_coords([match[u'lat'], match[u'lon']])
    else:
      self.address_geocode = None
      self.geocode_info = {k:None for k in self.GEOCODE_INFO_COLS}
      self.coords_geocode = (None, None)

    return self.tabulate()

  def tabulate(self):
    "Put the contents into a table row dictionary."
    return {
      "address_gold": self.address_gold,
      "address_geocode": self.address_geocode,
      "latitude_gold": self.coords_gold[0],
      "longitude_gold": self.coords_gold[1],
      "latitude_geocode": self.coords_geocode[0],
      "longitude_geocode": self.coords_geocode[1],
      "number_of_matches": self.match_count,
      "place_type": self.geocode_info['type'],
      "kilometers_off": self.error() if self.match_count>0 else None
    }

  def error(self):
    """
    Compare the geocoded coordinates to the gold standard;
    return an approximate distance in kilometers

    # In South Africa,
    # 1 degree of latitude is about 111.2 kilometers and
    # 1 degree of longitude is about 94.30 kilometers.
    http://www.movable-type.co.uk/scripts/latlong.html
    """
    coords_difference = map(operator.sub,*[self.coords_gold,self.coords_geocode])
    km_difference_legs = map(operator.mul,*[coords_difference, (111.2, 94.3)])
    km_difference_legs_square = map(lambda a: a**2,km_difference_legs)
    km_difference_hypotenuse = operator.add(*km_difference_legs_square)**0.5
    return km_difference_hypotenuse

#execute('DELETE FROM `geocoded` WHERE `address-column` = "address";')
#execute('''DELETE FROM `geocoded` WHERE `address-column` = '"branchName || ", " || provinceName || ", South Africa"';''')
#commit()
main()