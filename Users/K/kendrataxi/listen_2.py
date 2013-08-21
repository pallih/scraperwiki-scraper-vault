import scraperwiki
import simplejson
import urllib2
import re

QUERY = 'movie'
RESULTS_PER_PAGE = '100'
NUM_PAGES = 15

postcode_match = re.compile('(?<![0-9A-Z])([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]?[ABEHMNPRVWXY0-9]? {0,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)(?![0-9A-Z])', re.I)

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['from_user_name'] = result['from_user_name']
            data['to_user'] = result['to_user']
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break