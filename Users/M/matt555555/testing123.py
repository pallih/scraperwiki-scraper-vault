import scraperwiki

print "Hello, coding in the cloud!"
html = scraperwiki.scrape("http://www.")
import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div tr"):
    tds = tr.cssselect("td")
    data = {'country' : tds[0].text_content()
        }
    print data
print html
import scraperwiki

print "Hello, coding in the cloud!"
html = scraperwiki.scrape("http://www.")
import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div tr"):
    tds = tr.cssselect("td")
    data = {'country' : tds[0].text_content()
        }
    print data
print html
