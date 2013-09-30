import scraperwiki
import lxml.html
      
html = scraperwiki.scrape("http://www.greatamericanbeerfestival.com/at-the-festival/breweries-at-the-2012-festival")

root = lxml.html.fromstring(html)
i = 1
for tr in root.cssselect("#brewery_table tbody tr"):
    tds = tr.cssselect("td")
    data = {
        'id' : i,
        'name' : tds[0].text_content(),
        'city' : tds[1].text_content(),
        'state' : tds[2].text_content(),
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    i += 1import scraperwiki
import lxml.html
      
html = scraperwiki.scrape("http://www.greatamericanbeerfestival.com/at-the-festival/breweries-at-the-2012-festival")

root = lxml.html.fromstring(html)
i = 1
for tr in root.cssselect("#brewery_table tbody tr"):
    tds = tr.cssselect("td")
    data = {
        'id' : i,
        'name' : tds[0].text_content(),
        'city' : tds[1].text_content(),
        'state' : tds[2].text_content(),
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    i += 1