# Blank Python TEST sqlite query
sourcescraper = 'wikipedia_metal_bands'
import scraperwiki.sqlite
import cgi, simplejson
import os
get = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))

limit = 20
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
#keys = sdata.get("keys")
#rows = sdata.get("data")
#print get['name']

print simplejson.dumps(sdata)

# Blank Python TEST sqlite query
sourcescraper = 'wikipedia_metal_bands'
import scraperwiki.sqlite
import cgi, simplejson
import os
get = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))

limit = 20
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
#keys = sdata.get("keys")
#rows = sdata.get("data")
#print get['name']

print simplejson.dumps(sdata)

