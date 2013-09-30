import scraperwiki

import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep



def scrape(key, content, category): 
    for r in content:
        data = {}
        data['key'] = '%s-%s' % (r[1], key)
        data['category'] = category
        data['url'] = r[0]
        data['rank'] = r[1]
        data['site'] = r[2]
#        data['rank'] = r[0]
#        data['url'] = r[1]
        scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database


def data_prep(key, content, category):#function to grab urls
    records = []
    doc = etree.parse(StringIO(content), parser=etree.HTMLParser(encoding='utf-8'))
    for num in range(1,25):
#        xpath_test = '//*[@id="topsites-category"]/ul/li'
        xpath_string_rank = '//*[@id="topsites-category"]/ul/li[%d]/div[1]' % (num)
        xpath_string_site = '//*[@id="topsites-category"]/ul/li[%d]/div[2]/h2/a'  % (num)
        xpath_string_url = '//*[@id="topsites-category"]/ul/li[%d]/div[2]/span[@class="small topsites-label"]'  % (num)
#        print etree.tostring(doc.xpath(xpath_test)[0])
#        records += [(doc.xpath(xpath_string_rank)[0].text, doc.xpath(xpath_string_url)[0].text)]
        if doc.xpath(xpath_string_url): 
            doc_url = doc.xpath(xpath_string_url)[0].text
            doc_rank = doc.xpath(xpath_string_rank)[0].text
            doc_site = doc.xpath(xpath_string_site)[0].text
            records += [(doc_url, doc_rank , doc_site)]

    #for r in records:
        #print r
    return scrape(key, records, category)


def page_load(key, category,page): #function to scrape page
    link = []
    url = "http://www.alexa.com/topsites/category%s/%s" % (page,category)
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(key, content, category)

category = {"persian" : "Top/World/Persian", "news" : "Top/World/Persian/اخبار"}

pages = ["", ";1", ";2", ";3", ";4", ";5", ";6", ";7", ";8", ";9", ";10", ";11", ";12", ";13", ";14", ";15", ";16", ";17", ";18", ";19", ";20"] 

for k, c in category.items():
    for p in pages:
        page_load(k, c,p)
        sleep(1)




import scraperwiki

import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep



def scrape(key, content, category): 
    for r in content:
        data = {}
        data['key'] = '%s-%s' % (r[1], key)
        data['category'] = category
        data['url'] = r[0]
        data['rank'] = r[1]
        data['site'] = r[2]
#        data['rank'] = r[0]
#        data['url'] = r[1]
        scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database


def data_prep(key, content, category):#function to grab urls
    records = []
    doc = etree.parse(StringIO(content), parser=etree.HTMLParser(encoding='utf-8'))
    for num in range(1,25):
#        xpath_test = '//*[@id="topsites-category"]/ul/li'
        xpath_string_rank = '//*[@id="topsites-category"]/ul/li[%d]/div[1]' % (num)
        xpath_string_site = '//*[@id="topsites-category"]/ul/li[%d]/div[2]/h2/a'  % (num)
        xpath_string_url = '//*[@id="topsites-category"]/ul/li[%d]/div[2]/span[@class="small topsites-label"]'  % (num)
#        print etree.tostring(doc.xpath(xpath_test)[0])
#        records += [(doc.xpath(xpath_string_rank)[0].text, doc.xpath(xpath_string_url)[0].text)]
        if doc.xpath(xpath_string_url): 
            doc_url = doc.xpath(xpath_string_url)[0].text
            doc_rank = doc.xpath(xpath_string_rank)[0].text
            doc_site = doc.xpath(xpath_string_site)[0].text
            records += [(doc_url, doc_rank , doc_site)]

    #for r in records:
        #print r
    return scrape(key, records, category)


def page_load(key, category,page): #function to scrape page
    link = []
    url = "http://www.alexa.com/topsites/category%s/%s" % (page,category)
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(key, content, category)

category = {"persian" : "Top/World/Persian", "news" : "Top/World/Persian/اخبار"}

pages = ["", ";1", ";2", ";3", ";4", ";5", ";6", ";7", ";8", ";9", ";10", ";11", ";12", ";13", ";14", ";15", ";16", ";17", ";18", ";19", ";20"] 

for k, c in category.items():
    for p in pages:
        page_load(k, c,p)
        sleep(1)




