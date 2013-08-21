import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import random
import time

base_url = 'http://www.food.gov.uk/consultations/'
all_urls = [base_url, 'http://www.food.gov.uk/consultations/ukwideconsults/2010/?completed=Yes',
            'http://www.food.gov.uk/consultations/consulteng/2010/?completed=Yes',
            'http://www.food.gov.uk/consultations/consultscot/2010/?completed=Yes',
            'http://www.food.gov.uk/consultations/consultwales/2010/?completed=Yes',
            'http://www.food.gov.uk/consultations/consultni/2010/?completed=Yes']

def findConsultations():
  for url in all_urls:
    print(url)
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    for div in soup.find('div',{'id':'content'}).findAll('div',{'class':'consultationsItem'}):
      c = div.find('div',{'class':'padder'})
      link = c.find('h3')
      if link!=None:
        c_url = 'http://www.food.gov.uk' + str(link.find('a')['href'])
        scrapeConsultation(c_url)
        time.sleep(random.uniform(1, 3) )

def scrapeConsultation(url):
  record = {}
  record['department'] = ''
  record['sponsor'] = ''
  record['URI'] = url
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  container = soup.find('div',{'id':'content'})
  title_container = container.findAll('div',{'class':'contentPadder'})[1]
  c_title = title_container.find('h1').text
  c_description = container.find('div',{'property':'dc:abstract'})
  c_publisher = soup.find('div',{'property':'dc:publisher'})['content']
  record['title'] =  c_title
  record['description'] = c_description
  record['agency'] = c_publisher
  dates_container = soup.find('div',{'id':'page'})
  c_issued = datetime.strptime(str(dates_container.find('span',{'property':'dc:issued'})['content']),'%Y-%m-%d')
  c_available = datetime.strptime(str(dates_container.find('span',{'property':'dc:available'})['content']),'%Y-%m-%d')
  c_valid = datetime.strptime(str(dates_container.find('span',{'property':'dc:valid'})['content']),'%Y-%m-%d')
  record['start_date'] = c_issued
  record['end_date'] = c_valid
  record['published_date'] = c_available
  c_contact_div = soup.find('div',{'typeof':'v:VCard'})
  try: c_f_name = c_contact_div.find('p',{'property':'v:fn'}).text
  except: c_f_name = ''
  try:  c_f_email = c_contact_div.find('span',{'property':'v:email'}).text
  except: c_f_email = ''
  try: c_f_address = c_contact_div.find('div',{'property':'v:adr'}).text
  except: c_f_address = ''
  try: c_f_tel = c_contact_div.find('span',{'property':'v:tel'}).text
  except: c_f_tel = ''
  try: c_f_fax = c_contact_div.find('span',{'property':'v:fax'}).text
  except: c_f_fax = ''
  record['feedback_person_name'] = c_f_name
  record['feedback_person_email'] = c_f_email
  record['feedback_person_tel'] = c_f_tel
  record['feedback_person_fax'] = c_f_fax
  record['feedback_person_address'] = c_f_address
  scraperwiki.sqlite.save(['URI'], data=record, table_name='consultations')
  
  docs = soup.find('div',{'class':'documentLinks related'})
  if docs!=None:
    for doc in docs.findAll('div',{'class':'linkItem'}):
      document = {}
      document['consultation'] = url
      div = doc.find('div',{'class':'docDownload'})
      c_d_title_container = doc.find('div',{'class':'copy doc'})
      if c_d_title_container!= None:
        c_d_title = c_d_title_container.find('a').text
        c_d_link = 'http://www.food.gov.uk' + div.find('a')['href']
        c_d_type, c_d_size = doc_parse(div.text)
        document['URI'] = c_d_link
        document['title'] = c_d_title
        document['size'] = c_d_size
        document['type'] = c_d_type
      else:
        c_d_title_container = doc.find('div',{'class':'copy'}).find('a')
        document['URI'] = 'http://www.food.gov.uk' + c_d_title_container['href']
        document['title'] = c_d_title_container.text
        document['size'] = ''
        document['type'] = ''
      scraperwiki.sqlite.save(['URI'], data=document, table_name='documents')

def doc_parse(s):
  s = s[s.find('(')+1:-1]
  i = s.find('&nbsp;')
  return s[:i], s[i+6:]

example_url = 'http://www.food.gov.uk/consultations/consultni/2011/jointconsultni'

#scrapeConsultation(example_url)
findConsultations()