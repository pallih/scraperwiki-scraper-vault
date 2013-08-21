# -*- coding: utf-8 -*-
# I've never used lxml before, only BeautifulSoup, so this is mye first flirt with xpath
import re, sys
import scraperwiki
import lxml.html
import dateutil.parser 
import datetime 

"""
Urls for scraping
"""
urls = ["http://p3.no/filmpolitiet/category/spillanmeldelser/terningkast-6/","http://p3.no/filmpolitiet/category/spillanmeldelser/terningkast-5/","http://p3.no/filmpolitiet/category/spillanmeldelser/terningkast-4/","http://p3.no/filmpolitiet/category/spillanmeldelser/terningkast-3/","http://p3.no/filmpolitiet/category/spillanmeldelser/terningkast-2/", "http://p3.no/filmpolitiet/category/spillanmeldelser/terningkast-1/"]

def getDateSorted(string):
    '''function to convert norwegian full month name dates to a more computer friendly format. Returns date object'''
    no_months = {'januar': '01', 'februar': '02', 'mars': '03', 'april': '04', 'mai':'05', 'juni':'06', 'juli':'07', 'august':'08', 'september':'09', 'oktober':'10','november':'11', 'desember': '12'}
    dag = string.split(".")[0]
    #print string.split(" ")[1].replace(',', '').lower()
    month = no_months.get(string.split(" ")[1].replace(',', '').lower())
    year = string.split(",")[1].strip()
    dato = str(dag) + "/" + str(month)+ "/" +str(year)
    #print dato
    date = datetime.datetime.strptime(dato, '%d/%m/%Y').date()
    return date

#print getDateSorted("1. mars, 2012")
#print getDateSorted("18. november, 2011")
#print getDateSorted("9. september, 2011")    

"""
Scraping
"""

for url in urls:
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    #print root
    reviews = root.xpath("//div[contains(@class, 'fp-search-item')]")    
    #print reviews
    #print len(reviews)
    for review in reviews:
        #print review
        data = {}
        data['title'] = review.xpath("div/h3/a/text()")[0] #.split("'")[1]
        data['date'] = getDateSorted(str(review.xpath("div/small/text()")).split("'")[1])
        data['verdict'] = str(review.xpath("div/a/span/text()")).split("'")[1][-1]
        data['url'] = str(review.xpath("div/h3/a/@href")).split("'")[1]
        
        data['hook'] = review.xpath("div/p/text()")[0]
        #data['hook'] = review.xpath("div/p/text()") #.split("'")[1]
        #print data['hook']
        #data['hook'] = str(review.xpath("div/p/text()")).split("'")[1]
        #data['hook'].encode('utf8')
        #print lxml.html.tostring(review, pretty_print=True)
        #print data['hook'].encode('utf-8')
        scraperwiki.sqlite.save(unique_keys=['title','url'], data=data)
        #print data['title']
    #sys.exit("end here")



