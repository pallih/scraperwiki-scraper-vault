import scraperwiki

import lxml.etree
import lxml.html
   
html = lxml.html.parse('http://www.bbc.co.uk/radio4/factual/desertislanddiscs_archive.shtml').getroot()
links = html.cssselect('a')

for link in links:
    url = link.get('href')
    if url != None and url.startswith('/radio4/factual/desertislanddiscs_'):
        date = url.replace('/radio4/factual/desertislanddiscs_', '').replace('.shtml','').replace('.shtm','')
        guest = link.text

        record = {
            "date" : date,
            "url" : url,
            "guest" : guest
        }
        scraperwiki.datastore.save(["guest"], record)






