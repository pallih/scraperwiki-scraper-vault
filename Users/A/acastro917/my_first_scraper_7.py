import scraperwiki
import lxml.html 

html = scraperwiki.scrape("http://zigsa.com/demo/table/")

print html


root = lxml.html.fromstring(html) 

for tr in root.cssselect("div[align='left'] tr.tcont"): 
    tds = tr.cssselect("td") 
    data = { 
        'country' : tds[0].text_content(),
 '6' : tds[1].text_content(),
 '7' : tds[2].text_content(),
 '8' : tds[3].text_content(),
 
       
    }
    print data 
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)

import scraperwiki
import lxml.html 

html = scraperwiki.scrape("http://zigsa.com/demo/table/")

print html


root = lxml.html.fromstring(html) 

for tr in root.cssselect("div[align='left'] tr.tcont"): 
    tds = tr.cssselect("td") 
    data = { 
        'country' : tds[0].text_content(),
 '6' : tds[1].text_content(),
 '7' : tds[2].text_content(),
 '8' : tds[3].text_content(),
 
       
    }
    print data 
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)

