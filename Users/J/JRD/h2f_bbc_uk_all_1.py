# -*- coding: UTF-8 -*-                                             #include this to minimise encoding issues

import scraperwiki
import lxml.etree
import lxml.html
import re
import dateutil.parser as dateparser
import urllib2
from bs4 import BeautifulSoup,Tag
from datetime import datetime, timedelta

#==========REUTERS HEADLINE FEEDS TO CONVERT TO FULL-TEXT==========

feedList = {"http://feeds.bbci.co.uk/news/business/rss.xml" : "Business",
            "http://feeds.bbci.co.uk/news/rss.xml" : "News",
            "http://feeds.bbci.co.uk/news/world/rss.xml" : "News World",
            "http://feeds.bbci.co.uk/news/uk/rss.xml" : "News UK",
            "http://feeds.bbci.co.uk/news/politics/rss.xml" : "Politics",
            "http://feeds.bbci.co.uk/news/health/rss.xml" : "Health",
            "http://feeds.bbci.co.uk/news/education/rss.xml" : "Education",
            "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml" : "Science Environment",
            "http://feeds.bbci.co.uk/news/technology/rss.xml" : "Technology",
            "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml" : "Entertainment Arts"       
}

#==========FUNCTIONS==========

#General purpose RegEx & string functions to tidy up text
def regEx(cleanMe):                                               
    #cleanMe = re.sub('</?p>', '', cleanMe)                        #OPTIONAL:remove any openeing or closing paragraph tag                 
    #cleanMe = re.sub(r"^\s+", "", cleanMe, flags = re.MULTILINE)  #OPTIONAL:get rid of excess white-space                               
    #cleanMe = re.sub("[\['\]]", '', cleanMe)                      #OPTIONAL:remove the '[ & ]' that surrounds the text                  
    #cleanMe = re.sub('[\n\r\t]','',cleanMe)                       #OPTIONAL:remove newline,tab characters                               
    #cleanMe = re.sub('[\\\\][ntr]', '', cleanMe)                  #OPTIONAL:remove literal occurences of '\n' '\t' '\r' in the text     
    #cleanMe = re.escape(cleanMe)                                  #OPTIONAL: un-comment-out-this if you want to escape the text          
    return cleanMe                                                

#Site specific RegEx & string functions to remove boiler-plate text
def regEx_description(cleanMe):                                              
    cleanMe = (cleanMe.split(") - ").pop());                       #Remove all the pre-article text up to the dash following (Reuters),(Reuters Health) etc  
    #cleanMe = (cleanMe.split("\)\ \-\ ").pop());                  #OPTIONAL:use this version of the above line if you have choosen to escape the article text
    return(cleanMe)                                                         

#Check if article page has links that continue story to other pages
def checkMultipage(boup):                                         
    multipage = boup.findAll("div", { "class" : "multi-pager-headlines clearfix" })
    linklist = []
    if multipage != []:  
        mpsoup = BeautifulSoup(str(multipage))
        for link in mpsoup.find_all('a'):
            linkURL = "http://www.reuters.com/" + link.get('href')
            linklist.append(linkURL)
    return(linklist)

#Retrieve author(s) name by tag attibute name
def getAuthors(boup):
    author = boup.find("span", { "class" : "byline-name" })                #the author(s) need to be extracted from this node
    if author is not None:
        author = str(author.text)
    else:
        author = "No Author"
    return(author)

#Gather article info into a dictionary & write to datastore
def scraperwikiDatastore(data):
    try:                                                           #write to the ScraperWiki SQL-Lite datastore                                         
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)
    except scraperwiki.sqlite.SqliteError, e:
        print str(e)


def parse_iso8601_datetime(dtstr, loose=False):
    """
    Convert ISO8601 datetime string and return Python datetime.datetime.
    Specify loose=True for more relaxed parsing accepting eg "YYYY-MM-DD" format.

    Raise ValueError on malformed input.
    """
    dt = None
    if len(dtstr) == 19:    # (eg '2010-05-07T23:12:51')
        dt = datetime.strptime(dtstr, "%Y-%m-%dT%H:%M:%S")
    elif len(dtstr) == 20:  # (eg '2010-05-07T23:12:51Z')
        dt = datetime.strptime(dtstr, "%Y-%m-%dT%H:%M:%SZ")
    elif len(dtstr) == 25:  # (eg '2010-05-07T23:12:51-08:00')
        dt = datetime.strptime(dtstr[0:19], "%Y-%m-%dT%H:%M:%S")
        tzofs = int(dtstr[19:22])
        dt = dt - timedelta(hours=tzofs)
    else:
        if loose:
            if len(dtstr) == 10:  # (eg '2010-05-07')
                dt = datetime.strptime(dtstr, "%Y-%m-%d")
        if not dt:
            raise ValueError("Invalid ISO8601 format: '%s'" % dtstr)
    return dt


#==========MAIN SCRIPT==========
 
parserXML = lxml.etree.XMLParser(encoding='ISO-8859-1')                     #parser for RSS headline feed - 'view-info' on firefox showed page-encoding            

for feedPage,feedCat in feedList.iteritems():
    try:
        xmlData = lxml.etree.parse(feedPage, parserXML)
        items = xmlData.findall("//item")
        scrapeList = []                                                     #list of links to scrape (required as some articles straddle multiple pages)

#Main loop through <item> tags
        for item in items:                                                
            publisher = "BBC UK"  
            feedPage = feedPage
            feedCat = feedCat
            title = item.findtext("title")
            #link = item.findtext("link")
            link = "http://www.bbc.co.uk/news/uk-england-leicestershire-23451501"
            guid = item.findtext("guid")
            pubDate = item.findtext("pubDate")
            pubDate = (dateparser.parse(pubDate)).isoformat()               #OPTIONAL: for ScraperWiki's SQL-Lite datastore - date needs to be in ISO-8601 format - use if date is not already in this format
            #print pubDate
            #pubDate = parse_iso8601_datetime(pubDate)
            #print pubDate
            req = urllib2.Request(link)
            response = urllib2.urlopen(req)
            scrapeMainpage = response.read()    
            mainpageSoup = BeautifulSoup(scrapeMainpage)                  
            author = getAuthors(mainpageSoup)                               #including multipage articles, the author information is found on the initial page                                                          
            #scrapeList = checkMultipage(mainpageSoup)                      #if page has multi-links - we need to scrape the linked pags too                                                                           
            scrapeList.insert(0,link)                                       #if checkMultipage returns either an empty or populated list of links, insert the initial article webpage link at the beginning of the list
            
            multiDescription = ""
#Loop through all pages that make-up an article   
            for links in scrapeList:                                        #iterate through the list of page links - will iterate once unless its a multipage article
                bigParagraph = ""
                description = ""
                req = urllib2.Request(links)
                response = urllib2.urlopen(req)
                scrapeMe = response.read()        
                soup = BeautifulSoup(scrapeMe)
                if title.find("VIDEO:")!= -1 or title.find("AUDIO:")!= -1:
                    soup = soup.find("div", {"class" : "emp-decription"})    
                else:    
                    soup = soup.find("div", {"class" : "story-body"})                   #grab the div that wraps the article text                                                         
                [s.extract() for s in soup(['iframe', 'noscript', 'script', 'b'])]      #remove other unwanted tags from the scraped page                                                 
                #[s.extract() for s in soup("p", { "class" : "byline" })]               #having already grabbed the author information - delete this paragraph from the article text      
                paragraphList = soup.findAll('p')                                       #grab all the paragraphs that make up the article                                                
        
                for p in paragraphList:
                    paragraph = p.text
                                                             
                    bigParagraph = bigParagraph + ' ' + paragraph   
                
                description = bigParagraph                          
                description = regEx(bigParagraph)                           #OPTIONAL:call the generic tidy-up function                             
                #description = regEx_description(description)               #remove site-specific boiler-plate                                      
                multiDescription = multiDescription + description           #if it is a multipage article then add all the text from pages together
                scrapeList = []
                paragraphList = []
                
                data = {"title" : title, "link" : link,                              
                        "pubDate" : pubDate, "guid" : guid,
                        "description" : multiDescription,
                        "author" : author, "feedPage" : feedPage,
                        "feedCat" : feedCat, "publisher" : publisher    
            }
            #scraperwikiDatastore(data)
        
#Debugging   
            print("\n")
            print author
            print feedPage
            print title
            print multiDescription
            print link
    except:
        print("This Page Failed: " + feedPage)
        continue




# -*- coding: UTF-8 -*-                                             #include this to minimise encoding issues

import scraperwiki
import lxml.etree
import lxml.html
import re
import dateutil.parser as dateparser
import urllib2
from bs4 import BeautifulSoup,Tag
from datetime import datetime, timedelta

#==========REUTERS HEADLINE FEEDS TO CONVERT TO FULL-TEXT==========

feedList = {"http://feeds.bbci.co.uk/news/business/rss.xml" : "Business",
            "http://feeds.bbci.co.uk/news/rss.xml" : "News",
            "http://feeds.bbci.co.uk/news/world/rss.xml" : "News World",
            "http://feeds.bbci.co.uk/news/uk/rss.xml" : "News UK",
            "http://feeds.bbci.co.uk/news/politics/rss.xml" : "Politics",
            "http://feeds.bbci.co.uk/news/health/rss.xml" : "Health",
            "http://feeds.bbci.co.uk/news/education/rss.xml" : "Education",
            "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml" : "Science Environment",
            "http://feeds.bbci.co.uk/news/technology/rss.xml" : "Technology",
            "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml" : "Entertainment Arts"       
}

#==========FUNCTIONS==========

#General purpose RegEx & string functions to tidy up text
def regEx(cleanMe):                                               
    #cleanMe = re.sub('</?p>', '', cleanMe)                        #OPTIONAL:remove any openeing or closing paragraph tag                 
    #cleanMe = re.sub(r"^\s+", "", cleanMe, flags = re.MULTILINE)  #OPTIONAL:get rid of excess white-space                               
    #cleanMe = re.sub("[\['\]]", '', cleanMe)                      #OPTIONAL:remove the '[ & ]' that surrounds the text                  
    #cleanMe = re.sub('[\n\r\t]','',cleanMe)                       #OPTIONAL:remove newline,tab characters                               
    #cleanMe = re.sub('[\\\\][ntr]', '', cleanMe)                  #OPTIONAL:remove literal occurences of '\n' '\t' '\r' in the text     
    #cleanMe = re.escape(cleanMe)                                  #OPTIONAL: un-comment-out-this if you want to escape the text          
    return cleanMe                                                

#Site specific RegEx & string functions to remove boiler-plate text
def regEx_description(cleanMe):                                              
    cleanMe = (cleanMe.split(") - ").pop());                       #Remove all the pre-article text up to the dash following (Reuters),(Reuters Health) etc  
    #cleanMe = (cleanMe.split("\)\ \-\ ").pop());                  #OPTIONAL:use this version of the above line if you have choosen to escape the article text
    return(cleanMe)                                                         

#Check if article page has links that continue story to other pages
def checkMultipage(boup):                                         
    multipage = boup.findAll("div", { "class" : "multi-pager-headlines clearfix" })
    linklist = []
    if multipage != []:  
        mpsoup = BeautifulSoup(str(multipage))
        for link in mpsoup.find_all('a'):
            linkURL = "http://www.reuters.com/" + link.get('href')
            linklist.append(linkURL)
    return(linklist)

#Retrieve author(s) name by tag attibute name
def getAuthors(boup):
    author = boup.find("span", { "class" : "byline-name" })                #the author(s) need to be extracted from this node
    if author is not None:
        author = str(author.text)
    else:
        author = "No Author"
    return(author)

#Gather article info into a dictionary & write to datastore
def scraperwikiDatastore(data):
    try:                                                           #write to the ScraperWiki SQL-Lite datastore                                         
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)
    except scraperwiki.sqlite.SqliteError, e:
        print str(e)


def parse_iso8601_datetime(dtstr, loose=False):
    """
    Convert ISO8601 datetime string and return Python datetime.datetime.
    Specify loose=True for more relaxed parsing accepting eg "YYYY-MM-DD" format.

    Raise ValueError on malformed input.
    """
    dt = None
    if len(dtstr) == 19:    # (eg '2010-05-07T23:12:51')
        dt = datetime.strptime(dtstr, "%Y-%m-%dT%H:%M:%S")
    elif len(dtstr) == 20:  # (eg '2010-05-07T23:12:51Z')
        dt = datetime.strptime(dtstr, "%Y-%m-%dT%H:%M:%SZ")
    elif len(dtstr) == 25:  # (eg '2010-05-07T23:12:51-08:00')
        dt = datetime.strptime(dtstr[0:19], "%Y-%m-%dT%H:%M:%S")
        tzofs = int(dtstr[19:22])
        dt = dt - timedelta(hours=tzofs)
    else:
        if loose:
            if len(dtstr) == 10:  # (eg '2010-05-07')
                dt = datetime.strptime(dtstr, "%Y-%m-%d")
        if not dt:
            raise ValueError("Invalid ISO8601 format: '%s'" % dtstr)
    return dt


#==========MAIN SCRIPT==========
 
parserXML = lxml.etree.XMLParser(encoding='ISO-8859-1')                     #parser for RSS headline feed - 'view-info' on firefox showed page-encoding            

for feedPage,feedCat in feedList.iteritems():
    try:
        xmlData = lxml.etree.parse(feedPage, parserXML)
        items = xmlData.findall("//item")
        scrapeList = []                                                     #list of links to scrape (required as some articles straddle multiple pages)

#Main loop through <item> tags
        for item in items:                                                
            publisher = "BBC UK"  
            feedPage = feedPage
            feedCat = feedCat
            title = item.findtext("title")
            #link = item.findtext("link")
            link = "http://www.bbc.co.uk/news/uk-england-leicestershire-23451501"
            guid = item.findtext("guid")
            pubDate = item.findtext("pubDate")
            pubDate = (dateparser.parse(pubDate)).isoformat()               #OPTIONAL: for ScraperWiki's SQL-Lite datastore - date needs to be in ISO-8601 format - use if date is not already in this format
            #print pubDate
            #pubDate = parse_iso8601_datetime(pubDate)
            #print pubDate
            req = urllib2.Request(link)
            response = urllib2.urlopen(req)
            scrapeMainpage = response.read()    
            mainpageSoup = BeautifulSoup(scrapeMainpage)                  
            author = getAuthors(mainpageSoup)                               #including multipage articles, the author information is found on the initial page                                                          
            #scrapeList = checkMultipage(mainpageSoup)                      #if page has multi-links - we need to scrape the linked pags too                                                                           
            scrapeList.insert(0,link)                                       #if checkMultipage returns either an empty or populated list of links, insert the initial article webpage link at the beginning of the list
            
            multiDescription = ""
#Loop through all pages that make-up an article   
            for links in scrapeList:                                        #iterate through the list of page links - will iterate once unless its a multipage article
                bigParagraph = ""
                description = ""
                req = urllib2.Request(links)
                response = urllib2.urlopen(req)
                scrapeMe = response.read()        
                soup = BeautifulSoup(scrapeMe)
                if title.find("VIDEO:")!= -1 or title.find("AUDIO:")!= -1:
                    soup = soup.find("div", {"class" : "emp-decription"})    
                else:    
                    soup = soup.find("div", {"class" : "story-body"})                   #grab the div that wraps the article text                                                         
                [s.extract() for s in soup(['iframe', 'noscript', 'script', 'b'])]      #remove other unwanted tags from the scraped page                                                 
                #[s.extract() for s in soup("p", { "class" : "byline" })]               #having already grabbed the author information - delete this paragraph from the article text      
                paragraphList = soup.findAll('p')                                       #grab all the paragraphs that make up the article                                                
        
                for p in paragraphList:
                    paragraph = p.text
                                                             
                    bigParagraph = bigParagraph + ' ' + paragraph   
                
                description = bigParagraph                          
                description = regEx(bigParagraph)                           #OPTIONAL:call the generic tidy-up function                             
                #description = regEx_description(description)               #remove site-specific boiler-plate                                      
                multiDescription = multiDescription + description           #if it is a multipage article then add all the text from pages together
                scrapeList = []
                paragraphList = []
                
                data = {"title" : title, "link" : link,                              
                        "pubDate" : pubDate, "guid" : guid,
                        "description" : multiDescription,
                        "author" : author, "feedPage" : feedPage,
                        "feedCat" : feedCat, "publisher" : publisher    
            }
            #scraperwikiDatastore(data)
        
#Debugging   
            print("\n")
            print author
            print feedPage
            print title
            print multiDescription
            print link
    except:
        print("This Page Failed: " + feedPage)
        continue




