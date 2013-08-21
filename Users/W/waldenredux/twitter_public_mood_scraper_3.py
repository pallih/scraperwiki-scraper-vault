import scraperwiki
html = scraperwiki.scrape("http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDS60147.html")
print html
        
import lxml.html
root = lxml.html.fromstring(html)

tds = root.cssselect('td') # get all the <td> tags

for td in tds:
    #print lxml.html.tostring(td) # the full HTML tag
    #print td.text                # just the text inside the HTML tag
    record = { "td" : td.text } # column name and value
    scraperwiki.sqlite.save(["td"], record) # save the records one by one


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




    