import scraperwiki
import lxml.html           

# Blank Python

html = scraperwiki.scrape("http://www.linquist.net/motorsports/bmw/wheels")
print html

root = lxml.html.fromstring(html)
print root

for tr in root.cssselect("tr.green,tr.red"):
    tds = tr.cssselect("td")
    data = {
      'wheel' : tds[0].text_content(),
      'size' : tds[1].text_content(),
      'offset' : tds[2].text_content(),
      'lowered' : tds[3].text_content(),
      'tire' : tds[4].text_content(),
      'body' : tds[5].text_content(),
      'rubbing' : tds[6].text_content(),
      'user' : tds[7].text_content()}
    print data
    scraperwiki.sqlite.save(unique_keys=['user','size','tire','offset','rubbing'], data=data)
import scraperwiki
import lxml.html           

# Blank Python

html = scraperwiki.scrape("http://www.linquist.net/motorsports/bmw/wheels")
print html

root = lxml.html.fromstring(html)
print root

for tr in root.cssselect("tr.green,tr.red"):
    tds = tr.cssselect("td")
    data = {
      'wheel' : tds[0].text_content(),
      'size' : tds[1].text_content(),
      'offset' : tds[2].text_content(),
      'lowered' : tds[3].text_content(),
      'tire' : tds[4].text_content(),
      'body' : tds[5].text_content(),
      'rubbing' : tds[6].text_content(),
      'user' : tds[7].text_content()}
    print data
    scraperwiki.sqlite.save(unique_keys=['user','size','tire','offset','rubbing'], data=data)
