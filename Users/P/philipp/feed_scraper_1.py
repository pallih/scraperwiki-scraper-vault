from datetime import datetime
import time

import scraperwiki
import feedparser

FEEDS = [
    'http://feeds.pinboard.in/rss/t:clojure',
    'http://feeds.pinboard.in/rss/t:distributed',
    'http://feeds.pinboard.in/rss/t:github',
    'http://feeds.pinboard.in/rss/t:haskell',
    'http://feeds.pinboard.in/rss/t:javascript',
    'http://feeds.pinboard.in/rss/t:js',
    'http://feeds.pinboard.in/rss/t:llvm',
    'http://feeds.pinboard.in/rss/t:machinelearning',
    'http://feeds.pinboard.in/rss/t:mapreduce',
    'http://feeds.pinboard.in/rss/t:nodejs',
    'http://feeds.pinboard.in/rss/t:ocaml',
    'http://feeds.pinboard.in/rss/t:programming',
    'http://feeds.pinboard.in/rss/t:python',
    'http://feeds.pinboard.in/rss/t:stats',
    'http://feeds.pinboard.in/rss/t:ruby',
    'http://feeds.pinboard.in/rss/t:tools',
    'http://feeds.pinboard.in/rss/t:web',
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
                'title': title,
                'link': entry['link'],
                'modified' : modified,
                'feed': feed,
            }
            scraperwiki.sqlite.save(unique_keys=['link'], data=data)
            
ScrapeFeeds(FEEDS)