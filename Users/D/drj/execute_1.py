import scraperwiki

scraperwiki.sqlite.save([], dict(foo='bar'))
foo='bar'
print scraperwiki.sqlite.execute("select * from swdata where foo = ?", foo)