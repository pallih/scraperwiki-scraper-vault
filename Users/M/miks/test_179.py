import scraperwiki
import sys, httplib2, urllib, re, random
from lxml import etree
import lxml.html
from StringIO import StringIO
from time import sleep


def chunks(l, n):
    ''' 
    http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    '''
    return [l[i:i+n] for i in range(0, len(l), n)]


def scrape(records): 
    for r in records:
        data = {}
        data['key'] = random.random()
        data['Item'] = r[0].text
        data['price'] = r[1].text
        #print r[0].text, r[1].text
        #print records.text
        scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database
#once you have the raw data the scrape creates a spreadsheet
#spreadsheet is made of key and value
#they can be called anything after key

def data_prep(content):#function to grab urls
    #print content
    records = []
    doc = lxml.html.document_fromstring(content)
    datas = doc.cssselect('td')
    #datas = datas[5:]
    #records = chunks(datas, 3)
    #unhash print records and add hash to return to test what array you are calling
    print datas[7].text
    for r in datas:
        print r.text
    #return scrape(records)

def page_load(url): #function to scrape page
    link = []
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(content)

#if response is 200 (it's cool), if not 200 then error is returned


urls = ['http://www.expatistan.com/cost-of-living/dar-es-salaam']

for u in urls:
    page_load(u)
    sleep(1)




import scraperwiki
import sys, httplib2, urllib, re, random
from lxml import etree
import lxml.html
from StringIO import StringIO
from time import sleep


def chunks(l, n):
    ''' 
    http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    '''
    return [l[i:i+n] for i in range(0, len(l), n)]


def scrape(records): 
    for r in records:
        data = {}
        data['key'] = random.random()
        data['Item'] = r[0].text
        data['price'] = r[1].text
        #print r[0].text, r[1].text
        #print records.text
        scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database
#once you have the raw data the scrape creates a spreadsheet
#spreadsheet is made of key and value
#they can be called anything after key

def data_prep(content):#function to grab urls
    #print content
    records = []
    doc = lxml.html.document_fromstring(content)
    datas = doc.cssselect('td')
    #datas = datas[5:]
    #records = chunks(datas, 3)
    #unhash print records and add hash to return to test what array you are calling
    print datas[7].text
    for r in datas:
        print r.text
    #return scrape(records)

def page_load(url): #function to scrape page
    link = []
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(content)

#if response is 200 (it's cool), if not 200 then error is returned


urls = ['http://www.expatistan.com/cost-of-living/dar-es-salaam']

for u in urls:
    page_load(u)
    sleep(1)




