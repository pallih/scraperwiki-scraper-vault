import scraperwiki
import lxml.html
from datetime import datetime
          
html = scraperwiki.scrape("http://www.jsdb.io/?sort=new")

root = lxml.html.fromstring(html)

for el in root.cssselect("div .listing"): 

    data = {
            'title' : el.cssselect("h3 a")[0].text,
            'link' : 'http://www.jsdb.io' + el.cssselect("h3 a")[0].attrib['href'],
            'description' : el.cssselect("p")[0].text,
            'date' : datetime.now()
    }
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)

