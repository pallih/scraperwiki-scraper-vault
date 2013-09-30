import scraperwiki

url = 'http://electionsireland.org/results/general/31stdail/candidates.cfm'

from BeautifulSoup import BeautifulSoup

def scrapeCandidates():
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  container = soup.find('table',{'class':'table'})
  first_tr = container.find('tr')
  for tr in first_tr.findNextSiblings('tr'):
    first_td = tr.find('td')
    second_td = first_td.nextSibling
    urls = []
    for td in second_td.findNextSiblings('td'):
      cands = td.findAll('a')
      for cand in cands:
        link = cand['href']
        if link.startswith('../..'):
          record = {}
          record['href'] = 'http://electionsireland.org/' + link[9:]
          record['text'] = cand.text
          if cand.find('strong') :
            record['current'] = True
          else:
            record['current'] = False
          scraperwiki.datastore.save(['href'], record)

scrapeCandidates()
import scraperwiki

url = 'http://electionsireland.org/results/general/31stdail/candidates.cfm'

from BeautifulSoup import BeautifulSoup

def scrapeCandidates():
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  container = soup.find('table',{'class':'table'})
  first_tr = container.find('tr')
  for tr in first_tr.findNextSiblings('tr'):
    first_td = tr.find('td')
    second_td = first_td.nextSibling
    urls = []
    for td in second_td.findNextSiblings('td'):
      cands = td.findAll('a')
      for cand in cands:
        link = cand['href']
        if link.startswith('../..'):
          record = {}
          record['href'] = 'http://electionsireland.org/' + link[9:]
          record['text'] = cand.text
          if cand.find('strong') :
            record['current'] = True
          else:
            record['current'] = False
          scraperwiki.datastore.save(['href'], record)

scrapeCandidates()
