# Parses victorian ALP media releases

import scraperwiki
from bs4 import BeautifulSoup
import feedparser
import re
import dateutil.parser

url = "http://www.viclabor.com.au/feed/"

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
    desc = BeautifulSoup(entry["description"])
    #print desc.text
    published = dateutil.parser.parse(entry["updated"]);

    filtered_desc = re.sub(ur'\d\d\/\d\d\/\d\d\d\d', ur'', desc.text)
    print filtered_desc

    # now fetch the page and get the text
    page = scraperwiki.scrape(entry["link"])
    
    pagesoup = BeautifulSoup(page)
    page_content = pagesoup.find("div", { "class" : "entry-content" })
    new_page_content = page_content.findAll(['p','h1','h2','h3','h4','b','i','strong','em','a'])

    print new_page_content
    new_page_text = unicode.join(u'\n',map(unicode,new_page_content))

    '''
    [x.extract() for x in page_content.findAll('script')] #remove script tags
    [x.extract() for x in page_content.findAll('div', {"id" : "fb-root"})] #remove extra
    [x.extract() for x in page_content.findAll('fb:like')]
    '''

    record = {"link" : entry["link"],
              "title" : entry["title"],
              "author" : entry["author"],
              "published" : published,
              "description" : filtered_desc,
              "fulltext" : new_page_text}

    if re.search(ur'media-release', entry["link"]):
        scraperwiki.sqlite.save(unique_keys=["link"], data=record)




