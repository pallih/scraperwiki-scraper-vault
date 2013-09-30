import scraperwiki
import lxml.html           

html = scraperwiki.scrape("http://www.parliament.uk/business/publications/parliamentary-archives/archives-electronic/parliamentary-debates/historic-standing-committee-debates/")

root = lxml.html.fromstring(html)
for a in root.cssselect("div.inner div ul li a"):
    data = {
          'href' : a.get('href'),
        }
    scraperwiki.sqlite.save(unique_keys=['href'], data=data)
import scraperwiki
import lxml.html           

html = scraperwiki.scrape("http://www.parliament.uk/business/publications/parliamentary-archives/archives-electronic/parliamentary-debates/historic-standing-committee-debates/")

root = lxml.html.fromstring(html)
for a in root.cssselect("div.inner div ul li a"):
    data = {
          'href' : a.get('href'),
        }
    scraperwiki.sqlite.save(unique_keys=['href'], data=data)
