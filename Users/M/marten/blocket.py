import scraperwiki

# Blank Python

import scraperwiki
import lxml.html

print "Hello, coding in the cloud!"
html = scraperwiki.scrape("http://www.blocket.se/hela_sverige/bilar?q=volvo&cg=1020&st=s&l=0&ca=11&w=3&f=a&o=1")
print html

root = lxml.html.fromstring(html)

# <a href="http://www.blocket.se/hela_sverige/bilar?q=volvo&amp;cg=1020&amp;st=s&amp;l=0&ca=11&w=3&f=a&o=2">Nästa sida &raquo;</a>

#<div class="desc">
#<a tabindex="50" class="item_link" href="http://www.blocket.se/stockholm/Volvo_740_Turbo_39464914.htm?ca=11&w=3">Volvo 740 Turbo -86</a>
#<p class="list_price">11 500:-</p>

for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)
import scraperwiki

# Blank Python

import scraperwiki
import lxml.html

print "Hello, coding in the cloud!"
html = scraperwiki.scrape("http://www.blocket.se/hela_sverige/bilar?q=volvo&cg=1020&st=s&l=0&ca=11&w=3&f=a&o=1")
print html

root = lxml.html.fromstring(html)

# <a href="http://www.blocket.se/hela_sverige/bilar?q=volvo&amp;cg=1020&amp;st=s&amp;l=0&ca=11&w=3&f=a&o=2">Nästa sida &raquo;</a>

#<div class="desc">
#<a tabindex="50" class="item_link" href="http://www.blocket.se/stockholm/Volvo_740_Turbo_39464914.htm?ca=11&w=3">Volvo 740 Turbo -86</a>
#<p class="list_price">11 500:-</p>

for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)
