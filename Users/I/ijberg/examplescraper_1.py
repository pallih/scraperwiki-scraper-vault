import scraperwiki

# Blank Python

print "Hello, coding in the cloud!"

import scraperwiki
html = scraperwiki.scrape("http://www.statisticbrain.com/number-of-dui-arrests-per-state/")
print html

import lxml.html
root = lxml.html.fromstring(html)
mydiv = (root.cssselect("div.postcontent'))[0]:

for tr in mydiv.cssselect("tr")[4:-2]
tds = tr.cssselect("td")
    
print lxml.html.tostring(tr)

data = {
            'state' : tds[0].text_content(),
  'DUI' : tds[1].text_content(),
 'pop' : tds[1].text_content()
        }

print data
scraperwiki.sqlite.save(unique_keys=['state', 'DUI', 'pop'], data=data)



import scraperwiki

# Blank Python

print "Hello, coding in the cloud!"

import scraperwiki
html = scraperwiki.scrape("http://www.statisticbrain.com/number-of-dui-arrests-per-state/")
print html

import lxml.html
root = lxml.html.fromstring(html)
mydiv = (root.cssselect("div.postcontent'))[0]:

for tr in mydiv.cssselect("tr")[4:-2]
tds = tr.cssselect("td")
    
print lxml.html.tostring(tr)

data = {
            'state' : tds[0].text_content(),
  'DUI' : tds[1].text_content(),
 'pop' : tds[1].text_content()
        }

print data
scraperwiki.sqlite.save(unique_keys=['state', 'DUI', 'pop'], data=data)



