import scraperwiki
import lxml.html


url = 'https://twitter.com/search?q=%MOHARE2024&src=typd'

def scrapetweets(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tweets = root.cssselect("p.js-tweet-text")
    record = {}

    for tweet in tweets:

        print tweet.text_content()
        record['tweet'] = tweet.text_content()
        scraperwiki.sqlite.save(['tweet'],record)
        

scrapetweets(url)import scraperwiki
import lxml.html


url = 'https://twitter.com/search?q=%MOHARE2024&src=typd'

def scrapetweets(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tweets = root.cssselect("p.js-tweet-text")
    record = {}

    for tweet in tweets:

        print tweet.text_content()
        record['tweet'] = tweet.text_content()
        scraperwiki.sqlite.save(['tweet'],record)
        

scrapetweets(url)import scraperwiki
import lxml.html


url = 'https://twitter.com/search?q=%MOHARE2024&src=typd'

def scrapetweets(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tweets = root.cssselect("p.js-tweet-text")
    record = {}

    for tweet in tweets:

        print tweet.text_content()
        record['tweet'] = tweet.text_content()
        scraperwiki.sqlite.save(['tweet'],record)
        

scrapetweets(url)