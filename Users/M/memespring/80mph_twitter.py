import scraperwiki
import lxml.html, lxml.cssselect
import re
import dateutil.parser

root = lxml.html.parse('http://search.twitter.com/search.atom?q=80mph').getroot()
for item in root.cssselect('feed > entry'):
    tweet_id = item.cssselect('id')[0].text
    tweet = item.cssselect('title')[0].text
    date_time = dateutil.parser.parse(item.cssselect('published')[0].text) #2011-05-27T10:15:02Z
    scraperwiki.sqlite.save(unique_keys=["tweet_id"], data={"tweet_id":tweet_id, "tweet":tweet, "date_time": date_time})           

