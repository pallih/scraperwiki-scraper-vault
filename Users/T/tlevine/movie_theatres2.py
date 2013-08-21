#!/usr/bin/env python
from urllib2 import urlopen,HTTPError
from httplib import BadStatusLine
from lxml.html.soupparser import fromstring
from lxml.etree import tostring
from re import sub
from BeautifulSoup import BeautifulSoup
from demjson import decode
from scraperwiki.sqlite import save, get_var, save_var, commit, execute, select, show_tables
from time import sleep
from copy import copy

HTTPERROR_WAIT=30 #How long to wait on an HttpError
INTERVAL=0
URLS = {
  'ct-base':'http://cinematreasures.org/theaters?page='
, 'ct-domain':'http://cinematreasures.org'
}

def main():
  #finalpage=get_var('finalpage')
  prevpage=get_var('prevpage')

  #if None==finalpage:
  if True:
    finalpage=int(get_lastpage(getpage(1)))
    save_var('finalpage',finalpage)
  if None==prevpage:
    prevpage=1

  if prevpage<finalpage:
    step1(prevpage,finalpage)
  elif prevpage==finalpage:
    if not "step2completion" in show_tables():
      execute('create table `step2completion` (`url` text, `browsed` boolean)')
      execute("""
        INSERT INTO `step2completion`
        ( url , browsed )
        SELECT url, 0 as "browsed"
        FROM locations
        """)
      commit()
    step2()

def step1(prevpage,finalpage):
  for page in range(prevpage,finalpage+1):
    try:
      theaters_in=get_theaters(page)
    except BadStatusLine:
      url=URLS["ct-base"]+str(page)
      save(['url'],{"url":url,"scrape_error":'BadStatusLine'},'errors')
      continue

    theatres_out=[]
    for theater in theaters_in:
      info=theater_info(theater)
      info=clean_info(info)
      theatres_out.append(info2dictRow(info,page))

    save(['url'],theatres_out,'locations')
    sleep(INTERVAL)
    save_var('prevpage',page)

def step2():
  urls=[row['url'] for row in select('url from step2completion where browsed=0 limit 1456')] #That seems to be near the CPU-time limit
  for url in urls:
    save_sidebar(url)
    #Then update step2completion
    execute('UPDATE step2completion SET browsed=1 WHERE url=?',url)

def save_sidebar(url):
  """Get more information by visiting a theatre's particular page."""
  try:
    xml=getpage(url)
  except BadStatusLine:
    save(['url'],{"url":url,"scrape_error":"BadStatusLine"},'errors')
  else:
    sidebar_query=xml.xpath('id("stats")')
    if len(sidebar_query)!=1:
      save(['url'],{"url":url,"scrape_error":"No sidebar"},'errors')
    else:
      sidebar=copy(sidebar_query[0])
      for div in sidebar.xpath('div'):
        sidebar.remove(div)
      save(["url"],{"url":url,"sidebar":tostring(sidebar)},'sidebars')

def additional_info(url):
  """Doesn't work yet"""
#  sidebar=xml.xpath('id("stats")/div[@class="adsense"]/following-sibling::*/text()')
  for info in zip(key,value,infolink):
    save([],{
      "url":url
    , "key":info[0]
    , "value":info[1]
    , "infolink":info[2]
    },'additional_info')

def remove_tags(html):
  s= '\n'.join(BeautifulSoup(html).findAll(text=True))
  #print s
  return s

def get_lastpage(xml):
  pagination=xml.xpath('//div[@class="pagination"]/a')
  lastpage=1
  count=len(pagination)
  if count!=0:
    lastpage=pagination[count-2].text #Second-to-last link
  return lastpage

GETPAGE_URL_TYPES=(
  type('http://cinematreasures.org/theaters/23789')
, type(u'http://cinematreasures.org/theaters/23789')
)
MAX_RETRIES=2

def handle_weird_page(url,retries):
  if retries>=MAX_RETRIES:
    save(['url'],{"url":url,"scrape_error":'HTTPError'},'errors')
  else:
    print 'The webpage is being strange. Let\'s wait and try again.' #'
    sleep(HTTPERROR_WAIT)
    #Try again
    getpage(url,retries+1)

def getpage(page_or_url,retries=0):
  if type(page_or_url) in GETPAGE_URL_TYPES:
    url=page_or_url
  elif type(23789)==type(page_or_url):
    page=str(page_or_url)
    url=URLS["ct-base"]+page
  else:
    raise TypeError('getpage takes a url string or a page number.')

  try:
    text=urlopen(url).read()
    #urlopen('http://aoeusatohesuthasoeuthsateousaotehu.com') #Testing HTTPError
  except HTTPError:
    handle_weird_page(url,retries)
  else:
    xml=fromstring(text)
  return xml

def get_theaters(page):
  xml=getpage(page)
  theaters=xml.xpath(
    "//tr[@class='location odd theater']"
  + "|//tr[@class='even location theater']"
  )
  return theaters


def theater_info(tr):
  info={}
  info['name']=tr.xpath('td/a[@class="map-link"]')[1].text
  info['url']=URLS['ct-domain']+tr.xpath('td/a[@class="map-link"]')[1].attrib['href']
  placemark=decode(tr.attrib['data'])['point']
  info['lat']=placemark['lat']
  info['lng']=placemark['lng']
  info['contact']=tostring(tr.xpath(
    'td[@class="name"]/div[@class="info-box"]/p'
  )[0])
  for baz in ['location','status','screens']:
    info[baz]=tr.xpath('td[@class="'+baz+'"]')[0].text
  return info

def clean_info(info):
  """Remove tabs so I can use a tab-delimited file."""
  for key in info.keys():
    if isinstance(info[key],str):
      info[key]=info[key].replace('\n','')
      info[key]=info[key].replace('\t','')
      info[key]=remove_tags(info[key])
  return info

def info2dictRow(info,page):
    info['page']=page
    return info

main()
#step1(1077,1078)
#execute('drop table `step2completion`')
#execute('drop table `additional_info`')
#save_sidebar('http://cinematreasures.org/theaters/23789')
#save_sidebar('http://cinematreasures.org/theaters/2389')

