import scraperwiki
import urllib
import json

search_results = json.loads(urllib.urlopen("http://www.kickstarter.com/projects/search.json?search=&term=civic").read())

scraperwiki.sqlite.save(unique_keys=["id"], data=search_results["projects"])
