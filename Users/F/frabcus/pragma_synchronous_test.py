import scraperwiki

# Blank Python

scraperwiki.sqlite.save(['x'], {'x':1})

print scraperwiki.sqlite.execute("pragma synchronous")
scraperwiki.sqlite.execute("pragma synchronous=0")
print scraperwiki.sqlite.execute("pragma synchronous")
import scraperwiki

# Blank Python

scraperwiki.sqlite.save(['x'], {'x':1})

print scraperwiki.sqlite.execute("pragma synchronous")
scraperwiki.sqlite.execute("pragma synchronous=0")
print scraperwiki.sqlite.execute("pragma synchronous")
