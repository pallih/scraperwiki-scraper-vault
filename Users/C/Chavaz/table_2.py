import scraperwiki           

sourcescraper = 'agorapublix'

scraperwiki.sqlite.attach(sourcescraper )

req =     '''* from %s.swdata '''
req = req %  sourcescraper 
print 'req ', req
data = scraperwiki.sqlite.select(req)


print "<table>"           
print "<tr><th>Identifiant</th><th>Rang</th><th>Inscrit le</th><th>Messages</th>"
for d in data:
    print "<tr>"
    print "<td>", d["Identifiant"], "</td>"
    print "<td>", d["Rang"], "</td>"
    print "<td>", d["Inscritle"], "</td>"
    print "<td>", d["Messages"], "</td>"
    print "</tr>"
print "</table>"

