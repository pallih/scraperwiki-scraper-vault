#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import datetime

currentDate = datetime.date.today().strftime("%A, %B %d")

sourcescraper = "disneyland_hours"
limit = 1
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select Park, Date, Open, Close, Note from src.swdata where Date = ? and Park = 'Disneyland' ORDER BY date_scraped DESC limit ? offset ? ", (currentDate,limit, offset))

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
#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import datetime

currentDate = datetime.date.today().strftime("%A, %B %d")

sourcescraper = "disneyland_hours"
limit = 1
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select Park, Date, Open, Close, Note from src.swdata where Date = ? and Park = 'Disneyland' ORDER BY date_scraped DESC limit ? offset ? ", (currentDate,limit, offset))

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
