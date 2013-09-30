import scraperwiki   
from urllib2 import Request, urlopen, URLError, HTTPError       
import urllib, urllib2, urlparse
import lxml.etree, lxml.html, lxml
import re, os
from bs4 import BeautifulSoup
from BeautifulSoup import *
from time import sleep

## scrape next - archive http://2002-2009-fpc.state.gov/c18191.htm table / diff structure
scraperwiki.sqlite.execute('DROP TABLE int_studies;')
base_url = "https://www.cia.gov/library/center-for-the-study-of-intelligence/csi-publications/csi-studies/index.html"
pages = [ 200 ]

hosting_organization='Central Intelligence Agency'
for page in pages:
     url = base_url
     html =  scraperwiki.scrape(base_url, user_agent="Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1")
     scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS int_studies ( `pdf_title` VARCHAR, `pdf_url` VARCHAR PRIMARY KEY, `author` VARCHAR, `volume_url` VARCHAR, `volume_title` VARCHAR, `library_url` VARCHAR,  `agency_name` VARCHAR);')
     results = []
     soup = BeautifulSoup(html)
     pdf_url = []
     pdf_link = []
     volume_title = []
     volume_url = []
     agency_name = []
     volume_text = []
     lists = soup.findAll('ul')
     navLists = lists[5].findAll('li')
     for entry in navLists:
          href_link = entry.findChild('a')
          entry_url = 'https://www.cia.gov' + href_link.get('href')
          title = entry.text     
          response = urllib2.urlopen(entry_url)
          vol_html = response.read()
          vol_soup = BeautifulSoup(vol_html)
          if len(vol_soup.find('div', { "id" : "content" })) > 0:
             parent_documents=vol_soup.find('div',{"id":"content"}).findChildren('p')
          elif len(vol_soup.find('div',{"class":"plain"}).findChildren('p')) > 0:
             parent_documents=vol_soup.find('div',{"class":"plain"}).findChildren('p')
          else:
             parent_documents=vol_soup.find('div').findChildren('p')
          print parent_documents
          for document in parent_documents:
              record={}
              
              if len(document.findChildren('a')) > 0 and len(document.findChildren('img')) == 0 and re.search('^.*[Aa]dobe.*$|^.*Top of page.*$',str(document.contents[0])) == None and len(document.contents[0]) > 0 and document.contents[0].string != None:
                 pdf_title = document.contents[0]
                 pdf_title = pdf_title.string
                 pdf_link = document.find('a').get('href')
                 #pdf_title = re.sub(r'.*[Aa]dobe.*|.*Top of page.*','',pdf_title)
                 if pdf_link:
                    record['pdf_url'] = 'https://www.cia.gov' + str(pdf_link)
                 record['pdf_title'] = pdf_title.encode('utf-8')
#re.sub(r'([a-z0-9])([A-Z])',r'\1 \2',pdf_title)
                 record['volume_title']=title.encode("utf-8")
                 record['volume_url']=entry_url
                 record['library_url']=url.encode("utf-8")
                 record['agency_name']=hosting_organization
                 if re.sub('\s','',pdf_title) != "":
                   try:
                      scraperwiki.sqlite.save(['pdf_url'], record, table_name='int_studies')
                      print record
                   except:
                      print (record,"FAILED")
                 sleep(1)
              else:
                 sleep(0)
     scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byurl ON int_studies (`volume_url`)')      
     scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON int_studies (`volume_title`)')
     scraperwiki.sqlite.execute('ANALYZE')
     scraperwiki.sqlite.commit()


import scraperwiki   
from urllib2 import Request, urlopen, URLError, HTTPError       
import urllib, urllib2, urlparse
import lxml.etree, lxml.html, lxml
import re, os
from bs4 import BeautifulSoup
from BeautifulSoup import *
from time import sleep

## scrape next - archive http://2002-2009-fpc.state.gov/c18191.htm table / diff structure
scraperwiki.sqlite.execute('DROP TABLE int_studies;')
base_url = "https://www.cia.gov/library/center-for-the-study-of-intelligence/csi-publications/csi-studies/index.html"
pages = [ 200 ]

hosting_organization='Central Intelligence Agency'
for page in pages:
     url = base_url
     html =  scraperwiki.scrape(base_url, user_agent="Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1")
     scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS int_studies ( `pdf_title` VARCHAR, `pdf_url` VARCHAR PRIMARY KEY, `author` VARCHAR, `volume_url` VARCHAR, `volume_title` VARCHAR, `library_url` VARCHAR,  `agency_name` VARCHAR);')
     results = []
     soup = BeautifulSoup(html)
     pdf_url = []
     pdf_link = []
     volume_title = []
     volume_url = []
     agency_name = []
     volume_text = []
     lists = soup.findAll('ul')
     navLists = lists[5].findAll('li')
     for entry in navLists:
          href_link = entry.findChild('a')
          entry_url = 'https://www.cia.gov' + href_link.get('href')
          title = entry.text     
          response = urllib2.urlopen(entry_url)
          vol_html = response.read()
          vol_soup = BeautifulSoup(vol_html)
          if len(vol_soup.find('div', { "id" : "content" })) > 0:
             parent_documents=vol_soup.find('div',{"id":"content"}).findChildren('p')
          elif len(vol_soup.find('div',{"class":"plain"}).findChildren('p')) > 0:
             parent_documents=vol_soup.find('div',{"class":"plain"}).findChildren('p')
          else:
             parent_documents=vol_soup.find('div').findChildren('p')
          print parent_documents
          for document in parent_documents:
              record={}
              
              if len(document.findChildren('a')) > 0 and len(document.findChildren('img')) == 0 and re.search('^.*[Aa]dobe.*$|^.*Top of page.*$',str(document.contents[0])) == None and len(document.contents[0]) > 0 and document.contents[0].string != None:
                 pdf_title = document.contents[0]
                 pdf_title = pdf_title.string
                 pdf_link = document.find('a').get('href')
                 #pdf_title = re.sub(r'.*[Aa]dobe.*|.*Top of page.*','',pdf_title)
                 if pdf_link:
                    record['pdf_url'] = 'https://www.cia.gov' + str(pdf_link)
                 record['pdf_title'] = pdf_title.encode('utf-8')
#re.sub(r'([a-z0-9])([A-Z])',r'\1 \2',pdf_title)
                 record['volume_title']=title.encode("utf-8")
                 record['volume_url']=entry_url
                 record['library_url']=url.encode("utf-8")
                 record['agency_name']=hosting_organization
                 if re.sub('\s','',pdf_title) != "":
                   try:
                      scraperwiki.sqlite.save(['pdf_url'], record, table_name='int_studies')
                      print record
                   except:
                      print (record,"FAILED")
                 sleep(1)
              else:
                 sleep(0)
     scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byurl ON int_studies (`volume_url`)')      
     scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON int_studies (`volume_title`)')
     scraperwiki.sqlite.execute('ANALYZE')
     scraperwiki.sqlite.commit()


