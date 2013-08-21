#!/usr/bin/python
 
from BeautifulSoup import BeautifulSoup
import urllib2
 
#html = ['<html><body><table><tr><td>row 1 table1, cell 1</td><td>row 1, cell 2</td></tr><tr><td>row 2 table1, cell 1</td><td>row 2, cell 2</td></tr></table><table><tr><td>row 1 table2, cell 1</td><td>row 1, cell 2</td></tr><tr><td>row 2 table2, cell 1</td><td>row 2, cell 2</td></tr></table></html>']
url = 'http://www.bolsamadrid.es/comun/fichaemp/fichavalor.asp?isin=ES0136463017&id=ing'
usock = urllib2.urlopen(url)
html= usock.read()
usock.close()
 
#soup = BeautifulSoup(''.join(html))
soup = BeautifulSoup(html)
 
print soup.prettify()

#table = soup.find('table')
tables = soup.findAll('table') 
print len(tables)
for table in tables:
  print 'TABLE'
  rows = table.findAll('tr')
  for tr in rows:
    print 'TR'
    print tr
    cols = tr.findAll('td')
    for td in cols:
      print ' TD'
      print td
#        text = ''.join(td.find(text=True))
#        print text+"|",
#    print
