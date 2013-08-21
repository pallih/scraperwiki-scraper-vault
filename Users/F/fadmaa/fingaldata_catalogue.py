import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup
import re

url = "http://data.fingal.ie/ViewDataSets/"
base = "http://data.fingal.ie"


def scrapeDataset(dataset_url):
  html = scraperwiki.scrape(dataset_url)
  soup = BeautifulSoup(html)
  tbl = soup.find('table',{'class':'dataset'})
  dataset = {}
  dataset['url'] = dataset_url
  dataset['title'] = soup.find('h1',{'class':'title'}).text
  dataset['category'] = soup.find('b',text='Categories:').parent.parent.text
  print dataset['category']
  for tr in tbl.findAll('tr'):
    field = tr.find('th').text
    content = tr.find('td')
    a = content.find('a')
    if a:
      dataset[field] = base + a['href']
    else:
      dataset[field] = content.text
  return dataset

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(url)
while True:
    html = br.response().read()
    soup = BeautifulSoup(html)
    trs = soup.find('div',{'class':'mainBody'}).find('table').find('tbody').findAll('tr')
    for tr in trs:
        dataset = scrapeDataset(url + tr.find('td').find('a')['href'])
        scraperwiki.sqlite.save(['url'],dataset)
    mnext = re.search("""<a id="lnkNext" href="javascript:__doPostBack\(&#39;(.*?)&#39;,&#39;(.*?)&#39;\)">Next >></a>""", html)
    if not mnext:
        break
    br.form = list(br.forms())[0]
    print br.form
    br.set_all_readonly(False)
    br["__EVENTTARGET"] = mnext.group(1)
    br["__EVENTARGUMENT"] = mnext.group(2)
    for control in br.form.controls:
        if control.type == "submit":
            control.disabled = True
    response = br.submit()
