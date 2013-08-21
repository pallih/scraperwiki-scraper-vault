import scraperwiki
import lxml.html

from urllib2 import urlopen
from urllib import urlencode

import scraperwiki, simplejson,urllib

from json import loads, dumps


"""
service = 'http://nominatim.openstreetmap.org/search?q=pilkington+avenue,birmingham&format=json'
#GEOCODE_URL = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&json_callback=&%s'

#url = geocode_url(service)

url = service

json = urlopen(url).read()
print json

ent = simplejson.loads(json)
print ent[0]['display_name']
print ent[0]['lat']
print ent[0]['lon']
"""


#txt = "Am 6. Oktober fand im Logenhaus in der Emäserstraße 12-13 in Wilmersdorf eine Veranstaltung rechtspopulistischer Organisationen, der “zwischentag”, statt. Daran beteiligten sich u.a. die Junge Freiheit, die Blaue Narzisse, die Förderstiftung Konservative Bildung und Forschung (jungefreiheitnah). (Hinweis per Email, deren Website)"

txt = "Am Morgen des 5. Oktober campingplatz aa spielplatz gegen spiel platz 7 Uhr stellte eine vorbeifahrendestraße Autofahrerin an einer Mauer vor der „Ewigen Flamme“ auf dem Theodor-Heuss-Platz Hakenkreuz AAA Hakenkreuz BBB und abckreuz CCC lorem kreuz DDDweitere Schmierereien fest.Unbekannte Täter hatten das Symbol und den Schriftzug in einer Größe von etwa sechs mal einem Meter aufgebracht”. (Quelle: Pressemeldung der Polizei # 3208)"

import re

# (\S+|\S+\s+)^      (?!spiel)      (?!spiel).*
#p = re.compile('(\S+|\S+\s+)(straße|strasse|str\.?|weg|gasse|allee|ufer|platz|damm|ring)(\s+|\.{1}\s+)\d*', re.I) # %str | %str. | 
#p = re.compile('(\S+|\S+\s+)(straße|strasse|str\.?|weg|gasse|allee|ufer|platz|damm|ring)(\s+|\.{1}\s+)\d*', re.I)


#\b(?!snow)\w+tire
#p = re.compile('(\S+|\S+\s+)(kreuz|platz).?.?', re.I)
#p = re.compile('\b(?!spiel|camping)(\S+|\S+\s+)(kreuz|platz).?.?', re.I)

#p = re.compile('\S+(?!spiel|camping)(kreuz|platz).?.?', re.I)
#p = re.compile('(\S+|\S+\W+)(?!spiel|camping)(kreuz|platz).?.?.?', re.I)

#p = re.compile('(\S+|\S+\s+)^(?!spiel)(straße|strasse|str\.?|weg|gasse|allee|ufer|(((?!spiel)\s+)platz)|damm|ring)(\s+|\.{1}\s+)\d*', re.I)

p = re.compile('(\S+|\S+\s+)(straße|strasse|str\.?|weg|gasse|allee|ufer|platz|damm|ring)(\s+|\.{1}\s+)\d*', re.I)

m = p.search(txt)

#weg damm

# places: station bahnhof bhf.

print txt

if m:
    print m.group()
else:
    print 'No match'




"""
    d = loads(json)
    return d

d = load()

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

print self.address_geocode

#while True:
#    try:
#        json = urlopen(url).read()
#        print json
#    except:
#        sleep(90)
#    else:
#        break

        #    d = loads(json)
"""


