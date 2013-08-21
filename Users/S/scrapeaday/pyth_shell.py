import scraperwiki

import scraperwiki
html = scraperwiki.scrape('http://www.shell.nl/home/content/nld/aboutshell/careers_tpkg/students_and_graduates/is_shell_right_for_me/events/')


# -----------------------------------------------------------------------------
# Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# the HTML that was inside <td></td> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags
for td in tds:
        #print lxml.html.tostring(td) # the full HTML tag
         print td.text                # just the text inside the HTML tag



# -----------------------------------------------------------------------------
# Save the data in the ScraperWiki datastore.
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
# -----------------------------------------------------------------------------

for td in tds:
     record = { "td" : td.text } # column name and value
     scraperwiki.sqlite.save(["td"], record) # save the records one by one

