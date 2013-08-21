""" 
I have a bunch of tumblrs. I'd like to aggregate them on my own 
(horribly neglected) WordPres blog. This seems like  the natural
first step.

"""

import scraperwiki
import feedparser
import pprint
import datetime


feeds = {
    "Here's the thing."          :    'http://amandabees.tumblr.com/rss',
    'Capoeira Brooklyn Tumblr'   :    'http://raizes.tumblr.com/rss',
    'CS 101'                     :    'http://cs101.tumblr.com/rss',
    'If you want to be loved'    :    'http://keepyoungandbeautiful.tumblr.com/rss',
    'jour72312'                  :    'http://jour72312.tumblr.com/rss',
    'Lunch'                      :    'http://pickledcarrots.tumblr.com/rss',
    'moving'                     :    'http://nomadly.tumblr.com/rss',
    'News, Games'                :    'http://newsgamery.tumblr.com/rss',
    'Storytelling'               :    'http://craft-ii.tumblr.com/rss',
    'These are things.'          :    'http://moreia.tumblr.com/rss'
}

for k, v in feeds.iteritems():
    d = feedparser.parse(v)
    feed_url = d['feed']['link']
    feed_name = k
    for entry in d['entries']:
        # summary = entry.summary + ' (via <a href="' + feed_url + '">' + feed_name + '</a>)'
        if(entry.title):
            title = entry.title + ' / ' + feed_name + ''
        else:
            title = ''
        sort_date = datetime.datetime(entry.updated_parsed[0], entry.updated_parsed[1], 
            entry.updated_parsed[2], entry.updated_parsed[3], entry.updated_parsed[4], 
            entry.updated_parsed[5])
        data = {
            'pubDate' :  entry.updated,
            'title' : title,
            'tumblr_type' : entry.title_detail.type,
            'summary' : entry.summary,
            'link' : entry.link,
            'feed_url' : feed_url,
            'feed_name' : feed_name,
            'sort_date' : sort_date
        }
        scraperwiki.sqlite.save(table_name="feeds", unique_keys=['link'], data=data)
        # print entry.updated_parsed
        print entry.title
        print entry.title_detail.value + ' / ' + entry.title_detail.type
        """print entry.summary
        print entry.link"""
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(entry)

