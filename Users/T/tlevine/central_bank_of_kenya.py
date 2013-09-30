from scraperwiki.sqlite import save
from urllib2 import urlopen
from lxml.html import fromstring
from time import time

URL = "http://www.centralbank.go.ke/financialsystem/microfinance/deposittaking.aspx"
DATE = time()

def main():
  x = fromstring(urlopen(URL).read().replace('<br />','\n').replace('&nbsp;',' '))
  ps = x.xpath('//td[@width="596"]/p')
  d = []
  for p in ps:
    text = p.text_content()
    lines = [line.strip() for line in text.split('\n')]
    row = {"entity":lines.pop(0)}
    for line in lines:
      line = line.replace(' : ', '')
      if line != '':
        key, value = line.split(':')
        row[key] = value
      row['date_scraped'] = DATE
    d.append(row)
  save([], d)

main()from scraperwiki.sqlite import save
from urllib2 import urlopen
from lxml.html import fromstring
from time import time

URL = "http://www.centralbank.go.ke/financialsystem/microfinance/deposittaking.aspx"
DATE = time()

def main():
  x = fromstring(urlopen(URL).read().replace('<br />','\n').replace('&nbsp;',' '))
  ps = x.xpath('//td[@width="596"]/p')
  d = []
  for p in ps:
    text = p.text_content()
    lines = [line.strip() for line in text.split('\n')]
    row = {"entity":lines.pop(0)}
    for line in lines:
      line = line.replace(' : ', '')
      if line != '':
        key, value = line.split(':')
        row[key] = value
      row['date_scraped'] = DATE
    d.append(row)
  save([], d)

main()