from lxml.html import fromstring
from urllib2 import urlopen
from time import time
import re

from scraperwiki.sqlite import save, select
from scraperwiki import swimport
randomsleep=swimport('randomsleep').randomsleep

DATE=time()
DOMAIN="http://www.bk.rw"
STARTURL="http://www.bk.rw/index.php?option=com_content&view=article&id=54&Itemid=57"

def download():
  url=STARTURL
  d=[]
  while url!=None:
    a=Article(url)
    d.extend(a.parse())
    url=a.next()
    randomsleep()
  save(['date-scraped','branch-number'],d,'raw')

class MultipleNextButtons(Exception):
  pass

class Article:
  def __init__(self,url):
    self.url=url
    self.x=fromstring(urlopen(url).read())

  def is_branchlist(self):
    pass

  def paragraphs(self):
    return self.x.xpath('//div[@class="article"]/p')

  def cast(self):
    return reduce(self.cast_one,self.paragraphs(),[])

  def parse(self):
    d=self.cast()
    for row in d:
      row['date-scraped']=DATE
      row['url']=self.url
    return d

  @staticmethod
  def cast_one(data,p):
    if 1==p.xpath('count(descendant::strong)'):
      m=re.match(r'^([ 0-9]+)\.',p.text_content())
      branch_number=int(m.group(1))
      data.append({"branch-number":branch_number,"contact-info":""})
    if len(data)>0:
      data[-1]['contact-info']+=p.text_content()+'\n'
    return data

  def next(self):
    hrefs=self.x.xpath('//a[text()="NEXT >>" or text()="NEXT>>" or strong[text()=" NEXT >>"]]/@href')
    if 1==len(hrefs):
      return DOMAIN+hrefs[0]
    elif 0==len(hrefs):
      return None
    else:
      raise MultipleNextLinks

def parse():
  d = select('* from raw')
  for row in d:
    lines = row['contact-info'].split('Email')[0].split('\n')
    row['town'] = re.findall(r'[A-Z]+', lines[0])[0]
    for cell in lines:
      if 'B.P' == cell[0:3]:
        row['street-address'] = cell
      elif 'Email' in cell:
        row['email'] = cell
      elif 'Mob' in cell:
        row['mob'] = cell
      elif 'Phone' in cell:
        row['phone'] = cell
      else:
        print cell
  save(['date-scraped','branch-number'],d,'parsed')

download()
parse()from lxml.html import fromstring
from urllib2 import urlopen
from time import time
import re

from scraperwiki.sqlite import save, select
from scraperwiki import swimport
randomsleep=swimport('randomsleep').randomsleep

DATE=time()
DOMAIN="http://www.bk.rw"
STARTURL="http://www.bk.rw/index.php?option=com_content&view=article&id=54&Itemid=57"

def download():
  url=STARTURL
  d=[]
  while url!=None:
    a=Article(url)
    d.extend(a.parse())
    url=a.next()
    randomsleep()
  save(['date-scraped','branch-number'],d,'raw')

class MultipleNextButtons(Exception):
  pass

class Article:
  def __init__(self,url):
    self.url=url
    self.x=fromstring(urlopen(url).read())

  def is_branchlist(self):
    pass

  def paragraphs(self):
    return self.x.xpath('//div[@class="article"]/p')

  def cast(self):
    return reduce(self.cast_one,self.paragraphs(),[])

  def parse(self):
    d=self.cast()
    for row in d:
      row['date-scraped']=DATE
      row['url']=self.url
    return d

  @staticmethod
  def cast_one(data,p):
    if 1==p.xpath('count(descendant::strong)'):
      m=re.match(r'^([ 0-9]+)\.',p.text_content())
      branch_number=int(m.group(1))
      data.append({"branch-number":branch_number,"contact-info":""})
    if len(data)>0:
      data[-1]['contact-info']+=p.text_content()+'\n'
    return data

  def next(self):
    hrefs=self.x.xpath('//a[text()="NEXT >>" or text()="NEXT>>" or strong[text()=" NEXT >>"]]/@href')
    if 1==len(hrefs):
      return DOMAIN+hrefs[0]
    elif 0==len(hrefs):
      return None
    else:
      raise MultipleNextLinks

def parse():
  d = select('* from raw')
  for row in d:
    lines = row['contact-info'].split('Email')[0].split('\n')
    row['town'] = re.findall(r'[A-Z]+', lines[0])[0]
    for cell in lines:
      if 'B.P' == cell[0:3]:
        row['street-address'] = cell
      elif 'Email' in cell:
        row['email'] = cell
      elif 'Mob' in cell:
        row['mob'] = cell
      elif 'Phone' in cell:
        row['phone'] = cell
      else:
        print cell
  save(['date-scraped','branch-number'],d,'parsed')

download()
parse()