# multiple URLs all 16"

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re


def FindURLs(URLWITHLIST):
    html = scraperwiki.scrape(URLWITHLIST)
    
    soup = BeautifulSoup(html)
    
    divs = soup.findAll('div') 
    for div in divs :
        try:
            if div['class'] == 'subCategoryEntry' :
                hrefs = div.findAll('a')
                
                for href in hrefs:
                    print href['href']
                    ScrapeURL('http://www.retailmenot.com' + href['href'])
        except:
            print "Not Correct Class"
    
def ScrapeURL(URL2SCRAPE):
    html = scraperwiki.scrape(URL2SCRAPE)
    
    soup = BeautifulSoup(html)
    
    tds = soup.findAll('td') 
    for td in tds:
    
        ProdID = '-1'
        ProdName = '-1'
        ProdPrice = '-1'
    
        inputs = td.findAll('input')
    
        for input in inputs :
            if input['name'] == 'productName':
                ProdName = input['value']
            if input['name'] == 'productPrice':
                ProdPrice = input['value']
            if input['name'] == 'productID':
                ProdID = input['value']
    
        if ProdName != '-1' :
            if ProdPrice != '-1' :
                if ProdID != '-1' :
                    record = { "row" : ProdID + ', ' + ProdName + ', ' + ProdPrice} # column name and value
                    scraperwiki.datastore.save(["row"], record) # save the records one by one
                    print ProdID + ', ' + ProdName + ', ' + ProdPrice
            



urllist = '/'
baseurl = 'http://www.retailmenot.com'
FindURLs(baseurl + urllist)

# multiple URLs all 16"

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re


def FindURLs(URLWITHLIST):
    html = scraperwiki.scrape(URLWITHLIST)
    
    soup = BeautifulSoup(html)
    
    divs = soup.findAll('div') 
    for div in divs :
        try:
            if div['class'] == 'subCategoryEntry' :
                hrefs = div.findAll('a')
                
                for href in hrefs:
                    print href['href']
                    ScrapeURL('http://www.retailmenot.com' + href['href'])
        except:
            print "Not Correct Class"
    
def ScrapeURL(URL2SCRAPE):
    html = scraperwiki.scrape(URL2SCRAPE)
    
    soup = BeautifulSoup(html)
    
    tds = soup.findAll('td') 
    for td in tds:
    
        ProdID = '-1'
        ProdName = '-1'
        ProdPrice = '-1'
    
        inputs = td.findAll('input')
    
        for input in inputs :
            if input['name'] == 'productName':
                ProdName = input['value']
            if input['name'] == 'productPrice':
                ProdPrice = input['value']
            if input['name'] == 'productID':
                ProdID = input['value']
    
        if ProdName != '-1' :
            if ProdPrice != '-1' :
                if ProdID != '-1' :
                    record = { "row" : ProdID + ', ' + ProdName + ', ' + ProdPrice} # column name and value
                    scraperwiki.datastore.save(["row"], record) # save the records one by one
                    print ProdID + ', ' + ProdName + ', ' + ProdPrice
            



urllist = '/'
baseurl = 'http://www.retailmenot.com'
FindURLs(baseurl + urllist)

