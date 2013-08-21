import scraperwiki
from datetime import datetime

sourcescraper = 'city_of_ottawa_development_applications'
scraperwiki.sqlite.attach(sourcescraper)

id = scraperwiki.utils.GET()['id']

# Write the map and location
locs = scraperwiki.sqlite.select("* FROM %s.Locations WHERE Application_Number=? ORDER BY Address DESC" % sourcescraper, id)

labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
print "<div class='map' style='float: right;'>"
lat = None
lng = None
markers = ""
addresses = []
for loc in locs:
    lat = loc['Lat']
    lng = loc['Long']

    markers += "markers=label:%s%%7C%s,%s" % (labels[len(addresses)], lat, lng) 

    addresses.append(loc['Address'])


uri = "http://maps.google.com/maps?q=%s,%s+(%s)" % (lat, lng, addresses[0])
print "<a href='%s'><img src='https://maps.googleapis.com/maps/api/staticmap?size=300x300&zoom=14&%s&sensor=false'></a><br/>" % (uri, markers)

i = 0
for addr in addresses:
    print "%s. %s<br/>" % (labels[i], addr)
    i += 1

print "</div>" # map

# Map stuff is done.



# Show the application history
rows = scraperwiki.sqlite.select("* FROM %s.Applications WHERE Application_Number=? ORDER BY Last_Scrape DESC" % sourcescraper, id)

util = scraperwiki.utils.swimport("devapps_utils")


# Show the current state.
for row in rows:
    print "<h1>%s: %s</h1>" % (row['Application_Type'], id)
    
    print "<p>Ward: %s (%s). " % (util.WARDS[row['Ward']], row['Ward'])

    # Cross list with other amendments for the location.
    crossListHeaderPrinted = False
    for loc in locs:
        others = scraperwiki.sqlite.select("* FROM %s.Locations WHERE Application_Number<>? AND Address=? ORDER BY Address DESC" % sourcescraper, [id, loc['Address']])
        if len(others) > 0:
            if not crossListHeaderPrinted:
                print "<p>Other Applications sharing the same address</p>"
                crossListHeaderPrinted = True
                print "<ul>"
            print "<li>%s: " % loc['Address']
            for other in others:
                print "<a href='?id=%s'>%s</a>" % (other['Application_Number'], other['Application_Number'])
            print "</li>"
    if crossListHeaderPrinted:
        print "</ul>"
        

    print "<p>Last updated: %s." % datetime.fromtimestamp(row['Last_Scrape']).strftime('%Y-%m-%d')
    print "<p>%s</p>" % row['Description']

    print "<p><a href='%s'>City of Ottawa listing.</a></p>" % row['Application_URI']

    break


# Show the history
if len(rows) > 1:
    print "<h1>History</h1>"

for i in range(len(rows) - 1):
    print "<h2>%s</h2>" % datetime.fromtimestamp(rows[i]['Last_Scrape']).strftime('%Y-%m-%d')
    diff = util.application_diff([rows[i], rows[i+1]])
    print util.stringify_diff(diff)