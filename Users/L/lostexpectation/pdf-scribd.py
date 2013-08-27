###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://www.dublinstreams.com/temp/HAIDialogueGov_070705.pdf"
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
        scraperwiki.sqlite.save(["t"], {'t':t})###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://www.dublinstreams.com/temp/HAIDialogueGov_070705.pdf"
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
        scraperwiki.sqlite.save(["t"], {'t':t})###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://www.dublinstreams.com/temp/HAIDialogueGov_070705.pdf"
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
        scraperwiki.sqlite.save(["t"], {'t':t})