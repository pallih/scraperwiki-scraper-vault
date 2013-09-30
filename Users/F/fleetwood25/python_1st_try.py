print "Trying to make this work!"
import scraperwiki
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)print "Trying to make this work!"
import scraperwiki
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)