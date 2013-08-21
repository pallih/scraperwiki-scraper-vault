sourcescraper = 'superhrynove'
import scraperwiki 
scraperwiki.sqlite.attach("superhrynove")
data = scraperwiki.sqlite.select(
 '''* from superhrynove.swdata''' )
print "<tr><th>comment</th>"
for d in data:
    print  d
print "</table>"

