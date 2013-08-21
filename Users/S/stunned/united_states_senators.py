import scraperwiki

# Blank Python

import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.senate.gov/general/contact_information/senators_cfm.cfm")
root = lxml.html.fromstring(html)
for el in root.cssselect("td.contenttext[align='left']"): 
    sen = el.cssselect("a");
    if len(sen) > 0:
        print sen[0].text_content()

        data = {
            'Name' : sen[0].text_content(),
        }
        print data
    
    scraperwiki.sqlite.save(unique_keys=['Name'], data=data)
    print el.text


    

