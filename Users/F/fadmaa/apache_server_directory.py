import scraperwiki

# collect the data available on the Volvo Ocean Race 2011-2012 at http://www.volvooceanrace.com/en/datatables/rdc.html
import scraperwiki
from BeautifulSoup import BeautifulSoup
from time import gmtime, strftime

c_url = 'http://data.semanticweb.org/dumps/conferences/'
w_url = 'http://data.semanticweb.org/dumps/workshops/'

def scrape(url):
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  table = soup.find('table')
  trs = table.findAll('tr')
  for tr in trs[1:]:
    tds = tr.findAll('td')
    if len(tds)>3 and tds[1].find('a').text.endswith('.rdf'):
      f_url = url + tds[1].find('a').text
      scraperwiki.sqlite.save(["url"], {"url":f_url,"date":tds[2].text})

scrape(c_url)
scrape(w_url)


import scraperwiki

# collect the data available on the Volvo Ocean Race 2011-2012 at http://www.volvooceanrace.com/en/datatables/rdc.html
import scraperwiki
from BeautifulSoup import BeautifulSoup
from time import gmtime, strftime

c_url = 'http://data.semanticweb.org/dumps/conferences/'
w_url = 'http://data.semanticweb.org/dumps/workshops/'

def scrape(url):
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  table = soup.find('table')
  trs = table.findAll('tr')
  for tr in trs[1:]:
    tds = tr.findAll('td')
    if len(tds)>3 and tds[1].find('a').text.endswith('.rdf'):
      f_url = url + tds[1].find('a').text
      scraperwiki.sqlite.save(["url"], {"url":f_url,"date":tds[2].text})

scrape(c_url)
scrape(w_url)


