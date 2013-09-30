###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.2
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://www.nyc.gov/html/nypd/downloads/pdf/traffic_data/001sum.pdf"

a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))

name = None
all = []
data = {}
state = None
l = []

print s

for t in s.findAll('Brake'):
    if t.text != " ": 
        print t
        print t.text
    
###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.2
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://www.nyc.gov/html/nypd/downloads/pdf/traffic_data/001sum.pdf"

a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))

name = None
all = []
data = {}
state = None
l = []

print s

for t in s.findAll('Brake'):
    if t.text != " ": 
        print t
        print t.text
    
