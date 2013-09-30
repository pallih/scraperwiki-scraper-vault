import scraperwiki

from urllib2 import urlopen
from lxml.html import fromstring
from lxml.etree import tostring
from demjson import decode
from datetime import datetime
import re

if 'months' in scraperwiki.sqlite.show_tables():
  LAST=scraperwiki.sqlite.select('* from months where id=(select max(id) from months)')[0]
else:
  LAST={
    'id':0
  , 'year':2003
  , 'month':0
  }
NOW={
  "year":datetime.now().year
, "month":datetime.now().month
}
WHITESPACE=('\t','\n','\r','    ','   ','  ')
TABLE_NAMES=('sex','medium','age','motivation','spanish','foreigners')

def url(year,month):
    return 'http://peregrinossantiago.es/eng/pilgrims-office/statistics/?anio='+str(year)+'&mes='+str(month)

def get_scripts(xml):
  scripts=[]
  #Add inline scripts
  for s in xml.xpath('//script'):
    if (not s.attrib.has_key('src')) and ('serie' in s.text):
      scripts.append(s)
  return(scripts)

def clean_scripts(scripts):
  for s in scripts:
    for ws in WHITESPACE:
      s.text=s.text.replace(ws,'')
    #HTML entities
    #s.text=s.text.replace('&lt;','<').replace('&gt;','>')
    #Replace with letters for the sqlite store
    s.text=s.text.replace('&lt;','lt ').replace('&gt;','gt ')
  return scripts

def get_list(script):
  return decode(re.sub(r'<br[^\[]*','',script.text).split(';')[0].split('=')[1])

def ascii(uni):
  return uni.encode("ascii","ignore")


def lists2dict(decoded_script):
  """Converts a decoded script and a list of keys
  into a dict that can the scraperwiki api can take"""
  l=get_list(decoded_script)

  d={}
  for row in l:
    n=row[0].split('(')[0]
    if n[-1]==' ':
      n=n[:-1]
    #Handle blank names for "other"
    if n=='':
      n='Other'
    #d[n]=row[1]
    d[ascii(n)]=row[1]

  d["Total"]=sum([d[k] for k in d.keys()])
  return d

row_id=LAST['id']
for year in range(LAST['year']+1,NOW['year']+1):
  for month in range(0,NOW['month']):
    if (year == LAST['year'] and month <= LAST['month']) or (year == NOW['year'] and month > NOW['month']):
      continue
    row_id=row_id+1
    raw=urlopen(url(year,month)).read()
    xml=fromstring(raw)
    scripts=clean_scripts(get_scripts(xml))

    tables=[['months',{
      'id':row_id
    , 'year':year
    , 'month':month
    }]]
    for name in TABLE_NAMES:
      d=lists2dict(scripts.pop(0))
      d["id"]=row_id
      tables.append([name,d])

    #print tables
    for table in tables:
      name=table[0]
      data=table[1]
      scraperwiki.sqlite.save(unique_keys=['id'], data=data,table_name=name)import scraperwiki

from urllib2 import urlopen
from lxml.html import fromstring
from lxml.etree import tostring
from demjson import decode
from datetime import datetime
import re

if 'months' in scraperwiki.sqlite.show_tables():
  LAST=scraperwiki.sqlite.select('* from months where id=(select max(id) from months)')[0]
else:
  LAST={
    'id':0
  , 'year':2003
  , 'month':0
  }
NOW={
  "year":datetime.now().year
, "month":datetime.now().month
}
WHITESPACE=('\t','\n','\r','    ','   ','  ')
TABLE_NAMES=('sex','medium','age','motivation','spanish','foreigners')

def url(year,month):
    return 'http://peregrinossantiago.es/eng/pilgrims-office/statistics/?anio='+str(year)+'&mes='+str(month)

def get_scripts(xml):
  scripts=[]
  #Add inline scripts
  for s in xml.xpath('//script'):
    if (not s.attrib.has_key('src')) and ('serie' in s.text):
      scripts.append(s)
  return(scripts)

def clean_scripts(scripts):
  for s in scripts:
    for ws in WHITESPACE:
      s.text=s.text.replace(ws,'')
    #HTML entities
    #s.text=s.text.replace('&lt;','<').replace('&gt;','>')
    #Replace with letters for the sqlite store
    s.text=s.text.replace('&lt;','lt ').replace('&gt;','gt ')
  return scripts

def get_list(script):
  return decode(re.sub(r'<br[^\[]*','',script.text).split(';')[0].split('=')[1])

def ascii(uni):
  return uni.encode("ascii","ignore")


def lists2dict(decoded_script):
  """Converts a decoded script and a list of keys
  into a dict that can the scraperwiki api can take"""
  l=get_list(decoded_script)

  d={}
  for row in l:
    n=row[0].split('(')[0]
    if n[-1]==' ':
      n=n[:-1]
    #Handle blank names for "other"
    if n=='':
      n='Other'
    #d[n]=row[1]
    d[ascii(n)]=row[1]

  d["Total"]=sum([d[k] for k in d.keys()])
  return d

row_id=LAST['id']
for year in range(LAST['year']+1,NOW['year']+1):
  for month in range(0,NOW['month']):
    if (year == LAST['year'] and month <= LAST['month']) or (year == NOW['year'] and month > NOW['month']):
      continue
    row_id=row_id+1
    raw=urlopen(url(year,month)).read()
    xml=fromstring(raw)
    scripts=clean_scripts(get_scripts(xml))

    tables=[['months',{
      'id':row_id
    , 'year':year
    , 'month':month
    }]]
    for name in TABLE_NAMES:
      d=lists2dict(scripts.pop(0))
      d["id"]=row_id
      tables.append([name,d])

    #print tables
    for table in tables:
      name=table[0]
      data=table[1]
      scraperwiki.sqlite.save(unique_keys=['id'], data=data,table_name=name)