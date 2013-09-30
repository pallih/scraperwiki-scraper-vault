import scraperwiki
import lxml.html
from lxml.html.clean import Cleaner
import time

print "hello workd"

base_url = 'http://www.wheelsland.com/cas/site/intro.asp'

html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)

links = root.cssselect("select#idMarca option")

for link in links:

    """
    name = link.cssselect("a")[0].text_content()
    card_link = link.cssselect("a")[0].attrib['href']
    address = link.cssselect("p")[0].text_content()
    """

    print link
import scraperwiki
import lxml.html
from lxml.html.clean import Cleaner
import time

print "hello workd"

base_url = 'http://www.wheelsland.com/cas/site/intro.asp'

html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)

links = root.cssselect("select#idMarca option")

for link in links:

    """
    name = link.cssselect("a")[0].text_content()
    card_link = link.cssselect("a")[0].attrib['href']
    address = link.cssselect("p")[0].text_content()
    """

    print link
