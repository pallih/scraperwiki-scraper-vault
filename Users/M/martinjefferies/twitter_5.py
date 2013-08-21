import scraperwiki
import simplejson
import urllib2
import re

QUERY = 'torchreporter'
RESULTS_PER_PAGE = '100'
NUM_PAGES = 15

postcode_match = re.compile('(?<![0-9A-Z])([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]?[ABEHMNPRVWXY0-9]? {0,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)(?![0-9A-Z])', re.I)

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s&include_entities=1' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['from_user'] = result['from_user']
            data['profile_image_url'] = result['profile_image_url']
            data['text'] = result['text']
            data['location'] = scraperwiki.geo.extract_gb_postcode(result['text'])
            data['created_at'] = result['created_at']
            try:
                entities_json = result['entities']
                data['media_url_https'] = entities_json['media'][0]['media_url_https']
            except:
                print 'no media_url_https'
            if data['location'] and postcode_match.search(data['text']):
                print data['location'], data['text']
                scraperwiki.sqlite.save(["id"], data)
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break