import scraperwiki


# 1. Query the scraper's datastore
# --------------------------------

# Before you can read the scraper's datastore from the view, you need to attach to it, using its shortname (the name in its URL).
scraperwiki.sqlite.attach("esempio_lettura_da_csv_2")


# You can attach to as many datastores as you like. Then you can access their tables directly from queries.

# Example
# The data comes back as an array of dictionaries.
data = scraperwiki.sqlite.select(
    '''* from esempio_lettura_da_csv_2.swdata'''
)
#print data


# 2. Print out the results
# ------------------------

# Follows a simple example outputting HTML, but you could output a KML file, an iCal file, an RSS feed, or whatever you need.
print "<table>"
print "<tr><th>Department Family</th><th>Entity</th><th>Date</th><th>Expense Type</th><th>Expense Area</th><th>Supplier</th><th>Transaction Number</th><th>Narrative</th>"
for d in data:
    print "<tr>"
    print "<td>", d["Department Family"], "</td>"
    print "<td>", d["Entity"], "</td>"
    print "<td>", d["Date"], "</td>"
    print "<td>", d["Expense Type"], "</td>"
    print "<td>", d["Expense Area"], "</td>"
    print "<td>", d["Supplier"], "</td>"
    print "<td>", d["Transaction Number"], "</td>"
    print "</tr>"
print "</table>"


import scraperwiki


# 1. Query the scraper's datastore
# --------------------------------

# Before you can read the scraper's datastore from the view, you need to attach to it, using its shortname (the name in its URL).
scraperwiki.sqlite.attach("esempio_lettura_da_csv_2")


# You can attach to as many datastores as you like. Then you can access their tables directly from queries.

# Example
# The data comes back as an array of dictionaries.
data = scraperwiki.sqlite.select(
    '''* from esempio_lettura_da_csv_2.swdata'''
)
#print data


# 2. Print out the results
# ------------------------

# Follows a simple example outputting HTML, but you could output a KML file, an iCal file, an RSS feed, or whatever you need.
print "<table>"
print "<tr><th>Department Family</th><th>Entity</th><th>Date</th><th>Expense Type</th><th>Expense Area</th><th>Supplier</th><th>Transaction Number</th><th>Narrative</th>"
for d in data:
    print "<tr>"
    print "<td>", d["Department Family"], "</td>"
    print "<td>", d["Entity"], "</td>"
    print "<td>", d["Date"], "</td>"
    print "<td>", d["Expense Type"], "</td>"
    print "<td>", d["Expense Area"], "</td>"
    print "<td>", d["Supplier"], "</td>"
    print "<td>", d["Transaction Number"], "</td>"
    print "</tr>"
print "</table>"


