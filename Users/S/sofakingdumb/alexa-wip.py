# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import mechanize
import codecs
import lxml.etree
import lxml.html
from lxml.html.clean import Cleaner
import re
from BeautifulSoup import BeautifulSoup


# change these values to the target url 
# and the example text you want to find the path to
starturl = "http://www.alexa.com/topsites"
baseurl='http://www.alexa.com'
count = 1

def Main():
    
    getlinks(starturl)

    print "Finished"
    

################################################################################
#
#Retrieve function - given a url it will attempt to open the url and retrieve
#                   the data that was returned
#
################################################################################
def retrieve(url):
    check = False
    try:
        html=mechanize.Browser()
        html.set_handle_robots(False)
        html.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.44 Safari/534.7')]
        data=html.open(url)
        check=True
    except:
        print "unable to retrieve page"
    if check:
        return data
    else:
        return check
    
##########################################################################
#
# getlinks function - get the links to be parsed
#
##########################################################################
def getlinks(url):    
    #debug to track the url to visit
    print "get the links from "+url
    #call the retrieve function to try to get the url
    returl = retrieve(url)
    #check if data was returned
    if returl:
        #parse the address passed in
        root = lxml.html.parse(returl).getroot()
        returl.seek(0)
        #parser=lxml.etree.HTMLParser()
        #root = lxml.etree.parse(returl, parser)
        #root=lxml.etree.fromstring(returl,parser)
        soup = BeautifulSoup(returl)
        print soup
        #print(lxml.etree.tostring(root, pretty_print=True))
        #create a list of urls based on the css
        #get the href from the css element 'table#nav td a'
        urls = [a.get('href') for a in root.cssselect('li.site-listing h2 a')]#if re.search(r"next", lxml.etree.tostring(a))]
        for i,url in enumerate(urls):
            print i,baseurl+url
            #getdata(url)
        
        for n in root.cssselect('div.pagenav'):
            print(lxml.etree.tostring(n))
        
        next=soup.find("a",{"class":"next"})    
        print next#.a['href']
    else:
        print "unable to get the links"

def getdata(url):
    #present an id for each record in the table
    global count
    #debug to track the url to visit
    print "get the data from "+url
    #call the retrieve function to try to get the url
    returl = retrieve(url)
    #check if data was returned
    if returl:
        #parse the address passed in
        root = lxml.html.parse(returl).getroot()
        #print(lxml.etree.tostring(root, pretty_print=True))
        #create a list of urls based on the css
        #get the href from the css element 'table#nav td a'
        for tr in root.cssselect('div.articlecontent table tr'):
            record = {}
            if(len(tr)>1):
                if re.search(r"Date",lxml.etree.tostring(tr)):
                    continue
                else:# tr[0].text is None:
                    tr=cleanup(lxml.etree.tostring(tr),['p'])
                    record['Count']=count
                    record['Date']=tr[0].text
                    record['Time']=tr[1].text
                    record['Location']=tr[2].text
                    record['Incident']=tr[3].text
                    record['Outcome']=tr[4].text
                    count+=1
            #print record
                scraperwiki.datastore.save(['Count'], record)            
    else:
        print "unable to get the links"

def cleanup(data,tags):
    cleaner= Cleaner(remove_tags=tags)
    clean=cleaner.clean_html(data)
    root = lxml.html.fromstring(clean)
    return root

        
Main()

                        



'''
###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://scraperwiki.com/hello_world.html'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('td') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.datastore.save(["td"], record) 
    '''# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import mechanize
import codecs
import lxml.etree
import lxml.html
from lxml.html.clean import Cleaner
import re
from BeautifulSoup import BeautifulSoup


# change these values to the target url 
# and the example text you want to find the path to
starturl = "http://www.alexa.com/topsites"
baseurl='http://www.alexa.com'
count = 1

def Main():
    
    getlinks(starturl)

    print "Finished"
    

################################################################################
#
#Retrieve function - given a url it will attempt to open the url and retrieve
#                   the data that was returned
#
################################################################################
def retrieve(url):
    check = False
    try:
        html=mechanize.Browser()
        html.set_handle_robots(False)
        html.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.44 Safari/534.7')]
        data=html.open(url)
        check=True
    except:
        print "unable to retrieve page"
    if check:
        return data
    else:
        return check
    
##########################################################################
#
# getlinks function - get the links to be parsed
#
##########################################################################
def getlinks(url):    
    #debug to track the url to visit
    print "get the links from "+url
    #call the retrieve function to try to get the url
    returl = retrieve(url)
    #check if data was returned
    if returl:
        #parse the address passed in
        root = lxml.html.parse(returl).getroot()
        returl.seek(0)
        #parser=lxml.etree.HTMLParser()
        #root = lxml.etree.parse(returl, parser)
        #root=lxml.etree.fromstring(returl,parser)
        soup = BeautifulSoup(returl)
        print soup
        #print(lxml.etree.tostring(root, pretty_print=True))
        #create a list of urls based on the css
        #get the href from the css element 'table#nav td a'
        urls = [a.get('href') for a in root.cssselect('li.site-listing h2 a')]#if re.search(r"next", lxml.etree.tostring(a))]
        for i,url in enumerate(urls):
            print i,baseurl+url
            #getdata(url)
        
        for n in root.cssselect('div.pagenav'):
            print(lxml.etree.tostring(n))
        
        next=soup.find("a",{"class":"next"})    
        print next#.a['href']
    else:
        print "unable to get the links"

def getdata(url):
    #present an id for each record in the table
    global count
    #debug to track the url to visit
    print "get the data from "+url
    #call the retrieve function to try to get the url
    returl = retrieve(url)
    #check if data was returned
    if returl:
        #parse the address passed in
        root = lxml.html.parse(returl).getroot()
        #print(lxml.etree.tostring(root, pretty_print=True))
        #create a list of urls based on the css
        #get the href from the css element 'table#nav td a'
        for tr in root.cssselect('div.articlecontent table tr'):
            record = {}
            if(len(tr)>1):
                if re.search(r"Date",lxml.etree.tostring(tr)):
                    continue
                else:# tr[0].text is None:
                    tr=cleanup(lxml.etree.tostring(tr),['p'])
                    record['Count']=count
                    record['Date']=tr[0].text
                    record['Time']=tr[1].text
                    record['Location']=tr[2].text
                    record['Incident']=tr[3].text
                    record['Outcome']=tr[4].text
                    count+=1
            #print record
                scraperwiki.datastore.save(['Count'], record)            
    else:
        print "unable to get the links"

def cleanup(data,tags):
    cleaner= Cleaner(remove_tags=tags)
    clean=cleaner.clean_html(data)
    root = lxml.html.fromstring(clean)
    return root

        
Main()

                        



'''
###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://scraperwiki.com/hello_world.html'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('td') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.datastore.save(["td"], record) 
    '''