import scraperwiki

# Blank Python

import scraperwiki  
import lxml.html     
html = scraperwiki.scrape("http://everguide.com.au/melbourne/event/2012-jun-19/once-upon-a-warehouse")    
root = lxml.html.fromstring(html)


nl = root.cssselect("div.title span")[0]           

tl = root.cssselect("div.time *")[0]       

vl = root.cssselect("div.ven a")[0]           

scraperwiki.sqlite.save_var('theTitle', nl.text)    
scraperwiki.sqlite.save_var('theDate', tl.tail) 
scraperwiki.sqlite.save_var('theVenue', vl.text)    
   
print scraperwiki.sqlite.get_var('theTitle')
print scraperwiki.sqlite.get_var('theDate')
print scraperwiki.sqlite.get_var('theVenue')import scraperwiki

# Blank Python

import scraperwiki  
import lxml.html     
html = scraperwiki.scrape("http://everguide.com.au/melbourne/event/2012-jun-19/once-upon-a-warehouse")    
root = lxml.html.fromstring(html)


nl = root.cssselect("div.title span")[0]           

tl = root.cssselect("div.time *")[0]       

vl = root.cssselect("div.ven a")[0]           

scraperwiki.sqlite.save_var('theTitle', nl.text)    
scraperwiki.sqlite.save_var('theDate', tl.tail) 
scraperwiki.sqlite.save_var('theVenue', vl.text)    
   
print scraperwiki.sqlite.get_var('theTitle')
print scraperwiki.sqlite.get_var('theDate')
print scraperwiki.sqlite.get_var('theVenue')