import scraperwiki
from BeautifulSoup import BeautifulSoup

url = 'http://www.deri.ie/research/units/'
def scrape():
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  units = soup.findAll('div',{'class':'unititemleft'})
  for unit in units:
    name = unit.find('h2').find('a').text
    members = unit.findNextSiblings('div',{'class':'unititemright'})[0]
    links = members.findAll('p')[-1].findAll('a')
    for l in links:
      derian = l.text
      scraperwiki.sqlite.save(["name"], {"name":derian,"unit":name})

scrape()import scraperwiki
from BeautifulSoup import BeautifulSoup

url = 'http://www.deri.ie/research/units/'
def scrape():
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  units = soup.findAll('div',{'class':'unititemleft'})
  for unit in units:
    name = unit.find('h2').find('a').text
    members = unit.findNextSiblings('div',{'class':'unititemright'})[0]
    links = members.findAll('p')[-1].findAll('a')
    for l in links:
      derian = l.text
      scraperwiki.sqlite.save(["name"], {"name":derian,"unit":name})

scrape()