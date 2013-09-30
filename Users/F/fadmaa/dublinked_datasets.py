import scraperwiki

# collect the data available on datasets listed on dublinked.ie catalog at http://www.dublinked.ie/datastore/index.php
import scraperwiki
from BeautifulSoup import BeautifulSoup
from time import gmtime, strftime

url = 'http://www.dublinked.ie/datastore/index.php'
base = 'http://www.dublinked.ie'
def scrape():
  #the HTML is very very very very very very bogus!!! BeautifulSoup can't handle it. some cleaning up is hardcoded
  html = scraperwiki.scrape(url).replace('<!li>','<li>').replace('<!a','<a').replace('q=node/13"Home','q=node/13">Home').replace('"#"Forum','"#">Forum').replace('</div> <!-- end wrapper -->','').replace('<! ***','<!--***').replace('*** >','***-->').replace('<! >','')
  soup = BeautifulSoup(html)
  container = soup.find('div',{'class':'catalog'})
  for record in container.findAll('div',{'class':'catalog-line'}):
    dataset = {}
    dataset['title'] = record.find('div',{'class':'catalog-data-title'}).text
    dataset['category'] = record.find('div',{'class':'catalog-data-category'}).text
    dataset['region'] = record.find('div',{'class':'catalog-data-region'}).text
    dataset['url'] = base + record.find('div',{'class':'catalog-data-more'}).find('a')['href']
    scrapeDataset(dataset)
    scraperwiki.sqlite.save(['url'],dataset)

def scrapeDataset(dataset):
  html = scraperwiki.scrape(dataset['url']).replace('<!li>','<li>').replace('<!a','<a')
  soup = BeautifulSoup(html)
  metadata_lines= soup.findAll('div',{'class':'metadata-line'})
  for line in metadata_lines:
    field = line.find('div',{'class':'metadata-tag'}).text.replace('(s)','')
    if field=='Download Links':
      anchors = line.find('div',{'class':'metadata-content'}).findAll('a')
      dataset[field] = ' '.join([a['href'] for a in anchors])
    else:
      dataset[field] = line.find('div',{'class':'metadata-content'}).text
scrape()import scraperwiki

# collect the data available on datasets listed on dublinked.ie catalog at http://www.dublinked.ie/datastore/index.php
import scraperwiki
from BeautifulSoup import BeautifulSoup
from time import gmtime, strftime

url = 'http://www.dublinked.ie/datastore/index.php'
base = 'http://www.dublinked.ie'
def scrape():
  #the HTML is very very very very very very bogus!!! BeautifulSoup can't handle it. some cleaning up is hardcoded
  html = scraperwiki.scrape(url).replace('<!li>','<li>').replace('<!a','<a').replace('q=node/13"Home','q=node/13">Home').replace('"#"Forum','"#">Forum').replace('</div> <!-- end wrapper -->','').replace('<! ***','<!--***').replace('*** >','***-->').replace('<! >','')
  soup = BeautifulSoup(html)
  container = soup.find('div',{'class':'catalog'})
  for record in container.findAll('div',{'class':'catalog-line'}):
    dataset = {}
    dataset['title'] = record.find('div',{'class':'catalog-data-title'}).text
    dataset['category'] = record.find('div',{'class':'catalog-data-category'}).text
    dataset['region'] = record.find('div',{'class':'catalog-data-region'}).text
    dataset['url'] = base + record.find('div',{'class':'catalog-data-more'}).find('a')['href']
    scrapeDataset(dataset)
    scraperwiki.sqlite.save(['url'],dataset)

def scrapeDataset(dataset):
  html = scraperwiki.scrape(dataset['url']).replace('<!li>','<li>').replace('<!a','<a')
  soup = BeautifulSoup(html)
  metadata_lines= soup.findAll('div',{'class':'metadata-line'})
  for line in metadata_lines:
    field = line.find('div',{'class':'metadata-tag'}).text.replace('(s)','')
    if field=='Download Links':
      anchors = line.find('div',{'class':'metadata-content'}).findAll('a')
      dataset[field] = ' '.join([a['href'] for a in anchors])
    else:
      dataset[field] = line.find('div',{'class':'metadata-content'}).text
scrape()