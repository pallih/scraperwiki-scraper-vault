import scraperwiki

# collect the data available on the Volvo Ocean Race 2011-2012 at http://www.volvooceanrace.com/en/datatables/rdc.html
import scraperwiki
from BeautifulSoup import BeautifulSoup
from time import gmtime, strftime

url = 'http://www.volvooceanrace.com/en/datatables/rdc.html'
def scrape():
  scrape_time = strftime("%Y-%m-%d %H", gmtime())
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  tables = soup.findAll('table',{'class':'rdcTable'})
  for table in tables:
    trs = table.findAll('tr')
    teams = [td.text for td in trs[0].findAll('td')]
    for tr in trs[1:]:
      tds = tr.findAll('td')
      measure = tds[1].findAll('span')[-1].text
      for i in range(2,len(tds)):
        scraperwiki.sqlite.save(["team","measure","time"], {"team":teams[i-1],"measure":measure,"value":tds[i].text,"time":scrape_time})
scrape()


