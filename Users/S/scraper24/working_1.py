import scraperwiki
import xml.dom.minidom
import os
import csv
import urllib
import lxml.html
import lxml.cssselect
import sys
import codecs
import datetime

def get_url(url):
    return urllib.urlopen(url).read()
    
def parse(url,k):
    urls = url
    tree = lxml.html.fromstring(get_url(urls))
    result = {}
    titles = []
    i = k+1

    # for rowProd in tree.xpath("//div[@id='atfResults']"):

    #     for rowSp in rowProd.xpath(".//div[@id='result_1']"):
    #         print "hello"+rowSp.get('name')
        # if rowProd.get('id'):
        #      if 'result_' in rowProd.get('id'):                
        #          if rowProd.get('class'):
        #              if 'prod' in rowProd.get('class'):
        #                  print rowProd.get('id')+':'+rowProd.get('class')
        
        # for rowSp in rowProd.xpath('.//span'):
        #     print rowSp.text_content().strip()    span[@class='lrg bold']
    
    for rowSp in tree.xpath("//div"):        
        if rowSp.get('id'):
            if 'result_' in rowSp.get('id'):
                print rowSp.get('href')
                for rowA in rowSp.xpath("./div/a"):
                    #print 99
                    now = datetime.datetime.now()
                   # for product_span in rowSp.xpath("./a/span")
                   #     product_name = product_span.get('title')
                   # for manufacturer_span in rowSp.xpath("./div")
                   #     manufacturer = manufacturer_span.text()
                        
                    data = {
                        'product_link': rowA.get('href'),
                    #    'product_name': product_name,
                    #    'manufacturer': manufacturer,
                        'ExtractDate': str(now) ,
                    }
                    scraperwiki.sqlite.save(unique_keys=['product_link'],data=data)
                    #print rowA.get('href')
                    
                    #wr.writerow([rowA.get('href')])


    for rowNxp in tree.xpath('//div[@id="pagn"]'):
        
        if len(rowNxp.xpath('.//a[@class="pagnNext"]'))>0:
            for rowNext in rowNxp.xpath('.//a[@class="pagnNext"]'):                
                if rowNext.get('class'):
                    print "Page Number" + str(i)+rowNext.get('href')
                    parse(rowNext.get('href'),i)
                    

        else:
            print "last page"+str(i)
            
#url can be assigned for any product; link of 1st page out of 20 
url = "http://www.amazon.com/s/ref=sr_st?keywords=peter+pan+collar&qid=1366648363&rh=n%3A1036592%2Cn%3A!1036682%2Cn%3A1040660%2Cn%3A2368343011%2Ck%3Apeter+pan+collar&sort=price"
global i
i = 0
#resultFile = open("output.csv",'wb')
#wr = csv.writer(resultFile, delimiter=',',quoting=csv.QUOTE_ALL)
parse(url,i)



# Blank Python

import scraperwiki
import xml.dom.minidom
import os
import csv
import urllib
import lxml.html
import lxml.cssselect
import sys
import codecs
import datetime

def get_url(url):
    return urllib.urlopen(url).read()
    
def parse(url,k):
    urls = url
    tree = lxml.html.fromstring(get_url(urls))
    result = {}
    titles = []
    i = k+1

    # for rowProd in tree.xpath("//div[@id='atfResults']"):

    #     for rowSp in rowProd.xpath(".//div[@id='result_1']"):
    #         print "hello"+rowSp.get('name')
        # if rowProd.get('id'):
        #      if 'result_' in rowProd.get('id'):                
        #          if rowProd.get('class'):
        #              if 'prod' in rowProd.get('class'):
        #                  print rowProd.get('id')+':'+rowProd.get('class')
        
        # for rowSp in rowProd.xpath('.//span'):
        #     print rowSp.text_content().strip()    span[@class='lrg bold']
    
    for rowSp in tree.xpath("//div"):        
        if rowSp.get('id'):
            if 'result_' in rowSp.get('id'):
                print rowSp.get('href')
                for rowA in rowSp.xpath("./div/a"):
                    #print 99
                    now = datetime.datetime.now()
                   # for product_span in rowSp.xpath("./a/span")
                   #     product_name = product_span.get('title')
                   # for manufacturer_span in rowSp.xpath("./div")
                   #     manufacturer = manufacturer_span.text()
                        
                    data = {
                        'product_link': rowA.get('href'),
                    #    'product_name': product_name,
                    #    'manufacturer': manufacturer,
                        'ExtractDate': str(now) ,
                    }
                    scraperwiki.sqlite.save(unique_keys=['product_link'],data=data)
                    #print rowA.get('href')
                    
                    #wr.writerow([rowA.get('href')])


    for rowNxp in tree.xpath('//div[@id="pagn"]'):
        
        if len(rowNxp.xpath('.//a[@class="pagnNext"]'))>0:
            for rowNext in rowNxp.xpath('.//a[@class="pagnNext"]'):                
                if rowNext.get('class'):
                    print "Page Number" + str(i)+rowNext.get('href')
                    parse(rowNext.get('href'),i)
                    

        else:
            print "last page"+str(i)
            
#url can be assigned for any product; link of 1st page out of 20 
url = "http://www.amazon.com/s/ref=sr_st?keywords=peter+pan+collar&qid=1366648363&rh=n%3A1036592%2Cn%3A!1036682%2Cn%3A1040660%2Cn%3A2368343011%2Ck%3Apeter+pan+collar&sort=price"
global i
i = 0
#resultFile = open("output.csv",'wb')
#wr = csv.writer(resultFile, delimiter=',',quoting=csv.QUOTE_ALL)
parse(url,i)



# Blank Python

