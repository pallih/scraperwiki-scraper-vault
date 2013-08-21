#########################
# Scraping Research  URLs 
#########################

import scraperwiki
import lxml.html
from lxml.html import parse
import re

html = scraperwiki.scrape("http://research.webometrics.info/HELM.asp")
#html = scraperwiki.scrape("http://research.webometrics.info/top4000_r&d.asp")
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
# print root
# print html

# tds = root.cssselect('td') # get all the <td> tags
# for td in tds:
#    print lxml.html.tostring(td) # the full HTML tag
#   print td.text                # just the text inside the HTML tag

anav6as = root.cssselect('a.nav6a') # to get all the <a> tags with css-class nav6a 
for anav6a in anav6as: 
# the full HTML tag
#    print lxml.html.tostring(anav6a) # the full HTML tag
    print anav6a.text # the text inside the <a>

#for Single_Scraped_Entry in All_Scraped_Entries:
#    match = re.search("(?P<url>http?://[^\s]+)", Single_Scraped_Entry)
#    if match is not None: 
#        print match.group("url")
#    print lxml.html.tostring(a)
#    print a.text
# -----------------------------------------------------------------------------
# Save the data in the ScraperWiki datastore.
# -----------------------------------------------------------------------------
    record = { "Name_of_Institution" : anav6a.text } # column name and value
    scraperwiki.sqlite.save(["Name_of_Institution"], record) # save the records one by one
