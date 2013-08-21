import scraperwiki

sourcescraper = 'look_search'

scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select(
    '''* from `swdata`
    order by look, id desc'''
)



print "<html>"

css = """
<head>
<style type="text/css">
td {word-wrap: break-word}
</style>
</head>
"""
print css

print "<div>"
print "<table>"
print """
    <tr>
        <th>img</th>
        <th>id</th>
        <th>look</th>
        <th>title</th>
        <th>link</th>
        <th>brands</th>
    </tr>"""

for d in data:
    print "<tr>"
    print "<td>", "<img src=", d["img"], "/>", "</td>"
    print "<td><b>", d["id"],  "</b></td>"
    #print "<td>", d["width"], "</td>"
    #print "<td>", d["height"],"</td>"
    print "<td>", d["look"], "</td>"
    print "<td>", d["content"],  "</td>"
    print "<td>", "<a href='", d["link"], "'>", d["link"] ,"</a>", "</td>"
    #these brands should be split, best to do relational db
    print "<td>", d["brands"],"</td>"
    #print "<td>", d["keywords"],    "</td>"
    #print "<td>", d["description"], "</td>"
    print "</tr>"
print "</table>"
print "</div>"
print "</html>"