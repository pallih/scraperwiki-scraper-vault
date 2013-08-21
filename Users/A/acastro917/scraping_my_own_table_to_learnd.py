import scraperwiki

# Blank Python
print "Hello, coding in the cloud!"
import scraperwiki
html = scraperwiki.scrape("http://zigsa.com/tropo/newdata.html")
print html


import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[entry-content] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'title' : tds[0].text_content(),
'Autor' : tds[1].text_content(),

'last comment' : tds[3].text_content(),

'time' : tds[7].text_content(),

'custon' : tds[9].text_content(),
      'date' : int(tds[4].text_content())
    }
    scraperwiki.sqlite.save(unique_keys=['title'], data=data)






