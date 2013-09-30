import scraperwiki
import lxml.html
from datetime import date 
import re


record = {}

html = scraperwiki.scrape("http://www.nhs.uk/Services/hospitals/ReviewsAndRatings/DefaultView.aspx?id=352")
root = lxml.html.fromstring(html)
#print root

divs = root.cssselect('div.ratingsrow.clear div') #select all of the tr elements

for row in divs:
    
    info= row.cssselect('div div img') 
    #print info
    if info:
        #linkUrl = link[0].attrib.get('href')
        alt = info[0].attrib.get('alt')
        splitAlt = re.split('\ +',alt)
        record['scores'] =  str(splitAlt[0])
        #record['change'] = info[1].text_content()
        #record['Linkurl'] = link[0].attrib.get('href')
        scraperwiki.sqlite.save(unique_keys=[], data=record)






import scraperwiki
import lxml.html
from datetime import date 
import re


record = {}

html = scraperwiki.scrape("http://www.nhs.uk/Services/hospitals/ReviewsAndRatings/DefaultView.aspx?id=352")
root = lxml.html.fromstring(html)
#print root

divs = root.cssselect('div.ratingsrow.clear div') #select all of the tr elements

for row in divs:
    
    info= row.cssselect('div div img') 
    #print info
    if info:
        #linkUrl = link[0].attrib.get('href')
        alt = info[0].attrib.get('alt')
        splitAlt = re.split('\ +',alt)
        record['scores'] =  str(splitAlt[0])
        #record['change'] = info[1].text_content()
        #record['Linkurl'] = link[0].attrib.get('href')
        scraperwiki.sqlite.save(unique_keys=[], data=record)






