#!/usr/bin/env python
from urllib2 import urlopen
from lxml.html import fromstring
from lxml.etree import tostring
from re import sub

import scraperwiki

region_codes=["BB","BE","BW","BY","HB","HE","HH","MV","NI","NW","RP","SH","SL","SN","ST","TH"]

def schoolurl(mouseover):
  return (sub(r'>.*$','',sub(r'^[^=]*=','',mouseover)))

def scrape(url):
  raw=urlopen(url).read()
  xml=fromstring(raw)
  table=[td.text for td in xml.xpath('//table')[0].xpath('//td[@colspan="2"]')]
  d={'url':url}
  for raw in table:
     if raw!=None:
       row=raw.replace(u'\xa0','').split(': ')
       if len(row)==2:
         key,value=row
         d[key.encode('ascii')]=value

  return d

schools=[]
notschools=[]

#Get urls
for region_code in region_codes:
  raw=urlopen('http://www.klimaschutzschulenatlas.de/Klimaschutzschulen/yFrameWork/Maps/_Karte_BL.asp?BL='+region_code).read()
  xml=fromstring(raw)
  carte=xml.get_element_by_id('ifKarte')
  for school in carte.getchildren():
    try:
      schools.append(schoolurl(school.attrib['onmouseover']))
    except:
      notschools.append(school.attrib)

#Scrape and save
for url in schools:
  try:
    data=scrape(url)
    data['fail']=False
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)
  except:
    try:
      scraperwiki.sqlite.save(unique_keys=['url'], data={'url':url,'error':True})
    except:
      print 'Something is really wrong with '+url