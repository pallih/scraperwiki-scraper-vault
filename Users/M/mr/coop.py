sourcescraper = 'coop_gu'

import scraperwiki 
scraperwiki.sqlite.attach("coop_gu")

data = scraperwiki.sqlite.select(
    '''* from coop_gu.swdata 
    order by gazz desc limit 10'''
)

print "<head>"
print "<link rel='stylesheet' type='text/css' href='http://www.free-css.com/assets/files/free-css-templates/preview/page41/truly-simple/style.css' />"
print "</head><body><div id='wrap'>"
print "<div id='top'><h2>Cooperative - Provvedimenti MiSE in G.U.</h2></div>"
print "<div id='content'>"
for d in data:
    print "<p><b>", d["provv"], "</b>", d["titolo"], "<a href='", d["link"], "'>", d["gazz"], "</a></p>"
print "</div></div></body>"



