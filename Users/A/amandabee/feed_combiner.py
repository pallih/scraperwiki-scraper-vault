import scraperwiki
import feedparser
#import pprint
import datetime


feeds = {
    'Ajai' : 'http://ajairaj.com/tagged/data-visualization/feed/',
    'Amanda Hickman':  'http://jour72312.tumblr.com/rss',
    'Amanda Hou' : 'http://amandahou.tumblr.com/rss',
    'Dominik' : 'http://doli0000.tumblr.com/rss',
    'Heather': 'http://datavizwiz.tumblr.com/rss',
    'Jeannie' : 'http://vintagejeannie.tumblr.com/rss',
    'Jesse': 'http://jessemetzgerdata.tumblr.com/rss',
    'Jessica' : 'http://glazerdata.tumblr.com/rss',
    'Kathleen' : 'http://kathleencaulderwood.tumblr.com/rss',
    'Nick' : 'http://wellsangels.tumblr.com/rss',
    'Raed' : 'http://raedzdataviz.tumblr.com/rss',
    'Rebecca': 'http://rsesny.tumblr.com/rss',
    'Sophia':  'http://sophrosenba.tumblr.com/rss',
    'Susie' : 'http://pinterest.com/susarm/cool-data-visualizations/rss',
    'Tobias' : 'http://tobysal.com/category/dataaboutdata/feed/',
    'Guia Marie' : 'http://datavizness.tumblr.com/rss',
    'Michael' : 'http://datapalooza.tumblr.com/rss'
}

for k, v in feeds.iteritems():
    try:
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
    except:
            e = sys.exc_info()[0]
            write_to_page( "<p>Error: %s</p>" % e )

import scraperwiki
import feedparser
#import pprint
import datetime


feeds = {
    'Ajai' : 'http://ajairaj.com/tagged/data-visualization/feed/',
    'Amanda Hickman':  'http://jour72312.tumblr.com/rss',
    'Amanda Hou' : 'http://amandahou.tumblr.com/rss',
    'Dominik' : 'http://doli0000.tumblr.com/rss',
    'Heather': 'http://datavizwiz.tumblr.com/rss',
    'Jeannie' : 'http://vintagejeannie.tumblr.com/rss',
    'Jesse': 'http://jessemetzgerdata.tumblr.com/rss',
    'Jessica' : 'http://glazerdata.tumblr.com/rss',
    'Kathleen' : 'http://kathleencaulderwood.tumblr.com/rss',
    'Nick' : 'http://wellsangels.tumblr.com/rss',
    'Raed' : 'http://raedzdataviz.tumblr.com/rss',
    'Rebecca': 'http://rsesny.tumblr.com/rss',
    'Sophia':  'http://sophrosenba.tumblr.com/rss',
    'Susie' : 'http://pinterest.com/susarm/cool-data-visualizations/rss',
    'Tobias' : 'http://tobysal.com/category/dataaboutdata/feed/',
    'Guia Marie' : 'http://datavizness.tumblr.com/rss',
    'Michael' : 'http://datapalooza.tumblr.com/rss'
}

for k, v in feeds.iteritems():
    try:
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
    except:
            # e = sys.exc_info()[0]
            write_to_page( "<p>Error: %s</p>" % e )

