import scraperwiki

html = "http://unstats.un.org/unsd/demographic/products/socind/education.htm"

#"http://bestplaces.net/zip-code/illinois/des_plaines/60016"
#"http://unstats.un.org/unsd/demographic/products/socind/education.htm"

tagsyntax = "div[align='left'] tr.tcont"

#"table[rules='cols'] tr[class='header']+tr"
#"div[align='left'] tr.tcont"


htmldata = scraperwiki.scrape(html)

print htmldata

import lxml.html           
root = lxml.html.fromstring(htmldata)
for tr in root.cssselect(tagsyntax):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : tds[1].text_content()
    }
    print data
    
    

# (tr[class='header'])

import scraperwiki

html = "http://unstats.un.org/unsd/demographic/products/socind/education.htm"

#"http://bestplaces.net/zip-code/illinois/des_plaines/60016"
#"http://unstats.un.org/unsd/demographic/products/socind/education.htm"

tagsyntax = "div[align='left'] tr.tcont"

#"table[rules='cols'] tr[class='header']+tr"
#"div[align='left'] tr.tcont"


htmldata = scraperwiki.scrape(html)

print htmldata

import lxml.html           
root = lxml.html.fromstring(htmldata)
for tr in root.cssselect(tagsyntax):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : tds[1].text_content()
    }
    print data
    
    

# (tr[class='header'])

