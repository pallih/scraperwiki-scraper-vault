import scraperwiki
import sys, httplib2, urllib, re
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
        data['key'] = '%s-%s-%s' % (r[0].text, r[1].text, r[2].text)
        data['country'] = r[0].text
        data['province'] = r[1].text
        data['city'] = r[2].text
        scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database


def data_prep(content):#function to grab urls
    #print content
    records = []
    doc = lxml.html.document_fromstring(content)
    datas = doc.cssselect('font.item_data_style')
    records = chunks(datas, 3)
    return scrape(records)


def page_load(url): #function to scrape page
    link = []
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(content)

urls = ['http://www.humuch.com/prices/Bananas/______/22']

for u in urls:
    page_load(u)
    sleep(1)

import scraperwiki
import sys, httplib2, urllib, re
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
        data['key'] = '%s-%s-%s' % (r[0].text, r[1].text, r[2].text)
        data['country'] = r[0].text
        data['province'] = r[1].text
        data['city'] = r[2].text
        scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database


def data_prep(content):#function to grab urls
    #print content
    records = []
    doc = lxml.html.document_fromstring(content)
    datas = doc.cssselect('font.item_data_style')
    records = chunks(datas, 3)
    return scrape(records)


def page_load(url): #function to scrape page
    link = []
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(content)

urls = ['http://www.humuch.com/prices/Bananas/______/22']

for u in urls:
    page_load(u)
    sleep(1)

