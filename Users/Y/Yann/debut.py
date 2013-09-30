# Blank Python
sourcescraper = 'youtube_1'
import datetime
import scraperwiki
scraperwiki.sqlite.attach("youtube_1")

data0 = scraperwiki.sqlite.select(
    '''* from youtube_1.djeuns
     WHERE date=date()
    order by viewcount desc limit 60'''
)

data1 = scraperwiki.sqlite.select(
    '''* from youtube_1.djeuns 
    WHERE date=date('now','-1 day')
    order by viewcount desc limit 10'''
)

data2 = scraperwiki.sqlite.select(
    '''* from youtube_1.djeuns 
    WHERE date=date()
    order by commDV desc limit 20'''
)

print "<table>"           
print "<tr><th>Titre</th><th>Note</th><th>Vues</th><th>viewcountDV</th><th>fav</th><th>favDV</th><th>comm</th><th>JcommDV</th><th>J</th></tr>"
for d in data0:
    print "<tr>"
    print "<td><a href='", d["url"],"'>", d["title"],"</a></td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["rating"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["viewcount"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["viewcountDV"], "%</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["fav"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["favDV"], "%</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["comm"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["commDV"], "%</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["date"], "</td>"
    print "</tr>"
print "</table>"

print "<table>"           
print "<tr><th>Titre</th><th>Note</th><th>Vues</th><th>viewcountDV</th><th>fav</th><th>favDV</th><th>comm</th><th>JcommDV</th><th>J</th></tr>"
for d in data2:
    print "<tr>"
    print "<td><a href='", d["url"],"'>", d["title"],"</a></td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["rating"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["viewcount"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["viewcountDV"], "%</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["fav"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["favDV"], "%</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["comm"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["commDV"], "%</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["date"], "</td>"
    print "</tr>"
print "</table>"

print "<table>"           
print "<tr><th>Titre</th><th>Note</th><th>Vues</th><th>J-1</th></tr>"
for d in data1:
    print "<tr>"
    print "<td>", "<a href='", d["url"],"'>", d["title"],"</a></td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["rating"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["viewcount"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["date"], "</td>"
    print "</tr>"
print "</table>"

print "<table>"           
print "<tr><th>Titre</th><th>Note</th><th>Vues</th><th>Date</th></tr>"
for d in data0:
    print "<tr>"
    print "<td>", "<a href='", d["url"],"'>", d["title"],"</a></td>"
    print "<td>", d["rating"], "</td>"
    print "<td>", d["viewcount"], "</td>"
    print "<td>", d["date"], "</td>"
    print "</tr>"
print "</table>"# Blank Python
sourcescraper = 'youtube_1'
import datetime
import scraperwiki
scraperwiki.sqlite.attach("youtube_1")

data0 = scraperwiki.sqlite.select(
    '''* from youtube_1.djeuns
     WHERE date=date()
    order by viewcount desc limit 60'''
)

data1 = scraperwiki.sqlite.select(
    '''* from youtube_1.djeuns 
    WHERE date=date('now','-1 day')
    order by viewcount desc limit 10'''
)

data2 = scraperwiki.sqlite.select(
    '''* from youtube_1.djeuns 
    WHERE date=date()
    order by commDV desc limit 20'''
)

print "<table>"           
print "<tr><th>Titre</th><th>Note</th><th>Vues</th><th>viewcountDV</th><th>fav</th><th>favDV</th><th>comm</th><th>JcommDV</th><th>J</th></tr>"
for d in data0:
    print "<tr>"
    print "<td><a href='", d["url"],"'>", d["title"],"</a></td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["rating"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["viewcount"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["viewcountDV"], "%</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["fav"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["favDV"], "%</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["comm"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["commDV"], "%</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["date"], "</td>"
    print "</tr>"
print "</table>"

print "<table>"           
print "<tr><th>Titre</th><th>Note</th><th>Vues</th><th>viewcountDV</th><th>fav</th><th>favDV</th><th>comm</th><th>JcommDV</th><th>J</th></tr>"
for d in data2:
    print "<tr>"
    print "<td><a href='", d["url"],"'>", d["title"],"</a></td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["rating"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["viewcount"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["viewcountDV"], "%</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["fav"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["favDV"], "%</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["comm"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["commDV"], "%</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["date"], "</td>"
    print "</tr>"
print "</table>"

print "<table>"           
print "<tr><th>Titre</th><th>Note</th><th>Vues</th><th>J-1</th></tr>"
for d in data1:
    print "<tr>"
    print "<td>", "<a href='", d["url"],"'>", d["title"],"</a></td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["rating"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["viewcount"], "</td>"
    print "<td>&#xA0;&#xA0;&#xA0;", d["date"], "</td>"
    print "</tr>"
print "</table>"

print "<table>"           
print "<tr><th>Titre</th><th>Note</th><th>Vues</th><th>Date</th></tr>"
for d in data0:
    print "<tr>"
    print "<td>", "<a href='", d["url"],"'>", d["title"],"</a></td>"
    print "<td>", d["rating"], "</td>"
    print "<td>", d["viewcount"], "</td>"
    print "<td>", d["date"], "</td>"
    print "</tr>"
print "</table>"