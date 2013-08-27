###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://www.birmingham.gov.uk/cs/Satellite?%26ssbinary=true&blobcol=urldata&blobheader=application%2Fpdf&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223439077563&blobheadervalue1=attachment%3B+filename%3D444523Payments+over+£500+August.pdf"
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

pdfurl = "http://www.birmingham.gov.uk/cs/Satellite?%26ssbinary=true&blobcol=urldata&blobheader=application%2Fpdf&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223439077563&blobheadervalue1=attachment%3B+filename%3D444523Payments+over+£500+August.pdf"
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

pdfurl = "http://www.birmingham.gov.uk/cs/Satellite?%26ssbinary=true&blobcol=urldata&blobheader=application%2Fpdf&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223439077563&blobheadervalue1=attachment%3B+filename%3D444523Payments+over+£500+August.pdf"
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

pdfurl = "http://www.birmingham.gov.uk/cs/Satellite?%26ssbinary=true&blobcol=urldata&blobheader=application%2Fpdf&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223439077563&blobheadervalue1=attachment%3B+filename%3D444523Payments+over+£500+August.pdf"
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
    
