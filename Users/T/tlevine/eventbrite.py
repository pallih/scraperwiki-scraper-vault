from scraperwiki.sqlite import save,select,show_tables
from urllib import urlopen
from lxml.html import fromstring
from re import sub
from time import time


def scrape(url,table_name="swdata", how_many = 10000):
  listurl=attendeelisturl(url)
  d=getattendeelist(listurl)
  d = getattendeelist(listurl + '&show_more=%d&sortid=0' % how_many)

  if table_name in show_tables():
    scraped_so_far=select('count(*) as "c" from `%s`'%table_name)[0]['c']
    saveattendeelist(d[0:-scraped_so_far],table_name)
  else:
    saveattendeelist(d,table_name)

# -----------------------------

def attendeelisturl(url):
  "Get the url of the attendee list from the event main page."
  html=urlopen(url).read()
  url_noslash=sub(r'/$','',url)
  eid_qs=sub(r'.*(eid=[0-9]*)[^0-9].*$',r'\1',html.replace('\n',''))
  return '%s/attendee-list-more?%s' % (url_noslash,eid_qs)

def getattendeelist(url):
  html=urlopen(url).read()
  xml=fromstring(html)
  rows=xml.xpath('//li')

  d=[]
  for row in rows:
    keys=[sub(r'[^a-zA-Z]*$','',sub(r'^\s*','',key)) for key in row.xpath('text()[position()>1]')]
    values=row.xpath('b/text()')
    d.append(dict(zip(keys,values)))
  return d

def saveattendeelist(d,table_name):
  for row in d:
    row["first_scraped"]=time()
  save([],d,table_name)
from scraperwiki.sqlite import save,select,show_tables
from urllib import urlopen
from lxml.html import fromstring
from re import sub
from time import time


def scrape(url,table_name="swdata", how_many = 10000):
  listurl=attendeelisturl(url)
  d=getattendeelist(listurl)
  d = getattendeelist(listurl + '&show_more=%d&sortid=0' % how_many)

  if table_name in show_tables():
    scraped_so_far=select('count(*) as "c" from `%s`'%table_name)[0]['c']
    saveattendeelist(d[0:-scraped_so_far],table_name)
  else:
    saveattendeelist(d,table_name)

# -----------------------------

def attendeelisturl(url):
  "Get the url of the attendee list from the event main page."
  html=urlopen(url).read()
  url_noslash=sub(r'/$','',url)
  eid_qs=sub(r'.*(eid=[0-9]*)[^0-9].*$',r'\1',html.replace('\n',''))
  return '%s/attendee-list-more?%s' % (url_noslash,eid_qs)

def getattendeelist(url):
  html=urlopen(url).read()
  xml=fromstring(html)
  rows=xml.xpath('//li')

  d=[]
  for row in rows:
    keys=[sub(r'[^a-zA-Z]*$','',sub(r'^\s*','',key)) for key in row.xpath('text()[position()>1]')]
    values=row.xpath('b/text()')
    d.append(dict(zip(keys,values)))
  return d

def saveattendeelist(d,table_name):
  for row in d:
    row["first_scraped"]=time()
  save([],d,table_name)
