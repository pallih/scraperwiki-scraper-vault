import scraperwiki

baseUrl = 'http://www.boards.ie/vote/results.php?type=national'

from BeautifulSoup import BeautifulSoup

def scrapeVotes():
  html = scraperwiki.scrape(baseUrl)
  soup = BeautifulSoup(html)
  trs = soup.find('table',{'id':'natbreak'}).find('tbody').findAll('tr')
  urls = []
  for tr in trs:
    td = tr.find('td').find('a')
    urls.append({'text':td.text,'href':td['href']})
  return urls

def scrapeVote(url,name):
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  print(url)
  table = soup.find('table',{'id':'vote-candidate-results-table-pr'})
  if table==None:
    table= soup.find('table',{'id':'vote-candidate-results-table'})
  trs = table.find('tbody').findAll('tr')
  i = 1
  for tr in trs:
    siblings = tr.find('td').findNextSiblings('td')
    s = siblings[0].find('strong')
    r = siblings[1].find('strong')
    if s!=None :
      record = {}
      record['name'] = s.text
      record['party'] = r.text
      record['rank'] = i
      record['constituency'] = name
      scraperwiki.datastore.save(['rank','constituency'], record)
      i += 1
urls = scrapeVotes()
for url in urls:
  scrapeVote('http://www.boards.ie' + url['href'],url['text'])