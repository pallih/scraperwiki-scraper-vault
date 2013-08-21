#!/usr/bin/env python
from urllib2 import urlopen
from csv import reader, writer
from lxml.html.soupparser import fromstring
from lxml.etree import tostring
from re import sub
from BeautifulSoup import BeautifulSoup
from demjson import decode
from scraperwiki.sqlite import save, select, attach
from time import sleep

INTERVAL=0
URLS = {
  'zips':'http://www.census.gov/tiger/tms/gazetteer/zips.txt'
, 'ct-base':'http://cinematreasures.org/theaters/united-states?'
, 'ct-domain':'http://cinematreasures.org'
}
DIRS = {
  'raws':'raw_pages/'
, 'out':'out/'
}
FILES = {
  'zips':DIRS['raws']+'zips.txt'
}

def remove_tags(html):
  s= ' / '.join(BeautifulSoup(html).findAll(text=True))
  #print s
  return s

def get_zips(source):
  zipCsv=reader(source)
  zipList=[]
  for row in zipCsv:
    #The zip code is in the second column
    zipList.append(row[1])
  return zipList

def search(zipcode,page,source='web',save=False):
  #I should really check and throw an error
  #zipcode=str(zipcode)
  #page=str(page)
  for var in [zipcode,page]:
    try:
      isinstance(var,str)
    except:
      raise TypeError

  #Load raw
  if source=='web':
    try:
      raw=urlopen(URLS['ct-base']+'page='+page+'&q='+zipcode).read()
    except:
      #If it didn't work, try again
      sleep(20)
      raw=urlopen(URLS['ct-base']+'page='+page+'&q='+zipcode).read()
  elif source=='local':
    raw=open(DIRS['raws']+zipcode+'-'+page+'.html','r').read()

  #Save
  if save:
    f=open(DIRS['raws']+zipcode+'-'+page+'.html','w')
    f.write(raw)

  #Load xml with BeautifulSoup
  xml=fromstring(raw)

  return xml

def get_lastpage_fromgap(xml):
  gap=xml.xpath('//span[@class="gap"]')
  lastpage=1
  if len(gap)!=0:
    lastpage=gap[0].getnext().getnext().text
  return lastpage

def get_lastpage_frompagination(xml):
  pagination=xml.xpath('//div[@class="pagination"]/a')
  lastpage=1
  count=len(pagination)
  if count!=0:
    lastpage=pagination[count-2].text #Second-to-last link
  return lastpage

get_lastpage=get_lastpage_frompagination

def get_theaters(zipcode,page,save=True):
  xml=search(zipcode,page,save=save)
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

def info2csvRow(csvWriter,info,zipcode):
  csvWriter.writerow([
    zipcode
  , info['name']
  , info['url']
  , info['contact']
  , info['location']
  , info['status']
  , info['screens']
  , info['lat']
  , info['lng']
  ])

def info2dictRow(info,zipcode):
    info['zipcode']=zipcode
    return info

#def info2csv(handle,info,zipcode,page):
#print theater_info(get_theaters(str(10583),str(3))[7])

def local():
  zipcode=get_zips(open(FILES['zips'],'r'))

  #Prepare the csv
  handle=open(DIRS['out']+'theaters.csv','w')
  csvWriter=writer(handle,delimiter=',',quotechar='"')
  csvWriter.writerow(['zipcode','name','url','contact','location','status','screens','lat','lng'])

  for zipcode in ['10583']:
    lastpage=get_lastpage(search(zipcode,'1'))
#    for page in [str(p) for p in range(1,lastpage+1)]:
    for page in [str(lastpage)]:
      theaters=get_theaters(zipcode,page,save=True)
      for theater in theaters:
        info=theater_info(theater)
        info=clean_info(info)
        info2csvRow(csvWriter,info,zipcode)

  handle.close()

def scraperwiki():
  #zipcodes=get_zips(urlopen(URLS['zips']))
  attach('us_zip_codes')
  zipcodes=[str(row['zip']) for row in select('zip from zipcodes')]

  #Skip zipcodes that are already finished.
  try:
    finished_zipcodes=[row['zipcode'] for row in select('zipcode from finished_zipcodes')]
  except:
    pass
  else:
    #print 'Already scraped these zipcodes:'
    for zipcode in finished_zipcodes:
      try:
        zipcodes.remove(zipcode)
      except ValueError:
        #The zipcodes database isn't complete
        pass

  for zipcode in zipcodes:
    print 'Scraping '+zipcode
    lastpage=int(get_lastpage(search(zipcode,'1',save=False)))
    for page in [str(p) for p in range(1,lastpage+1)]:
      theaters=get_theaters(zipcode,page,save=False)
      for theater in theaters:
        info=theater_info(theater)
        info=clean_info(info)
        save(['url'],info2dictRow(info,zipcode),'locations')
      sleep(INTERVAL)
    save(['zipcode'],{'zipcode':zipcode},'finished_zipcodes')

scraperwiki()
