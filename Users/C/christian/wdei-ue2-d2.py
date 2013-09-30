# Attach to D1 Scraper
sourcescraper = 'd1'
import scraperwiki

# Headline
print "Master Studies at Vienna University of Technology:" 

# Attach to database from D1 and select all data from the default table
scraperwiki.sqlite.attach("d1")
data = scraperwiki.sqlite.select( '''* from swdata''' ) 

# Print out HTML table including the data values
print "<table>" 
print "<tr><th>URL</th><th>Name</th>" 
for d in data: 
 print "<tr>" 
 print "<td>", d["study"], "</td>" 
 print "<td>", d["title"], "</td>" 
 print "</tr>"

# Attach to D1 Scraper
sourcescraper = 'd1'
import scraperwiki

# Headline
print "Master Studies at Vienna University of Technology:" 

# Attach to database from D1 and select all data from the default table
scraperwiki.sqlite.attach("d1")
data = scraperwiki.sqlite.select( '''* from swdata''' ) 

# Print out HTML table including the data values
print "<table>" 
print "<tr><th>URL</th><th>Name</th>" 
for d in data: 
 print "<tr>" 
 print "<td>", d["study"], "</td>" 
 print "<td>", d["title"], "</td>" 
 print "</tr>"

