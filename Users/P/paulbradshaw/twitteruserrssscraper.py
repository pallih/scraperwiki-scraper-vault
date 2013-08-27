import scraperwiki
import lxml.html

url = 'http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=bishopofdurham'

def scrapetweets(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tweets = root.cssselect("item")
    record = {}
    for tweet in tweets:
        print tweet.text_content()
        record['tweet'] = tweet.text_content()
        scraperwiki.sqlite.save(['tweet'],record)
        

scrapetweets(url)import scraperwiki
import lxml.html

url = 'http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=bishopofdurham'

def scrapetweets(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tweets = root.cssselect("item")
    record = {}
    for tweet in tweets:
        print tweet.text_content()
        record['tweet'] = tweet.text_content()
        scraperwiki.sqlite.save(['tweet'],record)
        

scrapetweets(url)import scraperwiki
import lxml.html

url = 'http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=bishopofdurham'

def scrapetweets(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tweets = root.cssselect("item")
    record = {}
    for tweet in tweets:
        print tweet.text_content()
        record['tweet'] = tweet.text_content()
        scraperwiki.sqlite.save(['tweet'],record)
        

scrapetweets(url)