import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://www.premierleague.com/staticFiles/5f/52/0,,12306~152159,00.pdf"
url = scraperwiki.scrape(pdfurl)
soupurl = BeautifulSoup(scraperwiki.pdftoxml(url))

name = None
all = []
data = {}
state = None
l = []

for t in soupurl.findAll('text'):
    if t.text != " ": 
        print t
        print t.text
    

import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://www.premierleague.com/staticFiles/5f/52/0,,12306~152159,00.pdf"
url = scraperwiki.scrape(pdfurl)
soupurl = BeautifulSoup(scraperwiki.pdftoxml(url))

name = None
all = []
data = {}
state = None
l = []

for t in soupurl.findAll('text'):
    if t.text != " ": 
        print t
        print t.text
    

