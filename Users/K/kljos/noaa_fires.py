import scraperwiki
import urllib2, urllib
import re, os
import sqlite3
import uuid
import contextlib
from bs4 import *
import lxml
import unicodedata
from time import sleep
import scraperwiki

import csv         
url = "http://www.ngdc.noaa.gov/dmsp/data/viirs_fire/viirs-ir-sources-20120901.csv"
base_url = "http://www.ngdc.noaa.gov/dmsp/data/viirs_fire/"


scraperwiki.sqlite.execute('DROP TABLE IF EXISTS noaa_scraped;')
scraperwiki.sqlite.execute('DROP TABLE IF EXISTS swdata;')
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS noaa_scraped (`url` TEXT PRIMARY KEY);')
with contextlib.closing(urllib.urlopen(base_url)) as x:
    html = x.read()
soup = BeautifulSoup(html)
table = soup.body.find('div',attrs={"id":"main_text"}).table
rows = table.find_all('tr')
for x in range(8,len(rows)):
    if rows[x].find(href=re.compile('\.csv')) != None:
        data_stub_url = rows[x].find(href=re.compile('\.csv'))
        data_url = data_stub_url['href']
        results = scraperwiki.sqlite.execute('SELECT url from noaa_scraped WHERE url = ( ? )',(data_url))
        if len(results['data']) == 0:
            scraperwiki.sqlite.save(unique_keys=['url'], data={"url":data_url}, table_name="noaa_scraped",verbose=2)   
            data = scraperwiki.scrape(base_url + data_url)
            reader = csv.DictReader(data.splitlines())
            for row in reader:
                row['ID']=uuid.uuid1()
                scraperwiki.sqlite.save(unique_keys=['ID'], data=row)
        scraperwiki.sqlite.commit()