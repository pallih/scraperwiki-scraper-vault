import scraperwiki
from datetime import datetime

sourcescraper = 'city_of_ottawa_development_applications'
scraperwiki.sqlite.attach(sourcescraper)


rows = scraperwiki.sqlite.select("""Date_Status, Review_Status, Current, Last_Scrape, Application_Type, Apps.Application_Number, sb.grpd 
        FROM Applications AS Apps 
        INNER JOIN (
                SELECT Locations.Application_Number, GROUP_CONCAT(Locations.Address, ', ') AS grpd 
                    FROM Locations 
                    GROUP BY Locations.Application_Number
                ) AS sb ON Apps.Application_Number = sb.Application_Number 
        ORDER BY Last_Scrape DESC"""
)

print """
<html>
<head>
<style type="text/css">
tr.old td {
    font-style: italic;
}
</style>
<body>
"""

print "<table border='1'>";

lastDate = None
for row in rows:
    status = row['Last_Scrape']
    if lastDate != status:
        print "<tr><td colspan='3'><h1>%s</a></h1></td></tr>" % datetime.fromtimestamp(status).strftime('%Y-%m-%d')
        lastDate = status

    style = "old"
    if row['Current'] == 1:
        style = "current"

    print "<tr class='%s'><td><a href='/run/devapps_history/?id=%s'>%s</td><td>%s</td><td>%s</td></tr>" % (style, row['Application_Number'], row['grpd'], row['Application_Type'], row['Review_Status'])

print "</table>";