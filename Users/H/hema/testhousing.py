import scraperwiki

# Blank Python

# Blank Python

import scraperwiki           
html = scraperwiki.scrape("http://www.slha.org/housing-locations/")
print html
import lxml.html           
root = lxml.html.fromstring(html)
for el in root.cssselect("ul.linkList a"):
    name = el.text
    proplink = el.attrib['href']
    nestedhtml = scraperwiki.scrape(proplink)
    phoneaddress = lxml.html.fromstring(nestedhtml).cssselect("div.entry-content.full-content p")[0].text_content()
    management = lxml.html.fromstring(nestedhtml).cssselect("div.entry-content.full-content p")[1].text_content()
    description = lxml.html.fromstring(nestedhtml).cssselect("div.entry-content.full-content p")[2].text_content()
    data = {
            'name' : name, 
            'proplink' : proplink, 
            'phoneaddress' : phoneaddress,
            'management' : management,
            'description' : description
    }
    scraperwiki.sqlite.save(unique_keys=['name'], data=data)
