import scraperwiki

sourcescraper = 'basic_twitter_scraper_378'

scraperwiki.sqlite.attach("basic_twitter_scraper_378")
print "<table>"
print "<tr><th>Text</th><th>ID</th><th>User</th>"
for id in data:
    print "<tr>" 
    print "<td>", d["text"], "</td>" 
    print "<td>", d["id"], "</td>" 
    print "<td>", d["from_user"], "</td>" 
    print "</tr>" 
print "</table>"
import scraperwiki

sourcescraper = 'basic_twitter_scraper_378'

scraperwiki.sqlite.attach("basic_twitter_scraper_378")
print "<table>"
print "<tr><th>Text</th><th>ID</th><th>User</th>"
for id in data:
    print "<tr>" 
    print "<td>", d["text"], "</td>" 
    print "<td>", d["id"], "</td>" 
    print "<td>", d["from_user"], "</td>" 
    print "</tr>" 
print "</table>"
