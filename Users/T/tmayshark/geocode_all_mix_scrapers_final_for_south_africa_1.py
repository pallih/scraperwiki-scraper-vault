from scraperwiki import swimport
from scraperwiki.sqlite import attach, select, get_var, save_var, save, execute, commit, show_tables
from urllib2 import urlopen
from urllib import urlencode
from json import loads, dumps
from time import sleep, time
from unidecode import unidecode
from geopy import geocoders, distance
import re

GEOCODE_URL = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&json_callback=&%s'

def geocode_url(address):
    return GEOCODE_URL % urlencode({'q': address})

testaddr = "Washington, DC"

print geocode_url(testaddr)

class Encoder:
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

enc = Encoder()
print enc.geocode("Washington, DC")