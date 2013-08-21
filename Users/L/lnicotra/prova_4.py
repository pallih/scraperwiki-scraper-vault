###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://parlamento.openpolis.it/lista-dei-parlamentari-in-carica/camera/nome/asc')
print "Click on the ...more link to see the whole page"
print html

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
trs = root.cssselect('tr') # get all the <td> tags
for tr in trs:
    ths = tr.cssselect('th')
    th0 = ths[0]
    ass = th0.cssselect('a')
    for az in ass:
        # print lxml.html.tostring(az)
        #print az.text
        record = { "Nome" : az.text }
        scraperwiki.sqlite.save(["Nome"], record)
    tds = tr.cssselect('td')
    for td in tds:
        bss = td.cssselect('b')
        #b0 = bss[0]
        for b in bss:
            recordB = { "IndiceProduttivita" : b.text }    #print lxml.html.tostring(td)
            scraperwiki.sqlite.save(["IndiceProduttivita"], recordB)
            #print b.text
        # print td.text # print lxml.html.tostring(td) # the full HTML tag
    #print "Fine riga"
#                    # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE THREE LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

#for td in tds:
#     record = { "td" : td.text } # column name and value
#     scraperwiki.sqlite.save(["td"], record) # save the records one by one
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------

