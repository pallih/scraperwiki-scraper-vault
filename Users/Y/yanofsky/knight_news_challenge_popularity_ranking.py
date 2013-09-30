import scraperwiki   
sourcescraper = 'knight_news_challenge_popularity_scraper'
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select(           
    "* from %s.swdata order by total desc limit 200;" % sourcescraper
)
print "<h1>Knight News Challenge Popularity Contest Page by Page</h1>"
print "<p>This is a list of Knight News Challenge entries sorted by the combined number of likes and reblogs, as determined by how many of each are listed below the post. This differs from the numbers explicitly listed on the posts for an unknown reason.</p>"

print "<table border='1' cellspacing='3' cellpadding='3' style='border-collapse:collapse;'><thead><tr><th style='text-align:left'>Entry</th><th style='text-align:right'>Likes</th><th style='text-align:right'>Reblogs</th><th style='text-align:right'>Total</th><th style='text-align:left'>||||total||||</th></thead><tbody>"
for d in data:
    print "<tr>"
    print "<td style='text-align:left'><a href='", d['url'], "'>", d["title"], "</a></td>"
    print "<td style='text-align:right'>", d["likes"], "</td>"
    print "<td style='text-align:right'>", d["reblogs"], "</td>"
    print "<td style='text-align:right'>", d["total"], "</td>"
    print "<td style='text-align:;left'>", ' '.ljust(int(float(d["total"])),'|'), "</td>"
    print "</tr>"
print "</tbody></table>"

print "<p>Drawn from the <a href='http://newschallenge.tumblr.com/'>latest call for entries</a> daily. Made by <a href='https://www.twitter.com/yan0'>@YAN0</a>. Based on work by the <a href='https://twitter.com/#!/LATdatadesk'>@LATdatadesk</a>."import scraperwiki   
sourcescraper = 'knight_news_challenge_popularity_scraper'
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select(           
    "* from %s.swdata order by total desc limit 200;" % sourcescraper
)
print "<h1>Knight News Challenge Popularity Contest Page by Page</h1>"
print "<p>This is a list of Knight News Challenge entries sorted by the combined number of likes and reblogs, as determined by how many of each are listed below the post. This differs from the numbers explicitly listed on the posts for an unknown reason.</p>"

print "<table border='1' cellspacing='3' cellpadding='3' style='border-collapse:collapse;'><thead><tr><th style='text-align:left'>Entry</th><th style='text-align:right'>Likes</th><th style='text-align:right'>Reblogs</th><th style='text-align:right'>Total</th><th style='text-align:left'>||||total||||</th></thead><tbody>"
for d in data:
    print "<tr>"
    print "<td style='text-align:left'><a href='", d['url'], "'>", d["title"], "</a></td>"
    print "<td style='text-align:right'>", d["likes"], "</td>"
    print "<td style='text-align:right'>", d["reblogs"], "</td>"
    print "<td style='text-align:right'>", d["total"], "</td>"
    print "<td style='text-align:;left'>", ' '.ljust(int(float(d["total"])),'|'), "</td>"
    print "</tr>"
print "</tbody></table>"

print "<p>Drawn from the <a href='http://newschallenge.tumblr.com/'>latest call for entries</a> daily. Made by <a href='https://www.twitter.com/yan0'>@YAN0</a>. Based on work by the <a href='https://twitter.com/#!/LATdatadesk'>@LATdatadesk</a>."