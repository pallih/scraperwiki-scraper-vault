import scraperwiki
import re

url = 'http://www.dh.gov.uk/en/MediaCentre/Speeches/index.htm'

from BeautifulSoup import BeautifulSoup

def scrapeSpeeches():
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  container = soup.find('div',{'class':'contentWrapper'}).find('div',{'class':'linksContainer'})
  for div in container.findAll('div',{'class':re.compile('itemContainer')}):
    
    speaker = div.find('h3').text
    i = speaker.find(',')
    if i==-1:
      continue
    name = speaker[0:i]
    speaker_title = speaker[i+1:]
    speeches = div.find('ul',{'class':'itemLinks'}).findAll('li')
    for speech in speeches:
      record = {}
      record['department'] = 'Department of Health'
      record['department link'] = 'http://en.wikipedia.org/wiki/Department_of_Health_(United_Kingdom)'
      record['speaker'] = name
      record['speaker title'] = speaker_title
      title = speech.find('a').text
      j = title.find(':')
      d = title[0:j]
      t = title[j+1:]
      link = 'http://www.dh.gov.uk' + speech.find('a')['href']
      print(link)
      abstract = getAbstract(link)
      record['link'] = link
      record['title'] = t
      record['date'] = d
      record['abstract'] = abstract
      scraperwiki.sqlite.save(['link'], record)
      print(record)


def getAbstract(link):
  html = scraperwiki.scrape(link)
  soup = BeautifulSoup(html)
  container = soup.find('div',{'class':'introContent'})
  ps = container.findAll('p',recursive=False)
  num = min(3,len(ps))
  abstract = ''
  for i in range(0,num):
    abstract += ps[i].text
  return abstract
  
scrapeSpeeches()