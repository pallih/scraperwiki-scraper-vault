# forked from https://scraperwiki.com/scrapers/civic_kickstarters

import scraperwiki
import urllib
import json

search_results = json.loads(urllib.urlopen("http://hubmaps2.cityofboston.gov/ArcGIS/rest/services/Dev_services/food_trucks/MapServer/1/query?text=%25&outFields=GPS%2CLocation%2CXCoord%2CYCoord%2CDayOfWeek%2CTimeOfDay%2CTestFld%2CShape&f=pjson").read())

scraperwiki.sqlite.save(unique_keys=["attributes"], data=search_results["features"])

# scraperwiki.sqlite.save(unique_keys=["Id"], data=search_results["projects"])
