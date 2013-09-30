#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import simplejson as json

sourcescraper = "edinburgh_planning_applications"
limit = 200
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata where lat <> 0.0 and lng <> 0.0 order by date_scraped desc limit ? offset ?", (limit, offset))
keys = sdata['keys']
records = sdata['data']

print "gotback([",
for record in records:
    print json.dumps(dict(zip(keys,record))), ","
print "]);"

#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import simplejson as json

sourcescraper = "edinburgh_planning_applications"
limit = 200
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata where lat <> 0.0 and lng <> 0.0 order by date_scraped desc limit ? offset ?", (limit, offset))
keys = sdata['keys']
records = sdata['data']

print "gotback([",
for record in records:
    print json.dumps(dict(zip(keys,record))), ","
print "]);"

