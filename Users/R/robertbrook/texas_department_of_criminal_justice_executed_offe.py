import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.tdcj.state.tx.us/stat/dr_executed_offenders.html")
root = lxml.html.fromstring(html)

for tr in root.cssselect("table.os tbody"):
    tds = tr.cssselect("td")
    data = {
      'execution' : tds[0].text_content(),
      'lastName' : tds[3].text_content(),
      'firstName' : tds[4].text_content(),
      'tdcjNumber' : tds[5].text_content(),
      'age' : tds[6].text_content(),
      'date' : tds[7].text_content(),
      'race' : tds[8].text_content(),
      'county' : tds[9].text_content()
    }
    scraperwiki.sqlite.save(unique_keys=['tdcjNumber'], data=data)

import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.tdcj.state.tx.us/stat/dr_executed_offenders.html")
root = lxml.html.fromstring(html)

for tr in root.cssselect("table.os tbody"):
    tds = tr.cssselect("td")
    data = {
      'execution' : tds[0].text_content(),
      'lastName' : tds[3].text_content(),
      'firstName' : tds[4].text_content(),
      'tdcjNumber' : tds[5].text_content(),
      'age' : tds[6].text_content(),
      'date' : tds[7].text_content(),
      'race' : tds[8].text_content(),
      'county' : tds[9].text_content()
    }
    scraperwiki.sqlite.save(unique_keys=['tdcjNumber'], data=data)

