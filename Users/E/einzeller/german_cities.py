# Benjamin Dittwald

from urllib2 import urlparse
import scraperwiki
import lxml.html
import datetime

URL = "http://de.wikipedia.org/wiki/Liste_der_St%C3%A4dte_in_Deutschland"

root = lxml.html.parse(URL).getroot()

for elem in root.cssselect('dd'):
    city_elem = elem[0]
    city = {}
    city['name'] = city_elem.text.encode('utf-8')
    city['wikipedia_url'] = 'http://de.wikipedia.org' + city_elem.attrib['href']
    scraperwiki.sqlite.save(unique_keys=["name"], data = city)
    print 'Saved city: ' + city['name']# Benjamin Dittwald

from urllib2 import urlparse
import scraperwiki
import lxml.html
import datetime

URL = "http://de.wikipedia.org/wiki/Liste_der_St%C3%A4dte_in_Deutschland"

root = lxml.html.parse(URL).getroot()

for elem in root.cssselect('dd'):
    city_elem = elem[0]
    city = {}
    city['name'] = city_elem.text.encode('utf-8')
    city['wikipedia_url'] = 'http://de.wikipedia.org' + city_elem.attrib['href']
    scraperwiki.sqlite.save(unique_keys=["name"], data = city)
    print 'Saved city: ' + city['name']