import scraperwiki
import lxml.html
import requests
#import xlrd, re
import dateutil.parser
#import urlparse
#import json
from hashlib import sha1
from random import random



#html2text=scraperwiki.swimport('html2text')

# julians xls loader
def LoadXLlinks():
    book = xlrd.open_workbook(file_contents=requests.get(xlurl,verify=False).content)
    for i in [0,2,4,6,8,10,12]:
        sheet = book.sheet_by_index(i)
        print sheet.name, "rows:", sheet.nrows
        ldata = [ ] 
        for i in range(sheet.nrows): 
            sheetvalue = sheet.cell(i, 0).value.strip()
            if sheetvalue:
                ldata.append({"sheetname":sheet.name, "i":i, "url":sheetvalue})
        scraperwiki.sqlite.save(["sheetname", "i"], ldata, "xllinks")

# julians raw scraper
def ScrapeRaw():
    scraperwiki.sqlite.execute("create table if not exists htmlcache (url text)")
    urlbatch = scraperwiki.sqlite.execute("select xllinks.url from xllinks left join htmlcache on htmlcache.url = xllinks.url where htmlcache.url is null limit 30")
    urlbatch = [u[0]  for u in urlbatch["data"]]
    if not urlbatch:
        return False
    ldata = [ ]
    for url in urlbatch:
        page_req=requests.get(url)
        page_raw=page_req.content
        data = {'url':url, 'status':page_req.status_code}
        data['html']=unicode(page_raw, 'iso-8859-1')
        ldata.append(data)
    scraperwiki.sqlite.save(["url"], ldata, "htmlcache")
    return True

def parse_publications(results):
    ldata = []
    for result in results:
        record = {}
        try:
            old_url = result.xpath('p[@class="pdf"]/a')
            record['attachment'] = 'http://www.dfid.gov.uk/'+old_url[0].attrib['href']
            record['attachment_title'] = old_url[0].text
        except:
            record['attachment'] = 'n/a'
            record['attachment_title'] = 'n/a'
        date = result.xpath('p[@class="date"]')
        record['date_iso'] = dateutil.parser.parse(date[0].text, dayfirst=True).date().isoformat()
        record['date'] = date[0].text
        try:
            record['summary']  = result[2].text_content()
        except:
            record['summary'] = 'n/a'
        record['associated_organisations'] = 'DFID'
        #record['uid'] = sha1(str(record)).hexdigest() # a unique hash for the datastore save
        ldata.append(record)
    scraperwiki.sqlite.save(["attachment_title"], ldata, "publications")


def Publications(starting_page):
    #scraperwiki.sqlite.execute("drop table if exists publications")
    url = 'http://www.dfid.gov.uk/What-we-do/Publications/?q=&t=&c=&p=&page='+str(starting_page)
    html = requests.get(url).text
    root = lxml.html.fromstring(html)
    results = root.xpath('//div[@class="pub_result"]/div[@class="res_right"]')
    parse_publications(results)
    if root.xpath('//img[@id="pageNavNext"]'):
        Publications(int(starting_page)+1)
    
#scraperwiki.sqlite.execute("drop table if exists publications")
Publications('18')

import scraperwiki
import lxml.html
import requests
#import xlrd, re
import dateutil.parser
#import urlparse
#import json
from hashlib import sha1
from random import random



#html2text=scraperwiki.swimport('html2text')

# julians xls loader
def LoadXLlinks():
    book = xlrd.open_workbook(file_contents=requests.get(xlurl,verify=False).content)
    for i in [0,2,4,6,8,10,12]:
        sheet = book.sheet_by_index(i)
        print sheet.name, "rows:", sheet.nrows
        ldata = [ ] 
        for i in range(sheet.nrows): 
            sheetvalue = sheet.cell(i, 0).value.strip()
            if sheetvalue:
                ldata.append({"sheetname":sheet.name, "i":i, "url":sheetvalue})
        scraperwiki.sqlite.save(["sheetname", "i"], ldata, "xllinks")

# julians raw scraper
def ScrapeRaw():
    scraperwiki.sqlite.execute("create table if not exists htmlcache (url text)")
    urlbatch = scraperwiki.sqlite.execute("select xllinks.url from xllinks left join htmlcache on htmlcache.url = xllinks.url where htmlcache.url is null limit 30")
    urlbatch = [u[0]  for u in urlbatch["data"]]
    if not urlbatch:
        return False
    ldata = [ ]
    for url in urlbatch:
        page_req=requests.get(url)
        page_raw=page_req.content
        data = {'url':url, 'status':page_req.status_code}
        data['html']=unicode(page_raw, 'iso-8859-1')
        ldata.append(data)
    scraperwiki.sqlite.save(["url"], ldata, "htmlcache")
    return True

def parse_publications(results):
    ldata = []
    for result in results:
        record = {}
        try:
            old_url = result.xpath('p[@class="pdf"]/a')
            record['attachment'] = 'http://www.dfid.gov.uk/'+old_url[0].attrib['href']
            record['attachment_title'] = old_url[0].text
        except:
            record['attachment'] = 'n/a'
            record['attachment_title'] = 'n/a'
        date = result.xpath('p[@class="date"]')
        record['date_iso'] = dateutil.parser.parse(date[0].text, dayfirst=True).date().isoformat()
        record['date'] = date[0].text
        try:
            record['summary']  = result[2].text_content()
        except:
            record['summary'] = 'n/a'
        record['associated_organisations'] = 'DFID'
        #record['uid'] = sha1(str(record)).hexdigest() # a unique hash for the datastore save
        ldata.append(record)
    scraperwiki.sqlite.save(["attachment_title"], ldata, "publications")


def Publications(starting_page):
    #scraperwiki.sqlite.execute("drop table if exists publications")
    url = 'http://www.dfid.gov.uk/What-we-do/Publications/?q=&t=&c=&p=&page='+str(starting_page)
    html = requests.get(url).text
    root = lxml.html.fromstring(html)
    results = root.xpath('//div[@class="pub_result"]/div[@class="res_right"]')
    parse_publications(results)
    if root.xpath('//img[@id="pageNavNext"]'):
        Publications(int(starting_page)+1)
    
#scraperwiki.sqlite.execute("drop table if exists publications")
Publications('18')

