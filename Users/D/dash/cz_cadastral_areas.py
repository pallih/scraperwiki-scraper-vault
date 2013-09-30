# -*- coding: utf8 -*-

import scraperwiki
import requests
from bs4 import BeautifulSoup, BeautifulStoneSoup
import re
import time

# working from a list of Czech localities (Obce), find all the Cadastal Areas (Katastrální území)
scraperwiki.sqlite.attach("cz_localities_list")

obce_re = re.compile('/vdp/ruian/obce/(\d+)')


def foo_from_bar(page):
    rowdata = []

def details_from_page(page):
  rowdata = []
  soup = BeautifulSoup(page)
  table = soup.find('table', 'dataTable')
  for row in table.tbody.findAll('tr'):
    if row.get('class') == 'empty':
        print('skipping empty row -- maybe no plots in this cadastre?')
        continue
    details = {}
    cells = row.findAll('td')
    details['ku_code'] = cells[0].text
    details['ku_name'] = cells[1].text
    details['obec_name'] = cells[2].text
    obce_link = cells[2].find('a')['href']
    obce_code = obce_re.search(obce_link).group(1)
    details['obec_code'] = obce_code

    rowdata.append(details)
  return rowdata

def page_for_obec(obecno):
  url = "http://vdp.cuzk.cz/vdp/ruian/katastralniuzemi/vyhledej?ob.kod=%s&search=Vyhledat" % obecno
  print('loading url %s' % url)
  return(requests.get(url).text)


def iterate_obce(maxpages):
    for i in range(maxpages):
      count = 10
      offset = scraperwiki.sqlite.get_var('obec_db_offset', 0)
      try:
        for locgroup in scraperwiki.sqlite.select("code from cz_localities_list.swdata limit ? offset ?", (count, offset)):
              print('looking at page %s' % locgroup['code'])
              pt = page_for_obec(locgroup['code'])
              kus = details_from_page(pt)
              scraperwiki.sqlite.save(unique_keys=['ku_code'], data=kus)
      except scraperwiki.CPUTimeExceededError:
        print('out of CPU')
        break
      scraperwiki.sqlite.save_var('obec_db_offset', offset + count)
      print("done pages %s" % i)

if __name__ == '__main__': 
    iterate_obce(1000)

def test_one_page(code):
  pt = page_for_obec(code)
  kus = details_from_page(pt)
  print(kus)




# Blank Python# -*- coding: utf8 -*-

import scraperwiki
import requests
from bs4 import BeautifulSoup, BeautifulStoneSoup
import re
import time

# working from a list of Czech localities (Obce), find all the Cadastal Areas (Katastrální území)
scraperwiki.sqlite.attach("cz_localities_list")

obce_re = re.compile('/vdp/ruian/obce/(\d+)')


def foo_from_bar(page):
    rowdata = []

def details_from_page(page):
  rowdata = []
  soup = BeautifulSoup(page)
  table = soup.find('table', 'dataTable')
  for row in table.tbody.findAll('tr'):
    if row.get('class') == 'empty':
        print('skipping empty row -- maybe no plots in this cadastre?')
        continue
    details = {}
    cells = row.findAll('td')
    details['ku_code'] = cells[0].text
    details['ku_name'] = cells[1].text
    details['obec_name'] = cells[2].text
    obce_link = cells[2].find('a')['href']
    obce_code = obce_re.search(obce_link).group(1)
    details['obec_code'] = obce_code

    rowdata.append(details)
  return rowdata

def page_for_obec(obecno):
  url = "http://vdp.cuzk.cz/vdp/ruian/katastralniuzemi/vyhledej?ob.kod=%s&search=Vyhledat" % obecno
  print('loading url %s' % url)
  return(requests.get(url).text)


def iterate_obce(maxpages):
    for i in range(maxpages):
      count = 10
      offset = scraperwiki.sqlite.get_var('obec_db_offset', 0)
      try:
        for locgroup in scraperwiki.sqlite.select("code from cz_localities_list.swdata limit ? offset ?", (count, offset)):
              print('looking at page %s' % locgroup['code'])
              pt = page_for_obec(locgroup['code'])
              kus = details_from_page(pt)
              scraperwiki.sqlite.save(unique_keys=['ku_code'], data=kus)
      except scraperwiki.CPUTimeExceededError:
        print('out of CPU')
        break
      scraperwiki.sqlite.save_var('obec_db_offset', offset + count)
      print("done pages %s" % i)

if __name__ == '__main__': 
    iterate_obce(1000)

def test_one_page(code):
  pt = page_for_obec(code)
  kus = details_from_page(pt)
  print(kus)




# Blank Python