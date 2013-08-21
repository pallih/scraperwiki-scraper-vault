# Parses victorian ALP media releases

import scraperwiki
from bs4 import BeautifulSoup
import feedparser
import re
import datetime
import dateutil.parser

url = "http://www.danielandrews.com.au/feed/"

print url

feed = feedparser.parse(url)


for entry in feed.entries:

    published = dateutil.parser.parse(entry.date);
    description_text = BeautifulSoup(entry.description).get_text()

    print entry.id
    print entry.title  
    print entry.link
    print entry.author
    print description_text
    print entry.content[0].value

    record = {"link" : entry.link,
              "title" : entry.title,
              "author" : entry.author,
              "published" : published,
              "description" : description_text,
              "fulltext" : entry.content[0].value}
    
    # we changed over to this feed instead of viclabor
    # so we need to make sure we don't get the old items
    cutoff = dateutil.parser.parse('2013-02-20').date()
    
    if published.date() > cutoff:
        scraperwiki.sqlite.save(unique_keys=["link"], data=record)

