# Blank Python
import scraperwiki
import lxml.html
import re
import datetime

# INITIALIZE
d = datetime.date(2001,12,29)
url = "http://www.famouswhy.com/Born_Today/12/29/1/1.html"


# place your cssselection case here and extract the values
def parse_page(url):
    root = lxml.html.parse(url).getroot()
    pages = root.cssselect('a.pagerLinkStyle')
    for link in pages:
        print link.attrib["href"]

parse_page(url)