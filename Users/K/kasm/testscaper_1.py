import scraperwiki
import lxml.html
html = scraperwiki.scrape('http://www.un.org/en/members/index.shtml')
root = lxml.html.fromstring(html) 
for el in root.cssselect('.memberlistcountrylt .countryname a'): 
    mem = el.text
    print el 
    print el.text
    if mem is not None: 
        data = {
            "List Country" : mem, 
            }
        print data
        scraperwiki.sqlite.save(unique_keys=["List Country"], data=data) 


