import scraperwiki   
from urllib2 import Request, urlopen, URLError, HTTPError       
import urllib, urllib2, urlparse
import lxml.etree, lxml.html, lxml
import re, os
from bs4 import BeautifulSoup
from time import sleep

military_sites = "/MILITARY/miltop.htm"
civilian_sites = ['/CIVILIAN/fy2012/december2011/december2011.htm', 'CIVILIAN/fy2011/september2011/september2011.htm', '/CIVILIAN/fy2011/june2011/june2011.htm','/CIVILIAN/fy2010/june2010/june2010','/CIVILIAN/fy2011/march2011/march2011.htm',
'/CIVILIAN/fy2011/december2010/december2010.htm', '/CIVILIAN/fy2010/september2010/september2010.htm', '/CIVILIAN/fy2010/march2010/march2010.htm', '/CIVILIAN/fy2010/december2009/december2009.htm', '/CIVILIAN/fy2009/september2009/september2009.htm','/CIVILIAN/fy2009/august2009/august2009.htm', '/CIVILIAN/fy2009/july2009/july2009.htm', '/CIVILIAN/fy2009/june2009/june2009.htm','/CIVILIAN/fy2009/may2009/may2009.htm', '/CIVILIAN/fy2009/april2009/april2009.htm', '/CIVILIAN/fy2009/march2009/march2009.htm', '/CIVILIAN/fy2009/february2009/february2009.htm', '/CIVILIAN/fy2009/december2008/december2008.htm', '/CIVILIAN/fy2009/november2008/november2008.htm']
civ_manpower_stats = ['/CIVILIAN/M04SEP99.pdf','/CIVILIAN/m04sep98.pdf','/CIVILIAN/m04jun99.pdf','/CIVILIAN/M04JUN98.PDF','/CIVILIAN/M04MAR99.pdf', '/CIVILIAN/m04mar98.pdf', '/CIVILIAN/M04DEC98.pdf', '/CIVILIAN/M04DEC97.PDF']

base_url = "http://siadapp.dmdc.osd.mil/personnel"
url = base_url + str(military_sites)
html =  scraperwiki.scrape(url, user_agent="Mozilla Firefox")
soup = soup = BeautifulSoup(html)
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS dod_personnel (`pdf_url` VARCHAR PRIMARY KEY, `pdf_title` VARCHAR, `library_url` VARCHAR,  `agency_name` VARCHAR, `report_num` VARCHAR, `date` VARCHAR, `pdf_xml` BLOB, `series_title` VARCHAR  `pdf_xml` VARCHAR);')
results = []
soup = BeautifulSoup(html)
pdf_url = []
pdf_title = []
library_url = []
agency_name = []
pdf_text = []
pdf_desc = []
report_num = []
date = []
series_title = []

pdfs = soup.find_all(href=re.compile("pdf"))
for item in pdfs:
    record={}
    req = urllib2.Request("http://siadapp.dmdc.osd.mil/personnel/MILITARY/" + item['href'])
    response = urllib2.urlopen(req)
    ##except HTTPError, e:
      ##  pdf_xml = 'PDF not Found. Error code:', e.code
    ##else:
    the_page = response.read()
    pdfdata = the_page
    pdf_xml = str(scraperwiki.pdftoxml(pdfdata, ''))
    ##except scraperwiki.pdftoxml.UnicodeDecodeError, e:
    ##   pdf_xml = str(e), str(type(e)).replace("<", "&lt;")
    record['pdf_url']= "http://siadapp.dmdc.osd.mil/personnel/MILITARY/" + item['href'].encode("utf-8")
    if item.string:
        record['pdf_title']=item.string.encode("utf-8")
    else:
        record['pdf_title']=item.strip
##    if item.find_parents("ul")
  #3      record['pdf_desc']= item.find_parents("ul").find_parents("ul").b.string
    ##elif item.parent.div:
      ##  record['pdf_desc']= item.find_previous("ul").li.string
   ## if item.parent.parent.previous_sibling("p"):
     ##   record['pdf_desc']= item.parent.previous_sibling("p").string
    ## else:
    record['pdf_desc']= item.find_parent("ul").contents[0].string
    record['library_url']=url.encode("utf-8")
    record['pdf_xml']=str(pdf_xml)
    record['agency_name']=soup.title.string.encode("utf-8")
    print record
    scraperwiki.sqlite.save(['pdf_url'], record, table_name='dhs')
    sleep(20)
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byurl ON dod_personnel (`pdf_url`)')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON dod_personnel (`pdf_title`)')
scraperwiki.sqlite.execute('ANALYZE')
scraperwiki.sqlite.commit()
import scraperwiki   
from urllib2 import Request, urlopen, URLError, HTTPError       
import urllib, urllib2, urlparse
import lxml.etree, lxml.html, lxml
import re, os
from bs4 import BeautifulSoup
from time import sleep

military_sites = "/MILITARY/miltop.htm"
civilian_sites = ['/CIVILIAN/fy2012/december2011/december2011.htm', 'CIVILIAN/fy2011/september2011/september2011.htm', '/CIVILIAN/fy2011/june2011/june2011.htm','/CIVILIAN/fy2010/june2010/june2010','/CIVILIAN/fy2011/march2011/march2011.htm',
'/CIVILIAN/fy2011/december2010/december2010.htm', '/CIVILIAN/fy2010/september2010/september2010.htm', '/CIVILIAN/fy2010/march2010/march2010.htm', '/CIVILIAN/fy2010/december2009/december2009.htm', '/CIVILIAN/fy2009/september2009/september2009.htm','/CIVILIAN/fy2009/august2009/august2009.htm', '/CIVILIAN/fy2009/july2009/july2009.htm', '/CIVILIAN/fy2009/june2009/june2009.htm','/CIVILIAN/fy2009/may2009/may2009.htm', '/CIVILIAN/fy2009/april2009/april2009.htm', '/CIVILIAN/fy2009/march2009/march2009.htm', '/CIVILIAN/fy2009/february2009/february2009.htm', '/CIVILIAN/fy2009/december2008/december2008.htm', '/CIVILIAN/fy2009/november2008/november2008.htm']
civ_manpower_stats = ['/CIVILIAN/M04SEP99.pdf','/CIVILIAN/m04sep98.pdf','/CIVILIAN/m04jun99.pdf','/CIVILIAN/M04JUN98.PDF','/CIVILIAN/M04MAR99.pdf', '/CIVILIAN/m04mar98.pdf', '/CIVILIAN/M04DEC98.pdf', '/CIVILIAN/M04DEC97.PDF']

base_url = "http://siadapp.dmdc.osd.mil/personnel"
url = base_url + str(military_sites)
html =  scraperwiki.scrape(url, user_agent="Mozilla Firefox")
soup = soup = BeautifulSoup(html)
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS dod_personnel (`pdf_url` VARCHAR PRIMARY KEY, `pdf_title` VARCHAR, `library_url` VARCHAR,  `agency_name` VARCHAR, `report_num` VARCHAR, `date` VARCHAR, `pdf_xml` BLOB, `series_title` VARCHAR  `pdf_xml` VARCHAR);')
results = []
soup = BeautifulSoup(html)
pdf_url = []
pdf_title = []
library_url = []
agency_name = []
pdf_text = []
pdf_desc = []
report_num = []
date = []
series_title = []

pdfs = soup.find_all(href=re.compile("pdf"))
for item in pdfs:
    record={}
    req = urllib2.Request("http://siadapp.dmdc.osd.mil/personnel/MILITARY/" + item['href'])
    response = urllib2.urlopen(req)
    ##except HTTPError, e:
      ##  pdf_xml = 'PDF not Found. Error code:', e.code
    ##else:
    the_page = response.read()
    pdfdata = the_page
    pdf_xml = str(scraperwiki.pdftoxml(pdfdata, ''))
    ##except scraperwiki.pdftoxml.UnicodeDecodeError, e:
    ##   pdf_xml = str(e), str(type(e)).replace("<", "&lt;")
    record['pdf_url']= "http://siadapp.dmdc.osd.mil/personnel/MILITARY/" + item['href'].encode("utf-8")
    if item.string:
        record['pdf_title']=item.string.encode("utf-8")
    else:
        record['pdf_title']=item.strip
##    if item.find_parents("ul")
  #3      record['pdf_desc']= item.find_parents("ul").find_parents("ul").b.string
    ##elif item.parent.div:
      ##  record['pdf_desc']= item.find_previous("ul").li.string
   ## if item.parent.parent.previous_sibling("p"):
     ##   record['pdf_desc']= item.parent.previous_sibling("p").string
    ## else:
    record['pdf_desc']= item.find_parent("ul").contents[0].string
    record['library_url']=url.encode("utf-8")
    record['pdf_xml']=str(pdf_xml)
    record['agency_name']=soup.title.string.encode("utf-8")
    print record
    scraperwiki.sqlite.save(['pdf_url'], record, table_name='dhs')
    sleep(20)
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byurl ON dod_personnel (`pdf_url`)')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON dod_personnel (`pdf_title`)')
scraperwiki.sqlite.execute('ANALYZE')
scraperwiki.sqlite.commit()
