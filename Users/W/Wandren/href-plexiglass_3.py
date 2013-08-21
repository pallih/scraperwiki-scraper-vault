import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep
import random

urls = [


'http://zarnegar.blogfa.com',
'http://zaruee.blogfa.com',
'http://z-asghari.blogfa.com',
'http://zavieedid-8.blogfa.com',
'http://zdparizi.blogfa.com',
'http://zehne-ghatre.blogfa.com',
'http://zehneziba16.blogfa.com',
'http://zeinabtavagho.blogfa.com',
'http://zemzehayeshabane.blogfa.com',
'http://zenab59.blogsky.com',
'http://zende-bad-bahar.blogfa.com',
'http://zeynab-basij.blogfa.com',
'http://zhgh.parsiblog.com',
'http://zibatarinshakib.blogfa.com',
'http://zimegrat.blogfa.com',
'http://zion-islam.persianblog.ir',
'http://zionism.blogfa.com',
'http://znukhatesevom.ParsiBlog.com',
'http://zoboni.blogfa.com',
'http://zoboralhadid.mihanblog.com',
'http://zoha91zohour.blogfa.com',
'http://zohoor1.blogfa.com',
'http://zohoor-mahdi.blogfa.com',
'http://zohore-u.blogfa.com',
'http://zohour.mihanblog.com',
'http://zohreh2000.blogfa.com',
'http://zolfesokhan.persianblog.ir',
'http://zolfyar.blogfa.com',
'http://zurkhanehbabaali.ParsiBlog.com',
'http://zvm.parsiblog.com',
'http://zzz135.ParsiBlog.com',
'http://www.che-he.blogfa.com',
'http://www.montazergraph.ir',




]


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
