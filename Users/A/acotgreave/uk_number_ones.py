import scraperwiki
from bs4 import BeautifulSoup

for x in range(1960,2013):
    html = scraperwiki.scrape("http://www.officialcharts.com/all-the-number-ones-singles-list/_/" + str(x) + "/")
    import lxml.html
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("table.chart tr.entry"):
        tds = tr.cssselect("td")
    
        data = {
          'date' : tds[0].text_content(),
          'artist' : tds[1].text_content(),
          'title' : tds[2].text_content(),
          'weeks' : int(tds[3].text_content())
        }
        scraperwiki.sqlite.save(unique_keys=['date'], data=data)


