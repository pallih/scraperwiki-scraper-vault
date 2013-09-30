import scraperwiki
from lxml import etree
import time
import urllib

base = "http://www.quotedb.com/quotes/"



def GetPage(index):
    #http://www.quotedb.com/quotes/3987

    url = base + str(index)
    page = urllib.urlopen(url).read()
    return page
    
def GetQuotesFromDb(page):
    x = etree.HTML(page)
    quote = x.xpath("string(//input[@name='text']/@value)")
    author = x.xpath("string((//font[@class='text'])[3]/b/text())")
    category = x.xpath("string((//font[@class='text'])[4]/a/text())")
    res = {}
    res['quote'] = quote
    res['author'] = author
    res['category'] = category
    return res
    
for i in range(1004, 1009):
    page = GetPage(i)
    id1 = str(i)
    time.sleep(2)
    scraperwiki.sqlite.save(['quote'],'quote')
    print i, GetQuotesFromDb(page)['quote']
#    print '\n\n'

import scraperwiki
from lxml import etree
import time
import urllib

base = "http://www.quotedb.com/quotes/"



def GetPage(index):
    #http://www.quotedb.com/quotes/3987

    url = base + str(index)
    page = urllib.urlopen(url).read()
    return page
    
def GetQuotesFromDb(page):
    x = etree.HTML(page)
    quote = x.xpath("string(//input[@name='text']/@value)")
    author = x.xpath("string((//font[@class='text'])[3]/b/text())")
    category = x.xpath("string((//font[@class='text'])[4]/a/text())")
    res = {}
    res['quote'] = quote
    res['author'] = author
    res['category'] = category
    return res
    
for i in range(1004, 1009):
    page = GetPage(i)
    id1 = str(i)
    time.sleep(2)
    scraperwiki.sqlite.save(['quote'],'quote')
    print i, GetQuotesFromDb(page)['quote']
#    print '\n\n'

