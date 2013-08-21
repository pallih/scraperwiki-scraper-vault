import scraperwiki, sys
import urllib2
import lxml

tag = 'geology'

try:
    page = scraperwiki.scrape('https://scraperwiki.com/tags/%s' % tag)
except urllib2.HTTPError:
    sys.exit(1)

print page