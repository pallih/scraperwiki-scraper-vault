import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep
import random


urls = ['http://sobh.com',
'http://sobh.org',
'http://sobhesadegh.ir',
'http://sobh-o-setare.persianblog.ir',
'http://socialreporter.persianblog.ir',
'http://sodaidel.blogfa.com',
'http://soim.ir',
'http://sokutesabz110.blogfa.com',
'http://solarhome.org',
'http://solokegomnami.blogfa.com',
'http://soltaneerteza.blogfa.com',
'http://soltanesolouk.blogfa.com',
'http://soor.ir',
'http://soozanban.parsiblog.com',
'http://soozesokhan.blogfa.com',
'http://soros.org',
'http://sourehcinema.com',
'http://souzanchi.ir',
'http://sportsman1.blogfa.com',
'http://spy.blogfa.com',
'http://spypig.com',
'http://s-s-m.blogfa.com',
'http://stanhaaa.blogfa.com',
'http://startinglife.blogfa.com',
'http://statcounter.com',
'http://stubasij.blogfa.com',
'http://success13.blogfa.com',
'http://suldoz.ir',
'http://supermonharef.blogdoon.com',
'http://swat-133.blogfa.com',
'http://taamolnews.ir',
'http://tababa.blogfa.com',
'http://tabligheirani.com',
'http://tabnak.com',
'http://tabnak.ir',
'http://tabrizcartoons.com',
'http://tadavom.koolebar.ir',
'http://tahajomnarm.blogfa.com',
'http://taherehomidi.blogfa.com',
'http://tahlilpress.com',
'http://tajaliazam.blogfa.com',
'http://tajaliyenoor.blogfa.com',
'http://tajasomi.ir',
'http://takafsar.blogfa.com',
'http://takdid.com',
'http://taklearn.ir',
'http://talabeh.net',
'http://talatejan.blogfa.com',
'http://taleblo.blogfa.com',
'http://talkhandak.blogfa.com',
'http://tamarzejonoon.mypersianblog.com',
'http://tanhaapanaah.blogfa.com',
'http://tanhatarinetanhayan.blogsky.com',
'http://tarannomehekmat.blogfa.com',
'http://tardidnak.blogfa.com',
'http://tarik.ir'

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
    sleep(2)import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep
import random


urls = ['http://sobh.com',
'http://sobh.org',
'http://sobhesadegh.ir',
'http://sobh-o-setare.persianblog.ir',
'http://socialreporter.persianblog.ir',
'http://sodaidel.blogfa.com',
'http://soim.ir',
'http://sokutesabz110.blogfa.com',
'http://solarhome.org',
'http://solokegomnami.blogfa.com',
'http://soltaneerteza.blogfa.com',
'http://soltanesolouk.blogfa.com',
'http://soor.ir',
'http://soozanban.parsiblog.com',
'http://soozesokhan.blogfa.com',
'http://soros.org',
'http://sourehcinema.com',
'http://souzanchi.ir',
'http://sportsman1.blogfa.com',
'http://spy.blogfa.com',
'http://spypig.com',
'http://s-s-m.blogfa.com',
'http://stanhaaa.blogfa.com',
'http://startinglife.blogfa.com',
'http://statcounter.com',
'http://stubasij.blogfa.com',
'http://success13.blogfa.com',
'http://suldoz.ir',
'http://supermonharef.blogdoon.com',
'http://swat-133.blogfa.com',
'http://taamolnews.ir',
'http://tababa.blogfa.com',
'http://tabligheirani.com',
'http://tabnak.com',
'http://tabnak.ir',
'http://tabrizcartoons.com',
'http://tadavom.koolebar.ir',
'http://tahajomnarm.blogfa.com',
'http://taherehomidi.blogfa.com',
'http://tahlilpress.com',
'http://tajaliazam.blogfa.com',
'http://tajaliyenoor.blogfa.com',
'http://tajasomi.ir',
'http://takafsar.blogfa.com',
'http://takdid.com',
'http://taklearn.ir',
'http://talabeh.net',
'http://talatejan.blogfa.com',
'http://taleblo.blogfa.com',
'http://talkhandak.blogfa.com',
'http://tamarzejonoon.mypersianblog.com',
'http://tanhaapanaah.blogfa.com',
'http://tanhatarinetanhayan.blogsky.com',
'http://tarannomehekmat.blogfa.com',
'http://tardidnak.blogfa.com',
'http://tarik.ir'

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
    sleep(2)