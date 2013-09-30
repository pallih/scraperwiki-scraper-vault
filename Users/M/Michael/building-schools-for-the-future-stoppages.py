###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://news.bbc.co.uk/1/shared/bsp/hi/pdfs/19_07_10_school_error_list.pdf"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))

name = None
all = []
data = {}
state = None
l = []

scraperwiki.metadata.save('data_columns', ['School', 'Status', 'Constituency'])

def scrape(soup):
    for t in s.findAll('text'):
        record = {}
        if t['left'] == "18":
            if t['font'] == "4":
                record['Constituency'] = t.text
        if t['left'] == "69":
            if t['font'] == "5":
                record['School'] = t.text
        if t['left'] == "316":
            if t['font'] == "5":
                record['Status'] = t.text
        print record
        scraperwiki.datastore.save(["Day"], record)
scrape(pdfurl)
###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://news.bbc.co.uk/1/shared/bsp/hi/pdfs/19_07_10_school_error_list.pdf"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))

name = None
all = []
data = {}
state = None
l = []

scraperwiki.metadata.save('data_columns', ['School', 'Status', 'Constituency'])

def scrape(soup):
    for t in s.findAll('text'):
        record = {}
        if t['left'] == "18":
            if t['font'] == "4":
                record['Constituency'] = t.text
        if t['left'] == "69":
            if t['font'] == "5":
                record['School'] = t.text
        if t['left'] == "316":
            if t['font'] == "5":
                record['Status'] = t.text
        print record
        scraperwiki.datastore.save(["Day"], record)
scrape(pdfurl)
