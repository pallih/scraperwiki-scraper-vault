#!/usr/bin/env python
from urllib2 import Request,urlopen
from demjson import decode
from scraperwiki.sqlite import save,select

URL='http://apps.ams.usda.gov/nop/FetchNOPData.aspx'
HEADERS={
  "Accept":"application/json, text/javascript, */*"
, "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3"
, "Accept-Encoding":"gzip,deflate,sdch"
, "Accept-Language":"en-US,en;q=0.8"
, "Connection":"keep-alive"
, "Content-Type":"application/x-www-form-urlencoded"
, "Host":"apps.ams.usda.gov"
, "Referer":"http://apps.ams.usda.gov/nop/"
, "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.102 Safari/535.2"
, "X-Requested-With":"XMLHttpRequest"
}

def main():
  rowid=int(select('max(id) as id from organic_operations')[0]['id'])
  print 'Starting on '+str(rowid+1)
  while True:
    rowid=rowid+1
    done=parse(rowid)['done']
    #Python doesn't support recursion well because it does not support tail recursion elimination
    if done:
      break

def parse(rowid):
  d=grab(rowid)
  if len(d['rows'])>0:
    row=d['rows'][0]
    row['id']=rowid
    save(['id'],row,'organic_operations')
  return {"done":d['page']>=d['records']}

def params(rows=10,page=1):
  """Return the url params string given a rows count and page number."""
  return 'searchString=&searchField=&searchOper=&_search=true&nd=1320094066485&rows=%s&page=%s&sidx=CertifyingAgent&sord=asc' % (str(rows),str(page))

def grab(rowid):
  return decode(urlopen(Request(URL,params(rows=1,page=rowid),HEADERS)).read())

main()