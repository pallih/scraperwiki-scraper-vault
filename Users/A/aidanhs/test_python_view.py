import scraperwiki

sourcescraper = 'test_python'
limit = 20
offset = 0

scraperwiki.sqlite.attach(sourcescraper)
keys = scraperwiki.sqlite.execute('select * from `%s`.swdata limit 0' % sourcescraper)['keys']
keys.sort()  # alphabetically

print '<h2>Some data from scraper: %s  (%d columns)</h2>' % (sourcescraper, len(keys))
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>",
for key in keys:
    print "<th>%s</th>" % key,
print "</tr>"

# rows
for row in scraperwiki.sqlite.select('* from `%s`.swdata limit ? offset ?' % sourcescraper, [limit, offset]):
    print "<tr>",
    for key in keys:
        print "<td>%s</td>" % row.get(key),
    print "</tr>"
    
print "</table>"