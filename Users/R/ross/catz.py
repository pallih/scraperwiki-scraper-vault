import scraperwiki
import urlparse
import urllib2
import lxml.html

site = 'http://catoftheday.com/'
html = scraperwiki.scrape(site)
page = lxml.html.fromstring(html)

img = page.cssselect('td img')[11]
u = urlparse.urljoin(site, img.get('src'))

#scraperwiki.utils.httpresponseheader("Content-Type","image/jpg")
#print urllib2.urlopen(u).read()

# could just...

print uimport scraperwiki
import urlparse
import urllib2
import lxml.html

site = 'http://catoftheday.com/'
html = scraperwiki.scrape(site)
page = lxml.html.fromstring(html)

img = page.cssselect('td img')[11]
u = urlparse.urljoin(site, img.get('src'))

#scraperwiki.utils.httpresponseheader("Content-Type","image/jpg")
#print urllib2.urlopen(u).read()

# could just...

print u