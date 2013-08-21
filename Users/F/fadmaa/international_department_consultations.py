import scraperwiki
import time 
import random
from datetime import datetime


baseUrl = 'http://www.dfid.gov.uk/Working-with-DFID/Consultations/Closed-consultation/'

from BeautifulSoup import BeautifulSoup

def findConsultations():
  html = scraperwiki.scrape(baseUrl)
  soup = BeautifulSoup(html)
  hrs = soup.find('div',{'class':'notabstext'}).findAll('hr')
  for hr in hrs:
    ps = hr.findNextSiblings('p')
    if ps!=None:
      link = ps[0].find('a')
      if link!=None:
        url = 'http://www.dfid.gov.uk' + link['href']
        scrapeConsultation(url) 
        time.sleep(random.uniform(1,3))

def scrapeConsultation(url):
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  container = soup.find('div',{'class':'main_content'})
  c_title = container.find('h1',{'property':'dc:title'})
  c_description = container.find('div',{'property':'dc:abstract'})
  c_end_date = datetime.strptime(str(container.find('span',{'property':'dc:valid'})['content']),'%Y-%m-%d')
  c_start_date = datetime.strptime(str(container.find('span',{'property':'dc:issued'})['content']),'%Y-%m-%d')

  record = {}
  record['URI'] = url
  record['agency'] = ''
  record['sponsor'] = ''
  record['department'] = 'Department for International Development'

  record['title'] = c_title
  record['description'] = c_description
  record['start_date'] = c_start_date
  record['end_date'] = c_end_date
  record['published_date'] = c_start_date
  #related docs
  c_link = container.find('a',{'rel':'dc:hasPart'})
  if c_link:
    document = {}
    doc_url = 'http://www.dfid.gov.uk' + c_link['href']
    document['consultation'] = url
    document['URI'] = doc_url
    document['title'] = c_link.text
    document['type'] = 'HTML'
    document['size'] = ''
    scraperwiki.sqlite.save(['URI'], data=document, table_name='documents')
    try:
      getMoreDocuments(doc_url,url)
    except:
      None

  scraperwiki.sqlite.save(['URI'], data=record, table_name='consultations')

def getMoreDocuments(url,c_url):
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  container = soup.find('div',{'class':'right'})
  if container.find('h2').text.strip()=='More information':
    for elem in container.find('div',{'class':'panel_content'}).findAll('li'):
      document = {}
      document['consultation'] = c_url
      a = elem.find('a')
      d_a_url = a['href'] if a['href'].startswith('http://') else 'http://www.dfid.gov.uk' + a['href']
      document['URI'] = d_a_url
      document['title'] = a.contents[0]
      if elem['class']=='external':
        document['type'] = 'HTML'
        document['size'] = ''
      else:
        d_type,d_size = getDocInfo(a.find('span').text)
        document['type'] = d_type
        document['size'] = d_size
      scraperwiki.sqlite.save(['URI'], data=document, table_name='documents')

def getDocInfo(s):
  s = s.strip()
  s = s[s.find('[')+1:-1]
  i = s.find('-')
  d_type = s[0:i].strip()
  d_size = s[i+1:].strip()
  return d_type, d_size

example_url = 'http://www.dfid.gov.uk/Working-with-DFID/Consultations/CDC/'
#scrapeConsultation(example_url)
#getMoreDocuments('http://www.dfid.gov.uk/Media-Room/News-Stories/2010/Online-consultation-on-innovation-and-economic-growth-in-poor-countries/','')
findConsultations()
