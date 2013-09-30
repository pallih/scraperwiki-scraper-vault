from scraperwiki import swimport
from scraperwiki.sqlite import save
from time import time

DATE=time()

def main():
  #Load
  xml=swimport('dsp').dsp('http://www.khula.org.za/Admin/Contacts/RegionalContacts.aspx',False)

  #Parse
  t_nodes=xml.xpath('//table[@width="100%"]')
  assert len(t_nodes)==1
  table=t_nodes[0]
  d=parse_table(table)
  t=time()
  for row in d:
    row["date_scraped"]=t
  d=moreparsing(d)
  save([],d,'final')

def parse_table(table):
  keys=[key.replace(' ','_') for key in table.xpath('tr/td[@class="header1"]/text()')]
  print keys
  rows=table.xpath('tr[position()>1]')
  d=[dict(zip(keys,[td.text_content() for td in row.xpath('td')])) for row in rows]
  return d

def moreparsing(d):
  for row in d:
    row['province']=row['Regional_Office'].split('(')[0]
    row['town']=row['Address'].split(',')[-1]
    row['street-address']=','.join(row['Address'].split(',')[0:-1])
  return d


main()from scraperwiki import swimport
from scraperwiki.sqlite import save
from time import time

DATE=time()

def main():
  #Load
  xml=swimport('dsp').dsp('http://www.khula.org.za/Admin/Contacts/RegionalContacts.aspx',False)

  #Parse
  t_nodes=xml.xpath('//table[@width="100%"]')
  assert len(t_nodes)==1
  table=t_nodes[0]
  d=parse_table(table)
  t=time()
  for row in d:
    row["date_scraped"]=t
  d=moreparsing(d)
  save([],d,'final')

def parse_table(table):
  keys=[key.replace(' ','_') for key in table.xpath('tr/td[@class="header1"]/text()')]
  print keys
  rows=table.xpath('tr[position()>1]')
  d=[dict(zip(keys,[td.text_content() for td in row.xpath('td')])) for row in rows]
  return d

def moreparsing(d):
  for row in d:
    row['province']=row['Regional_Office'].split('(')[0]
    row['town']=row['Address'].split(',')[-1]
    row['street-address']=','.join(row['Address'].split(',')[0:-1])
  return d


main()