# Parses victorian Greens media releases

import scraperwiki
from bs4 import BeautifulSoup
import feedparser
import re
import dateutil.parser

url = "http://vicmps.greens.org.au/mediareleases/feed"

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
    page_content = pagesoup.find("div", { "class" : "node" }).find("div", {"class" : "content" })
    page_content = re.sub(ur'\d\d\/\d\d\/\d\d\d\d', ur'', page_content.text)


    #print page_content.string


    record = {"party" : "greens",
              "link" : entry["link"],
              "title" : entry["title"],
              "author" : entry["author"],
              "published" : published,
              "description" : filtered_desc,
              "fulltext" : page_content}

    scraperwiki.sqlite.save(unique_keys=["link"], data=record)
# Parses victorian Greens media releases

import scraperwiki
from bs4 import BeautifulSoup
import feedparser
import re
import dateutil.parser

url = "http://vicmps.greens.org.au/mediareleases/feed"

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
    page_content = pagesoup.find("div", { "class" : "node" }).find("div", {"class" : "content" })
    page_content = re.sub(ur'\d\d\/\d\d\/\d\d\d\d', ur'', page_content.text)


    #print page_content.string


    record = {"party" : "greens",
              "link" : entry["link"],
              "title" : entry["title"],
              "author" : entry["author"],
              "published" : published,
              "description" : filtered_desc,
              "fulltext" : page_content}

    scraperwiki.sqlite.save(unique_keys=["link"], data=record)
