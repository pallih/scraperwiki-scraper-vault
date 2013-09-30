import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://sy10.ukfilmcouncil.ry.com/sitePDF/4.2.pdf"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))

name = None
all = []
data = {}
state = None
l = []
cns = None
empty =None
for t in s.findAll('text'):
    if t.text != " " and len(t.text) < 40: 
        cns = t.text
        print cns
    elif len (t.text) > 40:
        empty = t.text 
        scraperwiki.datastore.save (unique_keys=["cns"],data={"cns":cns,"empty":empty})
        cns=""
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://sy10.ukfilmcouncil.ry.com/sitePDF/4.2.pdf"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))

name = None
all = []
data = {}
state = None
l = []
cns = None
empty =None
for t in s.findAll('text'):
    if t.text != " " and len(t.text) < 40: 
        cns = t.text
        print cns
    elif len (t.text) > 40:
        empty = t.text 
        scraperwiki.datastore.save (unique_keys=["cns"],data={"cns":cns,"empty":empty})
        cns=""
