import scraperwiki
import lxml.html
import datetime

candidates = (["mittromney", "barackobama", "ricksantorum", "newtgingrich"]);
date = datetime.date.today()

for i in candidates:
    url = ("http://twitter.com/" + i)
    print url
    html = scraperwiki.scrape(url)
    raw = lxml.html.fromstring(html)


    for row in raw.cssselect("span#follower_count"):
        print row.text
        data = {
            'date':date,
            'handle':i,
            'followers':row.text
        }
    scraperwiki.sqlite.save(unique_keys=['date'], data=data)
import scraperwiki
import lxml.html
import datetime

candidates = (["mittromney", "barackobama", "ricksantorum", "newtgingrich"]);
date = datetime.date.today()

for i in candidates:
    url = ("http://twitter.com/" + i)
    print url
    html = scraperwiki.scrape(url)
    raw = lxml.html.fromstring(html)


    for row in raw.cssselect("span#follower_count"):
        print row.text
        data = {
            'date':date,
            'handle':i,
            'followers':row.text
        }
    scraperwiki.sqlite.save(unique_keys=['date'], data=data)
