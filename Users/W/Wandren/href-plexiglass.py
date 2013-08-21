import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep
import random

urls = [

'http://nahrekhayen.blogfa.com',
'http://nahri.ir',
'http://naje-upload.ir',
'http://najmodin.parsiblog.com',
'http://najvabato.blogfa.com',
'http://najvabesabkema.blogfa.com',
'http://najvayedadar.blogfa.com',
'http://najvayeshabaane.parsiblog.com',
'http://najvayeshabane.blogfa.com',
'http://nakhile.blogfa.com',
'http://nakhl.blogfa.com',
'http://namahramane.blogsky.com',
'http://namak.wordpress.com',
'http://namakdoon110.blogfa.com',
'http://namakgir.blogfa.com',
'http://namaknews.ir',
'http://namaz-pray.blogsky.com',
'http://namehamin.blogfa.com',
'http://namira.blog.ir',
'http://namna.ir',
'http://nap-sh.blogfa.com',
'http://naragh313.blogfa.com',
'http://naranjak.blogfa.com',
'http://nardebanekhial.blogfa.com',
'http://nargesi.blogfa.com',
'http://narjes.blogfa.com',
'http://nasehin89.blogfa.com',
'http://naser18621.blogfa.com',
'http://nasim.ParsiBlog.com',
'http://nasime90.blogfa.com',
'http://nasimemahdi.blogfa.com',
'http://nasimesobhgahan.blogfa.com',
'http://nasimhayat.blogfa.com',
'http://nasiri1342.blogfa.com',
'http://nasle2vom.persianblog.ir',
'http://nasle3vomi.blogspot.com',
'http://nasle-bidar.blogfa.com',
'http://naslejavane90.mihanblog.com',
'http://naslemoharam.blogfa.com',
'http://naslvasel.blogfa.com',
'http://nasrclub.com',
'http://nasrnews.ir',
'http://natenamak.blogfa.com',
'http://navabiyan.blogfa.com'
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
