###
#philly funguide scraper, scrapes the rss feeds for classes of events
#
#TODO:
#needs to be cleaned up
#figure out better way to distinguish schemes for the item nodes
#optimize so we dont reread redundant data
#clean up parsing
###

import scraperwiki
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import NavigableString
from BeautifulSoup import Tag

BASE_STRING = "http://www.phillyfunguide.com/feeds/event/rss/"

#maps to get the correct titles for the schemas
DESCRIPTION_MAP_13 = {'title':0 , 'dates':1, 'link':4, 'address':5, 'admission':6, 'phone':8, 'email':9, 'times':11, 'desc':12}
DESCRIPTION_MAP_12 = {'title':0 , 'dates':1, 'link':4, 'address':3, 'admission':5, 'phone':7, 'email':8, 'times':10, 'desc':11}
DESCRIPTIONS = DESCRIPTION_MAP_12.keys()
DESCRIPTIONS.extend(['link','title','guide','type'])
#stripSurrounding tags
def getString(tag):
  s = str(tag)
  if(s.find('[CDATA[')>=0 and s.find(']]') >=0 ):
    return s[s.find('[CDATA[')+7:s.find(']]') ]
  return None

def splitDesc(desc):
  desc = desc[desc.find('<dd'):]
  ret = [];
  pos = desc.find('<dd>')
  while not pos  == -1:
    close = desc.find('</dd>')
    ret.append(desc[pos+4: close])
    desc=desc[close+5:]
    pos = desc.find('<dd>')
  ret.append(desc)
  return ret  

def parseItem(item):
  record = dict()
  link=getString(item.find('guid')) 
  title=getString(item.find('title'))
  desc=getString(item.find('description'))
  descArr=splitDesc(desc)
  record['guide']=link
  record['title']=title
  if len(descArr) == 13:
    for key in DESCRIPTION_MAP_13:
      record[key]=descArr[DESCRIPTION_MAP_13[key]]
      
  elif len(descArr) == 12:
    for key in DESCRIPTION_MAP_12:
      record[key]=descArr[DESCRIPTION_MAP_12[key]]
      
  else:
     print 'unknown schema'
     for key in DESCRIPTION_MAP_12:
       record[key] = 'none'
  return record

def parseRSS(i):
  string = BASE_STRING + str(i)
  try:
    html = scraperwiki.scrape(string)
  except:
    print('could not connect')
    return
    
  soup = BeautifulSoup(html)


  items = soup.findAll('item')
  for item in items:
    record = parseItem(item)
    record['type'] = getString(soup.find('title'))
    scraperwiki.sqlite.save(DESCRIPTIONS,record)

#parse each all of the feeds
for i in range(2,13):
  parseRSS(i)###
#philly funguide scraper, scrapes the rss feeds for classes of events
#
#TODO:
#needs to be cleaned up
#figure out better way to distinguish schemes for the item nodes
#optimize so we dont reread redundant data
#clean up parsing
###

import scraperwiki
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import NavigableString
from BeautifulSoup import Tag

BASE_STRING = "http://www.phillyfunguide.com/feeds/event/rss/"

#maps to get the correct titles for the schemas
DESCRIPTION_MAP_13 = {'title':0 , 'dates':1, 'link':4, 'address':5, 'admission':6, 'phone':8, 'email':9, 'times':11, 'desc':12}
DESCRIPTION_MAP_12 = {'title':0 , 'dates':1, 'link':4, 'address':3, 'admission':5, 'phone':7, 'email':8, 'times':10, 'desc':11}
DESCRIPTIONS = DESCRIPTION_MAP_12.keys()
DESCRIPTIONS.extend(['link','title','guide','type'])
#stripSurrounding tags
def getString(tag):
  s = str(tag)
  if(s.find('[CDATA[')>=0 and s.find(']]') >=0 ):
    return s[s.find('[CDATA[')+7:s.find(']]') ]
  return None

def splitDesc(desc):
  desc = desc[desc.find('<dd'):]
  ret = [];
  pos = desc.find('<dd>')
  while not pos  == -1:
    close = desc.find('</dd>')
    ret.append(desc[pos+4: close])
    desc=desc[close+5:]
    pos = desc.find('<dd>')
  ret.append(desc)
  return ret  

def parseItem(item):
  record = dict()
  link=getString(item.find('guid')) 
  title=getString(item.find('title'))
  desc=getString(item.find('description'))
  descArr=splitDesc(desc)
  record['guide']=link
  record['title']=title
  if len(descArr) == 13:
    for key in DESCRIPTION_MAP_13:
      record[key]=descArr[DESCRIPTION_MAP_13[key]]
      
  elif len(descArr) == 12:
    for key in DESCRIPTION_MAP_12:
      record[key]=descArr[DESCRIPTION_MAP_12[key]]
      
  else:
     print 'unknown schema'
     for key in DESCRIPTION_MAP_12:
       record[key] = 'none'
  return record

def parseRSS(i):
  string = BASE_STRING + str(i)
  try:
    html = scraperwiki.scrape(string)
  except:
    print('could not connect')
    return
    
  soup = BeautifulSoup(html)


  items = soup.findAll('item')
  for item in items:
    record = parseItem(item)
    record['type'] = getString(soup.find('title'))
    scraperwiki.sqlite.save(DESCRIPTIONS,record)

#parse each all of the feeds
for i in range(2,13):
  parseRSS(i)