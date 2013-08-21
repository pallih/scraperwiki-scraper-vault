import scraperwiki, sys

# Attaching scraper https://scraperwiki.com/scrapers/dod-contracts/
scraperwiki.sqlite.attach("dod-contracts") 

# Need to keep a count of which urls we have already visited so that if the scraper breaks we need only run it from the point at which it broke
# Creates a variable in the datastore called 'position' which is 1 iff the variable doesn't already exit
position = int(scraperwiki.sqlite.get_var('position', 1))
print "Starting run from id:%d" % position

#One off reset, uncomment next two lines and run. Don't forget to recomment them when finished.
#scraperwiki.sqlite.save_var('position', 1)
#sys.exit(0)

# Now we select that part of the dod-contracts datastore whose id is greater than or equal to our variable 'position'
links = scraperwiki.sqlite.select("id, URL from `dod-contracts`.swdata where id >= %d order by id" % position) 
print "Processing %d links" % len(links)

# Getting the html from the links
for link in links:
    url = link["URL"]
    print url


    # If this dies, then we when we re-run it will have this url processed first.
    html = scraperwiki.scrape(url)
    data = {"url": url, "html": html}
    scraperwiki.sqlite.save(["url"], data)
    
    # Successfully got the html, so will increment the current position to search from in case we fail next time
    position = position + 1  
    scraperwiki.sqlite.save_var('position', link["id"])

