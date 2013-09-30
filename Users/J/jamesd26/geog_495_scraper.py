import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.neighborhoodscout.com/neighborhoods/crime-rates/top100dangerous/")
print html

root = lxml.html.fromstring(html)
count = 0
for tr in root.cssselect("table tr"):
    tds = root.cssselect("td")
    if count < 200:
        rank = int(tds[0 + count].text_content())
        data = {
            'City' : tds[1 + count].text_content(),
            'Rank' : rank
        }
        print data
        count += 2
        scraperwiki.sqlite.save(unique_keys=['City'], data=data)

