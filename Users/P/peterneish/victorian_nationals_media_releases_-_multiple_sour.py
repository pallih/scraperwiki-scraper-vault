# Parses victorian Nationals media releases
# all nationals mps seem to use the same CMS, so we are assuming they
# can all be parsed with the one script.

# we also de-duplicate based on the media release title. The first one harvested
# is kept, so the order of the urls searched is important.



import scraperwiki
from bs4 import BeautifulSoup
import feedparser
import re
import dateutil.parser 


#url = "http://vic.nationals.org.au/DesktopModules/DnnForge%20-%20NewsArticles/Rss.aspx?TabID=131&ModuleID=450&MaxCount=25"
urls = ["http://vic.nationals.org.au/DesktopModules/DnnForge%20-%20NewsArticles/Rss.aspx?TabID=131&ModuleID=450&MaxCount=200",
        "http://jeanettepowell.com.au/RSSRetrieve.aspx?ID=6186&Type=RSS20",
        "http://www.peterryan.com.au/RSSRetrieve.aspx?ID=5052&Type=RSS20"]


for url in urls:
    print url
    
    feed = feedparser.parse(url)
    
    entries = []
    entries.extend(feed["items"])
    for entry in entries:
    
        print entry["guid"]
        print entry["title"]  
        print entry["link"]
        #print entry["author"]
        print entry["updated"]
        print entry["description"]
    
    
        # now fetch the page and get the text
        page = scraperwiki.scrape(entry["link"])
        
        pagesoup = BeautifulSoup(page)
        page_content = pagesoup.find(["div", { "class" : "post-body" }, "div", { "class" : "article" } ]).renderContents()
        published = dateutil.parser.parse(entry["updated"])
    
        print page_content
        #new_page_text = unicode.join(u'\n',map(unicode,new_page_content))
    
    
    
        record = {"link" : entry["link"],
                  "title" : entry["title"],
                  "author" : "unknown",
                  "published" : published,
                  "year" : published.year,
                  "month" : published.month,
                  "description" : entry["description"],
                  "fulltext" : page_content}
    
    
        scraperwiki.sqlite.save(unique_keys=["title", "month", "year"], data=record)




# Parses victorian Nationals media releases
# all nationals mps seem to use the same CMS, so we are assuming they
# can all be parsed with the one script.

# we also de-duplicate based on the media release title. The first one harvested
# is kept, so the order of the urls searched is important.



import scraperwiki
from bs4 import BeautifulSoup
import feedparser
import re
import dateutil.parser 


#url = "http://vic.nationals.org.au/DesktopModules/DnnForge%20-%20NewsArticles/Rss.aspx?TabID=131&ModuleID=450&MaxCount=25"
urls = ["http://vic.nationals.org.au/DesktopModules/DnnForge%20-%20NewsArticles/Rss.aspx?TabID=131&ModuleID=450&MaxCount=200",
        "http://jeanettepowell.com.au/RSSRetrieve.aspx?ID=6186&Type=RSS20",
        "http://www.peterryan.com.au/RSSRetrieve.aspx?ID=5052&Type=RSS20"]


for url in urls:
    print url
    
    feed = feedparser.parse(url)
    
    entries = []
    entries.extend(feed["items"])
    for entry in entries:
    
        print entry["guid"]
        print entry["title"]  
        print entry["link"]
        #print entry["author"]
        print entry["updated"]
        print entry["description"]
    
    
        # now fetch the page and get the text
        page = scraperwiki.scrape(entry["link"])
        
        pagesoup = BeautifulSoup(page)
        page_content = pagesoup.find(["div", { "class" : "post-body" }, "div", { "class" : "article" } ]).renderContents()
        published = dateutil.parser.parse(entry["updated"])
    
        print page_content
        #new_page_text = unicode.join(u'\n',map(unicode,new_page_content))
    
    
    
        record = {"link" : entry["link"],
                  "title" : entry["title"],
                  "author" : "unknown",
                  "published" : published,
                  "year" : published.year,
                  "month" : published.month,
                  "description" : entry["description"],
                  "fulltext" : page_content}
    
    
        scraperwiki.sqlite.save(unique_keys=["title", "month", "year"], data=record)




