import scraperwiki


html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/health.htm") 
print html

import lxml.html            
root = lxml.html.fromstring(html) 
for tr in root.cssselect("div[align='left'] tr.tcont"):    
    tds = tr.cssselect("td")     
    data = {       
     'country' : tds[1].text_content(),       
     'years_in_school' : tds[5].text_content()
     
    }     
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)


