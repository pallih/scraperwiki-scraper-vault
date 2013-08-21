# David Jones, ScraperWiki
# Test scraper to demonstrate the bogus cache behaviour:
# where it caches 5xx status codes.

# We create 10 endpoints, each of which has a 50% chance
# of returning either 200 or 500; we then fetch each one
# 10 times and see which we get.
# If the cache is being reasonable, we would expect that
# a bad (5xx) response would be not cached and so
# eventually each endpoint would get a good result in the
# cache.

import random
import sys
import urllib

base = "https://devviews.scraperwiki.com/run/set-status/"
epl = [base + ('?q=%f&choice=200,500' % random.random())
  for _ in range(10)]

for ep in epl:
    print ep
    s = ''
    for i in range(10):
        code = str(urllib.urlopen(ep).getcode())
        s += code[0]
    print s

print "script end"