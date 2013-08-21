# Blank Python
 
# import scraperwiki
# html = scraperwiki.scrape('http://www.vidal.ru/poisk_preparatov/xenical.htm')

import urllib2
html = urllib2.urlopen('http://www.vidal.ru/poisk_preparatov/xenical.htm').read()
print html
import lxml.html

root = lxml.html.fromstring(html.decode("utf8")) # turn our HTML into an lxml object
h2tags = root.cssselect('h2') # get all the <h2> tags
for h2 in h2tags:
    print lxml.html.tostring(h2) # the full HTML tag
    print h2.text                # just the text inside the HTML tag

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
