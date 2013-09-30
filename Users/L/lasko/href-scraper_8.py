import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep
import random


urls = ['http://www.google.com','http://www.sjidjaiodjaid.com','http://www.richmanmax.com']


def data_load(hrefs, url): #Function to store data in sqlite database
    for href in hrefs:
        data = {}
        data['hrefs'] = href
        data['url'] = url
        data['key'] = random.random()
        scraperwiki.sqlite.save(['key'], data) 


def href_find(content, url):#function to grab hrefs
    hrefs = re.findall(r'''href=[\'"]?([^\'" >]+)''', content)
    return data_load(hrefs, url)


def page_load(url): #function to scrape websites
    h = httplib2.Http(".cache")
    try:
        response, content = h.request(url, "GET")
    except: 
        pass
    return href_find(content, url)


for url in urls:
    page_load(url)
    sleep(1)

import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep
import random


urls = ['http://www.google.com','http://www.sjidjaiodjaid.com','http://www.richmanmax.com']


def data_load(hrefs, url): #Function to store data in sqlite database
    for href in hrefs:
        data = {}
        data['hrefs'] = href
        data['url'] = url
        data['key'] = random.random()
        scraperwiki.sqlite.save(['key'], data) 


def href_find(content, url):#function to grab hrefs
    hrefs = re.findall(r'''href=[\'"]?([^\'" >]+)''', content)
    return data_load(hrefs, url)


def page_load(url): #function to scrape websites
    h = httplib2.Http(".cache")
    try:
        response, content = h.request(url, "GET")
    except: 
        pass
    return href_find(content, url)


for url in urls:
    page_load(url)
    sleep(1)

