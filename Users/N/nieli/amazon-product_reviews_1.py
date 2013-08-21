import scraperwiki
import os
import csv
import urllib
import lxml.html
import sys

def get_url(url):    
    return urllib.urlopen(url).read()
    
def parse(url):
    urls = url
    tree = lxml.html.fromstring(get_url(urls))
    result = {}
    titles = []
    
    for rowTitle in tree.xpath('//table[@id="productReviews"]/tr/td/div/text()'):
        
        if len(rowTitle.strip())>0:            
            print rowTitle
    
    
    for rowP in tree.xpath('//table[@class="CMheadingBar"][position()=1]/tr/td/div[@class="CMpaginate"]/span[@class="paging"]/*'):
        print "??"+rowP.text_content().strip().encode('utf-8')
        print rowP
        print rowP.getparent().xpath('./a')
        lenA = len(rowP.getparent().xpath('./a'))
        t = 0
        print lenA
        if rowP.getparent().xpath('./a')[0]==rowP:
            print "&&&&"
        if rowP.get('href'):
            print "##"+rowP.get('href')
        else:
            print "no href"
            print (rowP.getparent().xpath('./a')[lenA -1]).get('href')
        
        
        if "Next" in (rowP.getparent().xpath('./a')[lenA -1]).text_content().strip().encode('utf-8'):
            print "not last page"
            #print (rowP.getparent().xpath('./a')[lenA -1]).text_content().strip().encode('utf-8')
            print (rowP.getparent().xpath('./a')[lenA -1]).get('href')
            i = 1
        else:
            print "last page"
            i = 0

    if i==1:
        parse((rowP.getparent().xpath('./a')[lenA -1]).get('href'))
            
        

urla = str('http://www.amazon.com/Xbox-360-250GB-Racing-Bundle/product-reviews/B0082SICGQ')
parse(urla)
# Blank Python

