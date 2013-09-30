import scraperwiki   
from urllib2 import Request, urlopen, URLError, HTTPError       
import urllib, urllib2, urlparse
import lxml.etree, lxml.html, lxml
import re, os
from bs4 import BeautifulSoup
from time import sleep

## scrape next - archive http://2002-2009-fpc.state.gov/c18191.htm table / diff structure
#scraperwiki.sqlite.execute('DROP TABLE state;')
base_url = "http://fpc.state.gov/"
pages = [ 'c18193', 'c28062', 'c18192', '', 'c28061' ]
hosting_organization='U.S. Department of State'
for page in pages:
     url = base_url + str(page) + '.htm'
     print url
     html =  scraperwiki.scrape(base_url + page + '.htm', user_agent="Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1")
     soup = soup = BeautifulSoup(html)
     scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS state (`pdf_url` VARCHAR PRIMARY KEY, `pdf_title` VARCHAR, `library_url` VARCHAR,  `agency_name` VARCHAR);')
     results = []
     soup = BeautifulSoup(html)
     pdf_url = []
     pdf_title = []
     library_url = []
     agency_name = []
     pdf_text = []
     link_tables = soup.find_all(id='body-col02-row02')
     for href in link_tables:
        links = href.find_all("a")
        for item in links:
           record={}
           record['pdf_url']=item['href'].encode("utf-8")
           if item.string:
               record['pdf_title']=re.sub(r'^\-\- ','',str(item.string)).encode("utf-8")
           else:
               record['pdf_title']=re.sub(r'^\-\- ','',str(item.strip)).encode("utf-8")
           record['library_url']=url.encode("utf-8")
           record['agency_name']=hosting_organization
           print record
           scraperwiki.sqlite.save(['pdf_url'], record, table_name='state')
     scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byurl ON state (`pdf_url`)')
     scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON state (`pdf_title`)')
     scraperwiki.sqlite.execute('ANALYZE')
     scraperwiki.sqlite.commit()


import scraperwiki   
from urllib2 import Request, urlopen, URLError, HTTPError       
import urllib, urllib2, urlparse
import lxml.etree, lxml.html, lxml
import re, os
from bs4 import BeautifulSoup
from time import sleep

## scrape next - archive http://2002-2009-fpc.state.gov/c18191.htm table / diff structure
#scraperwiki.sqlite.execute('DROP TABLE state;')
base_url = "http://fpc.state.gov/"
pages = [ 'c18193', 'c28062', 'c18192', '', 'c28061' ]
hosting_organization='U.S. Department of State'
for page in pages:
     url = base_url + str(page) + '.htm'
     print url
     html =  scraperwiki.scrape(base_url + page + '.htm', user_agent="Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1")
     soup = soup = BeautifulSoup(html)
     scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS state (`pdf_url` VARCHAR PRIMARY KEY, `pdf_title` VARCHAR, `library_url` VARCHAR,  `agency_name` VARCHAR);')
     results = []
     soup = BeautifulSoup(html)
     pdf_url = []
     pdf_title = []
     library_url = []
     agency_name = []
     pdf_text = []
     link_tables = soup.find_all(id='body-col02-row02')
     for href in link_tables:
        links = href.find_all("a")
        for item in links:
           record={}
           record['pdf_url']=item['href'].encode("utf-8")
           if item.string:
               record['pdf_title']=re.sub(r'^\-\- ','',str(item.string)).encode("utf-8")
           else:
               record['pdf_title']=re.sub(r'^\-\- ','',str(item.strip)).encode("utf-8")
           record['library_url']=url.encode("utf-8")
           record['agency_name']=hosting_organization
           print record
           scraperwiki.sqlite.save(['pdf_url'], record, table_name='state')
     scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byurl ON state (`pdf_url`)')
     scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON state (`pdf_title`)')
     scraperwiki.sqlite.execute('ANALYZE')
     scraperwiki.sqlite.commit()


