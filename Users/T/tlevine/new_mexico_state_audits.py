#!/usr/bin/env python
from urllib2 import urlopen
from lxml.html import fromstring
from datetime import datetime
from time import time
from scraperwiki.sqlite import save,select

START_YEAR=1998
BASEURL='http://www.saonm.org/nodes/view/'

def main():
  #Remove previously searched urls
  nodeIds=select('nodeId from nodeIds')
  for url in searchurls():
    parse(url,nodeIds)

def parse(url,nodeIds):
  xml=get(url)
  for a in xml.xpath('//div[@class="profile-container"]/div[@class="node-body"]/a'):
    nodeId=a.attrib['href'].split('/')[-1]
    if nodeId in nodeIds:
      #Remove it to speed up future runs
      nodeIds.pop(nodeId)
    else:
      #Add it to the database
      d={
        "nodeId":nodeId
      , "first_scraped":time()
      }
      save(['nodeId'],d,'nodeIds')

def searchurls():
  return [resulturl(year) for year in range(START_YEAR,datetime.now().year+1)]

def resulturl(year):
  return 'http://www.saonm.org/nodes/advanced_search/year:%s' % str(year)

def get(url,xml=True):
  html=urlopen(url).read()
  if xml:
    return fromstring(html)
  else:
    return html

main()