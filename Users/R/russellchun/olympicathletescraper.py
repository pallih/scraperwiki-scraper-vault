import scraperwiki
import lxml.html
import datetime


for i in range(1,75):
    url = ("http://www.teamusa.org/Athletes?season={79EDD928-E32F-4D4A-99DC-C3BE91F718DF}&page=" + i)
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

