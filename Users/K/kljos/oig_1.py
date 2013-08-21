import scraperwiki   
from urllib2 import Request, urlopen, URLError, HTTPError       
import urllib, urllib2, urlparse
import lxml.etree, lxml.html, lxml
import re, os
from bs4 import BeautifulSoup
from time import sleep

base_url = "http://www.dhs.gov/us-visit-documents-foia-electronic-reading-room"

url = base_url
html =  scraperwiki.scrape(base_url, user_agent="Mozilla Firefox")
soup = soup = BeautifulSoup(html)
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS dhsoig (`pdf_url` VARCHAR PRIMARY KEY, `pdf_title` VARCHAR, `library_url` VARCHAR,  `agency_name` VARCHAR, `report_num` VARCHAR, `date` VARCHAR, `pdf_xml` BLOB);')
results = []
soup = BeautifulSoup(html)
pdf_url = []
pdf_title = []
library_url = []
agency_name = []
pdf_text = []
report_num = []
date = []
pdfs = soup.find_all(href=re.compile("pdf"))
for item in pdfs:
    record={}
    req = urllib2.Request(item['href'])
    try: 
       response = urllib2.urlopen(req)
    except HTTPError, e:
       pdf_xml = 'PDF not Found. Error code:', e.code
    else:
       the_page = response.read()
       pdfdata = the_page
       pdf_xml = str(scraperwiki.pdftoxml(pdfdata, ''))
    ##except scraperwiki.pdftoxml.UnicodeDecodeError, e:
    ##   pdf_xml = str(e), str(type(e)).replace("<", "&lt;")
    record['pdf_url']=item['href'].encode("utf-8")
    if item.string:
       record['pdf_title']=item.string.encode("utf-8")
    else:
       record['pdf_title']=item.strip
    record['library_url']=url.encode("utf-8")
    record['pdf_xml']=str(pdf_xml)
##record['date']=item.parent.previous_sibling.string
##if item.parent.previous_sibling.previous_sibling:
##    record['report_num']=item.parent.previous_sibling.previous_sibling.string
##else:
##    record['report_num']=""
    record['agency_name']=soup.title.string.encode("utf-8")
    print record
    scraperwiki.sqlite.save(['pdf_url'], record, table_name='dhs')
    sleep(20)
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byurl ON dhs (`pdf_url`)')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON dhs (`pdf_title`)')
scraperwiki.sqlite.execute('ANALYZE')
scraperwiki.sqlite.commit()
