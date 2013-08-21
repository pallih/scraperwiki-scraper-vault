import scraperwiki
html = scraperwiki.scrape("http://dashboard.ed.gov/statecomparison.aspx?i=e&id=0&wt=40")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'state' : tds[0].text_content(),
      'total' : int(tds[4].text_content())
    }
    print data

