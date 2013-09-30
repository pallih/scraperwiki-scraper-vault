# Blank Python
sourcescraper = 'desura_games'
import scraperwiki
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('''
attr_theme, count(*) as count from game
group by 1 order by 2 desc
''')

print "<table>"
print "<tr><th>Theme</th><th>Number</th>"
for d in data:
    print "<tr>"
    print "<td>", d["attr_theme"], "</td>"
    print "<td>", d["count"], "</td>"
    print "</tr>"

print "</table>"

# Blank Python
sourcescraper = 'desura_games'
import scraperwiki
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('''
attr_theme, count(*) as count from game
group by 1 order by 2 desc
''')

print "<table>"
print "<tr><th>Theme</th><th>Number</th>"
for d in data:
    print "<tr>"
    print "<td>", d["attr_theme"], "</td>"
    print "<td>", d["count"], "</td>"
    print "</tr>"

print "</table>"

