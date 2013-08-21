import scraperwiki
import requests
import simplejson
import lxml.html
from lxml.cssselect import CSSSelector
import time
import urllib2
import urllib

import re
r = requests.post('http://www.callabike-interaktiv.de/kundenbuchung/hal2ajax_process.php?callback=jQuery183017127112749728457_1362432312351&after=&ajxmod=hal2map&before=&bereich=2&buchungsanfrage=N&callee=getMarker&centerLat=50.916887525784894&centerLng=10.10913848876957&key=&lat1=&lat2=&lng1=&lng2=&mapstadt_id=2&mapstation_id=&requester=bikesuche&searchmode=default&stadtCache=&stoinput=&verwaltungfirma=&webfirma_id=500&with_staedte=N&zoom=10')

s = r.text
reg = re.search(r'\((.*)\)', s).group(1)
#extract = s[s.find("(")+1:s.find(")")]
#print extract
json = simplejson.loads(reg)
print json



