import scraperwiki
#import inspect
import lxml.html 
import re
from dateutil import parser

#Load the html of the Conference alerts physics page
html = scraperwiki.scrape("http://www.conferencealerts.com/topic-listing?topic=Physics") 
root = lxml.html.fromstring(html) 


eventlinks = root.cssselect("table[align='left'] a")

for link in eventlinks:
    print link.get('href')



for link in eventlinks[4:-2] :

    
    print link.get('href')
    html2 = scraperwiki.scrape("http://www.conferencealerts.com/"+link.get('href')   )  
    root2 = lxml.html.fromstring(html2)
    

    eventinfo = root2.cssselect('div[id="eventInfoContainer"]')[0]

    confname_css = eventinfo.cssselect('span[id="eventNameHeader"]')[0]
    confname = confname_css.text_content()
    
    date_css = eventinfo.cssselect('span[id="eventDate"]')[0]
    date = date_css.text_content()

    date = re.sub(r'\xa0', ' ', date)
    date = re.sub(r'\s+', ' ', date)

    date_split = date.split(" ")
    print date_split
    
    if len(date_split) == 5:
        datebegin = date_split[0]+' '+date_split[3]+' '+date_split[4]
        dateend = date_split[2]+' '+date_split[3]+' '+date_split[4]
    elif len(date_split) == 6:
        datebegin = date_split[0]+' '+date_split[1]+' '+date_split[5]
        dateend = date_split[3]+' '+date_split[4]+' '+date_split[5]
    else:
        print "unexpected length of date string"
    
    print datebegin
    print dateend
    
    datebegin_ = parser.parse(datebegin, fuzzy=True)
    dateend_ = parser.parse(dateend, fuzzy=True)



    venue_css = eventinfo.cssselect('span[id="eventCountry"]')[0]
    venue = venue_css.text_content()
    

    url_css = eventinfo.cssselect('span[id="eventWebsite"]')[0]
    url = url_css.cssselect('a')[0].get('href')
    

        


    
    scraperwiki.sqlite.save(unique_keys=['name'], data={'name':confname,'url':url, 'venue':venue, 'datebegin':str(datebegin_.date()),'dateend':str(dateend_.date())})           
    




