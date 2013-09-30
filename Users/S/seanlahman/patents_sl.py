import scraperwiki

print "and here we go..."

import scraperwiki           
html = scraperwiki.scrape("http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query=ac%2Frochester&d=PTXT")
print html


import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'PAT NO.' : tds[0].text_content(),
            'Title' : int(tds[4].text_content())
        }
        print dataimport scraperwiki

print "and here we go..."

import scraperwiki           
html = scraperwiki.scrape("http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query=ac%2Frochester&d=PTXT")
print html


import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'PAT NO.' : tds[0].text_content(),
            'Title' : int(tds[4].text_content())
        }
        print data