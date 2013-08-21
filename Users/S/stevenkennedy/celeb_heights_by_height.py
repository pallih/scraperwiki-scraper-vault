import scraperwiki

sourcescraper = 'celebrity_heights'
scraperwiki.sqlite.attach(sourcescraper)
query = "SELECT name, height_ft, height_m FROM {0}.swdata ORDER BY height_m".format(sourcescraper)
data = scraperwiki.sqlite.execute(query)

print "<table>"           
print "<tr><th>Name</th><th>Height (imperial)</th><th>Height (metric)</th></tr>"
for d in data['data']:
    print "<tr>"
    for i in range(len(d)):
        print "<td>", d[i], "</td>"
    print "</tr>"
print "</table>"