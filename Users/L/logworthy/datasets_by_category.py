import scraperwiki

# Blank Python
sourcescraper = 'datagovau'

scraperwiki.sqlite.attach('datagovau')

data = scraperwiki.sqlite.select("coalesce(b.category, 'Uncategorised') as category, count(*) as k_sets from datagovau.href_to_desc a left join datagovau.category_to_desc b on a.desc = b.desc group by coalesce(b.category, 'Uncategorised')")

print "<table>" 
print "<tr><th>Category</th><th># of Datasets</th>" 
for d in data: 
    print "<tr>" 
    print "<td>", d["category"], "</td>" 
    print "<td>", d["k_sets"], "</td>" 
    print "</tr>" 
print "</table>"
