import scraperwiki

# Blank Python
print "Hello, coding in the cloud!"
import scraperwiki
html = scraperwiki.scrape("https://twitter.com/#!/newsmotion_org/ows-citizen/members")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'members' : tds[0].text_content(),
 }
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'members' : tds[0].text_content(),
      }
    print data
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'members' : tds[0].text_content(),
    }
    scraperwiki.sqlite.save(unique_keys=['members'], data=data)

import scraperwiki

# Blank Python
print "Hello, coding in the cloud!"
import scraperwiki
html = scraperwiki.scrape("https://twitter.com/#!/newsmotion_org/ows-citizen/members")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'members' : tds[0].text_content(),
 }
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'members' : tds[0].text_content(),
      }
    print data
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'members' : tds[0].text_content(),
    }
    scraperwiki.sqlite.save(unique_keys=['members'], data=data)

