import scraperwiki
import lxml.html
import datetime

candidates = (["jokowi_do2", "basuki_btp", "jasmev20", "jokowiahok", "kartikadjoemadi"])


date = datetime.date(2012, 9, 14)


for candidate_name in candidates:
    url = ("http://twitter.com/" + candidate_name)
    html = scraperwiki.scrape(url)
    raw = lxml.html.fromstring(html)

    for row in raw.cssselect("span#follower_count"):
        print row.text
        data = {
            'date':date,
            'handle': candidate_name,
            'followers':row.text
        }

        scraperwiki.sqlite.save(unique_keys=['date'], data=data)