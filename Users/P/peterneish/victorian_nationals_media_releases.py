# Parses victorian Nationals media releases

import scraperwiki
from bs4 import BeautifulSoup
import feedparser
import re
import dateutil.parser 


url = "http://vic.nationals.org.au/DesktopModules/DnnForge%20-%20NewsArticles/Rss.aspx?TabID=131&ModuleID=450&MaxCount=100"


print url

feed = feedparser.parse(url)

entries = []
entries.extend(feed["items"])
for entry in entries:

    print entry["guid"]
    print entry["title"]  
    print entry["link"]
    print entry["author"]
    print entry["updated"]
    print entry["description"]


    # now fetch the page and get the text
    page = scraperwiki.scrape(entry["link"])
    
    pagesoup = BeautifulSoup(page)
    page_content = pagesoup.find("div", { "class" : "article" })
    del(page_content["class"])
    published = dateutil.parser.parse(entry["updated"]);

    print page_content
    #new_page_text = unicode.join(u'\n',map(unicode,new_page_content))



    record = {"link" : entry["link"],
              "title" : entry["title"],
              "author" : entry["author"],
              "published" : published,
              "description" : entry["description"],
              "fulltext" : page_content}


    scraperwiki.sqlite.save(unique_keys=["link"], data=record)




