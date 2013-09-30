import scraperwiki
import lxml.etree
import lxml.html

# Blank Python

alphabet = [ 'A','B','C','D','E','F','G','H','I','J','K','L','N','M','O','P','Q','R','S','T','U','V','W','X','Y','Z']
a = 'A'

for i in alphabet:
    html = scraperwiki.scrape('http://waterbouwers.nl/totaaloverzicht/0_limit/'+i+'_select')
    root = lxml.html.fromstring(html)
    
    #print lxml.etree.tostring(root)
    for tr in root.cssselect(".news_box"):
        td = tr.cssselect('td')
        
        if len(td) == 5:
            print td[4]. text_content()
            data = {
                   'name':  td[1]. text_content(),
                   'address': td[3]. text_content(),
                   'contact': td[4]. text_content()
                   }
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)

import scraperwiki
import lxml.etree
import lxml.html

# Blank Python

alphabet = [ 'A','B','C','D','E','F','G','H','I','J','K','L','N','M','O','P','Q','R','S','T','U','V','W','X','Y','Z']
a = 'A'

for i in alphabet:
    html = scraperwiki.scrape('http://waterbouwers.nl/totaaloverzicht/0_limit/'+i+'_select')
    root = lxml.html.fromstring(html)
    
    #print lxml.etree.tostring(root)
    for tr in root.cssselect(".news_box"):
        td = tr.cssselect('td')
        
        if len(td) == 5:
            print td[4]. text_content()
            data = {
                   'name':  td[1]. text_content(),
                   'address': td[3]. text_content(),
                   'contact': td[4]. text_content()
                   }
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)

