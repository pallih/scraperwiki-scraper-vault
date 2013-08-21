# David Jones, Climate Code Foundation, 2011-09-06
# Prioritised list of stations for converting daily records to monthly records.

import scraperwiki

scraperwiki.sqlite.attach('canada-temperature-data', 'data')
scraperwiki.sqlite.attach('can-weather-stations', 'stations')

rows = scraperwiki.sqlite.select(
"""* from stations.missing_days join data.meta on stations.missing_days.webid = data.meta.webid
where substr(stations.missing_days.m,1,10) < '1991-01-01' and stations.missing_days.r > 1500 order by -latitude""")

print "<html>"
print "<table>"
for row in rows:
    print "<tr>" + ''.join("<td>%s</td>" % row[k] for k in ['Station Name', 'id', 'r', 'd', 'm', 'Latitude', 'Longitude']
        ) + "</tr>"
print "</table>"
print "</html>"