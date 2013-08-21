#!/usr/bin/env python2
from urllib2 import urlopen, build_opener,HTTPCookieProcessor
from lxml.html import fromstring
from httplib import BadStatusLine
from json import loads

try:
  from htmltable2matrix import htmltable2matrix
except ImportError:
  from scraperwiki.utils import swimport
  htmltable2matrix=swimport('htmltable2matrix').htmltable2matrix

from scraperwiki.sqlite import save,get_var,save_var

def main():
  if get_var('skip')==None:
    save_var('skip',0)
  routesTable=getroutes()
  for row in routesTable:
    if row['key'][0:2]!=row['key'][2:4]:
      get_route_schedules(row['id'],row['key'])

#------------------------------------------

def get_route_schedules(routeId,route):
  #Check that it's not a route within one city
  assert route[0:2]!=route[2:4]

  xml,theurl=grab(route)
  save(['routeId','url'],{
    "routeId":routeId
  , "url":theurl
  },'urls')

  try:
    table=get_table(xml)
  except:
    save([],{"url":theurl},'errors')
  else:
    d_raw=parse_table(table)
    d=[]

    for row_raw in d_raw:
      row_clean={}
      for key in row_raw:
        if key==":Route/Trip":
          row_clean['routeNum']=row_raw[key]
        else:
          foo,bar,baz=key.split(':')
          if foo=="From":
            row_clean['fromCity']=bar
            row_clean['fromStop']=baz
            row_clean['fromTime']=row_raw[key]
          elif foo=="To":
            row_clean['toCity']=bar
            row_clean['toStop']=baz
            row_clean['toTime']=row_raw[key]
      row_clean['routeId']=routeId

      if row_clean['toStop']=='megabus.com stop' and row_clean['fromStop']=='megabus.com stop':
        table_name='megabus'
      else:
        table_name='schedules'

      save([],row_clean,table_name)
    save_var('skip',get_var('skip')+1)


def getroutes():
  skip=get_var('skip')
  json=urlopen("http://coach.iriscouch.com/routes/_design/coach/_view/fullRoutes?skip=%d&limit=%d" % (skip,skip+1000)).read()
  table=loads(json)['rows']
  return table

def url(route):
  from_state,from_city,to_state,to_city=route
  return 'http://www.coachusa.com/ss.details.asp?action=Lookup&c1=%s&s1=%s&c2=%s&s2=%s' % (from_city.replace(' ','+'),from_state,to_city.replace(' ','+'),to_state)

def grab(route):
  theurl=url(route)
  opener = build_opener(HTTPCookieProcessor())

  try:
    o=opener.open(theurl)
  except BadStatusLine:
    return None,None
  else:
    xml=fromstring(o.read())
    return xml,theurl

def get_table(xml):
  table=xml.xpath('//table[tr[@class="tableHilightHeader"]]')[0]
  return table

def clean_whitespace(string):
  for ws in ('\t','\r','\n','    ','   ','  '):
    string=string.replace(ws,'')
  return string

def parse_table(table):
  head0=htmltable2matrix(table,cell_xpath='b/text()')[0]
  head1=htmltable2matrix(table,cell_xpath='descendant::img/@alt')[1]
  keys=[clean_whitespace(':'.join(col)) for col in zip(head0,head1)]

  body=htmltable2matrix(table,cell_xpath='text()')
  rows=[dict(zip(keys,row)) for row in body[2:len(body)]]
  for row in rows:
    del(row[':'])

  return rows

main()
#save_var('skip',78)