import scraperwiki
#import inspect
import lxml.html 
import re

#Load the html of the Conference alerts physics page
html = scraperwiki.scrape("http://www.conferencealerts.com/topic-listing?topic=Physics") 
root = lxml.html.fromstring(html) 


eventlinks = root.cssselect("table[align='left'] a")
print eventlinks

for link in eventlinks[3:-2] :

    


    html2 = scraperwiki.scrape("http://www.conferencealerts.com/"+link.get('href')   )  
    root2 = lxml.html.fromstring(html2)
    

    eventinfo = root2.cssselect('div[id="eventInfoContainer"]')[0]

    confname_css = eventinfo.cssselect('span[id="eventNameHeader"]')[0]
    confname = confname_css.text_content()
    
    date_css = eventinfo.cssselect('span[id="eventDate"]')[0]
    date = date_css.text_content()


    venue_css = eventinfo.cssselect('span[id="eventCountry"]')[0]
    venue = venue_css.text_content()
    

    url_css = eventinfo.cssselect('span[id="eventWebsite"]')[0]
    url = url_css.cssselect('a')[0].get('href')
    

        


    
    scraperwiki.sqlite.save(unique_keys=['name'], data={'name':confname,'url':url, 'venue':venue, 'date':date})           
    




