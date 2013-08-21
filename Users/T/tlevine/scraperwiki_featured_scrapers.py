#!/usr/bin/env python
"""Scraperwiki featured scrapers"""

from urllib2 import urlopen
from lxml.html import fromstring
from scraperwiki.sqlite import save,select,show_tables
import base64
import re
from time import time,sleep
from copy import copy

URL='https://scraperwiki.com'
PATH='id("page_inner")/div[@class="featured"]/ul/li[not(@class)]'

def parse(url,xml=None,suffix=''):
  if xml==None:
    xml=pull(url)
  print "Loading the page"
  scrapers=xml.xpath(PATH)
  for scraper in scrapers:
    if 'observations' in show_tables():
      observation_id=select('max(observation_id) as id from observations')[0]['id']+1
    else:
      observation_id=1
    identifiers={"observation_id":observation_id}
    info=copy(identifiers)
    screenshot_identity=copy(identifiers)

    identifiers['time_scraped']=time()
    identifiers['url']=scraper.xpath('a')[0].attrib['href']

    print "Extracting metadata"
    info['owner'],info['title']=scraper.xpath('a/h4')[0].text.split('/',1)
    info['language'],info['type']=re.split(r'[^a-zA-Z]+',scraper.xpath('a/span[@class="about"]')[0].text)
    info['created']=scraper.xpath('a/span[@class="when"]')[0].text

    screenshot_identity['url']=scraper.xpath('a/img')[0].attrib['src']
    print "Checking whether I've already saved the screenshot"
    exists,image=check_identical_screenshot(getimage(screenshot_identity['url']))
    if exists:
      #If I have, don't do anything with theimage
      print "Screenshot already saved"
    else:
      #If I haven't, save a new image
      print "Saving the new screenshot"
      image['observation_scraped_on']=observation_id
      save(['observation_scraped_on','screenshot_id'],image,'images')

    #Either way, link the observation to the saved image
    screenshot_identity['screenshot_id']=image['screenshot_id']
    save(['observation_id'],screenshot_identity,'screenshot_identidies')

    #Save these at the end to avoid partial rows
    print "Saving"
    save(['observation_id'],info,'homepage_metadata')
    save(['observation_id'],identifiers,'observations')

#---------
def check_identical_screenshot(image_base64):
  """Check whether there's an identical screenshot already saved"""

  #If,else to handle new tables
  if 'images' in show_tables():
    identical_screenshot=select('screenshot_id from images where image="'+image_base64+'" limit 1')
  else:
    identical_screenshot=[]

  if len(identical_screenshot)==0:
    #No identical screenshot
    if 'images' in show_tables():
      screenshot_id=select('max(screenshot_id) as id from images')[0]['id']+1
    else:
      screenshot_id=1
    return (False,{
      "screenshot_id":screenshot_id
    , "image":image_base64
    })
  elif len(identical_screenshot)==1:
    return (True,identical_screenshot[0])
      

def getimage(url):
  return base64.encodestring(urlopen(url).read())

def pull(url):
  try:
    raw=urlopen(url).read()
  except:
    sleep(60)
    raw=urlopen(url).read()
  return fromstring(raw)

parse(URL)