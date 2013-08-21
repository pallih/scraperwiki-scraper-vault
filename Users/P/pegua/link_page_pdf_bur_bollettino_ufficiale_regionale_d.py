# Blank Python
sourcescraper = ''

import scraperwiki 
scraperwiki.sqlite.attach('link_pdf_bur_bollettino_ufficiale_regionale_della_') 

data = scraperwiki.sqlite.select( '''* from link_pdf_bur_bollettino_ufficiale_regionale_della_.swdata''' ) 

print "<html><head>"
print "<title>Elenco URL PDF Bollettino Ufficiale Regionale della Liguria</title>"
print "</head>"
print "<body>"
print "<h1>Elenco URL PDF Bollettino Ufficiale Regionale della Liguria</h1>"
print "<table>"
print "<tr><th>URL</th>" 
for d in data: 
    print "<tr>" 
    print "<td> <a href=\"",  d["URL"], "\">", d["URL"],"</a></td>"
    print "</tr>"
print "</table>"
print "</body></html>"
