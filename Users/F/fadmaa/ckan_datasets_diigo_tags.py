import scraperwiki

import urllib2, urllib
import simplejson
from BeautifulSoup import BeautifulSoup
import re, time, random

datahub_base_url = "http://thedatahub.org/api/rest/dataset"
datasets_url = "http://thedatahub.org/api/search/dataset"
diigo_base_url = "http://www.diigo.com/search?" 

def get_diigo_tags(url):
  diigo_tags = ''
  #get rid of http://
  lookfor_url = url[len('http://'):]
  if lookfor_url[-1]=='/':
    lookfor_url = lookfor_url[0:-1]
  print lookfor_url
  params = {'adSScope':'community', 'what':lookfor_url}
  diiog_url = diigo_base_url + urllib.urlencode(params)
  html = scraperwiki.scrape(diiog_url)
  soup = BeautifulSoup(html)
  #introcude some pause not to overwhelm sites (and get banned)
  time.sleep(random.uniform(1,3))
  main_div = soup.find('div',{'id':'main'})
  if main_div.find('div',{'class':'noDitems'}):
    #no tags on Diigo for this dataset
    pass
  else:
    for div in main_div.find('div',{'id':'leftColumn'}).findAll('div',id=re.compile("^ditemItem_\\d")):
      #this is a result div, see if the URL matches
      candidate_url = div.find('p',{'class':'tags'}).find('span',{'class':'oriURL'}).text
      if candidate_url == lookfor_url:
        #get the tags
        for a in div.find('p',{'class':'tagspan'}).find('span',id=re.compile("^tags_\\d")).findAll('a'):
          diigo_tags += a.text + ' '
  return diigo_tags
  

req = urllib2.Request(datasets_url,urllib.urlencode({'q':'lod','limit':'1000'}))
resp = urllib2.urlopen(req)
datasets = simplejson.loads(resp.read())
for d in datasets['results']:
  #get tags from thedatahub.org
  d_url = datahub_base_url + '/'+ d
  d_resp = urllib2.urlopen(d_url)
  ds = simplejson.loads(d_resp.read())
  ckan_tags = ds['tags']
  url = ds['url']
  author = ds['author']
  author_email = ds['author_email']
  license_id = ds['license_id']
  license = ds['license']
  if not url:
    continue
  scraperwiki.sqlite.save(["url","id"], {"url":url,"id":d,"author":author,"author_email":author_email,"license":license,"license_id":license_id})
  continue
  #get tags from Diigo
  diigo_tags = ''
  try:
    diigo_tags = get_diigo_tags(url)
  except Exception as e:
    print 'failed with ' + url
    print e
    pass
  #scraperwiki.sqlite.save(["url","id"], {"url":url,"id":d,"tags":ckan_tags,"diigo_tags":diigo_tags})import scraperwiki

import urllib2, urllib
import simplejson
from BeautifulSoup import BeautifulSoup
import re, time, random

datahub_base_url = "http://thedatahub.org/api/rest/dataset"
datasets_url = "http://thedatahub.org/api/search/dataset"
diigo_base_url = "http://www.diigo.com/search?" 

def get_diigo_tags(url):
  diigo_tags = ''
  #get rid of http://
  lookfor_url = url[len('http://'):]
  if lookfor_url[-1]=='/':
    lookfor_url = lookfor_url[0:-1]
  print lookfor_url
  params = {'adSScope':'community', 'what':lookfor_url}
  diiog_url = diigo_base_url + urllib.urlencode(params)
  html = scraperwiki.scrape(diiog_url)
  soup = BeautifulSoup(html)
  #introcude some pause not to overwhelm sites (and get banned)
  time.sleep(random.uniform(1,3))
  main_div = soup.find('div',{'id':'main'})
  if main_div.find('div',{'class':'noDitems'}):
    #no tags on Diigo for this dataset
    pass
  else:
    for div in main_div.find('div',{'id':'leftColumn'}).findAll('div',id=re.compile("^ditemItem_\\d")):
      #this is a result div, see if the URL matches
      candidate_url = div.find('p',{'class':'tags'}).find('span',{'class':'oriURL'}).text
      if candidate_url == lookfor_url:
        #get the tags
        for a in div.find('p',{'class':'tagspan'}).find('span',id=re.compile("^tags_\\d")).findAll('a'):
          diigo_tags += a.text + ' '
  return diigo_tags
  

req = urllib2.Request(datasets_url,urllib.urlencode({'q':'lod','limit':'1000'}))
resp = urllib2.urlopen(req)
datasets = simplejson.loads(resp.read())
for d in datasets['results']:
  #get tags from thedatahub.org
  d_url = datahub_base_url + '/'+ d
  d_resp = urllib2.urlopen(d_url)
  ds = simplejson.loads(d_resp.read())
  ckan_tags = ds['tags']
  url = ds['url']
  author = ds['author']
  author_email = ds['author_email']
  license_id = ds['license_id']
  license = ds['license']
  if not url:
    continue
  scraperwiki.sqlite.save(["url","id"], {"url":url,"id":d,"author":author,"author_email":author_email,"license":license,"license_id":license_id})
  continue
  #get tags from Diigo
  diigo_tags = ''
  try:
    diigo_tags = get_diigo_tags(url)
  except Exception as e:
    print 'failed with ' + url
    print e
    pass
  #scraperwiki.sqlite.save(["url","id"], {"url":url,"id":d,"tags":ckan_tags,"diigo_tags":diigo_tags})