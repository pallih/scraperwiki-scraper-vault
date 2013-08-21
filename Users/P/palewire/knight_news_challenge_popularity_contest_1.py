import scraperwiki   
sourcescraper = 'knight_news_challenge_popularity_contest'
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select(           
    "* from %s.swdata order by total desc limit 200;" % sourcescraper
)
print "<h1>Knight News Challenge Popularity Contest</h1>"
print "<p>Drawn from the <a href='http://newschallenge.tumblr.com/'>latest call for entries.</a> Updated daily. Brought to you by <a href='https://twitter.com/#!/LATdatadesk'>@LATdatadesk</a>.</p>"
print "<table border='1' cellspacing='3' cellpadding='3' style='border-collapse:collapse;'><thead><tr><th style='text-align:left'>Entry</th><th style='text-align:right'>Likes</th></thead><tbody>"
for d in data:
    print "<tr>"
    print "<td style='text-align:left'><a href='", d['url'], "'>", d["title"], "</a></td>"
    print "<td style='text-align:right'>", d["likes"], "</td>"
    print "</tr>"
print "</tbody></table>"