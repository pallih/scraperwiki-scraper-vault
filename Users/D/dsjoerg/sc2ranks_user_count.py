import scraperwiki
import lxml.html
import datetime

html = scraperwiki.scrape('http://sc2ranks.com')

root = lxml.html.fromstring(html)
for div in root.cssselect('div."shadow stats"'):
    data = { "now": datetime.datetime.now(),
             "PlayerCount" : div.text_content() }
    scraperwiki.sqlite.save(["now"], data)
