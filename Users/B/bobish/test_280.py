import scraperwiki
html = scraperwiki.scrape("http://fantasy.mlssoccer.com/player-list/")
import lxml.html
from datetime import date
import time

root = lxml.html.fromstring(html)

for tr in root.cssselect("div tr"):
    tds = tr.cssselect("td")
    if len(tds)==4:
        data = {
            'Player' : tds[0].text_content(),
            'Points' : tds[2].text_content(),
            'Team' : tds[1].text_content(),
            'Cost' : tds[3].text_content(),
            'Run Date' : time.asctime(time.localtime(time.time()))
            
        }
        scraperwiki.sqlite.save(unique_keys=['Points'], data=data)
import scraperwiki
html = scraperwiki.scrape("http://fantasy.mlssoccer.com/player-list/")
import lxml.html
from datetime import date
import time

root = lxml.html.fromstring(html)

for tr in root.cssselect("div tr"):
    tds = tr.cssselect("td")
    if len(tds)==4:
        data = {
            'Player' : tds[0].text_content(),
            'Points' : tds[2].text_content(),
            'Team' : tds[1].text_content(),
            'Cost' : tds[3].text_content(),
            'Run Date' : time.asctime(time.localtime(time.time()))
            
        }
        scraperwiki.sqlite.save(unique_keys=['Points'], data=data)
