#!/usr/bin/env python
"""Download postsecret images"""

from urllib2 import urlopen
from lxml.html import fromstring
from scraperwiki.sqlite import save,select,NoSuchTableSqliteError,get_var,save_var
import base64

URL='http://www.postsecret.com'
WAYBACK_URL=get_var('wayback_url')


#End imports
#-----------

def wayback(url):
  """Download from the wayback machine."""
  xml=pull(url)
  try:
    parse(url,xml,suffix='_wayback')
    url=xml.xpath('//a[img[@src="http://staticweb.archive.org/images/toolbar/wm_tb_prv_on.png"]]')[0].attrib['href']
    print url
    wayback(url)
  except:
    save_var('wayback_url',url)

def parse(url,xml=None,suffix=''):
  if xml==None:
    xml=pull(url)
  sunday=xml.xpath('//h2[@class="date-header"]')[0].text

  twosided=xml.xpath('//div[@class="flipit"]/a[@onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"]')

  #Get the postcards
  postcards=xml.xpath('//div[@class="flipit"]/a[@onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"][2]')
  for postcard in xml.xpath('//a[@onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"]'):
    if not postcard in twosided:
      postcards.append(postcard)

  for a in postcards:
    if not 'bp.blogspot.com' in a.attrib['href']:
      #Not a postcard
      break

    save(["url","image"],image(a.attrib['href']),"images"+suffix)

    if _isTwosided(a):
      url2=a.getprevious().attrib['href']
      save(["url","image"],image(url2),"images"+suffix)
      save(["url1","url2"]
      , meta(a,sunday,url2=url2)
      , "postcards"+suffix)

    else:
      save(["url1"]
      , meta(a,sunday)
      , "postcards"+suffix)

#---------

def _isTwosided(a):
  div=a.getparent()
  if div.attrib.has_key('class') and div.attrib['class']=='flipit': # and a.getprevious().attrib.has_key('href'):
    return True
  else:
    return False

def meta(a,sunday,url2=None):
  m={
    "shortname":a.attrib['href'].split('/')[-1].split('.')[0]
  , "sunday":sunday
  , "url1":a.attrib['href']
  }
  if url2!=None:
    m["url2"]=url2
  return m

def image(url):
  return {
    "url":url
  , "image": base64.encodestring(urlopen(url).read())
  }

def pull(url):
  raw=urlopen(url).read()
  return fromstring(raw)

parse(URL)
wayback(WAYBACK_URL)#!/usr/bin/env python
"""Download postsecret images"""

from urllib2 import urlopen
from lxml.html import fromstring
from scraperwiki.sqlite import save,select,NoSuchTableSqliteError,get_var,save_var
import base64

URL='http://www.postsecret.com'
WAYBACK_URL=get_var('wayback_url')


#End imports
#-----------

def wayback(url):
  """Download from the wayback machine."""
  xml=pull(url)
  try:
    parse(url,xml,suffix='_wayback')
    url=xml.xpath('//a[img[@src="http://staticweb.archive.org/images/toolbar/wm_tb_prv_on.png"]]')[0].attrib['href']
    print url
    wayback(url)
  except:
    save_var('wayback_url',url)

def parse(url,xml=None,suffix=''):
  if xml==None:
    xml=pull(url)
  sunday=xml.xpath('//h2[@class="date-header"]')[0].text

  twosided=xml.xpath('//div[@class="flipit"]/a[@onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"]')

  #Get the postcards
  postcards=xml.xpath('//div[@class="flipit"]/a[@onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"][2]')
  for postcard in xml.xpath('//a[@onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"]'):
    if not postcard in twosided:
      postcards.append(postcard)

  for a in postcards:
    if not 'bp.blogspot.com' in a.attrib['href']:
      #Not a postcard
      break

    save(["url","image"],image(a.attrib['href']),"images"+suffix)

    if _isTwosided(a):
      url2=a.getprevious().attrib['href']
      save(["url","image"],image(url2),"images"+suffix)
      save(["url1","url2"]
      , meta(a,sunday,url2=url2)
      , "postcards"+suffix)

    else:
      save(["url1"]
      , meta(a,sunday)
      , "postcards"+suffix)

#---------

def _isTwosided(a):
  div=a.getparent()
  if div.attrib.has_key('class') and div.attrib['class']=='flipit': # and a.getprevious().attrib.has_key('href'):
    return True
  else:
    return False

def meta(a,sunday,url2=None):
  m={
    "shortname":a.attrib['href'].split('/')[-1].split('.')[0]
  , "sunday":sunday
  , "url1":a.attrib['href']
  }
  if url2!=None:
    m["url2"]=url2
  return m

def image(url):
  return {
    "url":url
  , "image": base64.encodestring(urlopen(url).read())
  }

def pull(url):
  raw=urlopen(url).read()
  return fromstring(raw)

parse(URL)
wayback(WAYBACK_URL)