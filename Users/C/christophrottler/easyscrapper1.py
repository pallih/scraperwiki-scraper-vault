import scraperwiki
html = scraperwiki.scrape('http://www.studentenwerk-kassel.de/faq.html')


import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('h3') # get all the <td> tags
for h3 in tds:
    print lxml.html.tostring(h3) # the full HTML tag
    print h3.text                # just the text inside the HTML tag


for h3 in tds:
     record = { "h3" : h3 } # column name and value
     scraperwiki.sqlite.save(["h3"], record) # save the records one by one
import scraperwiki
html = scraperwiki.scrape('http://www.studentenwerk-kassel.de/faq.html')


import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('h3') # get all the <td> tags
for h3 in tds:
    print lxml.html.tostring(h3) # the full HTML tag
    print h3.text                # just the text inside the HTML tag


for h3 in tds:
     record = { "h3" : h3 } # column name and value
     scraperwiki.sqlite.save(["h3"], record) # save the records one by one
