# Blank Python
sourcescraper = 'vereadoressp'
import scraperwiki

scraperwiki.sqlite.attach(sourcescraper)

fotos = scraperwiki.sqlite.select("* from swdata")

for foto in fotos:
    print "<img src='" + foto["foto"] + "'>"
    print foto["nome"]
# Blank Python
sourcescraper = 'vereadoressp'
import scraperwiki

scraperwiki.sqlite.attach(sourcescraper)

fotos = scraperwiki.sqlite.select("* from swdata")

for foto in fotos:
    print "<img src='" + foto["foto"] + "'>"
    print foto["nome"]
