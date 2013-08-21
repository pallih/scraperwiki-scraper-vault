import scraperwiki
html = scraperwiki.scrape("https://portal.aws.amazon.com/gp/aws/developer/account/index.html")
import lxml.html
from datetime import date
import time
root = lxml.html.fromstring(html)
for tr in root.cssselect("div tr"):
    tds = tr.cssselect("td")
    data = {
        'Player' : tds[0].text_content(),
    }
    scraperwiki.sqlite.save(unique_keys=['Player'], data=data)

