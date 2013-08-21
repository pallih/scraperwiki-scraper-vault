import scraperwiki           
html = scraperwiki.scrape("http://builtwith.com/target.com")

import lxml.html           
root = lxml.html.fromstring(html)

for el2 in root.cssselect("div.container_12 div.grid_8"):           
    print lxml.html.tostring(el2)

for el1 in root.cssselect("div.container_12 div.grid_8"):
     h3s = el1.cssselect("h3") 
     print h3s
     divpts = el1.cssselect("div.pT strong")  
     data = {
       'tech_function' : h3s[0].text_content(),
       'technology' : divpts[0].text_content()
     }
     print data

for el in root.cssselect("div.grid_8 div.pT strong"):           
    print el.text

