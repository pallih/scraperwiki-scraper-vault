import scraperwiki
import time

baseUrl = 'http://data.fingal.ie/ViewDataSets/Details/default.aspx?datasetID='

from BeautifulSoup import BeautifulSoup

def scrapeDataset(index):
  try:
    record = {}
    record['id'] = index
    url = baseUrl + str(index)
    record['url'] = url
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    print soup.prettify()
    content = soup.find('div',id='content')
    record['title'] = content.find('h1',{'class':'title'}).text
    ps = content.findAll('p')
  # record['created'] = ps[0].text
    record['categories'] = ps[1].text
  # record['description'] = ps[3:len(ps)]

    table = content.find('table',{'class':'dataset'})
    trs = table.findAll('tr')
    record['extent'] = trs[0].findAll('td')[0].text
    record['agency'] = trs[1].findAll('td')[0].text
    record['update_frequency'] = trs[2].findAll('td')[0].text
    record['date_range'] = trs[3].findAll('td')[0].text
    record['date_published'] = trs[4].findAll('td')[0].text
    record['date_of_last_revision'] = trs[5].findAll('td')[0].text
    record['license_summary'] = trs[6].findAll('td')[0].find('a')['href']
    distributions = trs[7:]
    dists = {}
    for dist in distributions:
      dists[dist.find('th').text] = dist.find('td').text
    record['distributions'] = dists
  # print(dists)
    scraperwiki.sqlite.save(unique_keys=['url'], data=[record])
    print record
  except:
    None
    #nothing

min = 400
max = 402
for i in range(min,max):
  scrapeDataset(i)
  time.sleep(1)
