import scraperwiki

#sourcescraper = 'getting_news_from_gifu_marathon_web_site'

scraperwiki.sqlite.attach("getting_news_from_gifu_marathon_web_site")

rows = scraperwiki.sqlite.select(
    '''* from swdata order by date desc'''
)

for row in rows:
    print "<table border='1' width='75%'>"
    print "<tr><td><b>", row["date"], "</b></td></tr>"
    print "<tr><td><b>", row["title"], "</b></td></tr>"
    if row["description"]:
        print "<tr><td><pre>", row["description"], "</pre></td></tr>"
    if row["link"]:
        print "<tr><td><a href='", row["link"], "'>詳しくはこちら</a></td></tr>"
    print "</table>"
    print "<br />"

