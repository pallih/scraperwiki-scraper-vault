import scraperwiki
import simplejson

# retrieve a page
url = 'https://api.twitter.com/1/statuses/user_timeline.json?screen_name=mindop_sk&count=100&exclude_replies%20=true'

html = scraperwiki.scrape(url)
soup = simplejson.loads(html)
for result in soup:
    data = {}
    data['id'] = result['id']
    data['text'] = result['text']
    scraperwiki.sqlite.save(["id"], data)
