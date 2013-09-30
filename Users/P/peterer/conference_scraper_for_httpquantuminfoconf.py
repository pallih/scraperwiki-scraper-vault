import scraperwiki
#import inspect
import lxml.html 


html = scraperwiki.scrape("http://quantum.info/conf/") 

root = lxml.html.fromstring(html) 

print html
eventlist = root.cssselect('li')

for event in eventlist :
    

    confname_css = event.cssselect('a')[0]
    confname = confname_css.text_content()
    
#   venueinfo_css = event.cssselect('div.venue_info')[0]

   
    date_css = event.cssselect('b')[0]
    
    dates = date_css.text_content()
    
    
    

    scraperwiki.sqlite.save(unique_keys=['name'], data={'name':confname,'dates':dates})           
    

#print idtags


import scraperwiki
#import inspect
import lxml.html 


html = scraperwiki.scrape("http://quantum.info/conf/") 

root = lxml.html.fromstring(html) 

print html
eventlist = root.cssselect('li')

for event in eventlist :
    

    confname_css = event.cssselect('a')[0]
    confname = confname_css.text_content()
    
#   venueinfo_css = event.cssselect('div.venue_info')[0]

   
    date_css = event.cssselect('b')[0]
    
    dates = date_css.text_content()
    
    
    

    scraperwiki.sqlite.save(unique_keys=['name'], data={'name':confname,'dates':dates})           
    

#print idtags


