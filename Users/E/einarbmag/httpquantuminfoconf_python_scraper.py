import scraperwiki
#import inspect
import lxml.html 
import re
from dateutil import parser




html = scraperwiki.scrape("http://quantum.info/conf/") 

root = lxml.html.fromstring(html) 

root2=root.cssselect('div#mainc')[0]

eventlist = root2.cssselect('li')

for event in eventlist :
    

    confname_css = event.cssselect('a')[0]
    confname = confname_css.text_content()

    date_css = event.cssselect('b')[0]
    
    dates1 = date_css.text_content()

    dates = re.split(' |–',dates1.encode('utf-8'))
    

    year = '2013'
    if len(dates) == 3:
        datebegin = parser.parse(dates[0]+' '+dates[1]+' '+year, fuzzy=True)
        dateend = parser.parse(dates[0]+' '+dates[2]+' '+year, fuzzy=True)
    elif len(dates) == 4:
        datebegin = parser.parse(dates[0]+' '+dates[1]+' '+year, fuzzy=True)
        dateend = parser.parse(dates[2]+' '+dates[3]+' '+year, fuzzy=True)
    elif len(dates) == 2:
        datebegin = parser.parse(dates[0]+' '+dates[1]+' '+year, fuzzy=True)
        dateend = datebegin
    else:
        print 'Unexpected date length'
        print dates

    
    url = event.cssselect('a')[0].get('href')
    

    
    alltext = event.text_content()

    location_t = re.split(confname,alltext)[1]

    print location_t

    if location_t.find('(')>0:
        location_t = location_t[location_t.find(','):]
    if location_t.endswith('*'):
        location_t = location_t[0:-2]

    location=location_t[2:-1]
    print location

    scraperwiki.sqlite.save(unique_keys=['name'], data={'name':confname,'datebegin':str(datebegin.date()),
                            'dateend':str(dateend.date()),'url':url})           
    



import scraperwiki
#import inspect
import lxml.html 
import re
from dateutil import parser




html = scraperwiki.scrape("http://quantum.info/conf/") 

root = lxml.html.fromstring(html) 

root2=root.cssselect('div#mainc')[0]

eventlist = root2.cssselect('li')

for event in eventlist :
    

    confname_css = event.cssselect('a')[0]
    confname = confname_css.text_content()

    date_css = event.cssselect('b')[0]
    
    dates1 = date_css.text_content()

    dates = re.split(' |–',dates1.encode('utf-8'))
    

    year = '2013'
    if len(dates) == 3:
        datebegin = parser.parse(dates[0]+' '+dates[1]+' '+year, fuzzy=True)
        dateend = parser.parse(dates[0]+' '+dates[2]+' '+year, fuzzy=True)
    elif len(dates) == 4:
        datebegin = parser.parse(dates[0]+' '+dates[1]+' '+year, fuzzy=True)
        dateend = parser.parse(dates[2]+' '+dates[3]+' '+year, fuzzy=True)
    elif len(dates) == 2:
        datebegin = parser.parse(dates[0]+' '+dates[1]+' '+year, fuzzy=True)
        dateend = datebegin
    else:
        print 'Unexpected date length'
        print dates

    
    url = event.cssselect('a')[0].get('href')
    

    
    alltext = event.text_content()

    location_t = re.split(confname,alltext)[1]

    print location_t

    if location_t.find('(')>0:
        location_t = location_t[location_t.find(','):]
    if location_t.endswith('*'):
        location_t = location_t[0:-2]

    location=location_t[2:-1]
    print location

    scraperwiki.sqlite.save(unique_keys=['name'], data={'name':confname,'datebegin':str(datebegin.date()),
                            'dateend':str(dateend.date()),'url':url})           
    



