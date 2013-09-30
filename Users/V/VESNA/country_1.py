import scraperwiki

print "Hello World, my head is in the cloud!"

import scraperwiki
html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html

import lxml.html 

root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'report_year' : int(tds[1].text_content()),
            'total_years_in_school' : int(tds[4].text_content()),
            'average_men' : int(tds[7].text_content()),            
            'average_women' : int(tds[10].text_content()) 
        }
           

        scraperwiki.sqlite.save(unique_keys=['country'], data=data)import scraperwiki

print "Hello World, my head is in the cloud!"

import scraperwiki
html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html

import lxml.html 

root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'report_year' : int(tds[1].text_content()),
            'total_years_in_school' : int(tds[4].text_content()),
            'average_men' : int(tds[7].text_content()),            
            'average_women' : int(tds[10].text_content()) 
        }
           

        scraperwiki.sqlite.save(unique_keys=['country'], data=data)