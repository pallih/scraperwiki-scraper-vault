# Blank Python
import scraperwiki
html = scraperwiki.scrape('http://www.unitar.org/unosat/node/44/1261')
import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td br') # get all the <td> tags
for td in tds:
  print lxml.html.tostring(td) # the full HTML tag

test = lxml.html.tostring(td) 
print test
record = {}
scraperwiki.sqlite.save(unique_keys=["test"], data = test)  
        # Blank Python
import scraperwiki
html = scraperwiki.scrape('http://www.unitar.org/unosat/node/44/1261')
import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td br') # get all the <td> tags
for td in tds:
  print lxml.html.tostring(td) # the full HTML tag

test = lxml.html.tostring(td) 
print test
record = {}
scraperwiki.sqlite.save(unique_keys=["test"], data = test)  
        