import scraperwiki
import lxml.html
import dateutil.parser
import datetime

url = 'https://www.census.gov/foreign-trade/statistics/state/data/al.html'
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
print(html)
table = root.cssselect("table")[3]

i = 1
for tr in table:
    tds = tr.cssselect("td")
    data = {
        'id' : i,
        'rank' : tds[0].text_content(),
        'country' : tds[1].text_content(),
        'y2008' : tds[6].text_content(),
        'y2009' : tds[7].text_content(),
        'y2010' : tds[8].text_content(),
        'y2011' : tds[9].text_content(),

#        'Description' : tds[6].text_content(),
        }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    i += 1

