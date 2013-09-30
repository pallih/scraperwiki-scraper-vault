from time import time
from scraperwiki.sqlite import save,select
from scraperwiki import swimport
from lxml.etree import fromstring
from urllib2 import urlopen
import re
strip_address = swimport('strip_address').strip_address

DATE=time()
URL="http://www.saccol.org.za/saccos_in_saccol.php"

def main():
  d=download()
  save([],d,'initial')
  d=clean()
  save([],d,'final')

def download():
  #Load page
  raw=urlopen(URL).read()
  cleaned=clean_page(raw)

  #Load table
  table=fromstring(cleaned)
  d=parse_table(table)
  return d

def clean():
  d=select('* from `initial`')
  for row in d:
    row['date_scraped']=DATE
    parse_address(row)
  return d

POSTCODE1=re.compile(r', ?([0-9]*)$')
POSTCODE2=re.compile(r'^[0-9 ]{4,7}$')
TELEPHONE=re.compile(r'^[0-9; ]*$')
TOWN=re.compile(r'^[^ 0-9]*$')

def parse_address(row):
  address=row['Telephone_or_Address'].split('\n')

  for line in address:
    postcode1=re.findall(POSTCODE1,line)
    postcode2=re.findall(POSTCODE2,line)
    town=re.findall(TOWN,line)

    #Scientific notation telephone numbers
    if "+" in line:
      address.remove(line)

    #Postcodes with town names
    elif len(postcode1)==1:
      row['postal-code']=postcode1[0]
      row['town']=re.sub(POSTCODE1,'',line)
      address.remove(line)

    #Postcodes without town names
    elif len(postcode2)==2:
      row['postal-code']=line.replace(' ','')
      address.remove(line)

    #Town names without postcodes. And not street names
    elif len(town)==1:
      row['town']=line
      address.remove(line)

    #Useful telephone numbers
    elif re.match(TELEPHONE,line):
      row['phone']=line
      address.remove(line)

    else:
      pass
      #print line

  row['street-address']=', '.join(address)

def clean_page(raw):
  raw=raw.split('<table width="98%" border="1" align="center" cellpadding="3" cellspacing="0">')[1]
  raw=raw.split('</table>')[0]
  raw=raw.replace('<col width="64" span="4"  />','')
  cleaned='<table>%s</table>' % raw
  return cleaned

def parse_table(table):
  t=BizarreTable(table)
  t.parse()
  return t.d

class BizarreTable:
  def __init__(self,table):
    self.table=table
    self.colnames=None
    self.region=None
    self.row=None
    self.d=[]

  def getheader(self,tr):
    self.colnames=[t.replace('/','_or_') for t in tr.xpath('td/strong/text()')]

  def getregion(self,tr):
    nodes=tr.xpath('td/strong/text()')
    assert len(nodes)==1
    self.region=nodes[0]

  def getrow(self,tr):
    nodes=tr.xpath('td/text()')
    assert 4==len(nodes)
    self.row=nodes

  def record(self):
    self.d.append(dict(zip(self.colnames,self.row)))

  @staticmethod
  def rowspan(tr):
    "Get the rowspan. I don't need this."
    rowspans=set(tr.xpath('td/@rowspan'))
    assert len(rowspans)==1
    return int(rowspans.pop())

  def parse(self):
    #Parse the rows
    for tr in self.table.xpath('tr'):
      self.parse_tr(tr)
    #Record the last row because that's in the middle of my loop rather than the end.
    self.record()

  def parse_tr(self,tr):
    if self.colnames==None:
      #The header
      self.getheader(tr)

    elif 1==tr.xpath('count(td[@colspan="4"])'):
      #A new region
      self.getregion(tr)

    elif 4==tr.xpath('count(td)'):
      #A full row

      #Record the last row if this isn't first
      if self.row!=None:
        self.record()

      #Then save the new row
      self.getrow(tr)

    elif 1==tr.xpath('count(td)'):
      #Continuation of an address row
      nodes=tr.xpath('td/text()')
      assert 1==len(nodes)
      self.row[2]+='\n'+nodes[0]

main()from time import time
from scraperwiki.sqlite import save,select
from scraperwiki import swimport
from lxml.etree import fromstring
from urllib2 import urlopen
import re
strip_address = swimport('strip_address').strip_address

DATE=time()
URL="http://www.saccol.org.za/saccos_in_saccol.php"

def main():
  d=download()
  save([],d,'initial')
  d=clean()
  save([],d,'final')

def download():
  #Load page
  raw=urlopen(URL).read()
  cleaned=clean_page(raw)

  #Load table
  table=fromstring(cleaned)
  d=parse_table(table)
  return d

def clean():
  d=select('* from `initial`')
  for row in d:
    row['date_scraped']=DATE
    parse_address(row)
  return d

POSTCODE1=re.compile(r', ?([0-9]*)$')
POSTCODE2=re.compile(r'^[0-9 ]{4,7}$')
TELEPHONE=re.compile(r'^[0-9; ]*$')
TOWN=re.compile(r'^[^ 0-9]*$')

def parse_address(row):
  address=row['Telephone_or_Address'].split('\n')

  for line in address:
    postcode1=re.findall(POSTCODE1,line)
    postcode2=re.findall(POSTCODE2,line)
    town=re.findall(TOWN,line)

    #Scientific notation telephone numbers
    if "+" in line:
      address.remove(line)

    #Postcodes with town names
    elif len(postcode1)==1:
      row['postal-code']=postcode1[0]
      row['town']=re.sub(POSTCODE1,'',line)
      address.remove(line)

    #Postcodes without town names
    elif len(postcode2)==2:
      row['postal-code']=line.replace(' ','')
      address.remove(line)

    #Town names without postcodes. And not street names
    elif len(town)==1:
      row['town']=line
      address.remove(line)

    #Useful telephone numbers
    elif re.match(TELEPHONE,line):
      row['phone']=line
      address.remove(line)

    else:
      pass
      #print line

  row['street-address']=', '.join(address)

def clean_page(raw):
  raw=raw.split('<table width="98%" border="1" align="center" cellpadding="3" cellspacing="0">')[1]
  raw=raw.split('</table>')[0]
  raw=raw.replace('<col width="64" span="4"  />','')
  cleaned='<table>%s</table>' % raw
  return cleaned

def parse_table(table):
  t=BizarreTable(table)
  t.parse()
  return t.d

class BizarreTable:
  def __init__(self,table):
    self.table=table
    self.colnames=None
    self.region=None
    self.row=None
    self.d=[]

  def getheader(self,tr):
    self.colnames=[t.replace('/','_or_') for t in tr.xpath('td/strong/text()')]

  def getregion(self,tr):
    nodes=tr.xpath('td/strong/text()')
    assert len(nodes)==1
    self.region=nodes[0]

  def getrow(self,tr):
    nodes=tr.xpath('td/text()')
    assert 4==len(nodes)
    self.row=nodes

  def record(self):
    self.d.append(dict(zip(self.colnames,self.row)))

  @staticmethod
  def rowspan(tr):
    "Get the rowspan. I don't need this."
    rowspans=set(tr.xpath('td/@rowspan'))
    assert len(rowspans)==1
    return int(rowspans.pop())

  def parse(self):
    #Parse the rows
    for tr in self.table.xpath('tr'):
      self.parse_tr(tr)
    #Record the last row because that's in the middle of my loop rather than the end.
    self.record()

  def parse_tr(self,tr):
    if self.colnames==None:
      #The header
      self.getheader(tr)

    elif 1==tr.xpath('count(td[@colspan="4"])'):
      #A new region
      self.getregion(tr)

    elif 4==tr.xpath('count(td)'):
      #A full row

      #Record the last row if this isn't first
      if self.row!=None:
        self.record()

      #Then save the new row
      self.getrow(tr)

    elif 1==tr.xpath('count(td)'):
      #Continuation of an address row
      nodes=tr.xpath('td/text()')
      assert 1==len(nodes)
      self.row[2]+='\n'+nodes[0]

main()