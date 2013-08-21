import scraperwiki

print scraperwiki.sqlite.select(""""foo" """)
print scraperwiki.sqlite.select("?", ['foo'])
