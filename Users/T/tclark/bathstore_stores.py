import scraperwiki
html = scraperwiki.scrape('http://www.bathstore.com/_application/showrooms_all.html')
print "Click on the ...more link to see the whole page"
print html


import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
h2s = root.cssselect('h2') # get all the <td> tags
for h2 in h2s:
    print lxml.html.tostring(h2) # the full HTML tag
    print h2.text                # just the text inside the HTML tag


for h2 in h2s:
     record = { "h2" : h2.text } # column name and value
     scraperwiki.sqlite.save(["h2"], record) # save the records one by one

import scraperwiki
html = scraperwiki.scrape('http://www.bathstore.com/_application/showrooms_all.html')
print "Click on the ...more link to see the whole page"
print html


import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
h2s = root.cssselect('h2') # get all the <td> tags
for h2 in h2s:
    print lxml.html.tostring(h2) # the full HTML tag
    print h2.text                # just the text inside the HTML tag


for h2 in h2s:
     record = { "h2" : h2.text } # column name and value
     scraperwiki.sqlite.save(["h2"], record) # save the records one by one

