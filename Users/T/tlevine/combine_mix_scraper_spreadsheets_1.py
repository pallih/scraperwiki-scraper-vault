from scraperwiki.sqlite import save
from lxml.html import fromstring
from urllib2 import urlopen
from time import time

def main(testing = False):
  out = ''
  x = fromstring(urlopen('https://views.scraperwiki.com/run/mix_scraper_spreadsheets/?date='+str(time())).read())
  csv_links = x.xpath('//td[position()=3]/a/@href')

  if testing:
    csv_links = csv_links[0:2]

  #Manual data
  csv_links.append('http://hacks.thomaslevine.com/manual-SA-data-cleaned.csv')

  #Standard Bank data, which was run with Highwall instead of ScraperWiki
  csv_links.append('http://hacks.thomaslevine.com/standardbank-branches-cleaned.csv')
  csv_links.append('http://hacks.thomaslevine.com/standardbank-atm.csv')

  header0, body = getCsv(csv_links[0])
  out += header0[:-2]
  for csv_link in csv_links:
    header, body = getCsv(csv_link)

    if header0 == header:
      out += body[:-2]
    else:
      header_pairs = zip(header0.split(','), header.split(','))
      for pair in header_pairs:
        if pair[0] != pair[1]:
          print pair
      raise ValueError("Headers from %s and %s don't match." % (csv_links[0], csv_link))
  save(['time'], {"time": time(), "spreadsheet": out}, 'combined_spreadsheets')

def getCsv(csv_link):
  h = urlopen(csv_link)
  header = h.readline()
  body = h.read()
  return header, body

main()
from scraperwiki.sqlite import save
from lxml.html import fromstring
from urllib2 import urlopen
from time import time

def main(testing = False):
  out = ''
  x = fromstring(urlopen('https://views.scraperwiki.com/run/mix_scraper_spreadsheets/?date='+str(time())).read())
  csv_links = x.xpath('//td[position()=3]/a/@href')

  if testing:
    csv_links = csv_links[0:2]

  #Manual data
  csv_links.append('http://hacks.thomaslevine.com/manual-SA-data-cleaned.csv')

  #Standard Bank data, which was run with Highwall instead of ScraperWiki
  csv_links.append('http://hacks.thomaslevine.com/standardbank-branches-cleaned.csv')
  csv_links.append('http://hacks.thomaslevine.com/standardbank-atm.csv')

  header0, body = getCsv(csv_links[0])
  out += header0[:-2]
  for csv_link in csv_links:
    header, body = getCsv(csv_link)

    if header0 == header:
      out += body[:-2]
    else:
      header_pairs = zip(header0.split(','), header.split(','))
      for pair in header_pairs:
        if pair[0] != pair[1]:
          print pair
      raise ValueError("Headers from %s and %s don't match." % (csv_links[0], csv_link))
  save(['time'], {"time": time(), "spreadsheet": out}, 'combined_spreadsheets')

def getCsv(csv_link):
  h = urlopen(csv_link)
  header = h.readline()
  body = h.read()
  return header, body

main()
