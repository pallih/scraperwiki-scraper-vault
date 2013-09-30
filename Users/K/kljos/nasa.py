import scraperwiki
import urllib2, urllib
import re, os
import sqlite3
import uuid
import contextlib
from bs4 import *
import lxml
import unicodedata
import base64
from time import sleep

###


# #scraperwiki.sqlite.execute('DROP TABLE IF EXISTS nasa;')
# scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS nasa (`article_url` TEXT PRIMARY KEY, `article_title` TEXT,  `article_date` TEXT, `article_image` TEXT, `image_caption` TEXT, `article_keywords` TEXT, `parent_page_url` TEXT,  `instrument_title` TEXT, `article_contents` BLOB, `credit` TEXT );')
# ###
# baseUrl = "http://earthobservatory.nasa.gov/IOTD/index.php?"
# ###
# year = 2009
# while year <= 2013:
#    if year == 2009:
#       minRange = 2
#    else:
#       minRange = 1
#    for month in range(minRange,12):
#       url = baseUrl + "m=" + str(month) + "&y=" + str(year)
#       with contextlib.closing(urllib2.urlopen(url)) as x:
#          html = x.read()
#       soup = BeautifulSoup(html)
#       grid = soup.find('div',attrs={"class":"grid-mid"})
#       articles = grid.findAll('a')
#       for ix in range(len(articles)):
#          record = {}
#          record['parent_page_url'] = url
#          article_url = articles[ix].get('href')
#          date_str = articles[ix].parent.get_text()
#          record['article_date'] = re.sub('^\n{0,}([^ \n]+)[ ]{1,}([^ ,\n]+),*[ ]{1,}([0-9]{4,4})\n.*$', r'\1 \2, \3', date_str).replace('\n', '')
#          with contextlib.closing(urllib2.urlopen("http://earthobservatory.nasa.gov/IOTD/" + article_url)) as x:
#             html = x.read()
#          soup = BeautifulSoup(html)
#          record['article_url'] = "http://earthobservatory.nasa.gov/IOTD/" + article_url
#          record['article_title'] = soup.title.text.replace('\n|\r', '').replace(' : Image of the Day','')
#          record['article_keywords'] = ""
#          if soup.dd != None and soup.dl.dd != None:
#             record['instrument_title'] = soup.dl.dd.text.replace('\n|\r', '')
#          else:
#              record['instrument_title'] = ""
#          if soup.find('p',attrs={"class":"credit"}) != None:
#             record['credit'] = soup.find('p',attrs={"class":"credit"}).text.replace('\n|\r', '')
#          else:
#              record['credit'] = ""
#          record['article_contents'] = soup.find('div',attrs={"class": "stnd-desc globalimages"}).get_text()
#          record['article_image'] = soup.find('div',attrs={"class":"headimage-detail"}).img.get('src')
#          record['image_caption'] = soup.find('div',attrs={"class":"headimage-detail"}).img.get('alt')
#          try:
#             scraperwiki.sqlite.execute('INSERT OR IGNORE into nasa values( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(record['article_url'], record['article_title'], record['article_date'], record['article_image'], record['image_caption'],record['article_keywords'], record['parent_page_url'], record['instrument_title'], record['article_contents'], record['credit']))
#             scraperwiki.sqlite.commit()
#          except:
#             print("fail")
#          sleep(0.5)
#    year += 1
# scraperwiki.sqlite.execute('CREATE UNIQUE INDEX IF NOT EXISTS uqurl ON nasa (`article_url`)')
# scraperwiki.sqlite.execute('ANALYZE')
# scraperwiki.sqlite.commit()
#scraperwiki.sqlite.execute("ALTER TABLE `nasa` DROP COLUMN image;")
#scraperwiki.sqlite.execute("ALTER TABLE `nasa` ADD COLUMN `image_64` BLOB;")
#scraperwiki.sqlite.execute('DROP TABLE IF EXISTS `nasa_images`')

##
##scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS nasa_images (`article_url` TEXT PRIMARY KEY, `article_title` TEXT,  `article_date` TEXT, `article_image` TEXT, `image_caption` TEXT, `article_keywords` TEXT, `parent_page_url` TEXT,  `instrument_title` TEXT, `article_contents` BLOB, `credit` TEXT, `image_64` BLOB);')
##
##records = scraperwiki.sqlite.select("* from `nasa`")
##for i in range(len(scraperwiki.sqlite.select("article_url,article_image from `nasa`"))):
##    image_url = records[i]['article_image']
##    article_url = records[i]['article_url']
##    image = urllib.urlopen(image_url)
##    records[i]['image_64'] = base64.encodestring(image.read())
##    try:
##        scraperwiki.sqlite.save(['article_url'], records[i], table_name='nasa_images')
##    except:
##        print ("record already exists")

# 
# 
# records = scraperwiki.sqlite.select("article_url from `nasa_images`")
# print len(records)
# for i in range(len(records)):
#     scraperwiki.sqlite.execute("update nasa_images set  `article_title` = CAST(TRIM(replace(replace(CAST(`article_title` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `article_date` = CAST(TRIM(replace(replace(CAST(`article_date` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `article_image` = CAST(TRIM(replace(replace(CAST(`article_image` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `image_caption` = CAST(TRIM(replace(replace(CAST(`image_caption` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `article_keywords` = CAST(TRIM(replace(replace(CAST(`article_keywords` as BLOB), X'0A',' '), X'0D', ''), ' ' ) AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `parent_page_url` = CAST(TRIM(replace(replace(CAST(`parent_page_url` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `instrument_title` = CAST(TRIM(replace(replace(CAST(`instrument_title` as BLOB), X'0A',' '), X'0D', ''), ' ')  AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `article_contents` = CAST(TRIM(replace(replace(CAST(`article_contents` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `credit` = CAST(TRIM(replace(replace(CAST(`credit` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     
#     scraperwiki.sqlite.commit()

scraperwiki.sqlite.execute('CREATE UNIQUE INDEX IF NOT EXISTS uqurl ON nasa_images (`article_url`)')
scraperwiki.sqlite.execute('ANALYZE nasa_images')
#scraperwiki.sqlite.commit()
#scraperwiki.sqlite.execute("create virtual table `snasa_images` using fts3 (`article_url`, `article_contents`, `article_title`);")
#scraperwiki.sqlite.commit()
#scraperwiki.sqlite.execute("insert into `snasa_images` select `article_url`, `article_contents`, `article_title` from nasa_images;")
#scraperwiki.sqlite.commit()import scraperwiki
import urllib2, urllib
import re, os
import sqlite3
import uuid
import contextlib
from bs4 import *
import lxml
import unicodedata
import base64
from time import sleep

###


# #scraperwiki.sqlite.execute('DROP TABLE IF EXISTS nasa;')
# scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS nasa (`article_url` TEXT PRIMARY KEY, `article_title` TEXT,  `article_date` TEXT, `article_image` TEXT, `image_caption` TEXT, `article_keywords` TEXT, `parent_page_url` TEXT,  `instrument_title` TEXT, `article_contents` BLOB, `credit` TEXT );')
# ###
# baseUrl = "http://earthobservatory.nasa.gov/IOTD/index.php?"
# ###
# year = 2009
# while year <= 2013:
#    if year == 2009:
#       minRange = 2
#    else:
#       minRange = 1
#    for month in range(minRange,12):
#       url = baseUrl + "m=" + str(month) + "&y=" + str(year)
#       with contextlib.closing(urllib2.urlopen(url)) as x:
#          html = x.read()
#       soup = BeautifulSoup(html)
#       grid = soup.find('div',attrs={"class":"grid-mid"})
#       articles = grid.findAll('a')
#       for ix in range(len(articles)):
#          record = {}
#          record['parent_page_url'] = url
#          article_url = articles[ix].get('href')
#          date_str = articles[ix].parent.get_text()
#          record['article_date'] = re.sub('^\n{0,}([^ \n]+)[ ]{1,}([^ ,\n]+),*[ ]{1,}([0-9]{4,4})\n.*$', r'\1 \2, \3', date_str).replace('\n', '')
#          with contextlib.closing(urllib2.urlopen("http://earthobservatory.nasa.gov/IOTD/" + article_url)) as x:
#             html = x.read()
#          soup = BeautifulSoup(html)
#          record['article_url'] = "http://earthobservatory.nasa.gov/IOTD/" + article_url
#          record['article_title'] = soup.title.text.replace('\n|\r', '').replace(' : Image of the Day','')
#          record['article_keywords'] = ""
#          if soup.dd != None and soup.dl.dd != None:
#             record['instrument_title'] = soup.dl.dd.text.replace('\n|\r', '')
#          else:
#              record['instrument_title'] = ""
#          if soup.find('p',attrs={"class":"credit"}) != None:
#             record['credit'] = soup.find('p',attrs={"class":"credit"}).text.replace('\n|\r', '')
#          else:
#              record['credit'] = ""
#          record['article_contents'] = soup.find('div',attrs={"class": "stnd-desc globalimages"}).get_text()
#          record['article_image'] = soup.find('div',attrs={"class":"headimage-detail"}).img.get('src')
#          record['image_caption'] = soup.find('div',attrs={"class":"headimage-detail"}).img.get('alt')
#          try:
#             scraperwiki.sqlite.execute('INSERT OR IGNORE into nasa values( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(record['article_url'], record['article_title'], record['article_date'], record['article_image'], record['image_caption'],record['article_keywords'], record['parent_page_url'], record['instrument_title'], record['article_contents'], record['credit']))
#             scraperwiki.sqlite.commit()
#          except:
#             print("fail")
#          sleep(0.5)
#    year += 1
# scraperwiki.sqlite.execute('CREATE UNIQUE INDEX IF NOT EXISTS uqurl ON nasa (`article_url`)')
# scraperwiki.sqlite.execute('ANALYZE')
# scraperwiki.sqlite.commit()
#scraperwiki.sqlite.execute("ALTER TABLE `nasa` DROP COLUMN image;")
#scraperwiki.sqlite.execute("ALTER TABLE `nasa` ADD COLUMN `image_64` BLOB;")
#scraperwiki.sqlite.execute('DROP TABLE IF EXISTS `nasa_images`')

##
##scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS nasa_images (`article_url` TEXT PRIMARY KEY, `article_title` TEXT,  `article_date` TEXT, `article_image` TEXT, `image_caption` TEXT, `article_keywords` TEXT, `parent_page_url` TEXT,  `instrument_title` TEXT, `article_contents` BLOB, `credit` TEXT, `image_64` BLOB);')
##
##records = scraperwiki.sqlite.select("* from `nasa`")
##for i in range(len(scraperwiki.sqlite.select("article_url,article_image from `nasa`"))):
##    image_url = records[i]['article_image']
##    article_url = records[i]['article_url']
##    image = urllib.urlopen(image_url)
##    records[i]['image_64'] = base64.encodestring(image.read())
##    try:
##        scraperwiki.sqlite.save(['article_url'], records[i], table_name='nasa_images')
##    except:
##        print ("record already exists")

# 
# 
# records = scraperwiki.sqlite.select("article_url from `nasa_images`")
# print len(records)
# for i in range(len(records)):
#     scraperwiki.sqlite.execute("update nasa_images set  `article_title` = CAST(TRIM(replace(replace(CAST(`article_title` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `article_date` = CAST(TRIM(replace(replace(CAST(`article_date` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `article_image` = CAST(TRIM(replace(replace(CAST(`article_image` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `image_caption` = CAST(TRIM(replace(replace(CAST(`image_caption` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `article_keywords` = CAST(TRIM(replace(replace(CAST(`article_keywords` as BLOB), X'0A',' '), X'0D', ''), ' ' ) AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `parent_page_url` = CAST(TRIM(replace(replace(CAST(`parent_page_url` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `instrument_title` = CAST(TRIM(replace(replace(CAST(`instrument_title` as BLOB), X'0A',' '), X'0D', ''), ' ')  AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `article_contents` = CAST(TRIM(replace(replace(CAST(`article_contents` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     scraperwiki.sqlite.execute("update nasa_images set  `credit` = CAST(TRIM(replace(replace(CAST(`credit` as BLOB), X'0A',' '), X'0D', ''), ' ') AS TEXT) where `article_url` = ?;", (str(records[i]['article_url'])))
#     
#     scraperwiki.sqlite.commit()

scraperwiki.sqlite.execute('CREATE UNIQUE INDEX IF NOT EXISTS uqurl ON nasa_images (`article_url`)')
scraperwiki.sqlite.execute('ANALYZE nasa_images')
#scraperwiki.sqlite.commit()
#scraperwiki.sqlite.execute("create virtual table `snasa_images` using fts3 (`article_url`, `article_contents`, `article_title`);")
#scraperwiki.sqlite.commit()
#scraperwiki.sqlite.execute("insert into `snasa_images` select `article_url`, `article_contents`, `article_title` from nasa_images;")
#scraperwiki.sqlite.commit()