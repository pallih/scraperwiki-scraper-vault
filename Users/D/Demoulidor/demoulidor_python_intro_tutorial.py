# Demoulidor Python intro tutorial
import scraperwiki
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
#print html

import lxml.html
root = lxml.html.fromstring(html)
t = root.cssselect("title")
print t.text_content()
data = {}
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'Media de anos na Escola' : int(tds[4].text_content())
    }
    #print data
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)




# Demoulidor Python intro tutorial
import scraperwiki
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
#print html

import lxml.html
root = lxml.html.fromstring(html)
t = root.cssselect("title")
print t.text_content()
data = {}
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'Media de anos na Escola' : int(tds[4].text_content())
    }
    #print data
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)




