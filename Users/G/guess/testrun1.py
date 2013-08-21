# Blank Python

import scraperwiki
import simplejson
import urllib2

# Get results from the Twitter API! Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = '#BeforeBlackPresidents'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
# NUM_PAGES = 5

# for page in range(1, NUM_PAGES+1):

base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, 1)

try:
    print simplejson.loads(scraperwiki.scrape(base_url))
except:
    print 'Oh dear, failed to scrape %s' % base_url

