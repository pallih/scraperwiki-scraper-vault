""" 
I have a bunch of tumblrs. I'd like to aggregate them on my own 
(horribly neglected) WordPres blog. This seems like  the natural
first step.

"""

import scraperwiki
import feedparser
#import pprint
import datetime


feeds = {
    "Nassol's Blog"    :    'http://nassol.tumblr.com/rss',
}

for k, v in feeds.iteritems():
    d = feedparser.parse(v)
    feed_url = d['feed']['link']
    feed_name = k
    for entry in d['entries']:
        # summary = entry.summary + ' (via <a href="' + feed_url + '">' + feed_name + '</a>)'
        title = entry.title + ' (via ' + feed_name + ')'
        sort_date = datetime.datetime(entry.updated_parsed[0], entry.updated_parsed[1], 
            entry.updated_parsed[2], entry.updated_parsed[3], entry.updated_parsed[4], 
            entry.updated_parsed[5])
        data = {
            'pubDate' :  entry.updated,
            'title' : title,
            'summary' : entry.summary,
            'link' : entry.link,
            'feed_url' : feed_url,
            'feed_name' : feed_name,
            'sort_date' : sort_date
        }
        scraperwiki.sqlite.save(table_name="feeds", unique_keys=['link'], data=data)
        """print entry.updated_parsed
        print entry.title
        print entry.summary
        print entry.link
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(entry)"""

""" 
I have a bunch of tumblrs. I'd like to aggregate them on my own 
(horribly neglected) WordPres blog. This seems like  the natural
first step.

"""

import scraperwiki
import feedparser
#import pprint
import datetime


feeds = {
    "Nassol's Blog"    :    'http://nassol.tumblr.com/rss',
}

for k, v in feeds.iteritems():
    d = feedparser.parse(v)
    feed_url = d['feed']['link']
    feed_name = k
    for entry in d['entries']:
        # summary = entry.summary + ' (via <a href="' + feed_url + '">' + feed_name + '</a>)'
        title = entry.title + ' (via ' + feed_name + ')'
        sort_date = datetime.datetime(entry.updated_parsed[0], entry.updated_parsed[1], 
            entry.updated_parsed[2], entry.updated_parsed[3], entry.updated_parsed[4], 
            entry.updated_parsed[5])
        data = {
            'pubDate' :  entry.updated,
            'title' : title,
            'summary' : entry.summary,
            'link' : entry.link,
            'feed_url' : feed_url,
            'feed_name' : feed_name,
            'sort_date' : sort_date
        }
        scraperwiki.sqlite.save(table_name="feeds", unique_keys=['link'], data=data)
        """print entry.updated_parsed
        print entry.title
        print entry.summary
        print entry.link
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(entry)"""

