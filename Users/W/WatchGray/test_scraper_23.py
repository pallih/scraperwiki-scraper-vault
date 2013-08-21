import scraperwiki
import lxml.html
import datetime

candidates = (["mittromney", "BarackObama", "RickSantorum", "newtgingrich"]);
date = datetime.date.today()

for i in candidates:
    url = ("http://twitter.com/" + i)
    html = scraperwiki.scrape(url)
    raw = lxml.html.fromstring(html)

    print html

