#This one scrapes the top 200 list

import scraperwiki
import lxml.html
import decimal
import urlparse
import string
import urllib2
import time

ID = 1




##############################################################################


# scrapeScore takes 2 urls url1/url2 and stores the name and average score
  
def scrapeScore(url, url2):
    
    Rurl, Rurl2 = loadUrl(url, url2)
    
    #html = scraperwiki.scrape(url)
    #html2 = scraperwiki.scrape(url2)

    root = lxml.html.fromstring(Rurl)
    root2 = lxml.html.fromstring(Rurl2)

    titleTag = root.cssselect('title') #finds name of hotel on page
    for name in titleTag:
        hotelName = name.text
        #print hotelName
        
        global ID
        #print ID
        
        
    values = root.cssselect('img') #take img tags
    total = 0
    average = 0
    L = []

    for img in values:
    
    
        if img.get('content') != None: #ignore all images with no 'content' attribute

            #print img.get('content')  #print the contents of 'content' (a number)
        
            score = float(img.get('content'))
            L.append(score)
            total = total + score
        

    del L[11:] #take first 11 numbers
    del L[:1] #1st number doesnt count

    average = sum(L)/10

    #print L
    #print average


    values2 = root2.cssselect('img') #take img tags
    total2 = 0
    average2 = 0
    L2 = []

    for img in values2:
    
    
        if img.get('content') != None: #ignore all images with no 'content' attribute

            #print img.get('content')  #print the contents of 'content' (a number)
        
            score2 = float(img.get('content'))
            L2.append(score)
            total2 = total2 + score2
        

    del L2[11:] #take first 11 numbers
    del L2[:1] #1st number doesnt count

    average2 = sum(L2)/10

    finalAverage = (average + average2)/2

    

    #print L2
    #print average2
    #print finalAverage

    



    scraperwiki.sqlite.save(unique_keys=["HotelName"], data={'HotelName':hotelName, 'Score':finalAverage, 'OverallPosition':ID}, table_name='scores')

    ID +=1


###############################################################################
# trying to handle random timeout error (may need to look at closing urllib)

def loadUrl(url, url2):
    
    retries = 3
    for i in range(retries):
        try:
            handle = scraperwiki.scrape(url)
            handle2 = scraperwiki.scrape(url2)
            return(handle, handle2)
        except urllib2.URLError:
            if i + 1 == retries:
                raise
            else:
                time.sleep(30)
    # never get here



##################################################################

#findUrl2 takes a url and finds the url of the next page (next 10 scores)

def findUrl2(htmlIN):
    
       
    html = scraperwiki.scrape(htmlIN)
    root = lxml.html.fromstring(html)

    #print html

    link = root.cssselect('a.guiArw')
    if link:
        for l in link:
            url2 = 'http://www.tripadvisor.co.uk/' + l.attrib.get('href')
            
            return url2
    else:
        return 'http://www.google.com' #we have to return something!


###################################################################


def urlIn(root):

    urlRoot = root.cssselect('div.quality a')

    for link in urlRoot:

        #print link.attrib['href']
        url = 'http://www.tripadvisor.co.uk' + link.attrib['href']       
        url2 = findUrl2(url)
        
        scrapeScore(url, url2)
        #loadUrl(url, url2)

##################################################################


#calls scrape (urlIn) function then finds the next link

def scrapeFindNext(nextUrl):

    html = scraperwiki.scrape(nextUrl)
    root = lxml.html.fromstring(html)

    urlIn(root) # calls urlIn function to scrape page of links
    nextLink = root.cssselect('a.guiArw.sprite-pageNext')

    if nextLink:
        nextUrl = urlparse.urljoin(baseUrl, nextLink[0].attrib.get('href'))

        scrapeFindNext(nextUrl)

########################################################################################

#need a function which takes the list of hotels and calls scrapefindnext for each link

def scrapeFindHotels(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    links = root.cssselect('span.dt2 a')

    for link in links:

        url = 'http://www.tripadvisor.co.uk' + link.attrib['href']
        scrapeFindNext(url)



#########################################################################################
#
#a function to take the a-z list and grabs list of hotels for each city
#
#def scrapeCityList(pageUrl):
#    html = scraperwiki.scrape(pageUrl)
#    root = lxml.html.fromstring(html)
#    links = root.cssselect('td.dt1 a')
#    
#    for link in links[1:]: 
#
#        url = 'http://www.tripadvisor.co.uk/pages/' + link.attrib['href']
#        print url
#        scrapeFindHotels(url)
#
########################################################################################

baseUrl = 'http://www.tripadvisor.co.uk/'





scrapeFindHotels('http://www.tripadvisor.co.uk/pages/citiesAM.html')
scrapeFindHotels('http://www.tripadvisor.co.uk/pages/citiesNZ.html')
#This one scrapes the top 200 list

import scraperwiki
import lxml.html
import decimal
import urlparse
import string
import urllib2
import time

ID = 1




##############################################################################


# scrapeScore takes 2 urls url1/url2 and stores the name and average score
  
def scrapeScore(url, url2):
    
    Rurl, Rurl2 = loadUrl(url, url2)
    
    #html = scraperwiki.scrape(url)
    #html2 = scraperwiki.scrape(url2)

    root = lxml.html.fromstring(Rurl)
    root2 = lxml.html.fromstring(Rurl2)

    titleTag = root.cssselect('title') #finds name of hotel on page
    for name in titleTag:
        hotelName = name.text
        #print hotelName
        
        global ID
        #print ID
        
        
    values = root.cssselect('img') #take img tags
    total = 0
    average = 0
    L = []

    for img in values:
    
    
        if img.get('content') != None: #ignore all images with no 'content' attribute

            #print img.get('content')  #print the contents of 'content' (a number)
        
            score = float(img.get('content'))
            L.append(score)
            total = total + score
        

    del L[11:] #take first 11 numbers
    del L[:1] #1st number doesnt count

    average = sum(L)/10

    #print L
    #print average


    values2 = root2.cssselect('img') #take img tags
    total2 = 0
    average2 = 0
    L2 = []

    for img in values2:
    
    
        if img.get('content') != None: #ignore all images with no 'content' attribute

            #print img.get('content')  #print the contents of 'content' (a number)
        
            score2 = float(img.get('content'))
            L2.append(score)
            total2 = total2 + score2
        

    del L2[11:] #take first 11 numbers
    del L2[:1] #1st number doesnt count

    average2 = sum(L2)/10

    finalAverage = (average + average2)/2

    

    #print L2
    #print average2
    #print finalAverage

    



    scraperwiki.sqlite.save(unique_keys=["HotelName"], data={'HotelName':hotelName, 'Score':finalAverage, 'OverallPosition':ID}, table_name='scores')

    ID +=1


###############################################################################
# trying to handle random timeout error (may need to look at closing urllib)

def loadUrl(url, url2):
    
    retries = 3
    for i in range(retries):
        try:
            handle = scraperwiki.scrape(url)
            handle2 = scraperwiki.scrape(url2)
            return(handle, handle2)
        except urllib2.URLError:
            if i + 1 == retries:
                raise
            else:
                time.sleep(30)
    # never get here



##################################################################

#findUrl2 takes a url and finds the url of the next page (next 10 scores)

def findUrl2(htmlIN):
    
       
    html = scraperwiki.scrape(htmlIN)
    root = lxml.html.fromstring(html)

    #print html

    link = root.cssselect('a.guiArw')
    if link:
        for l in link:
            url2 = 'http://www.tripadvisor.co.uk/' + l.attrib.get('href')
            
            return url2
    else:
        return 'http://www.google.com' #we have to return something!


###################################################################


def urlIn(root):

    urlRoot = root.cssselect('div.quality a')

    for link in urlRoot:

        #print link.attrib['href']
        url = 'http://www.tripadvisor.co.uk' + link.attrib['href']       
        url2 = findUrl2(url)
        
        scrapeScore(url, url2)
        #loadUrl(url, url2)

##################################################################


#calls scrape (urlIn) function then finds the next link

def scrapeFindNext(nextUrl):

    html = scraperwiki.scrape(nextUrl)
    root = lxml.html.fromstring(html)

    urlIn(root) # calls urlIn function to scrape page of links
    nextLink = root.cssselect('a.guiArw.sprite-pageNext')

    if nextLink:
        nextUrl = urlparse.urljoin(baseUrl, nextLink[0].attrib.get('href'))

        scrapeFindNext(nextUrl)

########################################################################################

#need a function which takes the list of hotels and calls scrapefindnext for each link

def scrapeFindHotels(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    links = root.cssselect('span.dt2 a')

    for link in links:

        url = 'http://www.tripadvisor.co.uk' + link.attrib['href']
        scrapeFindNext(url)



#########################################################################################
#
#a function to take the a-z list and grabs list of hotels for each city
#
#def scrapeCityList(pageUrl):
#    html = scraperwiki.scrape(pageUrl)
#    root = lxml.html.fromstring(html)
#    links = root.cssselect('td.dt1 a')
#    
#    for link in links[1:]: 
#
#        url = 'http://www.tripadvisor.co.uk/pages/' + link.attrib['href']
#        print url
#        scrapeFindHotels(url)
#
########################################################################################

baseUrl = 'http://www.tripadvisor.co.uk/'





scrapeFindHotels('http://www.tripadvisor.co.uk/pages/citiesAM.html')
scrapeFindHotels('http://www.tripadvisor.co.uk/pages/citiesNZ.html')
