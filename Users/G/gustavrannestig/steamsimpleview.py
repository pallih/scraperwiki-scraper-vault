
import scraperwiki   

sourcescraper = 'steamsalescraperin_dev'        
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(           
    '''* from steamsalescraperin_dev.swdata 
    '''
)

print "<table>"           
print "<tr><th>Game</th><th>Price</th>"
for d in data:
    print "<tr>"
    print "<td>", d["title"], "</td>"
    print "<td>", d["price"], "</td>"
    print "</tr>"
print "</table>"