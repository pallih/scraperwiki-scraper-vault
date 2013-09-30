import scraperwiki

sourcescraper = 'knight_news_challenge_2010_entrants'
scraperwiki.sqlite.attach('knight_news_challenge_2010_entrants')

results = scraperwiki.sqlite.execute("select title, amount_requested, details_url from knight_news_challenge_2010_entrants.swdata order by amount_requested, title")

print "<html><body><table border=1>"
for title, amount_requested, details_url in results['data']:
    print "<tr><td><a href='", details_url, "'>", title, "</td><td>", amount_requested, "</td></tr>"

print "</table></body></html>"


import scraperwiki

sourcescraper = 'knight_news_challenge_2010_entrants'
scraperwiki.sqlite.attach('knight_news_challenge_2010_entrants')

results = scraperwiki.sqlite.execute("select title, amount_requested, details_url from knight_news_challenge_2010_entrants.swdata order by amount_requested, title")

print "<html><body><table border=1>"
for title, amount_requested, details_url in results['data']:
    print "<tr><td><a href='", details_url, "'>", title, "</td><td>", amount_requested, "</td></tr>"

print "</table></body></html>"


