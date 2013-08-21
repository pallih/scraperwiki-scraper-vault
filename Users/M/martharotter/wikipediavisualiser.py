import scraperwiki           

scraperwiki.sqlite.attach("wikipedia_paper_scraper_until_jan_20")

data = scraperwiki.sqlite.select(           
    '''* from wikipedia_paper_scraper_until_jan_20.swdata 
    order by id desc limit 10'''
)


print "<table>"           
print "<tr><th>ID</th><th>Tweet</th><th>User</th>"
for d in data:
    print "<tr>"
    print "<td>", d["id"], "</td>"
    print "<td>", d["text"], "</td>"
    print "<td>", d["from_user"], "</td>"
    print "</tr>"
print "</table>"

