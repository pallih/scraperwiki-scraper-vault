import scraperwiki
import BeautifulSoup
import random
import time

start_url = 'http://datos.gijon.es/pag/1/page/1808-catalogo-de-datos'

def get_page_number():
  html = scraperwiki.scrape(start_url)
  soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8")

  pagination_container = soup.find('div',{'class':'search-results-pagination'})
  before_last_a = pagination_container.findAll('a')[-2].text
  return int(before_last_a)

def get_urls_in_page(url):
  hrefs = []
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8")
  datasets_table = soup.find('div',{'class':'og-content-objects-listing risp_datasets'}).find('table')
  for tr in datasets_table.findAll('tr'):
    td =  tr.find('td')
    if td!=None:
      hrefs.append('http://datos.gijon.es' + td.find('a')['href'])
  return hrefs

def get_dcat_url_of_dataset(url):
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8")
  return soup.find('div',{'class':'rdf_dcat'}).find('a')['href']

num_of_pages = get_page_number()
hrefs = []
for i in range(1,num_of_pages+1):
  url = 'http://datos.gijon.es/pag/' + str(i) + '/page/1808-catalogo-de-datos'
  hrefs.extend(get_urls_in_page(url))

for url in hrefs:
  dcat_url = get_dcat_url_of_dataset(url)
  scraperwiki.sqlite.save(['URL'],{'URL':dcat_url})
  time.sleep(random.uniform(1,2))import scraperwiki
import BeautifulSoup
import random
import time

start_url = 'http://datos.gijon.es/pag/1/page/1808-catalogo-de-datos'

def get_page_number():
  html = scraperwiki.scrape(start_url)
  soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8")

  pagination_container = soup.find('div',{'class':'search-results-pagination'})
  before_last_a = pagination_container.findAll('a')[-2].text
  return int(before_last_a)

def get_urls_in_page(url):
  hrefs = []
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8")
  datasets_table = soup.find('div',{'class':'og-content-objects-listing risp_datasets'}).find('table')
  for tr in datasets_table.findAll('tr'):
    td =  tr.find('td')
    if td!=None:
      hrefs.append('http://datos.gijon.es' + td.find('a')['href'])
  return hrefs

def get_dcat_url_of_dataset(url):
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8")
  return soup.find('div',{'class':'rdf_dcat'}).find('a')['href']

num_of_pages = get_page_number()
hrefs = []
for i in range(1,num_of_pages+1):
  url = 'http://datos.gijon.es/pag/' + str(i) + '/page/1808-catalogo-de-datos'
  hrefs.extend(get_urls_in_page(url))

for url in hrefs:
  dcat_url = get_dcat_url_of_dataset(url)
  scraperwiki.sqlite.save(['URL'],{'URL':dcat_url})
  time.sleep(random.uniform(1,2))