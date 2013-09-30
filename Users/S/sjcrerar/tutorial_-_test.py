import scraperwiki
import lxml.html  

html = scraperwiki.scrape('http://www.civicarts.com/')
 
print html   
import lxml.html 
root = lxml.html.fromstring(html) 

print root.cssselect("div[align='left'] tr.tcont")

for tr in root.cssselect("div[align='left'] tr.tcont"): 
    tds = tr.cssselect("td") 
print tds
data = { 'country' : tds[0].text_content(), 'years_in_school' : int(tds[4].text_content()) } 

print data 

scraperwiki.sqlite.save(unique_keys=['country'], data=data)

#
#root = lxml.html.fromstring(html)  

#print scraperwiki.sqlite.show_tables() 

#for tr in root.cssselect("div[align='left'] tr.tcont"): 
#    tds = tr.cssselect("td") 

#data = { 'arts' : tds[0].text_content(), 'years' : int(tds[4].text_content()) } 

#print data 
#scraperwiki.sqlite.save(unique_keys=['country'], data=data)import scraperwiki
import lxml.html  

html = scraperwiki.scrape('http://www.civicarts.com/')
 
print html   
import lxml.html 
root = lxml.html.fromstring(html) 

print root.cssselect("div[align='left'] tr.tcont")

for tr in root.cssselect("div[align='left'] tr.tcont"): 
    tds = tr.cssselect("td") 
print tds
data = { 'country' : tds[0].text_content(), 'years_in_school' : int(tds[4].text_content()) } 

print data 

scraperwiki.sqlite.save(unique_keys=['country'], data=data)

#
#root = lxml.html.fromstring(html)  

#print scraperwiki.sqlite.show_tables() 

#for tr in root.cssselect("div[align='left'] tr.tcont"): 
#    tds = tr.cssselect("td") 

#data = { 'arts' : tds[0].text_content(), 'years' : int(tds[4].text_content()) } 

#print data 
#scraperwiki.sqlite.save(unique_keys=['country'], data=data)