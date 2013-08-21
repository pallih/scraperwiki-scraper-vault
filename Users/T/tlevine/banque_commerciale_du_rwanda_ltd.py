from scraperwiki.sqlite import save
from lxml.html import fromstring
from urllib2 import urlopen
from time import time, sleep
import re

URL = "http://www.bcr.co.rw/index.php/site-map/our-branch-network"
DATE = time()

def main():
  table = gettbody()

  head = table.xpath('tr[position()=1]')[0]
  body = table.xpath('tr[position()>1 and position()<last()]')
  foot = table.xpath('tr[position()=last()]')[0] #Ignored

  d = parsetable(head,body)
  for row in d:
    row['date_scraped'] = DATE
    row.update(parseaddress(row['ADDRESS']))
  save([], d)

def gettbody():
  x = fromstring(urlopen(URL).read())
  tables = x.cssselect('table > tbody')
  assert 1 == len(tables)
  return tables[0]

def parsetable(headtr,bodytrs):
  keys = [td.text_content().strip().replace(' ','-') for td in headtr]
  return [dict(zip(keys,[td.text_content().encode('utf-8') for td in tr])) for tr in bodytrs]

def parseaddress(address):
  words_after = filter(None, re.split(r'[\./ ,]', address.strip()))
  words_before = []
  data = {}

  while len(words_after) > 0:
    this_word = words_after.pop(0)
    words_before.append(this_word)

    # Fix typos and French
    if this_word.lower() == 'distric':
      this_word = 'district'
    elif this_word.lower() == 'secteur':
      this_word = 'sector'

    # Save if we've reached a relevant word
    if this_word.lower() in ['sector', 'district', 'province']:
      data[this_word.lower()] = ' '.join(words_before[:-1])
      words_before = []

  # Remove "Rwanda"
  if len(words_before) > 0 and words_before[-1].lower() == 'rwanda':
    del(words_before[-1])

  # Post office boxes
  if len(words_before) >= 4 and words_before[0:3] == ['P', u'O', u'Box']:
    data['street_address'] = 'P.O. Box %d' % int(words_before[3])
    words_before = words_before[4:]

  # Province is probably at the end
  if len(words_before) >= 1:
    data['province'] = words_before.pop()

  # The rest is street address
  if len(words_before) > 0:
    data['street_address'] = ' '.join(words_before)
    del(words_before)

  return data

main()

#from scraperwiki.sqlite import select
#for row in select('address from swdata'):
#  print parseaddress(row['ADDRESS'])