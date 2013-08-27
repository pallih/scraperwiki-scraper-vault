import scraperwiki
html = scraperwiki.scrape('http://www.horsedeathwatch.com/')
print "Click on the ...more link to see the whole page"
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
#tds = root.cssselect('tr td') # get all the <tr><td> tags
trs = root.cssselect('tr td[0]') # get all the first <tr><td> tags
for tr in trs:
    print lxml.html.tostring(tr)
    tds = tr.cssselect('td')
    for td in tds:
#for td in tds:
 #   print lxml.html.tostring(td) # the full HTML tag
        print td.text_content()               # just the text inside the HTML tag

#for td in tds:
 #    record = { "td" : td.text_content() } # column name and value
  #   scraperwiki.sqlite.save(["td"], record) # save the records one by oneimport scraperwiki
html = scraperwiki.scrape('http://www.horsedeathwatch.com/')
print "Click on the ...more link to see the whole page"
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
#tds = root.cssselect('tr td') # get all the <tr><td> tags
trs = root.cssselect('tr td[0]') # get all the first <tr><td> tags
for tr in trs:
    print lxml.html.tostring(tr)
    tds = tr.cssselect('td')
    for td in tds:
#for td in tds:
 #   print lxml.html.tostring(td) # the full HTML tag
        print td.text_content()               # just the text inside the HTML tag

#for td in tds:
 #    record = { "td" : td.text_content() } # column name and value
  #   scraperwiki.sqlite.save(["td"], record) # save the records one by oneimport scraperwiki
html = scraperwiki.scrape('http://www.horsedeathwatch.com/')
print "Click on the ...more link to see the whole page"
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
#tds = root.cssselect('tr td') # get all the <tr><td> tags
trs = root.cssselect('tr td[0]') # get all the first <tr><td> tags
for tr in trs:
    print lxml.html.tostring(tr)
    tds = tr.cssselect('td')
    for td in tds:
#for td in tds:
 #   print lxml.html.tostring(td) # the full HTML tag
        print td.text_content()               # just the text inside the HTML tag

#for td in tds:
 #    record = { "td" : td.text_content() } # column name and value
  #   scraperwiki.sqlite.save(["td"], record) # save the records one by oneimport scraperwiki
html = scraperwiki.scrape('http://www.horsedeathwatch.com/')
print "Click on the ...more link to see the whole page"
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
#tds = root.cssselect('tr td') # get all the <tr><td> tags
trs = root.cssselect('tr td[0]') # get all the first <tr><td> tags
for tr in trs:
    print lxml.html.tostring(tr)
    tds = tr.cssselect('td')
    for td in tds:
#for td in tds:
 #   print lxml.html.tostring(td) # the full HTML tag
        print td.text_content()               # just the text inside the HTML tag

#for td in tds:
 #    record = { "td" : td.text_content() } # column name and value
  #   scraperwiki.sqlite.save(["td"], record) # save the records one by one