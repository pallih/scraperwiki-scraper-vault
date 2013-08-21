import scraperwiki
import BeautifulSoup
from datetime import datetime
import random
import time
import urllib
import re

base_urls = ['http://www.ofgem.gov.uk/CustomPages/Pages/LiveConsultations.aspx', 'http://www.ofgem.gov.uk/CustomPages/Pages/ClosedConsultations.aspx?year=2010', 'http://www.ofgem.gov.uk/CustomPages/Pages/ClosedConsultations.aspx?year=2011']
lookup_table = {'title':'title','document&nbsp;overview':'description','publication&nbsp;date':'start_date','closing&nbsp;date':'end_date', 
            'contact&nbsp;name':'feedback_person_name','contact&nbsp;email&nbsp;address':'feedback_person_email','contact&nbsp;telephone&nbsp;number':
'feedback_person_tel', 'associated&nbsp;documents':'associated_documents'}

def special_case(key):
  return key in ['title', 'start_date', 'end_date', 'associated_documents']

def findConsultations():
  for base_url in base_urls:
    html = scraperwiki.scrape(base_url)
    soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8")
    container = soup.find('table',{'class':'docTable2'})
    first_tr = container.find('tr')
    for tr in first_tr.findNextSiblings('tr'):
      scrapeConsultation('http://www.ofgem.gov.uk' + tr.findAll('td')[1].find('a')['href'])
      time.sleep(random.uniform(1,3))
    
def scrapeConsultation(url):
  url = url.replace(' ','%20')
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8")
  container = soup.find('table',{'class':'docTable2'})
  first_tr = container.find('tr') 
  record = {}
  record['URI'] = url
  record['department'] = ''
  record['sponsor'] = ''
  record['agency'] = 'OFGEM'
  for tr in first_tr.findNextSiblings('tr'):
    key = tr.find('th').text.strip().lower()
    field_name = lookup_table.get(key)
    if field_name != None:
      if special_case(field_name):
        field_value = handle_special_case(field_name,tr,url)
      else:
        field_value = tr.find('td').text
      if field_value != None:
        record[field_name] = field_value
  #as published date is not provided I assume it is the same as start date
  record['published_date'] = record['start_date']
  scraperwiki.sqlite.save(['URI'], data=record, table_name='consultations')

def handle_special_case(key,tr,url):
  if key in ['start_date', 'end_date']:
    return datetime.strptime(str(tr.find('td').text),'%d/%m/%Y')
  elif key=='title':
    #add related document
    return parse_title(tr.find('td').text,tr.find('a')['href'],url)
  elif key=='associated_documents':
    for a in tr.find('td').findAll('a'):
      doc = {}
      doc['consultation'] = url
      doc['URI'] = str('http://www.ofgem.gov.uk') + a['href'].replace(' ','%20')
      doc['title'], doc['size'], doc['type'] = parse_doc(a.text)
      scraperwiki.sqlite.save(['URI'], data=doc, table_name='documents')
  else:
    return ''

def parse_doc(s):
  i = s.rfind('-')
  d_size = s[i+1:].strip()
  rest = s[:i]
  j = rest.find('-')
  d_title = rest[:j].strip()
  d_type = rest[j+1:].strip()
  return d_title,d_size,d_type

def parse_title(txt,doc_url,url):
  indx = txt.rfind('PDF')
  title = txt[0:indx].strip()
  title = title[0:title.rfind('-')].strip()
  size = txt[indx+5:].strip()
  print(size)
  doc = {}
  doc['consultation'] = url
  doc['URI'] = str('http://www.ofgem.gov.uk') + doc_url.replace(' ','%20')
  doc['title'] = txt
  doc['size'] = size
  doc['type'] = 'PDF'
  scraperwiki.sqlite.save(['URI'], data=doc, table_name='documents')
  return title


#example_url = 'http://www.ofgem.gov.uk/Pages/MoreInformation.aspx?file=EDFE%20Hill%20Top%20Farm%20Exemption%20Consultation.pdf&refer=Markets/WhlMkts/CompandEff/TPAccess'
#example_url ='http://www.ofgem.gov.uk/Pages/MoreInformation.aspx?file=RIIOGD1%20overview.pdf&refer=Networks/GasDistr/RIIO-GD1/ConRes'
#print(parse_title('Providing a greater role for third parties in electricity transmission: Early thinking- PDF - 817Kb',''))

#scrapeConsultation(example_url)
findConsultations()