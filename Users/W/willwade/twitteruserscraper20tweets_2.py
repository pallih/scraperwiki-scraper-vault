import scraperwiki
import lxml.html

url = 'https://twitter.com/search?q=ashfordvineyard&src=typd'

def scrapetweets(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    people = root.cssselect("div.stream-item-header")
    tweets = root.cssselect("p.js-tweet-text")
    record = {}
    
    for tweet in tweets:
        record['tweet'] = tweet.text_content()
        scraperwiki.sqlite.save(['tweet'],record)
    
    for person in people:        
        #print tweet.csselect("a.tweet-timestamp").text_content()
        pimg = person.xpath("/img/src")
        print pimg
        print person.text_content()
        
scrapetweets(url)