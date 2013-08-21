import scraperwiki
import lxml.html
import dateutil.parser

html = scraperwiki.scrape("http://vault.fbi.gov/recently-added")
root = lxml.html.fromstring(html)
for dd in root.cssselect("dd[class='contenttype-folder']"):
    anchor = dd.cssselect("a")[0]
    if anchor:
        link = anchor.get("href")
        title = dd.cssselect("h3")[0].text_content()
        created = dd.cssselect("span[class='created']")[0].text_content()
        data = {
          'created': dateutil.parser.parse(created),
          'title': title,
          'link': link
        }
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)

