import scraperwiki

sourcescraper = '1_2'

scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select(
    '''* from `swdata`
    order by id'''
)

print "<table>"
#print "<tr><th>id</th><th>width</th><th>height</th><th>link</th><th>title</th><th>img</th></tr>"
print "<tr><th>title</th><th>link</th><th>img</th><th>keywords</th><th>extra info</th></tr>"

for d in data:
    print "<tr>"
    #print "<td>", d["id"],    "</td>"
    #print "<td>", d["width"], "</td>"
    #print "<td>", d["height"],"</td>"
    print "<td>", d["content"],  "</td>"
    print "<td>", "<a href='", d["link"], "'>", d["link"] ,"</a>", "</td>"
    print "<td>", "<img src=", d["img"], "/>", "</td>"
    print "<td>", d["keywords"], "</td>"
    print "<td>", d["description"], "</td>"
    print "</tr>"
print "</table>"
import scraperwiki

sourcescraper = '1_2'

scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select(
    '''* from `swdata`
    order by id'''
)

print "<table>"
#print "<tr><th>id</th><th>width</th><th>height</th><th>link</th><th>title</th><th>img</th></tr>"
print "<tr><th>title</th><th>link</th><th>img</th><th>keywords</th><th>extra info</th></tr>"

for d in data:
    print "<tr>"
    #print "<td>", d["id"],    "</td>"
    #print "<td>", d["width"], "</td>"
    #print "<td>", d["height"],"</td>"
    print "<td>", d["content"],  "</td>"
    print "<td>", "<a href='", d["link"], "'>", d["link"] ,"</a>", "</td>"
    print "<td>", "<img src=", d["img"], "/>", "</td>"
    print "<td>", d["keywords"], "</td>"
    print "<td>", d["description"], "</td>"
    print "</tr>"
print "</table>"
