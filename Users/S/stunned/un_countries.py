import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.un.org/en/members/index.shtml")
root = lxml.html.fromstring(html)
for el in root.cssselect("li.countryname a"): 
    coun = el.text   
    print el
    print el.text
    if coun is not None:
        data = {
            'Country' : coun,
                }
        print data
        scraperwiki.sqlite.save(unique_keys=['Country'], data=data)
import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.un.org/en/members/index.shtml")
root = lxml.html.fromstring(html)
for el in root.cssselect("li.countryname a"): 
    coun = el.text   
    print el
    print el.text
    if coun is not None:
        data = {
            'Country' : coun,
                }
        print data
        scraperwiki.sqlite.save(unique_keys=['Country'], data=data)
