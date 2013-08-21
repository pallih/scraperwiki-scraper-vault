###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://www.co.washoe.nv.us/repository/files/21/TELEPHONE%20REFERRAL%20LIST.pdf"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))


for t in s.findAll('text'):
    if t.text != " ": 
        print t.text
        scraperwiki.sqlite.save(['entry'], {'entry': t.text}, table_name='entries') 
