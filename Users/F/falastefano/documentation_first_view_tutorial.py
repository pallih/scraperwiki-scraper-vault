import scraperwiki

#
# Documentation / First view tutorial
#

# Test Python
#print "This is a <em>fragment</em> of HTML."


# 1. Query the scraper's datastore
# --------------------------------

# Before you can read the scraper's datastore from the view, you need to attach to it, using its shortname (the name in its URL).
scraperwiki.sqlite.attach("first_scraper_tutorial_6")


# You can attach to as many datastores as you like. Then you can access their tables directly from queries.

# Example
# The data comes back as an array of dictionaries.
data = scraperwiki.sqlite.select(
    '''* from first_scraper_tutorial_6.swdata order by years_in_school desc limit 5'''
)
#print data


# 2. Print out the results
# ------------------------

# Follows a simple example outputting HTML, but you could output a KML file, an iCal file, an RSS feed, or whatever you need.
print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"


