# forked from https://scraperwiki.com/scrapers/civic_kickstarters

import scraperwiki
import urllib
import json

search_results = json.loads(urllib.urlopen("http://api.spacehive.com/api/Projects/GetAll/1").read())

scraperwiki.sqlite.save(unique_keys=["Id"], data=search_results)

# scraperwiki.sqlite.save(unique_keys=["Id"], data=search_results["projects"])
