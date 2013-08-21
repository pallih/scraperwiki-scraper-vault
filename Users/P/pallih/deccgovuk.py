import scraperwiki
import lxml.html
import requests
#import xlrd, re
import dateutil.parser
#import urlparse
#import json
from hashlib import sha1
from random import random
import re

date_check = re.compile("\d+ \S+ \d\d\d\d")



html2text=scraperwiki.swimport('html2text')

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
        record['attachment'] = 'http://www.decc.gov.uk'+result[0].attrib['href']
        record['attachment_title'] = result[0].text.strip()        
        fileinfo = result.xpath('div[@class="fileinfo"]')
        record['summary'] = fileinfo[0][1].tail.strip()
        record['date'] = fileinfo[0][7].tail.strip()
        record['date_iso'] = dateutil.parser.parse(record['date'], dayfirst=True).date().isoformat()
        record['urn'] = fileinfo[0][9].tail.strip()
        record['associated_organisations'] = 'DECC'
        ldata.append(record)
    scraperwiki.sqlite.save(["attachment_title","summary"], ldata, "publications")


def Publications(starting_page):
    #scraperwiki.sqlite.execute("drop table if exists publications")
    url = 'http://www.decc.gov.uk/publications/AdvancedSearch.aspx?term=&resultsNumber=10&tags=&alpha=&urn=&fromDate=01/05/2010&toDate=21/09/2012&PageNumber='+str(starting_page)
    html = requests.get(url).text
    root = lxml.html.fromstring(html)
    results = root.xpath('//ul[@class="search-results"]/li')
    parse_publications(results)
    try:
        root.xpath('//a[@id="ctl00_ContentPlaceHolder1_nextLink"]')[0].attrib['href']
        next_page = starting_page +1
        #print 'done: ', starting_page, 'next: ', next_page
        scraperwiki.sqlite.save_var('last_page', starting_page) 
        Publications(next_page)
    except:
        print 'done'

def parse_speeches(url):
    print url
    html = requests.get(url).text
    root = lxml.html.fromstring(html)
    record = {}   
    try:
        record['old_url'] = url
        record['title'] = root.xpath('//div[@class="cms heading"]/h1')[0].text
        if root.xpath('//div[@class="cms text"]')[1]:
            body = root.xpath('//div[@class="cms text"]')[1]
            record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(body))
        else:
            bodys = root.xpath('//div[@class="cms text"]')
            for body in bodys:
                if len(body.text_content())>50:
                    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(body))
    
        date_or_type = root.xpath('//div[@class="cms text"]')[0]
        h2_or_h3 = date_or_type.xpath('h2 | h3')
        for x in h2_or_h3:
            try:
                r = date_check.search(x.text.strip())
                if r:
                    record['date'] = x.text.strip()
                    record['date_iso'] = dateutil.parser.parse(record['date'], dayfirst=True).date().isoformat()
            except:
                pass
            else:
                if 'against' in x.text:
                    record['type'] = x.text.strip()

    except:
         record['check'] = 1 
    scraperwiki.sqlite.save(["old_url"], record, "speeches")

def Speeches():
    #scraperwiki.sqlite.execute("drop table if exists publications")
    url = 'http://www.decc.gov.uk/en/News/Categories.aspx?CategoryID=28&PageNumber=0&ResultsOnPage=100' # all speeches on one page
    html = requests.get(url).text
    root = lxml.html.fromstring(html)
    resultlinks = root.xpath('//ol[@class="search-results"]//a')
    for resultlink in resultlinks:
        parse_speeches('http://decc.gov.uk'+resultlink.attrib['href'])
    #parse_publications(results)
    


    
#scraperwiki.sqlite.execute("drop table if exists publications")
#scraperwiki.sqlite.save_var('last_page',1) 
#last_page = scraperwiki.sqlite.get_var('last_page')
#Publications(last_page)

#scraperwiki.sqlite.execute("drop table if exists speeches")
Speeches()
