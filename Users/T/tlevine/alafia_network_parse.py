#!/usr/bin/env python
from urllib2 import urlopen
from lxml.html import fromstring
from lxml.etree import tostring
from scraperwiki.sqlite import save,attach,select
from BeautifulSoup import BeautifulSoup

attach('alafia_network')
pages=select('* from html')

def main():
  for page in pages:
    number=page['page']

    #Replace brs with a better delimeter
    html=page.pop('table').replace('<br />','|')
    text=''.join(BeautifulSoup(html).findAll(text=True))

    for row in text.split('=-=-=-=-=-=-=-=-=-=-=-=-=-=-='):
      for column in row.split('|'):
        cell=column.split(':')
        if len(cell)==2:
          key,value=cell
          key=key.encode('ascii','ignore').replace(' ','')
          if '&#' in key:
            key=key.split('&#')[0]
          page[key]=value
    save(['page'],page,'microfinance_institutions')

main()#!/usr/bin/env python
from urllib2 import urlopen
from lxml.html import fromstring
from lxml.etree import tostring
from scraperwiki.sqlite import save,attach,select
from BeautifulSoup import BeautifulSoup

attach('alafia_network')
pages=select('* from html')

def main():
  for page in pages:
    number=page['page']

    #Replace brs with a better delimeter
    html=page.pop('table').replace('<br />','|')
    text=''.join(BeautifulSoup(html).findAll(text=True))

    for row in text.split('=-=-=-=-=-=-=-=-=-=-=-=-=-=-='):
      for column in row.split('|'):
        cell=column.split(':')
        if len(cell)==2:
          key,value=cell
          key=key.encode('ascii','ignore').replace(' ','')
          if '&#' in key:
            key=key.split('&#')[0]
          page[key]=value
    save(['page'],page,'microfinance_institutions')

main()