###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re

# retrieve a page
starting_url = 'https://web.barclayscyclehire.tfl.gov.uk/maps'
html = scraperwiki.scrape(starting_url)

regex = re.compile("station=\{id:\"([^\"]*)\",name:\"([^\"]*)\",lat:\"([^\"]*)\",long:\"([^\"]*)\",nbBikes:\"([^\"]*)\",nbEmptyDocks:\"([^\"]*)\",installed:\"([^\"]*)\",locked:\"([^\"]*)\",temporary:\"([^\"]*)\"\}")

records =  regex.findall(html)

for record in records:
    scraperwiki.datastore.save(['id'], dict(zip(["id", "name", "lat", "long", "nbBikes", "nbEmptyDocks", "installed", "locked", "temporary"], record)))
###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re

# retrieve a page
starting_url = 'https://web.barclayscyclehire.tfl.gov.uk/maps'
html = scraperwiki.scrape(starting_url)

regex = re.compile("station=\{id:\"([^\"]*)\",name:\"([^\"]*)\",lat:\"([^\"]*)\",long:\"([^\"]*)\",nbBikes:\"([^\"]*)\",nbEmptyDocks:\"([^\"]*)\",installed:\"([^\"]*)\",locked:\"([^\"]*)\",temporary:\"([^\"]*)\"\}")

records =  regex.findall(html)

for record in records:
    scraperwiki.datastore.save(['id'], dict(zip(["id", "name", "lat", "long", "nbBikes", "nbEmptyDocks", "installed", "locked", "temporary"], record)))
