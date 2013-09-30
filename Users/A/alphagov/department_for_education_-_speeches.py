import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import time
import random

url ='http://www.education.gov.uk/inthenews/speeches/'

def getPageNumber():
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  page_container = soup.find('div', {'class':'pagination'})
  last_page_link = page_container.findAll('a')[-2]
  last_page_number = last_page_link.find('span').nextSibling
  return int(last_page_number)

def scrapeLinks(num_of_pages):
  links = []
  for i in range(1,num_of_pages + 1):
    links.extend(scrapePage('http://www.education.gov.uk/inthenews/speeches/?page=' + str(i)))
    time.sleep(1)
  return links

def scrapePage(page_url):
  html = scraperwiki.scrape(page_url)
  soup = BeautifulSoup(html)
  links = []
  for sp in soup.find('div',{'class':'itemlist'}).findAll('li'):
    link = sp.find('h3').find('a')['href']
    links.append('http://www.education.gov.uk' + link)
  return links

def scrapeSpeech(speech_url):
  html = scraperwiki.scrape(speech_url)
  soup = BeautifulSoup(html)
  title = soup.find('div',{'class':'pagetitle'}).text
  attributes = soup.find('div',{'class':'documentattributes'}).findAll('dd')
  speaker = attributes[0].find('strong').nextSibling
  given_on = datetime.strptime(str(attributes[1].find('strong').nextSibling),'%d %B %Y').date() 
  where = '' if len(attributes)==3 else attributes[2].find('strong').nextSibling
  content = getBody(soup.find('div',{'class':'middlecolumn'}).find('div',{'class':'articlebody'}))
  record = {}
  record['body'] = content
  record['given_on'] = given_on
  record['minister_name'] = speaker + ' MP'
  record['permalink'] = speech_url
  record['title'] = title
  record['where'] = where
  record['dept_name'] = 'Education'
  scraperwiki.sqlite.save(['permalink'], record)
  
def getBody(div):
  content = ''
  for item in div.findAll(lambda tag:True):
    content += ' ' + str(item)
  return content

num = getPageNumber()
links = scrapeLinks(num)
print(len(links))
for l in links:
  scrapeSpeech(l)
  time.sleep(random.uniform(1, 3) )
#scrapeSpeech('http://www.education.gov.uk/inthenews/speeches/a0064996/tim-loughton-to-the-safety-2010-conference')
#links = scrapePage('http://www.education.gov.uk/inthenews/speeches/?page=4')
import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import time
import random

url ='http://www.education.gov.uk/inthenews/speeches/'

def getPageNumber():
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  page_container = soup.find('div', {'class':'pagination'})
  last_page_link = page_container.findAll('a')[-2]
  last_page_number = last_page_link.find('span').nextSibling
  return int(last_page_number)

def scrapeLinks(num_of_pages):
  links = []
  for i in range(1,num_of_pages + 1):
    links.extend(scrapePage('http://www.education.gov.uk/inthenews/speeches/?page=' + str(i)))
    time.sleep(1)
  return links

def scrapePage(page_url):
  html = scraperwiki.scrape(page_url)
  soup = BeautifulSoup(html)
  links = []
  for sp in soup.find('div',{'class':'itemlist'}).findAll('li'):
    link = sp.find('h3').find('a')['href']
    links.append('http://www.education.gov.uk' + link)
  return links

def scrapeSpeech(speech_url):
  html = scraperwiki.scrape(speech_url)
  soup = BeautifulSoup(html)
  title = soup.find('div',{'class':'pagetitle'}).text
  attributes = soup.find('div',{'class':'documentattributes'}).findAll('dd')
  speaker = attributes[0].find('strong').nextSibling
  given_on = datetime.strptime(str(attributes[1].find('strong').nextSibling),'%d %B %Y').date() 
  where = '' if len(attributes)==3 else attributes[2].find('strong').nextSibling
  content = getBody(soup.find('div',{'class':'middlecolumn'}).find('div',{'class':'articlebody'}))
  record = {}
  record['body'] = content
  record['given_on'] = given_on
  record['minister_name'] = speaker + ' MP'
  record['permalink'] = speech_url
  record['title'] = title
  record['where'] = where
  record['dept_name'] = 'Education'
  scraperwiki.sqlite.save(['permalink'], record)
  
def getBody(div):
  content = ''
  for item in div.findAll(lambda tag:True):
    content += ' ' + str(item)
  return content

num = getPageNumber()
links = scrapeLinks(num)
print(len(links))
for l in links:
  scrapeSpeech(l)
  time.sleep(random.uniform(1, 3) )
#scrapeSpeech('http://www.education.gov.uk/inthenews/speeches/a0064996/tim-loughton-to-the-safety-2010-conference')
#links = scrapePage('http://www.education.gov.uk/inthenews/speeches/?page=4')
