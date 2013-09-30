import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://xkcd.com/1")

root = lxml.html.fromstring(html)

middle = root.csselect("div[id='middleContainer']")[0]

print middle

import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://xkcd.com/1")

root = lxml.html.fromstring(html)

middle = root.csselect("div[id='middleContainer']")[0]

print middle

