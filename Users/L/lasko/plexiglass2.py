import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep
import random


urls = [
'http://shahidman.persianblog.ir',
'http://www.man-amar.blogfa.com',
'http://szareiorg.blogfa.com',
'http://hajmohammad.ir',
'http://infinity.hasanalmasi.ir',
'http://1175.blogfa.com',
'http://antimosalasizm.blogfa.com',
'http://elysian313.blogfa.com',
'http://moradian.info',
'http://nishkhand.blogfa.com',
'http://shbesf.persianblog.ir',
'http://mazloomin.mihanblog.com',
'http://meysamrashidi.blogfa.com',
'http://zolfaqar.ir',
'http://a3moony.blogfa.com',
'http://www.sokhan-kootah.blogfa.com',
'http://www.shahryari1404.blogfa.com',
'http://bohran.blogfa.com',
'http://tashackol.blogfa.com',
'http://www.bahmaneyar.blogfa.com',
'http://takhodaaaaaaa.blogfa.com',
'http://hadihamidi62.blogfa.com',
'http://ghafer.blogfa.com',
'http://sahel-oftadeh.blogsky.com',
'http://parsnevesht.blogfa.com',
'http://shahabadi.blogfa.com',
'http://www.sarir209.com',
'http://sobhh.blogfa.com',
'http://www.2yavar.mihanblog.com',
'http://www.nadafie.persianblog.ir',
'http://www.dart.vcp.ir',
'http://nojoki.blogfa.com',
'http://ghobarfetneh.mihanblog.com',
'http://mahdi-kh.persianblog.ir',
'http://m-yavaran.blogfa.com',
'http://pelakehasht.blogfa.com',
'http://mostafamobin.blogfa.com',
'http://javanemruz.persianblog.ir',
'http://www.mabar10.blogfa.com',
'http://www.faran133.blogfa.com',
'http://www.avami.blogfa.com',
'http://dustdar.blogfa.com',
'http://www.shaheid.blogfa.com',
'http://bazm.blogfa.com',
'http://was.blogfa.com',
'http://meshkinimehdi.blogfa.com',
'http://zarnegar.blogfa.com',
'http://aghaliyat.blogfa.com',
'http://dardnameh.mihanblog.com',
'http://30rat.blogfa.com',
'http://agajan.blogfa.com',
'http://chamraniha.blogfa.com',
'http://logical.blogfa.com',
'http://montazergraph.blog.ir',
'http://sadeghonline.mihanblog.com',
'http://shamsayi.blogfa.com',
'http://www.ahestan.ir',
'http://davodabadi.blogfa.com',
'http://yaminpour.ir/fa',
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