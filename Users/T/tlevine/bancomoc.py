#!/usr/bin/env python
from urllib2 import urlopen
from lxml.html import fromstring
from lxml.etree import tostring
import scraperwiki

def url(num):
  return 'http://www.bancomoc.mz/Instituicoes_en.aspx?id=GINS00%02d&ling=en' % (num)

def main():
  for num in range(1,30):
    if num in load_finished():
      print 'Already scraped page %02d' % (num)
      continue
    xml=get(url(num))
    organization_type=xml.get_element_by_id('ctl00_ContentPlaceHolder1_LblTitulo').text
    if organization_type=="Label":
      print 'Nothing at page %02d' % (num)
      mark_finished(num)
      continue
    organizations=xml.xpath('//div[@class="column1-unit"]/h1/div/span/b/font')
    addresses=xml.xpath('//div[@class="column1-unit"]/h1/div/span/font')
    if len(organizations)!=len(addresses):
      raise AlignmentError
    print 'Scraping page %02d' % (num)
    while len(organizations)>0:
      row={
        "organization":tostring(organizations.pop()).split('<br/>')[1]
      , "pagenum":num
      , "type":organization_type
      , "address":addresses.pop().text
      }
      scraperwiki.sqlite.save(['organization'],row,'banconmoc')
    mark_finished(num)

class AlignmentError(Exception):
  pass

def get(url):
  raw=urlopen(url).read()
  return fromstring(raw)

def mark_finished(num):
  finishedOld=scraperwiki.sqlite.get_var('finished_pages')
  if finishedOld==None:
    finishedNew=str(num)
  else:
    finishedNew=finishedOld+','+str(num)
  scraperwiki.sqlite.save_var('finished_pages',finishedNew)

def load_finished():
  finished=scraperwiki.sqlite.get_var('finished_pages')
  if finished==None:
    return []
  else:
    return [int(s) for s in finished.split(',')]

main()#!/usr/bin/env python
from urllib2 import urlopen
from lxml.html import fromstring
from lxml.etree import tostring
import scraperwiki

def url(num):
  return 'http://www.bancomoc.mz/Instituicoes_en.aspx?id=GINS00%02d&ling=en' % (num)

def main():
  for num in range(1,30):
    if num in load_finished():
      print 'Already scraped page %02d' % (num)
      continue
    xml=get(url(num))
    organization_type=xml.get_element_by_id('ctl00_ContentPlaceHolder1_LblTitulo').text
    if organization_type=="Label":
      print 'Nothing at page %02d' % (num)
      mark_finished(num)
      continue
    organizations=xml.xpath('//div[@class="column1-unit"]/h1/div/span/b/font')
    addresses=xml.xpath('//div[@class="column1-unit"]/h1/div/span/font')
    if len(organizations)!=len(addresses):
      raise AlignmentError
    print 'Scraping page %02d' % (num)
    while len(organizations)>0:
      row={
        "organization":tostring(organizations.pop()).split('<br/>')[1]
      , "pagenum":num
      , "type":organization_type
      , "address":addresses.pop().text
      }
      scraperwiki.sqlite.save(['organization'],row,'banconmoc')
    mark_finished(num)

class AlignmentError(Exception):
  pass

def get(url):
  raw=urlopen(url).read()
  return fromstring(raw)

def mark_finished(num):
  finishedOld=scraperwiki.sqlite.get_var('finished_pages')
  if finishedOld==None:
    finishedNew=str(num)
  else:
    finishedNew=finishedOld+','+str(num)
  scraperwiki.sqlite.save_var('finished_pages',finishedNew)

def load_finished():
  finished=scraperwiki.sqlite.get_var('finished_pages')
  if finished==None:
    return []
  else:
    return [int(s) for s in finished.split(',')]

main()