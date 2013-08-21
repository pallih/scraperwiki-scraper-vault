# Blank Python
###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import re
import scraperwiki
#html = scraperwiki.scrape('http://appsdps.mef.gov.it/visto/vistohtm/scripts/broker.exe?importo=12345678&settore=AMBIENTE&tipo=NR&ente=COM&procedura=PUBLINC&provincia=AG&range=50&bm=35&_PROGRAM=code.visto.sas&_SERVICE=default&_DEBUG=0')

html = scraperwiki.scrape('http://appsdps.mef.gov.it/visto/visto.html')
html = scraperwiki.scrape('http://appsdps.mef.gov.it/visto/vistohtm/visto.html')


#print "Click on the ...more link to see the whole page"
#print html

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
ps = root.cssselect('p') # get all the <p> tags
for p in ps:
    print lxml.html.tostring(p) # the full HTML tag
    tipica = re.search("Tipica.\d+\,\d",lxml.html.tostring(p))
    if tipica:
        print tipica.group()
    #print td.text                # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE THREE LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

#for td in tds:
#     record = { "td" : td.text } # column name and value
#     scraperwiki.datastore.save(["td"], record) # save the records one by one
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------