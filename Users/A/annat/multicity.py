import requests
import simplejson
import re

url = requests.post("https://kunden.multicity-carsharing.de/kundenbuchung/hal2ajax_process.php?callback=jQuery172042462066053246283_1362647846982&zoom=10&lng1=&lat1=&lng2=&lat2=&stadtCache=&mapstation_id=&mapstadt_id=&verwaltungfirma=&centerLng=13.454010870361344&centerLat=52.51188581934838&searchmode=buchanfrage&with_staedte=true&buchungsanfrage=J&lat=52.51188581934838&lng=13.454010870361344&instant_access=J&open_end=J&objectname=multicitymarker&clustername=multicitycluster&ignore_virtual_stations=J&before=null&after=null&ajxmod=hal2map&callee=getMarker&_=1362647848815")

t = url.text

js = re.search(r'\((.*)\)', t).group(1)

jsonM = simplejson.loads(js)
