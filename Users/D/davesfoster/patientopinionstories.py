import scraperwiki
import lxml.html
from datetime import date 


record = {}

html = scraperwiki.scrape("https://www.patientopinion.org.uk/services/rbk")
root = lxml.html.fromstring(html)
#print root

ul = root.cssselect('div.module.standard_module div.inner') #select all of the tr elements
print ul
for row in ul:
    
    info= row.cssselect('ul li strong') 
    print info
    if info:
        #linkUrl = link[0].attrib.get('href')
        #record['stories'] = "PatOpin"
        record['number'] = info[0].text_content()
        #record['number2'] = info[1].text_content()
        #record['Linkurl'] = link[0].attrib.get('href')
        scraperwiki.sqlite.save(unique_keys=[], data=record)





import scraperwiki
import lxml.html
from datetime import date 


record = {}

html = scraperwiki.scrape("https://www.patientopinion.org.uk/services/rbk")
root = lxml.html.fromstring(html)
#print root

ul = root.cssselect('div.module.standard_module div.inner') #select all of the tr elements
print ul
for row in ul:
    
    info= row.cssselect('ul li strong') 
    print info
    if info:
        #linkUrl = link[0].attrib.get('href')
        #record['stories'] = "PatOpin"
        record['number'] = info[0].text_content()
        #record['number2'] = info[1].text_content()
        #record['Linkurl'] = link[0].attrib.get('href')
        scraperwiki.sqlite.save(unique_keys=[], data=record)





