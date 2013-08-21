#########################################
# Simple table of values from one scraper
#########################################


import scraperwiki  
import scraperwiki.sqlite


sourcescraper = "twitter_public_mood_scraper_3"         
scraperwiki.sqlite.attach("twitter_public_mood_scraper_3","src")
limit=80
offset=0


# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
keys = sdata.get("keys")
rows = sdata.get("data")

print '<h2>Some data from scraper: %s  (%d columns)</h2>' % (sourcescraper, len(keys))
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>",
for key in keys:
    print "<th>%s</th>" % key,
print "</tr>"

# rows
for row in rows:
    print "<tr>",
    for value in row:
        print "<td>%s</td>" % value,
    print "</tr>"
    
print "</table>"
