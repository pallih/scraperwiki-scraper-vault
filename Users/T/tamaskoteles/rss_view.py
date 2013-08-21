import scraperwiki

# Blank Python
sourcescraper = 'rss_1'

scraperwiki.sqlite.attach("rss_1")
data = scraperwiki.sqlite.select("* from rss_1.swdata order by added desc")
print "<table>"
print "<tr><th>Poster</th><th>Title</th><th>Rating</th><th>Genre</th><th>Description</th></tr>"
for d in data:
    rating = float(d["rating"])
    bg_color = "#FFFFF5"
    if (rating < 5):
        bg_color = "#FAE6E6"
    if (rating >= 7):
        bg_color = "#E6FAE6"        
    
    print "<tr style='background-color:", bg_color ,"'>"
    print "<td><a target='blank' href='http://derefer.me/?",d['imdb'], "'> <img width='100px' src='", d["img"], "'/></a></td>"

    print "<td>", d["title"],"<strong>", d["year"], "</strong><br/>"
    if d["trailer"]:
        print "<a target='blank' href='http://derefer.me/?", d["trailer"], "'>Trailer</a><br/>"
    print "<a href='", d["url"], "'>Download</a></td>"

    print "<td><strong>", d["rating"], "</strong></td>"
    print "<td>", d["genre"], "</td>"
    print "<td>", d["description"], "</td>"

    print "</tr>"
print "</table>"