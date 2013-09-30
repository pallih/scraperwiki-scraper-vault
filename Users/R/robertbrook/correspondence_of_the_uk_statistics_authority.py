import scraperwiki
import lxml.html           

html = scraperwiki.scrape("http://www.statisticsauthority.gov.uk/reports---correspondence/correspondence/index.html")

root = lxml.html.fromstring(html)
for tr in root.cssselect("div#content-display table tbody tr"):
    tds = tr.cssselect("td")
    for td in tds:
        data = {
          'from' : tds[0].text_content(),
          'to' : tds[1].text_content(),
          'regarding' : tds[2].text_content(),
          'date' : tds[3].text_content()
        }
    print data
    scraperwiki.sqlite.save(unique_keys=['regarding'], data=data)


import scraperwiki
import lxml.html           

html = scraperwiki.scrape("http://www.statisticsauthority.gov.uk/reports---correspondence/correspondence/index.html")

root = lxml.html.fromstring(html)
for tr in root.cssselect("div#content-display table tbody tr"):
    tds = tr.cssselect("td")
    for td in tds:
        data = {
          'from' : tds[0].text_content(),
          'to' : tds[1].text_content(),
          'regarding' : tds[2].text_content(),
          'date' : tds[3].text_content()
        }
    print data
    scraperwiki.sqlite.save(unique_keys=['regarding'], data=data)


