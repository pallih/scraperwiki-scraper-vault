#!/usr/bin/env python
from urllib2 import urlopen
from lxml.html import fromstring
from re import sub
from scraperwiki.sqlite import save,select, show_tables
from time import sleep

URLS={
  "SCRAPERS":'https://scraperwiki.com/browse/scrapers/'
, "VIEWS":'https://scraperwiki.com/browse/views/'
}
XPATHS={
  "_PAGECONTENT":'id("divContent")/div[@class="content"]'
}
XPATHS.update({
  "URLS":XPATHS['_PAGECONTENT'] \
  + '/ul[@class="scraper_list"]/li[@class="code_object_line"]' \
  + '/h3/a[not(@class)]'
, "PAGE":XPATHS['_PAGECONTENT'] \
  + '/div[@class="pagination"]/span[@class="step_links"]/' \
  + '/span[@class="current"]'
})

def main():
  go(1,"SCRAPERS")
  go(1,"VIEWS")

def go(number=1,pagetype="SCRAPERS"):
  foo=scrapepage(number,pagetype)
  is_end=('scraper_urls' in show_tables()) and (foo['lasturl'] in select('url from scraper_urls'))
  #Save after checking whether it's the end because that's how I check.
  save(['url'],foo['scraper_urls'],'scraper_urls')

  if foo['lastpage']:
    #End when we reach the last page
    print "I scraped all the scrapers!"
  elif is_end:
    #End when we reach page where a scraper has already been scraped
    print "I scraped all of the new scrapers!"
  else:
    go(number+1,pagetype)

def scrapepage(number,pagetype):
  xml=pull(page_url(number,pagetype))
  lastpage=is_last_page(xml)
  if lastpage:
    print "This is the last page."
  scraper_urls=[{"url":a.attrib['href']} for a in xml.xpath(XPATHS['URLS'])]
  return {
    "lastpage":lastpage
  , "scraper_urls":scraper_urls
  , "lasturl":scraper_urls[-1]
  }

#----

def is_last_page(xml):
  """Check whether it's the last page"""
  page_string=xml.xpath(XPATHS['PAGE'])[0].text
  print page_string
  current_page,last_page=[sub(r'[^0-9]*','',t) for t in page_string.split(' of ')]
  return current_page==last_page

def page_url(number,pagetype):
  return URLS[pagetype]+str(number)

def pull(url):
  try:
    raw=urlopen(url).read()
  except:
    #Try again
    sleep(60)
    raw=urlopen(url).read()
  return fromstring(raw)

main()