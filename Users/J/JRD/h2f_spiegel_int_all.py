# -*- coding: UTF-8 -*-                                                      #include this to minimise encoding issues

import scraperwiki
import lxml.etree
import lxml.html
import re
import dateutil.parser as dateparser
import urllib2
from bs4 import BeautifulSoup,Tag


#==========HEADLINE FEEDS TO CONVERT TO FULL-TEXT==========

feedList = {"http://www.spiegel.de/international/index.rss" : "Index",              
            "http://www.spiegel.de/international/germany/index.rss" : "Germany",      
            "http://www.spiegel.de/international/europe/index.rss" : "Europe",       
            "http://www.spiegel.de/international/world/index.rss" : "World",        
            "http://www.spiegel.de/international/business/index.rss" : "Business",     
            "http://www.spiegel.de/international/zeitgeist/index.rss" : "Zeitgeist",    
            "http://www.spiegel.de/schlagzeilen/tops/index.rss" : "Tops"
}          
                                                                          
#==========FUNCTIONS==========

#General purpose RegEx to tidy up text
def regEx(cleanMe):                                               
    cleanMe = re.sub(r"^\s+", "", cleanMe, flags = re.MULTILINE)             #get rid of excess white-space                               
    cleanMe = re.sub("[\['\]]", '', cleanMe)                                 #remove the '[ & ]' that surrounds the text                  
    cleanMe = re.sub('[\n\r\t]','',cleanMe)                                  #remove newline,tab characters                               
    cleanMe = re.sub('[\\\\][ntr]', '', cleanMe)                             #remove literal occurences of '\n' '\t' '\r' in the text     
    #cleanMe = re.escape(cleanMe)                                            #OPTIONAL: un-comment-out-this if you want to escape the text
    return cleanMe                                                

#Site specific RegEx to remove boiler-plate text
def regEx_description(cleanMe):                                              
    cleanMe = re.sub('Translated\s*from(\s*the??)\s*German.*', '', cleanMe)
    cleanMe = re.sub('Post\s*to\s*other\s*social.*', '', cleanMe)            
    cleanMe = re.sub('Stay\s*informed\s*with\s*our\s*free\s*news.*', '', cleanMe)
    cleanMe = re.sub('\w{3}\s*--\s*with\s*wires?.*', '', cleanMe)
    cleanMe = re.sub('--\s*\w{3},?\s*with\s*wires?.*', '', cleanMe)         
    return(cleanMe)                                                         

#Check if article page has links that continue story to other pages
def checkMultipage(boup):                                         
    multipage = boup.findAll("div", { "class" : "multi-pager-headlines clearfix" })
    linklist = []
    if multipage != []:  
        mpsoup = BeautifulSoup(str(multipage))
        for link in mpsoup.find_all('a'):
            linkURL = "http://www.spiegel.de/" + link.get('href')
            linklist.append(linkURL)
    return(linklist)

#Retrieve author(s) name by tag attibute name
def getAuthors(boup):
    author = boup.find("p", { "class" : "author" })                         #the author(s) need to be extracted from this node
    if author is not None:
        author = (author.text).encode('utf-8')
        author = str(author)
        print author
    else:
        author = "No Author"
    return(author)

#If its a 'Picture this:' page the text needs to be grabbed with XPath
def grabPictureText(scrapings):
    if scrapings.xpath(".//*[@id='js-article-column']/div[1]/text()[2]"):                      #'js-article-column' seems to have replaced 'spArticleSection'
        bigParagraph = str(scrapings.xpath(".//*[@id='js-article-column']/div[1]/text()[2]"))
        bigParagraph = regEx(bigParagraph)   
    elif scrapings.xpath(".//*[@id='spArticleSection']/text()[2]"):                            #legacy 'spArticleSection' check
        bigParagraph = str(scrapings.xpath(".//*[@id='spArticleSection']/text()[2]"))
        bigParagraph = regEx(bigParagraph)    
    return(bigParagraph)

#Gather article info into a dictionary & write to datastore
def scraperwikiDatastore(data):
    try:                                                                   #write to the ScraperWiki SQL-Lite datastore                                         
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)
    except scraperwiki.sqlite.SqliteError, e:
        print str(e)

#==========MAIN SCRIPT==========
 
parserXML = lxml.etree.XMLParser(encoding='utf-8')                         #parser for RSS headline feed - 'view-info' on firefox showed page-encoding            

for feedPage,feedCat in feedList.iteritems():
    try:
        xmlData = lxml.etree.parse(feedPage, parserXML)
        items = xmlData.findall("//item")
        scrapeList = []                                                    #list of links to scrape (required as some articles straddle multiple pages)
            
#Main loop through <item> tags
        for item in items:                                                
            publisher = "Spiegel International"  
            feedPage = feedPage
            feedCat = feedCat            
            title = item.findtext("title")
            link = item.findtext("link")
            guid = item.findtext("guid")
            pubDate = item.findtext("pubDate")
            pubDate = (dateparser.parse(pubDate)).isoformat()              #OPTIONAL: for ScraperWiki's SQL-Lite datastore - date needs to be in ISO-8601 format - use if date is not already in this format
               
            req = urllib2.Request(link)
            response = urllib2.urlopen(req)
            scrapeMainpage = response.read()    
        
            mainpageSoup = BeautifulSoup(scrapeMainpage)                   #wonderful BeautifulSoup! BS replaced my original XPath approach primarily due to xpath encoding issues
            author = getAuthors(mainpageSoup)                              #including multipage articles, the author information is found on the initial page                     
            
            scrapeList = checkMultipage(mainpageSoup)                      #if page has multi-links - we need to scrape the linked pags too                                                                           
            scrapeList.insert(0,link)                                      #if checkMultipage returns either an empty or populated list of links, insert the initial article webpage link at the beginning of the list
            multiDescription = ""
#Loop through all pages that make-up an article   
            for links in scrapeList:                                       #iterate through the list of page links - will iterate once unless its a multipage article
                bigParagraph = ""
                description = ""
                req = urllib2.Request(links)
                response = urllib2.urlopen(req)
                scrapeMe = response.read()         
                boup = BeautifulSoup(scrapeMe)
            
                [s.extract() for s in boup("p", { "class" : "author" })]   #remove the paragraph class of author before it is appended to the article text
                [s.extract() for s in boup(['iframe', 'script', 'b'])]     #remove other unwanted tags from the scraped page                             
            
                paragraphList = boup.findAll('p')                          #grab all the paragraphs that make up the article
                scrapings = lxml.html.fromstring(scrapeMe)                 #we need xml node structure to use xpath        
            
#!!!!!This XPath section works but has encoding issues!!!!!
                if title.find("Picture This:") != -1:                      #if its a picture story, grab the short text from beneath the image - XPath for pin-pointing the text
                    bigParagraph = grabPictureText(scrapings)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                else:
                    for p in paragraphList:
                        paragraph = p.text
                        paragraph = regEx(paragraph)                                                
                        bigParagraph = bigParagraph + paragraph   
                
                description = regEx_description(bigParagraph)
                multiDescription = multiDescription + description          #if it is a multipage article then add all the text from pages together
                scrapeList = []
                paragraphList = []

                data = {"title" : title, "link" : link,                              
                        "pubDate" : pubDate, "guid" : guid,
                        "description" : multiDescription,
                        "author" : author, "feedPage" : feedPage,
                        "feedCat" : feedCat, "publisher" : publisher    
            }
            scraperwikiDatastore(data)
        
        #Debugging:   
            #print("\n")
            #print title                                                  
            #print multiDescription
            #print link

    except:
        print("This Page Failed: " + feedPage)
        continue


# -*- coding: UTF-8 -*-                                                      #include this to minimise encoding issues

import scraperwiki
import lxml.etree
import lxml.html
import re
import dateutil.parser as dateparser
import urllib2
from bs4 import BeautifulSoup,Tag


#==========HEADLINE FEEDS TO CONVERT TO FULL-TEXT==========

feedList = {"http://www.spiegel.de/international/index.rss" : "Index",              
            "http://www.spiegel.de/international/germany/index.rss" : "Germany",      
            "http://www.spiegel.de/international/europe/index.rss" : "Europe",       
            "http://www.spiegel.de/international/world/index.rss" : "World",        
            "http://www.spiegel.de/international/business/index.rss" : "Business",     
            "http://www.spiegel.de/international/zeitgeist/index.rss" : "Zeitgeist",    
            "http://www.spiegel.de/schlagzeilen/tops/index.rss" : "Tops"
}          
                                                                          
#==========FUNCTIONS==========

#General purpose RegEx to tidy up text
def regEx(cleanMe):                                               
    cleanMe = re.sub(r"^\s+", "", cleanMe, flags = re.MULTILINE)             #get rid of excess white-space                               
    cleanMe = re.sub("[\['\]]", '', cleanMe)                                 #remove the '[ & ]' that surrounds the text                  
    cleanMe = re.sub('[\n\r\t]','',cleanMe)                                  #remove newline,tab characters                               
    cleanMe = re.sub('[\\\\][ntr]', '', cleanMe)                             #remove literal occurences of '\n' '\t' '\r' in the text     
    #cleanMe = re.escape(cleanMe)                                            #OPTIONAL: un-comment-out-this if you want to escape the text
    return cleanMe                                                

#Site specific RegEx to remove boiler-plate text
def regEx_description(cleanMe):                                              
    cleanMe = re.sub('Translated\s*from(\s*the??)\s*German.*', '', cleanMe)
    cleanMe = re.sub('Post\s*to\s*other\s*social.*', '', cleanMe)            
    cleanMe = re.sub('Stay\s*informed\s*with\s*our\s*free\s*news.*', '', cleanMe)
    cleanMe = re.sub('\w{3}\s*--\s*with\s*wires?.*', '', cleanMe)
    cleanMe = re.sub('--\s*\w{3},?\s*with\s*wires?.*', '', cleanMe)         
    return(cleanMe)                                                         

#Check if article page has links that continue story to other pages
def checkMultipage(boup):                                         
    multipage = boup.findAll("div", { "class" : "multi-pager-headlines clearfix" })
    linklist = []
    if multipage != []:  
        mpsoup = BeautifulSoup(str(multipage))
        for link in mpsoup.find_all('a'):
            linkURL = "http://www.spiegel.de/" + link.get('href')
            linklist.append(linkURL)
    return(linklist)

#Retrieve author(s) name by tag attibute name
def getAuthors(boup):
    author = boup.find("p", { "class" : "author" })                         #the author(s) need to be extracted from this node
    if author is not None:
        author = (author.text).encode('utf-8')
        author = str(author)
        print author
    else:
        author = "No Author"
    return(author)

#If its a 'Picture this:' page the text needs to be grabbed with XPath
def grabPictureText(scrapings):
    if scrapings.xpath(".//*[@id='js-article-column']/div[1]/text()[2]"):                      #'js-article-column' seems to have replaced 'spArticleSection'
        bigParagraph = str(scrapings.xpath(".//*[@id='js-article-column']/div[1]/text()[2]"))
        bigParagraph = regEx(bigParagraph)   
    elif scrapings.xpath(".//*[@id='spArticleSection']/text()[2]"):                            #legacy 'spArticleSection' check
        bigParagraph = str(scrapings.xpath(".//*[@id='spArticleSection']/text()[2]"))
        bigParagraph = regEx(bigParagraph)    
    return(bigParagraph)

#Gather article info into a dictionary & write to datastore
def scraperwikiDatastore(data):
    try:                                                                   #write to the ScraperWiki SQL-Lite datastore                                         
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)
    except scraperwiki.sqlite.SqliteError, e:
        print str(e)

#==========MAIN SCRIPT==========
 
parserXML = lxml.etree.XMLParser(encoding='utf-8')                         #parser for RSS headline feed - 'view-info' on firefox showed page-encoding            

for feedPage,feedCat in feedList.iteritems():
    try:
        xmlData = lxml.etree.parse(feedPage, parserXML)
        items = xmlData.findall("//item")
        scrapeList = []                                                    #list of links to scrape (required as some articles straddle multiple pages)
            
#Main loop through <item> tags
        for item in items:                                                
            publisher = "Spiegel International"  
            feedPage = feedPage
            feedCat = feedCat            
            title = item.findtext("title")
            link = item.findtext("link")
            guid = item.findtext("guid")
            pubDate = item.findtext("pubDate")
            pubDate = (dateparser.parse(pubDate)).isoformat()              #OPTIONAL: for ScraperWiki's SQL-Lite datastore - date needs to be in ISO-8601 format - use if date is not already in this format
               
            req = urllib2.Request(link)
            response = urllib2.urlopen(req)
            scrapeMainpage = response.read()    
        
            mainpageSoup = BeautifulSoup(scrapeMainpage)                   #wonderful BeautifulSoup! BS replaced my original XPath approach primarily due to xpath encoding issues
            author = getAuthors(mainpageSoup)                              #including multipage articles, the author information is found on the initial page                     
            
            scrapeList = checkMultipage(mainpageSoup)                      #if page has multi-links - we need to scrape the linked pags too                                                                           
            scrapeList.insert(0,link)                                      #if checkMultipage returns either an empty or populated list of links, insert the initial article webpage link at the beginning of the list
            multiDescription = ""
#Loop through all pages that make-up an article   
            for links in scrapeList:                                       #iterate through the list of page links - will iterate once unless its a multipage article
                bigParagraph = ""
                description = ""
                req = urllib2.Request(links)
                response = urllib2.urlopen(req)
                scrapeMe = response.read()         
                boup = BeautifulSoup(scrapeMe)
            
                [s.extract() for s in boup("p", { "class" : "author" })]   #remove the paragraph class of author before it is appended to the article text
                [s.extract() for s in boup(['iframe', 'script', 'b'])]     #remove other unwanted tags from the scraped page                             
            
                paragraphList = boup.findAll('p')                          #grab all the paragraphs that make up the article
                scrapings = lxml.html.fromstring(scrapeMe)                 #we need xml node structure to use xpath        
            
#!!!!!This XPath section works but has encoding issues!!!!!
                if title.find("Picture This:") != -1:                      #if its a picture story, grab the short text from beneath the image - XPath for pin-pointing the text
                    bigParagraph = grabPictureText(scrapings)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                else:
                    for p in paragraphList:
                        paragraph = p.text
                        paragraph = regEx(paragraph)                                                
                        bigParagraph = bigParagraph + paragraph   
                
                description = regEx_description(bigParagraph)
                multiDescription = multiDescription + description          #if it is a multipage article then add all the text from pages together
                scrapeList = []
                paragraphList = []

                data = {"title" : title, "link" : link,                              
                        "pubDate" : pubDate, "guid" : guid,
                        "description" : multiDescription,
                        "author" : author, "feedPage" : feedPage,
                        "feedCat" : feedCat, "publisher" : publisher    
            }
            scraperwikiDatastore(data)
        
        #Debugging:   
            #print("\n")
            #print title                                                  
            #print multiDescription
            #print link

    except:
        print("This Page Failed: " + feedPage)
        continue


