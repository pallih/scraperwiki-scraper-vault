from datetime import datetime
import time

import scraperwiki
import feedparser

FEEDS = [
    'http://feeds.guiainfantil.com/guia_infantil_ninos_bebes',
    'http://www.consejos-de-belleza.com/feed',
    'http://feeds.feedburner.com/periodicoelzocalo',
]

def ScrapeFeeds(feeds):
    for feed in feeds:
        parsed_feed = feedparser.parse(feed)
        entries = []
        entries.extend(parsed_feed['items'])
        for entry in entries:
            modified = datetime.fromtimestamp(time.mktime(entry['updated_parsed']))
            title = entry['title'] or entry['link']
            data = {
                'tito' : entry['links'],
                'title': title,
                'link': entry['link'],
                'modified' : modified,
                'feed': feed,
            }
            scraperwiki.sqlite.save(unique_keys=['link'], data=data)
            
ScrapeFeeds(FEEDS)from datetime import datetime
import time

import scraperwiki
import feedparser

FEEDS = [
    'http://feeds.guiainfantil.com/guia_infantil_ninos_bebes',
    'http://www.consejos-de-belleza.com/feed',
    'http://feeds.feedburner.com/periodicoelzocalo',
]

def ScrapeFeeds(feeds):
    for feed in feeds:
        parsed_feed = feedparser.parse(feed)
        entries = []
        entries.extend(parsed_feed['items'])
        for entry in entries:
            modified = datetime.fromtimestamp(time.mktime(entry['updated_parsed']))
            title = entry['title'] or entry['link']
            data = {
                'tito' : entry['links'],
                'title': title,
                'link': entry['link'],
                'modified' : modified,
                'feed': feed,
            }
            scraperwiki.sqlite.save(unique_keys=['link'], data=data)
            
ScrapeFeeds(FEEDS)