import scraperwiki
import json

html = scraperwiki.scrape("http://search.twitter.com/search.json?q=arts+place%3Aecca95cfe1a0dca1")
root = json.loads(html)
for result in root['results']:
    print result['text']
    data = {
        'name' : result['from_user'],
        'text' : result['text']
        }
    scraperwiki.sqlite.save(unique_keys=['text'],data=data)


