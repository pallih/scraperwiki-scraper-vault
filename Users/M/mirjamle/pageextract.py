import scraperwiki, sys
#attach your first scraper which collected a list of URLs of the pages that need to be scraped (use the name shown in the scraperwiki URL!)
scraperwiki.sqlite.attach("workshop_3")
# Need to keep a count of which urls we have already visited so that if the scraper breaks we need only run it from the point at which it broke
# Creates a variable in the datastore called 'position' which is 1 if the variable doesn't already exist
position = int(scraperwiki.sqlite.get_var("position",1))
print "Starting run from id:%d" % position

#One off reset, uncomment next two lines and run. Don't forget to recomment them when finished.
#scraperwiki.sqlite.save_var('position', 1)
#sys.exit(0)

#select the URL column from the data table and select the not yet visited pages whose id is greater than or equal to our variable 'position'
links = scraperwiki.sqlite.select("id, URL from 'workshop_3'.swdata where id >= %d order by id" % position)
print "Processing %d links" % len(links)
#read the URL of each page from the dictionary
for link in links:
    url = link["URL"]
#scrape the page and save its source code in dictionary
    html = scraperwiki.scrape(url)
    data = {"url": url, "html": html}
    scraperwiki.sqlite.save(["url"],data)

    position += 1
    scraperwiki.sqlite.save_var("position", link["id"])import scraperwiki, sys
#attach your first scraper which collected a list of URLs of the pages that need to be scraped (use the name shown in the scraperwiki URL!)
scraperwiki.sqlite.attach("workshop_3")
# Need to keep a count of which urls we have already visited so that if the scraper breaks we need only run it from the point at which it broke
# Creates a variable in the datastore called 'position' which is 1 if the variable doesn't already exist
position = int(scraperwiki.sqlite.get_var("position",1))
print "Starting run from id:%d" % position

#One off reset, uncomment next two lines and run. Don't forget to recomment them when finished.
#scraperwiki.sqlite.save_var('position', 1)
#sys.exit(0)

#select the URL column from the data table and select the not yet visited pages whose id is greater than or equal to our variable 'position'
links = scraperwiki.sqlite.select("id, URL from 'workshop_3'.swdata where id >= %d order by id" % position)
print "Processing %d links" % len(links)
#read the URL of each page from the dictionary
for link in links:
    url = link["URL"]
#scrape the page and save its source code in dictionary
    html = scraperwiki.scrape(url)
    data = {"url": url, "html": html}
    scraperwiki.sqlite.save(["url"],data)

    position += 1
    scraperwiki.sqlite.save_var("position", link["id"])