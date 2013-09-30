import scraperwiki   
from urllib2 import Request, urlopen, URLError, HTTPError       
import urllib, urllib2, urlparse
import lxml.etree, lxml.html, lxml
import re, os
from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from time import sleep

## scrape next - archive http://2002-2009-fpc.state.gov/c18191.htm table / diff structure
scraperwiki.sqlite.execute('DROP TABLE foreign_relations;')
base_url = "http://history.state.gov/services/volumes?title=&yearpublishedstart=1861&yearpublishedend=2012&yearcoveredstart=1861&yearcoveredend=2012&providers=db&perpage="
pages = [ 200 ]
#response = urllib2.urlopen(base_url)
#html = response.read()
hosting_organization='U.S. Department of State'
for page in pages:
     url = base_url + str(page)
     print url
     html =  scraperwiki.scrape(base_url + str(page), user_agent="Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1")
     soup = BeautifulSoup(html)
     scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS foreign_relations (`volume_url` VARCHAR PRIMARY KEY, `volume_title` VARCHAR, `library_url` VARCHAR,  `agency_name` VARCHAR);')
     results = []
     soup = BeautifulStoneSoup(html)
     pdf_url = []
     volume_title = []
     volume_url = []
     agency_name = []
     volume_text = []
     queryResults = soup.findAll('hit')
     for hit in queryResults:
         record={}
         title=hit.find('title')
         href=hit.find('url')
         record['volume_title']=title.string.encode("utf-8")
         record['volume_url']='http://history.state.gov' + href.string

         record['library_url']=url.encode("utf-8")
         record['agency_name']=hosting_organization
         print record
       #  response = urllib2.urlopen(base_url)
#html = response.read()
         scraperwiki.sqlite.save(['volume_url'], record, table_name='foreign_relations')
     scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byurl ON foreign_relations (`volume_url`)')
     scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON foreign_relations (`volume_title`)')
     scraperwiki.sqlite.execute('ANALYZE')
     scraperwiki.sqlite.commit()


import scraperwiki   
from urllib2 import Request, urlopen, URLError, HTTPError       
import urllib, urllib2, urlparse
import lxml.etree, lxml.html, lxml
import re, os
from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from time import sleep

## scrape next - archive http://2002-2009-fpc.state.gov/c18191.htm table / diff structure
scraperwiki.sqlite.execute('DROP TABLE foreign_relations;')
base_url = "http://history.state.gov/services/volumes?title=&yearpublishedstart=1861&yearpublishedend=2012&yearcoveredstart=1861&yearcoveredend=2012&providers=db&perpage="
pages = [ 200 ]
#response = urllib2.urlopen(base_url)
#html = response.read()
hosting_organization='U.S. Department of State'
for page in pages:
     url = base_url + str(page)
     print url
     html =  scraperwiki.scrape(base_url + str(page), user_agent="Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1")
     soup = BeautifulSoup(html)
     scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS foreign_relations (`volume_url` VARCHAR PRIMARY KEY, `volume_title` VARCHAR, `library_url` VARCHAR,  `agency_name` VARCHAR);')
     results = []
     soup = BeautifulStoneSoup(html)
     pdf_url = []
     volume_title = []
     volume_url = []
     agency_name = []
     volume_text = []
     queryResults = soup.findAll('hit')
     for hit in queryResults:
         record={}
         title=hit.find('title')
         href=hit.find('url')
         record['volume_title']=title.string.encode("utf-8")
         record['volume_url']='http://history.state.gov' + href.string

         record['library_url']=url.encode("utf-8")
         record['agency_name']=hosting_organization
         print record
       #  response = urllib2.urlopen(base_url)
#html = response.read()
         scraperwiki.sqlite.save(['volume_url'], record, table_name='foreign_relations')
     scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byurl ON foreign_relations (`volume_url`)')
     scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON foreign_relations (`volume_title`)')
     scraperwiki.sqlite.execute('ANALYZE')
     scraperwiki.sqlite.commit()


