import scraperwiki

# Blank Python
print "Jake"

# Download HTML from the web, crawl
import scraperwiki
html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html

# Parsing HTML to get the content
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"): # tr.cont is CSS selector
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    # SQL store 
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)
import scraperwiki

# Blank Python
print "Jake"

# Download HTML from the web, crawl
import scraperwiki
html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html

# Parsing HTML to get the content
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"): # tr.cont is CSS selector
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    # SQL store 
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)
