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


########## Secrecy Blog #####################

scraperwiki.sqlite.execute('DROP TABLE IF EXISTS fas_secrecy;')
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS fas_secrecy ( `uid` TEXT PRIMARY KEY, `pdf_title` TEXT, `pdf_url` TEXT UNIQUE,  `date` INTEGER, `author` TEXT, `source_article_title` TEXT, `source_article_url` TEXT);')
pdf_title = []
pdf_url = []
year = []
author = []
author = "Congressional Research Service"
## Step 1 - find links to each article from 20 pages of article archives.
IDX = 1
while IDX < 2:
    if IDX == 1:
        URL = "http://www.fas.org/blog/secrecy/category/secrecy/"
    else:
        URL = "http://www.fas.org/blog/secrecy/category/secrecy/" + 'page/' +  str(IDX)
    response = urllib2.urlopen(URL)
    html = response.read()
    soup = BeautifulSoup(html)
    articles = soup.findAll('h3',attrs={"id": re.compile("post")})
## step 2 - traverse each article, grabbing pdf links + metadata
    for ix in range(len(articles)):
       article_url = articles[ix].a.get('href')
       article_title = articles[ix].a.text
       response = urllib2.urlopen(article_url)
       html = response.read()
       soup = BeautifulSoup(html)
       if soup.find('meta',attrs={"property":"og:title"}).get("content") != None:
           article_title = soup.find('meta',attrs={"property":"og:title"}).get("content")
       else:
           article_title
       reports = soup.body.find('div',attrs={"class":"post"}).findAll('a',attrs={"href": re.compile(r'^.*\.pdf$')})
       for ix2 in range(len(reports)):
          record = {}
          record['author'] = author
          record['uid'] = uuid.uuid1()
          try:
              record['date'] = re.sub(r'^.*[ ]{1,}([^ ]+)[ ]{1,}([^ ]+)[ ]{1,}([^ ]+) *$', r'\1 \2 \3', reports[ix2].find_parent('p').text)
          except:
              record['date'] = ""

          record['pdf_url'] = reports[ix2].get('href')
          record['pdf_title'] = reports[ix2].text
          record['source_article_title'] = article_title
          record['source_article_url'] = article_url
          try:
              scraperwiki.sqlite.save(['uid'], record, table_name='fas_secrecy')
              print record
          except:
              print (record,"FAILED")
    IDX += 1
    sleep(1)
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byuid ON fas_secrecy (`uid`)')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON fas_secrecy (`pdf_title`)')
scraperwiki.sqlite.execute('ANALYZE')
scraperwiki.sqlite.commit()

########## Congressional Research Service Scrape ############

# scraperwiki.sqlite.execute('DROP TABLE IF EXISTS fas_crs;')
# scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS fas_crs ( `uid` TEXT PRIMARY KEY, `pdf_title` TEXT, `pdf_url` TEXT UNIQUE,  `date` INTEGER, `author` TEXT, `source_article_title` TEXT, `source_article_url` TEXT);')
# pdf_title = []
# pdf_url = []
# year = []
# author = []
# author = "Congressional Research Service"
# ## Step 1 - find links to each article from 20 pages of article archives.
# BASE_URL = "http://www.fas.org/blog/secrecy/category/crs/page/"
# IDX = 1
# 
# while IDX < 21:
#     if IDX == 1:
#         URL = "http://www.fas.org/blog/secrecy/category/crs/"
#     else:
#         URL = "http://www.fas.org/blog/secrecy/category/crs/" + 'page/' +  str(IDX)
#     response = urllib2.urlopen(URL)
#     html = response.read()
#     soup = BeautifulSoup(html)
#     articles = soup.findAll('h3',attrs={"id": re.compile("post")})
# ## step 2 - traverse each article, grabbing pdf links + metadata
#     for ix in range(len(articles)):
#        article_url = articles[ix].a.get('href')
#        article_title = articles[ix].a.text
#        response = urllib2.urlopen(article_url)
#        html = response.read()
#        soup = BeautifulSoup(html)
#        reports = soup.body.find('div',attrs={"class":"post"}).findAll('a',attrs={"href": re.compile(r'^.*\.pdf$')})
#        for ix2 in range(len(reports)):
#           record = {}
#           record['author'] = author
#           record['uid'] = uuid.uuid1()
#           try:
#               record['date'] = re.sub(r'^.*[ ]{1,}([^ ]+)[ ]{1,}([^ ]+)[ ]{1,}([^ ]+) *$', r'\1 \2 \3', reports[ix2].find_parent('p').text)
#           except:
#               record['date'] = ""
# 
#           record['pdf_url'] = reports[ix2].get('href')
#           record['pdf_title'] = reports[ix2].text
#           record['source_article_title'] = article_title
#           record['source_article_url'] = article_url
#           try:
#               scraperwiki.sqlite.save(['uid'], record, table_name='fas_crs')
#               print record
#           except:
#               print (record,"FAILED")
#     IDX += 1
#     sleep(1)
# scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byuid ON fas_crs (`uid`)')
# scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON fas_crs (`pdf_title`)')
# scraperwiki.sqlite.execute('ANALYZE')
# scraperwiki.sqlite.commit()