# -*- coding: UTF-8 -*-                                             #include this to minimise encoding issues

import scraperwiki
import lxml.etree
import lxml.html
import re
import dateutil.parser as dateparser
import urllib2
from bs4 import BeautifulSoup,Tag

#==========REUTERS HEADLINE FEEDS TO CONVERT TO FULL-TEXT==========

feedList = {"http://mf.feeds.reuters.com/reuters/UKTopNews" : "Top News",
            "http://mf.feeds.reuters.com/reuters/UKdomesticNews" : "News",
            "http://mf.feeds.reuters.com/reuters/UKWorldNews" : "News World",
            "http://mf.feeds.reuters.com/reuters/technologyNews" : "Technology",
            "http://mf.feeds.reuters.com/reuters/UKScienceNews" : "Science",
            "http://mf.feeds.reuters.com/reuters/UKHealthNews" : "Health",
            "http://mf.feeds.reuters.com/reuters/UKSportsNews" : "Sports",
            "http://mf.feeds.reuters.com/reuters/UKFootballNews" : "UK Football",
            "http://mf.feeds.reuters.com/reuters/UKWorldFootballNews" : "World Football",
            "http://mf.feeds.reuters.com/reuters/UKEuropeanFootballNews" : "European Football",        
            "http://mf.feeds.reuters.com/reuters/UKPremierFootballNews" : "Premier Leaugue Football",
            "http://mf.feeds.reuters.com/reuters/UKChampionsFootballNews" : "Champions Leaugue Football",
            "http://mf.feeds.reuters.com/reuters/UKCricketNews" : "UK Cricket",
            "http://mf.feeds.reuters.com/reuters/UKRugbyNews" : "UK Rugby",
            "http://mf.feeds.reuters.com/reuters/UKGolfNews" : "UK Golf",
            "http://mf.feeds.reuters.com/reuters/UKTennisNews" : "UK Tennis",
            "http://mf.feeds.reuters.com/reuters/UKMotorSportsNews" : "UK Motor Sport",
            "http://mf.feeds.reuters.com/reuters/UKFeaturesNews" : "UK Features",
            "http://mf.feeds.reuters.com/reuters/UKOddlyEnoughNews" : "UK oddly enough",
            "http://mf.feeds.reuters.com/reuters/UKEntertainment" : "UK Entertainment",
            "http://mf.feeds.reuters.com/reuters/UKPersonalFinanceNews" : "UK Personal Finance News",
            "http://mf.feeds.reuters.com/reuters/UKFundsNews" : "UK Fund News",
            "http://mf.feeds.reuters.com/reuters/UKConsumerProducts" : "UK Consumer Products",    
            "http://mf.feeds.reuters.com/reuters/UKRealEstateRestaurantsHotels" : "UK Real Estate, Restaurants & Hotels",         
            "http://mf.feeds.reuters.com/reuters/UKMedia" : "UK Media and Teleco",
            "http://mf.feeds.reuters.com/reuters/UKBankingFinancial" : "UK Banking Financial",
            "http://mf.feeds.reuters.com/reuters/UKHealth" : "UK Health",
            "http://mf.feeds.reuters.com/reuters/UKBasicIndustries" : "UK Basic Industries",
            "http://mf.feeds.reuters.com/reuters/UKNaturalResources" : "UK Natural Resources"
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
    author = boup.find("p", { "class" : "byline" })                #the author(s) need to be extracted from this node
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

#==========MAIN SCRIPT==========
 
parserXML = lxml.etree.XMLParser(encoding='ISO-8859-1')            #parser for RSS headline feed - 'view-info' on firefox showed page-encoding            

for feedPage,feedCat in feedList.iteritems():
    try:
        xmlData = lxml.etree.parse(feedPage, parserXML)
        items = xmlData.findall("//item")
        scrapeList = []                                            #list of links to scrape (required as some articles straddle multiple pages)

#Main loop through <item> tags
        for item in items:                                                
            publisher = "Reuters UK"  
            feedPage = feedPage
            feedCat = feedCat
            title = item.findtext("title")
            link = item.findtext("link")
            guid = item.findtext("guid")
            pubDate = item.findtext("pubDate")
            pubDate = (dateparser.parse(pubDate)).isoformat()      #OPTIONAL: for ScraperWiki's SQL-Lite datastore - date needs to be in ISO-8601 format - use if date is not already in this format
            req = urllib2.Request(link)
            response = urllib2.urlopen(req)
            scrapeMainpage = response.read()    
            mainpageSoup = BeautifulSoup(scrapeMainpage)                  
            author = getAuthors(mainpageSoup)                      #including multipage articles, the author information is found on the initial page                                                          
            #scrapeList = checkMultipage(mainpageSoup)             #if page has multi-links - we need to scrape the linked pags too                                                                           
            scrapeList.insert(0,link)                              #if checkMultipage returns either an empty or populated list of links, insert the initial article webpage link at the beginning of the list

            multiDescription = ""
#Loop through all pages that make-up an article   
            for links in scrapeList:                               #iterate through the list of page links - will iterate once unless its a multipage article                
                bigParagraph = ""
                description = ""
                req = urllib2.Request(links)
                response = urllib2.urlopen(req)
                scrapeMe = response.read()        
                soup = BeautifulSoup(scrapeMe)
                soup = soup.find("span", {"id" : "articleText"})           #grab the div that wraps the article text                                                         
                [s.extract() for s in soup(['iframe', 'script', 'b'])]     #remove other unwanted tags from the scraped page                                                 
                [s.extract() for s in soup("p", { "class" : "byline" })]   #having already grabbed the author information - delete this paragraph from the article text      
                paragraphList = soup.findAll('p')                          #grab all the paragraphs that make up the article                                                 
                del paragraphList[-1]                                      #we have grabbed the author information from here already - so this last paragraph can be deleted
        
                for p in paragraphList:
                    paragraph = p.text                                            
                    bigParagraph = bigParagraph + ' ' + paragraph   
                
                description = bigParagraph                          
                #description = regEx(bigParagraph)                         #OPTIONAL:call the generic tidy-up function                             
                description = regEx_description(description)               #remove site-specific boiler-plate                                      
                multiDescription = multiDescription + description          #if it is a multipage article then add all the text from pages together
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
                print feedPage
                print title
                print multiDescription
                print link
    except:
        print("This Page Failed: " + feedPage)
        continue




