import scraperwiki

print "Hello, coding in the cloud!"

import scraperwiki
html = scraperwiki.scrape("http://www.vacationhomes.com/")
print html

import lxml.html
root = lxml.html.fromstring(html)
for a in root.cssselect("div[class^='usa']>ul>li>a[href^='/united-states']"):
    #tds = tr.cssselect("td")
    print a.text_content()
    data = {
      'country' : 'United States',
      'state' : a.text_content()
    }
    scraperwiki.sqlite.save(unique_keys=['state'], data=data) 
# Blank Python

import scraperwiki

print "Hello, coding in the cloud!"

import scraperwiki
html = scraperwiki.scrape("http://www.vacationhomes.com/")
print html

import lxml.html
root = lxml.html.fromstring(html)
for a in root.cssselect("div[class^='usa']>ul>li>a[href^='/united-states']"):
    #tds = tr.cssselect("td")
    print a.text_content()
    data = {
      'country' : 'United States',
      'state' : a.text_content()
    }
    scraperwiki.sqlite.save(unique_keys=['state'], data=data) 
# Blank Python

