import scraperwiki
import lxml.html
import datetime


handle = ("mittromney")
url = ("http://twitter.com/" + handle)
#print url

html = scraperwiki.scrape(url)
raw = lxml.html.fromstring(html)

#print html

date = datetime.date.today()
#print date


for row in raw.cssselect("span#follower_count"):
    print row.text
    data = {
        'date':date,
        'handle':handle,
        'followers':row.text
    }
    scraperwiki.sqlite.save(unique_keys=['date'], data=data)


import scraperwiki
import lxml.html
import datetime


handle = ("mittromney")
url = ("http://twitter.com/" + handle)
#print url

html = scraperwiki.scrape(url)
raw = lxml.html.fromstring(html)

#print html

date = datetime.date.today()
#print date


for row in raw.cssselect("span#follower_count"):
    print row.text
    data = {
        'date':date,
        'handle':handle,
        'followers':row.text
    }
    scraperwiki.sqlite.save(unique_keys=['date'], data=data)


