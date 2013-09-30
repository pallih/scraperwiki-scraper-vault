###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "https://docs.google.com/viewer?a=v&pid=explorer&chrome=true&srcid=11et7j6PUcuHrAGxYrEnm1yqetmS6ZXn1IpsUA7wglO0U8omZUBw6kyDMtatC&hl=en_GB"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))

name = None
all = []
data = {}
state = None
l = []

for t in s.findAll('text'):
    if t.text != " ": 
        print t
        print t.text
    
###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "https://docs.google.com/viewer?a=v&pid=explorer&chrome=true&srcid=11et7j6PUcuHrAGxYrEnm1yqetmS6ZXn1IpsUA7wglO0U8omZUBw6kyDMtatC&hl=en_GB"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))

name = None
all = []
data = {}
state = None
l = []

for t in s.findAll('text'):
    if t.text != " ": 
        print t
        print t.text
    
