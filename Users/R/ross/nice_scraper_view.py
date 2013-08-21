import scraperwiki

sourcescraper = 'nice_scraper'

scraperwiki.sqlite.attach(sourcescraper)
query = "select title,`Quick reference guide - PDF` from swdata where not `Quick reference guide - PDF` IS NULL order by title"
results = scraperwiki.sqlite.execute( query )

print '<html><body>'

print '<ul>'
data = results['data']
for name,url in data:
    print '<li><a href="%s">%s</a></li>' %  (url,name)

print '</ul>'

print '</body></html>'