import scraperwiki
import lxml.html
import dateutil.parser

html = scraperwiki.scrape("https://github.com/bodil/catnip/tags")
root = lxml.html.fromstring(html)
for li in root.cssselect("ol.download-list li"):
    data = {
        "tag": li.cssselect("a[title]")[0].attrib["title"],
        "hash": li.cssselect("p a[title]")[0].text_content(),
        "time": dateutil.parser.parse(li.cssselect("time[datetime]")[0].attrib["datetime"]),
        "href": "https://github.com" + li.cssselect("p a[title]")[0].attrib["href"]
    }
    scraperwiki.sqlite.save(unique_keys=["tag"], data=data)

import scraperwiki
import lxml.html
import dateutil.parser

html = scraperwiki.scrape("https://github.com/bodil/catnip/tags")
root = lxml.html.fromstring(html)
for li in root.cssselect("ol.download-list li"):
    data = {
        "tag": li.cssselect("a[title]")[0].attrib["title"],
        "hash": li.cssselect("p a[title]")[0].text_content(),
        "time": dateutil.parser.parse(li.cssselect("time[datetime]")[0].attrib["datetime"]),
        "href": "https://github.com" + li.cssselect("p a[title]")[0].attrib["href"]
    }
    scraperwiki.sqlite.save(unique_keys=["tag"], data=data)

