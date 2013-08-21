#!/usr/bin/env python
from scraperwiki.sqlite import save, select, show_tables
from urllib2 import Request, urlopen
from lxml.html import fromstring

URL="http://www.elections.ca/scripts/webpep/fin2/detail_report.aspx"
def postdata(pagenumber):
  return ''.join([
     'entity=1&lang=e&filter=34&option=4&ids=&id=&part=&page='
   , str(pagenumber)
   , '&sort=0&return=1&PrevReturn=0&style=0&table='
   , '&searchentity=0&contribname=&contribclass=12%2C14%2C15%2C16%2C17'
   , '&contribprov=-1&contribrange=-1&contribed=-1&contribpp=-1'
   , '&contribfiscalfrom=0&contribfiscalto=0&EVENTARGUMENT=&period=-1'
   ])

def main():
  #What has already been scraped
  if 'contributions' in show_tables():
    scraped=[row['querystring'] for row in select('querystring from contributions')]
  else:
    scraped=[]

  pagenumber=0
  while True:
    pagenumber=pagenumber+1
    xml=load(pagenumber)

    #Get the header row
    rows=xml.xpath('//table[@class="table_text"][tr[@class="tan_row"]]')[0].getchildren()[1:]
    keys=['name','contestant_party_district','date_received','class_and_partnum','association','monetary','non-monetary']

    #Get the data rows
    ds=[]
    d={}
    for row in rows:
      cells=row.getchildren()
      contributor=cells.pop(0).getchildren()[0]

      d['querystring']=contributor.attrib['href'].replace("javascript:PopUp('contributor.aspx?",'').replace("', '300', '300');",'')
      d[keys[0]]=contributor.text
      for i in range(1,len(cells)):
        d[keys[i]]=cells[i].text
      ds.append(d)

    #Don't run again if already run
    if ds[0]['querystring'] in scraped:
      break
    else:
      save(['querystring'],ds,'contributions')

def load(pagenumber):
  req=Request(url=URL,data=postdata(pagenumber))
  html=urlopen(req).read()
  xml=fromstring(html)
  return xml

main()
#print load(1)
