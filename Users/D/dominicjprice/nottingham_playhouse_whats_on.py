import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.nottinghamplayhouse.co.uk/whats-on/")
root = lxml.html.fromstring(html)
order = 0
for li in root.cssselect("ol li.production"):
    data = {
        'order' : order,
        'title' : li.cssselect("h2 a")[0].text_content(),
        'date' : li.cssselect("p.production-dates")[0].text_content(),
        'description' : li.cssselect("p.excerpt")[0].text_content(),
        'link' : li.cssselect("h2 a")[0].get("href")
    }
    order = order + 1
    scraperwiki.sqlite.save(unique_keys=['order'], data=data)import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.nottinghamplayhouse.co.uk/whats-on/")
root = lxml.html.fromstring(html)
order = 0
for li in root.cssselect("ol li.production"):
    data = {
        'order' : order,
        'title' : li.cssselect("h2 a")[0].text_content(),
        'date' : li.cssselect("p.production-dates")[0].text_content(),
        'description' : li.cssselect("p.excerpt")[0].text_content(),
        'link' : li.cssselect("h2 a")[0].get("href")
    }
    order = order + 1
    scraperwiki.sqlite.save(unique_keys=['order'], data=data)