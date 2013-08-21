import scraperwiki
import lxml.html

url = 'https://api.twitter.com/1.1/statuses/user_timeline.json&screen_name=kaidiekmann&include_rts=true&since_id=1&max_id=20'

def scrapetweets(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tweets = root.cssselect("item")
    record = {}
    for tweet in tweets:
        print tweet.text_content()
        record['tweet'] = tweet.text_content()[16:]
        scraperwiki.sqlite.save(['tweet'],record)
        

scrapetweets(url)