###############################################################################
# Scraping Bitkom members
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.bitkom.org/de/mitglieder/2854.aspx')
#print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object

#for el in root.cssselect("a"):
#    print lxml.html.tostring(el)
#    print el.attrib['href']
     #print el.text


#    print el
#    print lxml.html.tostring(el)
#    print a.text

#    print el.text

# print el.text
# members = root.cssselect('article') # get all the <a href> tags

for el in root.cssselect("div.article a"):     
#    print lxml.html.tostring(el)
#    print el.attrib['href']

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -----------------------------------------------------------------------------

#    print lxml.html.tostring(el)
     el = lxml.html.tostring(el)
     record = { "url" : el } # column name and value
     scraperwiki.sqlite.save(["url"], record) # save the records one by one

#for a in members:
#     record = { "h3" : h3.text } # column name and value
#     scraperwiki.sqlite.save(["h3"], record) # save the records one by one
    

###############################################################################
# Scraping Bitkom members
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.bitkom.org/de/mitglieder/2854.aspx')
#print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object

#for el in root.cssselect("a"):
#    print lxml.html.tostring(el)
#    print el.attrib['href']
     #print el.text


#    print el
#    print lxml.html.tostring(el)
#    print a.text

#    print el.text

# print el.text
# members = root.cssselect('article') # get all the <a href> tags

for el in root.cssselect("div.article a"):     
#    print lxml.html.tostring(el)
#    print el.attrib['href']

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -----------------------------------------------------------------------------

#    print lxml.html.tostring(el)
     el = lxml.html.tostring(el)
     record = { "url" : el } # column name and value
     scraperwiki.sqlite.save(["url"], record) # save the records one by one

#for a in members:
#     record = { "h3" : h3.text } # column name and value
#     scraperwiki.sqlite.save(["h3"], record) # save the records one by one
    

