import scraperwiki
import json

html = scraperwiki.scrape("http://search.twitter.com/search.json?q=%23nhshd&rpp=100&include_entities=false&result_type=recent")
root = json.loads(html)
for result in root['results']:
    print result['text']
    data = {
        'name' : result['from_user'],
        'text' : result['text']
        }
    scraperwiki.sqlite.save(unique_keys=['text'],data=data)


