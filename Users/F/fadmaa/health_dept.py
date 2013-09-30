import scraperwiki
import re
from datetime import datetime
import time
import random

url = 'http://www.dh.gov.uk/en/MediaCentre/Speeches/index.htm'

from BeautifulSoup import BeautifulSoup

def scrapeSpeeches():
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  container = soup.find('div',{'class':'contentWrapper'}).find('div',{'class':'linksContainer'})
  for div in container.findAll('div',{'class':re.compile('itemContainer')}):
    
    speaker = div.find('h3').text
    i = speaker.find(',')
    if i==-1:
      continue
    name = speaker[0:i]
    speeches = div.find('ul',{'class':'itemLinks'}).findAll('li')
    for speech in speeches:
      record = {}
      record['dept_name'] = 'Department of Health'
      record['minister_name'] = name
      header = speech.find('a').text
      j = header.find(':')
      d = header[0:j]
      t = header[j+1:]
      given_on = datetime.strptime(d,'%d %B %Y').date() 
      where = getWhere(t)
      link = 'http://www.dh.gov.uk' + speech.find('a')['href']
      title, body = getBody(link)
      record['title'] = title
      record['body'] = body
      record['permalink'] = link
      record['given_on'] = given_on
      record['where'] = where
      scraperwiki.sqlite.save(['permalink'], record)
      time.sleep(random.uniform(1,3))
      

def getWhere(t):
  index = t.lower().find('speech at the')
  if index == -1:
    index = t.lower().find('speech to ')
  if index == -1:
    return ''
  end_pos = t.find('-')
  if end_pos==-1:
    end_pos = len(t)
  return t[index:end_pos]

def getBody(link):
  html = scraperwiki.scrape(link)
  soup = BeautifulSoup(html)
  title = soup.find('div',{'class':'introContent'}).find('h2')
  title_str = getTitle(title.text)
  dd = soup.find('div',{'class':'subContent first'})
  if dd!=None:
    body = unicode(str(dd), "utf-8")
    return title_str,body
  start_div = title.findNextSiblings('div')[0].nextSibling
  body = ''
  while start_div != None:
    body += ' ' + str(start_div)
    start_div = start_div.nextSibling
  body = unicode(body, "utf-8")
  print soup.originalEncoding
  return title_str, body

def getTitle(t):
  #hardcoded
  if t.endswith('Thursday 22 July'):
    return t[:-16]
  i = t.find('"')
  if i!=-1:
    j = t.find('"',i+1)
    return t[i+1:j]
  i = t.find("- '")
  if i!=-1:
    return t.strip()[i+3:-1]
  i = t.find(':')
  if i!=-1:
    s = t[i+1:].strip()
    if s[0]=="'":
      s = s[1:-1]
    return s
  
  return t
  
scrapeSpeeches()
#print(getTitle("""Simon Burns's speech to the Royal College of Surgeons of Edinburgh's conference "In Safe Hands: Reducing Errors in the Operating Team"Wednesday 8 December"""))
#print(getBody('http://www.dh.gov.uk/en/MediaCentre/Speeches/DH_123423')[0])
import scraperwiki
import re
from datetime import datetime
import time
import random

url = 'http://www.dh.gov.uk/en/MediaCentre/Speeches/index.htm'

from BeautifulSoup import BeautifulSoup

def scrapeSpeeches():
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  container = soup.find('div',{'class':'contentWrapper'}).find('div',{'class':'linksContainer'})
  for div in container.findAll('div',{'class':re.compile('itemContainer')}):
    
    speaker = div.find('h3').text
    i = speaker.find(',')
    if i==-1:
      continue
    name = speaker[0:i]
    speeches = div.find('ul',{'class':'itemLinks'}).findAll('li')
    for speech in speeches:
      record = {}
      record['dept_name'] = 'Department of Health'
      record['minister_name'] = name
      header = speech.find('a').text
      j = header.find(':')
      d = header[0:j]
      t = header[j+1:]
      given_on = datetime.strptime(d,'%d %B %Y').date() 
      where = getWhere(t)
      link = 'http://www.dh.gov.uk' + speech.find('a')['href']
      title, body = getBody(link)
      record['title'] = title
      record['body'] = body
      record['permalink'] = link
      record['given_on'] = given_on
      record['where'] = where
      scraperwiki.sqlite.save(['permalink'], record)
      time.sleep(random.uniform(1,3))
      

def getWhere(t):
  index = t.lower().find('speech at the')
  if index == -1:
    index = t.lower().find('speech to ')
  if index == -1:
    return ''
  end_pos = t.find('-')
  if end_pos==-1:
    end_pos = len(t)
  return t[index:end_pos]

def getBody(link):
  html = scraperwiki.scrape(link)
  soup = BeautifulSoup(html)
  title = soup.find('div',{'class':'introContent'}).find('h2')
  title_str = getTitle(title.text)
  dd = soup.find('div',{'class':'subContent first'})
  if dd!=None:
    body = unicode(str(dd), "utf-8")
    return title_str,body
  start_div = title.findNextSiblings('div')[0].nextSibling
  body = ''
  while start_div != None:
    body += ' ' + str(start_div)
    start_div = start_div.nextSibling
  body = unicode(body, "utf-8")
  print soup.originalEncoding
  return title_str, body

def getTitle(t):
  #hardcoded
  if t.endswith('Thursday 22 July'):
    return t[:-16]
  i = t.find('"')
  if i!=-1:
    j = t.find('"',i+1)
    return t[i+1:j]
  i = t.find("- '")
  if i!=-1:
    return t.strip()[i+3:-1]
  i = t.find(':')
  if i!=-1:
    s = t[i+1:].strip()
    if s[0]=="'":
      s = s[1:-1]
    return s
  
  return t
  
scrapeSpeeches()
#print(getTitle("""Simon Burns's speech to the Royal College of Surgeons of Edinburgh's conference "In Safe Hands: Reducing Errors in the Operating Team"Wednesday 8 December"""))
#print(getBody('http://www.dh.gov.uk/en/MediaCentre/Speeches/DH_123423')[0])
