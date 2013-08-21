import scraperwiki
import simplejson
import urllib2

#

QUERY = '#srf OR @srf OR @srfmedien OR #srfmedien OR @srfarchiv OR #srfarchiv OR @srfnews OR #srfnews OR @maier_ch OR @danielalager OR @mr_klapproth OR @retolipp OR @SteffiBuchli'
RESULTS_PER_PAGE = '100'
#LANGUAGE = 'de'
NUM_PAGES = 15


for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print data['from_user'], data['text'], data['profile_image'],
            scraperwiki.sqlite.save(["id",], result, verbose=0)

    except:
        print 'Abgebrochen %s' % base_url
        
    
