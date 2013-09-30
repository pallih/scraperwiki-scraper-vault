#!/usr/bin/env python
"""Get a list of node ids, which correspond to urls."""

from urllib2 import urlopen, URLError, HTTPError
from lxml.html import fromstring
from time import time, sleep
from scraperwiki.sqlite import save,attach,select

BASEURL='http://www.saonm.org/nodes/view/'
FANCYCHARS=(':','\n')

class ServerBroke(Exception):
  pass

def main():
  try:
    go()
  except ServerBroke:
    print "The server broke."

def go():
  attach('new_mexico_state_audits')
  nodeIds=[row['nodeId'] for row in select('nodeId from nodeIds')]
  scraped_nodeIds=[row['nodeId'] for row in select('nodeId from opinions order by time_scraped')] #So you get different information from consecutive partial runs.
  for nodeId in scraped_nodeIds:
    nodeIds.remove(nodeId)
  if len(nodeIds)==0:
    nodeIds=scraped_nodeIds
  for nodeId in nodeIds:
    print 'Scraping node '+nodeId
    parse(nodeId)

def parse(nodeId):
  url=url_from_id(nodeId)
  xml=get(url)
  opinion={
    "nodeId":nodeId
  , "time_scraped":time()
  }
  if is_wrong_page(xml):
    #raise ServerBroke
    opinion['Opinion']='error'
    save([],opinion,'opinions')
    return None
  else:
    auditId,district=xml.xpath('//div[@id="copy"]/h1')[0].text.split(' - ')[0:2]
    #Remove junk
    keys=[clean_key(key.text) for key in xml.xpath('//div[@id="copy"]/div/div/strong')[:-1]]
    values_text=[clean_key(s) for s in xml.xpath('//div[@id="copy"]/div/div/text()')]
    value_a=xml.xpath('//div[@id="copy"]/div/div/a')[0].text

    audit={
      "nodeId":nodeId
    , "auditId":auditId
    , "district":district
    , keys[0]:values_text[1].replace('\n','')
    , keys[2]:values_text[3].replace('\n','')
    }
    opinion[keys[1]]=value_a.replace('\n','')
    save(['nodeId'],audit,'audits')
    save([],opinion,'opinions')

def get(url,xml=True):
  try:
    html=urlopen(url).read()
  except URLError, HTTPError:
#    try:
#      html=urlopen(url).read()
#    except:
      return None
  if xml:
    return fromstring(html)
  else:
    return html

def clean_key(s):
  for c in FANCYCHARS:
    s=s.replace(c,'')
  return s

def url_from_id(nodeId):
  return BASEURL+nodeId

def is_wrong_page(xml):
  if xml==None:
    return True
  else:
    return 'Home | New Mexico Office of the State Auditor'==xml.xpath('//title/text()')[0] or 'Sorry, you reached a page that does not exist.'==xml.xpath('id("int-content")/p/text()')[0]

main()#!/usr/bin/env python
"""Get a list of node ids, which correspond to urls."""

from urllib2 import urlopen, URLError, HTTPError
from lxml.html import fromstring
from time import time, sleep
from scraperwiki.sqlite import save,attach,select

BASEURL='http://www.saonm.org/nodes/view/'
FANCYCHARS=(':','\n')

class ServerBroke(Exception):
  pass

def main():
  try:
    go()
  except ServerBroke:
    print "The server broke."

def go():
  attach('new_mexico_state_audits')
  nodeIds=[row['nodeId'] for row in select('nodeId from nodeIds')]
  scraped_nodeIds=[row['nodeId'] for row in select('nodeId from opinions order by time_scraped')] #So you get different information from consecutive partial runs.
  for nodeId in scraped_nodeIds:
    nodeIds.remove(nodeId)
  if len(nodeIds)==0:
    nodeIds=scraped_nodeIds
  for nodeId in nodeIds:
    print 'Scraping node '+nodeId
    parse(nodeId)

def parse(nodeId):
  url=url_from_id(nodeId)
  xml=get(url)
  opinion={
    "nodeId":nodeId
  , "time_scraped":time()
  }
  if is_wrong_page(xml):
    #raise ServerBroke
    opinion['Opinion']='error'
    save([],opinion,'opinions')
    return None
  else:
    auditId,district=xml.xpath('//div[@id="copy"]/h1')[0].text.split(' - ')[0:2]
    #Remove junk
    keys=[clean_key(key.text) for key in xml.xpath('//div[@id="copy"]/div/div/strong')[:-1]]
    values_text=[clean_key(s) for s in xml.xpath('//div[@id="copy"]/div/div/text()')]
    value_a=xml.xpath('//div[@id="copy"]/div/div/a')[0].text

    audit={
      "nodeId":nodeId
    , "auditId":auditId
    , "district":district
    , keys[0]:values_text[1].replace('\n','')
    , keys[2]:values_text[3].replace('\n','')
    }
    opinion[keys[1]]=value_a.replace('\n','')
    save(['nodeId'],audit,'audits')
    save([],opinion,'opinions')

def get(url,xml=True):
  try:
    html=urlopen(url).read()
  except URLError, HTTPError:
#    try:
#      html=urlopen(url).read()
#    except:
      return None
  if xml:
    return fromstring(html)
  else:
    return html

def clean_key(s):
  for c in FANCYCHARS:
    s=s.replace(c,'')
  return s

def url_from_id(nodeId):
  return BASEURL+nodeId

def is_wrong_page(xml):
  if xml==None:
    return True
  else:
    return 'Home | New Mexico Office of the State Auditor'==xml.xpath('//title/text()')[0] or 'Sorry, you reached a page that does not exist.'==xml.xpath('id("int-content")/p/text()')[0]

main()