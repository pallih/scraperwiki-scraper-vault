# 1. In the scraper's views section, choose "create a new view" 
# pick Python as your language.

# Blank Python
sourcescraper = 'first_scraper_tutorial_5'

# Put in a few lines of code, and click the "Preview" button or type Ctrl+P, e.g.
# print "This is a <em>fragment</em> of HTML."

# 2. Query the scraper's datastore
# Before you can read the scraper's datastore from the view, 
# you need to attach to it, using its shortname (the name in its URL).

import scraperwiki           
scraperwiki.sqlite.attach("first_scraper_tutorial_5")

# You can attach to as many datastores as you like. 
# Then you can access their tables directly from queries.

data = scraperwiki.sqlite.select(           
    '''* from first_scraper_tutorial_5.swdata 
    order by years_in_school desc limit 10'''
)

# The data comes back as an array of dictionaries:
# print data

# 3. Print out the results
# To output, you simply print to standard output.

print "<table>"           
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"

# That's an example outputting HTML.
# You could output a KML file, an iCal file, an RSS feed, whatever you need.

