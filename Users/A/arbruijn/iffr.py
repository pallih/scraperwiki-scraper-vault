start_url = "http://www.filmfestivalrotterdam.com/nl/iffr-2011/films-a-z/"

import scraperwiki
html = scraperwiki.scrape(start_url)
import re

from urlparse import urljoin

#html = '<div id="bla_pnlAlfabet"><a href="?Letter=Q">one</a></div>'

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html)
alfadiv = soup.find('div', {'id':re.compile('_pnlAlfabet$')})
#alfadiv = soup.find('div', {'id':(lamba id: .endswith('_pnlAlfabet'))})
#alfadiv = soup.find('div', {'id':'_pnlAlfabet'})
if not alfadiv:
  raise Exception("alfadiv not found")
#for div in divs:
#  if div['id'] and div['id'].endswith('_pnlAlfabet'):
links = [a['href'] for a in alfadiv.findAll('a')]
links = [urljoin(start_url, link) for link in links]

def clean(s):
  return re.sub(r'[\t\r\n][ \t\r\n]*| [\t\r\n ]+', u' ', s).strip()

for link in links:
  html = scraperwiki.scrape(link)
  soup = BeautifulSoup(html)
  #mainColumn = soup.find('div', {'id':'mainColumn'})
  tables = soup.findAll('table', {'id':re.compile('_rptFilms_')})
  print len(tables)
  for table in tables:
    img = table.find('img')
    text = table.find('td', {'class':'text'})
    a = text.find('a')
    info = {}
    #print a['href']
    m = re.search(r'/films/([^/]+)/$', a['href'])
    if not m:
      continue
    data = clean(text.find('span').string)
    mdata = re.match(r'([0-9]*[^0-9]+),? ([0-9]+), (([^0-9]+), )?([0-9]+) min\.$', data)
    if not mdata:
      print "fail " + clean(a.string) + " " + data
      continue
    info['id'] = m.group(1)
    info['title'] = clean(a.string)
    info['url'] = urljoin(link, a['href'])
    info['dir'] = mdata.group(1)
    info['year'] = mdata.group(2)
    info['country'] = mdata.group(4)
    info['length'] = mdata.group(5)
    #print info
    #scraperwiki.datastore.save(unique_keys=['id'], data=info)
    scraperwiki.sqlite.save(unique_keys=['id'], data=info)

