import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.rightmove.co.uk/property-for-sale/Central-London.html?maxPrice=650000&minBedrooms=2&radius=3.0&index=10")

root = lxml.html.fromstring(html)
for el in root.cssselect("div.summarymaincontent"):
    for em in el.cssselect("p.price"):
        print em.text
    for em in el.cssselect("span.displayaddress"):
        print em.text
    for em in el.cssselect("h2.'address bedrooms'"):
        print em.text
