# Blank Python
sourcescraper = 'energyshare_top_100'

import scraperwiki           
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('''project, max(url) as url, max(supporters) as supporters, group_concat(supporters) as previous, rank from energyshare_top_100.swdata
    group by project order by rank asc limit 100''')

print "<table>"
print "<tr><th>Position</th><th>Name</th><th>Supporters</th><th>Points history</th></tr>"
for d in data:
    print "<tr><td>%d</td><td><a href='http://www.energyshare.com/%s'>%s</a></td><td>%s</td><td>%s</td></tr>" % (d["rank"], d["url"], d["project"], d["supporters"],d["previous"])
print "</table>"
# Blank Python
sourcescraper = 'energyshare_top_100'

import scraperwiki           
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('''project, max(url) as url, max(supporters) as supporters, group_concat(supporters) as previous, rank from energyshare_top_100.swdata
    group by project order by rank asc limit 100''')

print "<table>"
print "<tr><th>Position</th><th>Name</th><th>Supporters</th><th>Points history</th></tr>"
for d in data:
    print "<tr><td>%d</td><td><a href='http://www.energyshare.com/%s'>%s</a></td><td>%s</td><td>%s</td></tr>" % (d["rank"], d["url"], d["project"], d["supporters"],d["previous"])
print "</table>"
