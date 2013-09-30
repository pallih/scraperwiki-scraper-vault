import scraperwiki
import BeautifulSoup
from urllib2 import HTTPError
from scraperwiki import datastore

constituency = 'Wimbledon'
html = scraperwiki.scrape('http://en.wikipedia.org/wiki/' + constituency + '_(UK_Parliament_constituency)')
page = BeautifulSoup.BeautifulSoup(html)

print page







import scraperwiki
import BeautifulSoup
from urllib2 import HTTPError
from scraperwiki import datastore

constituency = 'Wimbledon'
html = scraperwiki.scrape('http://en.wikipedia.org/wiki/' + constituency + '_(UK_Parliament_constituency)')
page = BeautifulSoup.BeautifulSoup(html)

print page







