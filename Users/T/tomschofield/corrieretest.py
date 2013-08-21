
import scraperwiki           
import lxml.html
from bs4 import BeautifulSoup
import urllib2
from mechanize import Browser
from urlparse import urlparse
mech = Browser()
html = scraperwiki.scrape("http://www.corriere.it/")
root = lxml.html.fromstring(html)
#print root.text_content()

url = "http://www.corriere.it/"
page = urllib2.urlopen(url)
#page = urlparse(url)
#print page
soup = BeautifulSoup(page)
print soup.get_text()


