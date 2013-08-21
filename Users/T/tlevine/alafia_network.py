#!/usr/bin/env python
from urllib2 import urlopen
from lxml.html import fromstring
from lxml.etree import tostring
from scraperwiki.sqlite import save

BASEURL='http://www.alafianetwork.org/repimf.php?page='

def main():
  for page in range(0,lastpage()):
    xml=getpage(page)
    p=xml.xpath('//p[font/strong]')[0]
    d={
      "page":page
    , "table":tostring(p)
    }
    save(['page'],d,'html')

def lastpage():
  xml=getpage(0)
  return int(xml.xpath('//center/a')[-2].text)

def get(url,xml=True):
  html=urlopen(url).read()
  if xml:
    return fromstring(html)
  else:
    return html

def getpage(number,xml=True):
  return get(BASEURL+str(number),xml)

main()
