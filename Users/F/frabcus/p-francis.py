import scraperwiki

print "hello, world"

download = scraperwiki.scrape("http://un.org/")

print download

data = { 'foo': 10, 'bar': 'hello' }
scraperwiki.sqlite.save( ['foo'], data )
import scraperwiki

print "hello, world"

download = scraperwiki.scrape("http://un.org/")

print download

data = { 'foo': 10, 'bar': 'hello' }
scraperwiki.sqlite.save( ['foo'], data )
