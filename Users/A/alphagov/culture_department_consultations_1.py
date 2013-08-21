import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from datetime import date
import random
import time
import urllib

base_url = 'http://www.culture.gov.uk/consultations/default.aspx'

consultation_ids=[7759,7760,7887,7720,6596,7437,7449,7459,7806,7313,7363,7825,7070,6773,6743,6744,6740,7036,6651,6564]
min_consultation_id = 6564
max_consultation_id = 7888

def findConsultations():
  #for i in range(min_consultation_id ,max_consultation_id ):
  for i in consultation_ids:
    try:
      if i==7036:
        continue
      if i==6564:
        special_scrape('http://www.culture.gov.uk/consultations/' + str(i) + '.aspx')
      else:
        
        scrapeConsultation('http://www.culture.gov.uk/consultations/' + str(i) + '.aspx')
    except:
      None
      #Do nothing
    time.sleep(random.uniform(1,3))

def special_scrape(url):
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  published_date = datetime.strptime(str(soup.find('meta',{'name':'DC.date.created'})['content']),'%Y-%m-%d %H:%M')
  container = soup.find('div',{'id':'contentcolumn'})
  print(url)
  record = {}
  record['URI'] = url
  record['agency'] = ''
  record['sponsor'] = ''
  record['department'] = 'Department for Culture, Media and Sport'
  c_title = container.find('h1').text
  div = container.find('div',{'class':'introtext'})
  start_date, end_date = getDates(div.text)
  ps = div.findNextSiblings('p')
  c_description = str(ps[0]) + str(ps[1])

  record['title'] = c_title
  record['description'] = c_description
  record['published_date'] = published_date 
  #hard-coded values for 6564
  record['start_date'] = date(2010,1,7)
  record['end_date'] = date(2010,4,1)

  scraperwiki.sqlite.save(['URI'], data=record, table_name='consultations')

def scrapeConsultation(url):
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  container = soup.find('div',{'id':'contentcolumn'})
  print(url)
  record = {}
  record['URI'] = url
  record['agency'] = ''
  record['sponsor'] = ''
  record['department'] = 'Department for Culture, Media and Sport'

  c_title = container.find('h1',{'property':'dc:title'}).text
  c_description = container.find('div',{'property':'dc:abstract'})
  c_issued = datetime.strptime(str(container.find('span',{'property':'dc:issued'})['content']),'%Y-%m-%d')
  c_available = datetime.strptime(str(container.find('span',{'property':'dc:available'})['content']),'%Y-%m-%d')
  c_valid = datetime.strptime(str(container.find('span',{'property':'dc:valid'})['content']),'%Y-%m-%d')

  record['title'] = c_title
  record['description'] = c_description
  record['start_date'] = c_available
  record['end_date'] = c_valid
  record['published_date'] = c_issued
  scraperwiki.sqlite.save(['URI'], data=record, table_name='consultations')
  for doc in container.findAll('a',{'rel':'dc:hasPart'}):
    document = {}
    document['consultation'] = url
    c_d_title = doc.text
    c_d_url = 'http://www.culture.gov.uk' + doc['href']
    c_d_type, c_d_size = doc_parse(str(doc.nextSibling).strip())
    document['URI'] = c_d_url
    document['title'] = c_d_title
    document['size'] = c_d_size
    document['type'] = c_d_type
    scraperwiki.sqlite.save(['URI'], data=document, table_name='documents')

def doc_parse(s):
  s = s[s.find('(')+1:-1]
  i = s.find(' ')
  return s[:i], s[i+1:]

example_url = 'http://www.culture.gov.uk/consultations/6564.aspx'
wrong_url= 'http://www.culture.gov.uk/consultations/6565.aspx'
#specialScrape(example_url)
findConsultations()

