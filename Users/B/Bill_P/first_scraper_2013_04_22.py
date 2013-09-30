import scraperwiki

# Blank Python
# no 1. Make a new scraper
print "Hello, coding in the cloud!"

print "no. 2 Download HTML from the web"

import scraperwiki
html = scraperwiki.scrape( "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html


print "no. 3 Parsing the HTML to get your content (I typed this one)" 
print "this only prints the last row, the only difference is the print data not being indented"
print "this one I cannot add tabs or spaces to indent print data"
print "it works if it aligns with the data = " 

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
            }
        print data


print "no. 4 Saving to the ScraperWiki datastore, this one has the indent problem"
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
            }
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)

print "no. 3 Copy / Paste"
print "this one only prints the last row if not indented, but I can indent with tabs or spaces and it works" 

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        print data

print "no. 4 Saving to the ScraperWiki datastore"
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)

print "no. 5 Getting the data out again" 

print "in the SQL query box type: select * from swdata order by years_in_school desc limit 10"
import scraperwiki

# Blank Python
# no 1. Make a new scraper
print "Hello, coding in the cloud!"

print "no. 2 Download HTML from the web"

import scraperwiki
html = scraperwiki.scrape( "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html


print "no. 3 Parsing the HTML to get your content (I typed this one)" 
print "this only prints the last row, the only difference is the print data not being indented"
print "this one I cannot add tabs or spaces to indent print data"
print "it works if it aligns with the data = " 

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
            }
        print data


print "no. 4 Saving to the ScraperWiki datastore, this one has the indent problem"
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
            }
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)

print "no. 3 Copy / Paste"
print "this one only prints the last row if not indented, but I can indent with tabs or spaces and it works" 

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        print data

print "no. 4 Saving to the ScraperWiki datastore"
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)

print "no. 5 Getting the data out again" 

print "in the SQL query box type: select * from swdata order by years_in_school desc limit 10"
