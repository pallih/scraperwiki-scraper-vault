import scraperwiki

url = 'http://election.fiannafail.ie/candidates/'

from BeautifulSoup import BeautifulSoup

def scrapeCandidate(div,cons):
  record = {}
  record['party'] = 'Fianna Fail'
  record['constituency'] = cons
  record['name'] = div.find('h4').find('a').text
  record['img'] = div.find('div',{'class':'candidate-photo'}).find('img')['src']
  links = div.findAll('a')
  sites = {}
  for link in links:
    sites[link.text] = link['href']
  record['sites'] = sites
  scraperwiki.datastore.save(['name','constituency','party'], record)
def scrapeCandidates():
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  container = soup.find('ul',id='peopleList')
  constituencies = container.findAll('h4',{'class':'cons_header'})
  for cons in constituencies:
    print(cons.text)
    next = cons.nextSibling
    while next!=None and getattr(next, 'name', None) != 'h4':
      if getattr(next, 'name', None)=='div':
        if getattr(next,'attrs',None) != None and next['class']=='clearfix candidate':
          scrapeCandidate(next,cons.text)
      next = next.nextSibling


scrapeCandidates()import scraperwiki

url = 'http://election.fiannafail.ie/candidates/'

from BeautifulSoup import BeautifulSoup

def scrapeCandidate(div,cons):
  record = {}
  record['party'] = 'Fianna Fail'
  record['constituency'] = cons
  record['name'] = div.find('h4').find('a').text
  record['img'] = div.find('div',{'class':'candidate-photo'}).find('img')['src']
  links = div.findAll('a')
  sites = {}
  for link in links:
    sites[link.text] = link['href']
  record['sites'] = sites
  scraperwiki.datastore.save(['name','constituency','party'], record)
def scrapeCandidates():
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  container = soup.find('ul',id='peopleList')
  constituencies = container.findAll('h4',{'class':'cons_header'})
  for cons in constituencies:
    print(cons.text)
    next = cons.nextSibling
    while next!=None and getattr(next, 'name', None) != 'h4':
      if getattr(next, 'name', None)=='div':
        if getattr(next,'attrs',None) != None and next['class']=='clearfix candidate':
          scrapeCandidate(next,cons.text)
      next = next.nextSibling


scrapeCandidates()