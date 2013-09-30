###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here:
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize
import scraperwiki
import lxml.html as lh 
import urllib
import urllib2
import urllib2, cookielib
from BeautifulSoup import BeautifulSoup

# set things up
jar = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(jar)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)



ansurl="http://www.laguiaclasificados.com.co/ws"
print ansurl
req = urllib2.Request(ansurl)
response = urllib2.urlopen(req)
the_page = response.read()
soup = BeautifulSoup(the_page)
soup.prettify()
print "the page is",the_page
print soup

#data = { 'ans' : str(i+1+inicio), 'html' : soup }
#scraperwiki.sqlite.save(unique_keys=['ans'], data=data);
###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here:
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize
import scraperwiki
import lxml.html as lh 
import urllib
import urllib2
import urllib2, cookielib
from BeautifulSoup import BeautifulSoup

# set things up
jar = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(jar)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)



ansurl="http://www.laguiaclasificados.com.co/ws"
print ansurl
req = urllib2.Request(ansurl)
response = urllib2.urlopen(req)
the_page = response.read()
soup = BeautifulSoup(the_page)
soup.prettify()
print "the page is",the_page
print soup

#data = { 'ans' : str(i+1+inicio), 'html' : soup }
#scraperwiki.sqlite.save(unique_keys=['ans'], data=data);
