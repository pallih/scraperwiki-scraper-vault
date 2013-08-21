#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite

sourcescraper = "ie_pres_events_details"
limit = 20
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
DATEs = sdata.get("DATE")
TIME_PLACEs = sdata.get("TIME_PLACE")

print '<h2>Some data from scraper: %s  (%d columns)</h2>' % (sourcescraper, len(DATEs))
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>",
for DATE in DATEs:
    print "<th>%s</th>" % DATE,
print "</tr>"

# rows
for TIME_PLACE in TIME_PLACEs:
    print "<tr>",
    for TIME_PLACE in row:
        print "<td>%s</td>" % TIME_PLACE,
    print "</tr>"
    
print "</table>"

#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite

sourcescraper = "ie_pres_events_details"
limit = 20
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
DATEs = sdata.get("DATE")
TIME_PLACEs = sdata.get("TIME_PLACE")

print '<h2>Some data from scraper: %s  (%d columns)</h2>' % (sourcescraper, len(DATEs))
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>",
for DATE in DATEs:
    print "<th>%s</th>" % DATE,
print "</tr>"

# rows
for TIME_PLACE in TIME_PLACEs:
    print "<tr>",
    for TIME_PLACE in row:
        print "<td>%s</td>" % TIME_PLACE,
    print "</tr>"
    
print "</table>"

