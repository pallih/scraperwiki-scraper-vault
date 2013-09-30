import scraperwiki
html = scraperwiki.scrape('http://www.scie.org.uk/workforce/getconnected/cycle3successful.asp')

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
lis = root.cssselect('li') # get all the <li> tags
#for li in lis:
#    print lxml.html.tostring(li) # the full HTML tag
#    print li.text                # just the text inside the HTML tag

for li in lis:
     record = { "organisation" : li.text } # column name and value
     scraperwiki.sqlite.save(["organisation"], record) # save the records one by oneimport scraperwiki
html = scraperwiki.scrape('http://www.scie.org.uk/workforce/getconnected/cycle3successful.asp')

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
lis = root.cssselect('li') # get all the <li> tags
#for li in lis:
#    print lxml.html.tostring(li) # the full HTML tag
#    print li.text                # just the text inside the HTML tag

for li in lis:
     record = { "organisation" : li.text } # column name and value
     scraperwiki.sqlite.save(["organisation"], record) # save the records one by one