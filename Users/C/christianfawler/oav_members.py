###############################################################################
# Scraping OAV members: "Im OAV sind Unternehmen aller Branchen aus ganz Deutschland organisiert – 
# das gemeinsame Interesse ist die asiatisch-pazifische Region."
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.oav.de/ueber-uns/mitgliedsunternehmen/liste/')
#print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object

# for el in root.cssselect("div.industrydb-list-item"):

for el in root.cssselect("a"):

#    print el
#    print lxml.html.tostring(el)
#    print el.attrib['href']
# print el.text
# members = root.cssselect('industrydb-list-item') # get all the <a href> tags
# for a in members:
#    print lxml.html.tostring(a) # the full HTML tag
#    print a.text                # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -----------------------------------------------------------------------------

     record = { "url" : el.attrib['href'] } # column name and value
     scraperwiki.sqlite.save(["url"], record) # save the records one by one

#for a in members:
#     record = { "h3" : h3.text } # column name and value
#     scraperwiki.sqlite.save(["h3"], record) # save the records one by one
    

###############################################################################
# Scraping OAV members: "Im OAV sind Unternehmen aller Branchen aus ganz Deutschland organisiert – 
# das gemeinsame Interesse ist die asiatisch-pazifische Region."
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.oav.de/ueber-uns/mitgliedsunternehmen/liste/')
#print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object

# for el in root.cssselect("div.industrydb-list-item"):

for el in root.cssselect("a"):

#    print el
#    print lxml.html.tostring(el)
#    print el.attrib['href']
# print el.text
# members = root.cssselect('industrydb-list-item') # get all the <a href> tags
# for a in members:
#    print lxml.html.tostring(a) # the full HTML tag
#    print a.text                # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -----------------------------------------------------------------------------

     record = { "url" : el.attrib['href'] } # column name and value
     scraperwiki.sqlite.save(["url"], record) # save the records one by one

#for a in members:
#     record = { "h3" : h3.text } # column name and value
#     scraperwiki.sqlite.save(["h3"], record) # save the records one by one
    

