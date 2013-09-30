# Blank Python
import scraperwiki       
   
sourcescraper = 'test_127' 
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(           
    '''name, max(views) as views from test_127.swdata 
    group by name order by views desc limit 10'''
)

print "<table>"           
print "<tr><th>Name</th><th>Views</th>"
for d in data:
    print "<tr>"
    print '<td><a href="http://www.roblox.com/User.aspx?username=',d["name"],'">', d["name"], "</a></td>"
    print "<td>", d["views"], "</td>"
    print "</tr>"
print "</table>"# Blank Python
import scraperwiki       
   
sourcescraper = 'test_127' 
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(           
    '''name, max(views) as views from test_127.swdata 
    group by name order by views desc limit 10'''
)

print "<table>"           
print "<tr><th>Name</th><th>Views</th>"
for d in data:
    print "<tr>"
    print '<td><a href="http://www.roblox.com/User.aspx?username=',d["name"],'">', d["name"], "</a></td>"
    print "<td>", d["views"], "</td>"
    print "</tr>"
print "</table>"