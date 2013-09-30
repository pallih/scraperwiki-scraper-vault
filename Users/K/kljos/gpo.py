import scraperwiki
from urllib2 import Request, urlopen, URLError, HTTPError       
import urllib, urllib2, urlparse
import re, os
import sqlite3
import uuid
from bs4 import *
import lxml
import unicodedata
from time import sleep

# scraperwiki.sqlite.execute('DROP TABLE IF EXISTS gpo;')
# scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS gpo ( `uid` TEXT PRIMARY KEY, `pdf_title` TEXT, `pdf_html` TEXT, `year` INTEGER, `author` TEXT, `library_url` TEXT);')
pdf_title = []
pdf_url = []
year = []
author = []


##
## to create the query url go to http://catalog.gpo.gov/F/, search for your topic of interest. Copy the query key from the results page url like:
## http://catalog.gpo.gov/F/{{QUERY KEY}}?func= ....
##
library_url="http://catalog.gpo.gov/F/5PFVDU1U1KJHYQRJLMDJE3PMGFX7UJU6BD8EDUU3EJ8YIRMESC-46001?func=short-jump&jump="
IDX = 1
while IDX < 4088:
   response = urllib2.urlopen(library_url + str(IDX))
   html = response.read()
   soup = BeautifulSoup(html)
   if soup.body.find('table',attrs={'width':'*','cellspacing':'2'}) != None:
      data_table = soup.body.find('table',attrs={'width':'*','cellspacing':'2'})
      data_rows = data_table.findAll('tr')
      record = {}
      for ix in range(len(data_rows)):
          record = {}
          if ix > 0:
              record['library_url'] = library_url + str(IDX)
              record['uid'] = uuid.uuid1()
              record['pdf_html'] = data_rows[ix].contents[1].a.get('href')
              record['pdf_title'] = re.sub(".*document.write\(\'>\'\);\s*", "", re.sub('\s+',' ', str(unicode(data_rows[ix].contents[5].text.encode('ascii','ignore')))))
              record['year'] = float(data_rows[ix].contents[7].string)
              try:
                  record['author'] = re.sub('\.([A-Z])',r' \1',data_rows[ix].contents[9].string)
              except:
                  record['author'] = data_rows[ix].contents[9].string
              record['gpo_id'] = data_rows[ix].contents[11].string
              try:
                  record['pdf_url'] = re.sub('^(.+)(http://.*)$',r'\1;\2',data_rows[ix].contents[13].text)
              except:
                  record['pdf_url'] = data_rows[ix].contents[13].text
              try:
                  scraperwiki.sqlite.save(['uid'], record, table_name='gpo')
                  print record
              except:
                  print (record,"FAILED")
   IDX += 10
   sleep(1)
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byuid ON gpo (`uid`)')

scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON gpo (`pdf_title`)')

scraperwiki.sqlite.execute('ANALYZE')
scraperwiki.sqlite.execute('UPDATE `gpo` set pdf_title = rtrim(ltrim(replace(pdf_title,"/","")))')
scraperwiki.sqlite.execute('UPDATE `gpo` set author = rtrim(ltrim(replace(author,".","")))')
scraperwiki.sqlite.execute('UPDATE `gpo` set pdf_url = replace(pdf_url," ","")')
scraperwiki.sqlite.execute('UPDATE `gpo` set gpo_id = rtrim(ltrim(gpo_id))')
scraperwiki.sqlite.commit()import scraperwiki
from urllib2 import Request, urlopen, URLError, HTTPError       
import urllib, urllib2, urlparse
import re, os
import sqlite3
import uuid
from bs4 import *
import lxml
import unicodedata
from time import sleep

# scraperwiki.sqlite.execute('DROP TABLE IF EXISTS gpo;')
# scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS gpo ( `uid` TEXT PRIMARY KEY, `pdf_title` TEXT, `pdf_html` TEXT, `year` INTEGER, `author` TEXT, `library_url` TEXT);')
pdf_title = []
pdf_url = []
year = []
author = []


##
## to create the query url go to http://catalog.gpo.gov/F/, search for your topic of interest. Copy the query key from the results page url like:
## http://catalog.gpo.gov/F/{{QUERY KEY}}?func= ....
##
library_url="http://catalog.gpo.gov/F/5PFVDU1U1KJHYQRJLMDJE3PMGFX7UJU6BD8EDUU3EJ8YIRMESC-46001?func=short-jump&jump="
IDX = 1
while IDX < 4088:
   response = urllib2.urlopen(library_url + str(IDX))
   html = response.read()
   soup = BeautifulSoup(html)
   if soup.body.find('table',attrs={'width':'*','cellspacing':'2'}) != None:
      data_table = soup.body.find('table',attrs={'width':'*','cellspacing':'2'})
      data_rows = data_table.findAll('tr')
      record = {}
      for ix in range(len(data_rows)):
          record = {}
          if ix > 0:
              record['library_url'] = library_url + str(IDX)
              record['uid'] = uuid.uuid1()
              record['pdf_html'] = data_rows[ix].contents[1].a.get('href')
              record['pdf_title'] = re.sub(".*document.write\(\'>\'\);\s*", "", re.sub('\s+',' ', str(unicode(data_rows[ix].contents[5].text.encode('ascii','ignore')))))
              record['year'] = float(data_rows[ix].contents[7].string)
              try:
                  record['author'] = re.sub('\.([A-Z])',r' \1',data_rows[ix].contents[9].string)
              except:
                  record['author'] = data_rows[ix].contents[9].string
              record['gpo_id'] = data_rows[ix].contents[11].string
              try:
                  record['pdf_url'] = re.sub('^(.+)(http://.*)$',r'\1;\2',data_rows[ix].contents[13].text)
              except:
                  record['pdf_url'] = data_rows[ix].contents[13].text
              try:
                  scraperwiki.sqlite.save(['uid'], record, table_name='gpo')
                  print record
              except:
                  print (record,"FAILED")
   IDX += 10
   sleep(1)
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byuid ON gpo (`uid`)')

scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON gpo (`pdf_title`)')

scraperwiki.sqlite.execute('ANALYZE')
scraperwiki.sqlite.execute('UPDATE `gpo` set pdf_title = rtrim(ltrim(replace(pdf_title,"/","")))')
scraperwiki.sqlite.execute('UPDATE `gpo` set author = rtrim(ltrim(replace(author,".","")))')
scraperwiki.sqlite.execute('UPDATE `gpo` set pdf_url = replace(pdf_url," ","")')
scraperwiki.sqlite.execute('UPDATE `gpo` set gpo_id = rtrim(ltrim(gpo_id))')
scraperwiki.sqlite.commit()