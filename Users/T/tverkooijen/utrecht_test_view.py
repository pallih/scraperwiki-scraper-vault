sourcescraper = 'utrecht_test_scraper'

import scraperwiki           
scraperwiki.sqlite.attach("utrecht_test_scraper")

# You can attach to as many datastores as you like. 
# Then you can access their tables directly from queries.

data = scraperwiki.sqlite.select(           
    '''* from utrecht_test_scraper.swdata 
    order by id desc limit 10'''
)

# The data comes back as an array of dictionaries:
# print data

# 3. Print out the results
# To output, you simply print to standard output.

print "<table>"           
print "<tr><th>Utrecht</th><th>Mentions</th>"
for d in data:
    print "<tr>"
    print "<td>", d["text"], "</td>"
    print "<td>", d["from_user"], "</td>"
    print "</tr>"
print "</table>"

# That's an example outputting HTML.
# You could output a KML file, an iCal file, an RSS feed, whatever you need.

