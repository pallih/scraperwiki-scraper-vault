import scraperwiki
import simplejson
import urllib2
import re

QUERY = '#15m'
RESULTS_PER_PAGE = '900'
LANGUAGE = 'en'
NUM_PAGES = 10
PATTERN_REPLY = r'^@(\w+)'
PATTERN_RT = r'^RT @(\w+)'

for page in range(1, NUM_PAGES):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            reply = re.match(PATTERN_REPLY, result['text'])
            rt = re.match(PATTERN_RT, result['text'])
            if (reply):
                to_user = reply.group(1)
                tweet_type = 'reply'
            elif (rt):
                to_user = rt.group(1)
                tweet_type = 'retweet'
            else:
                to_user = ''
                tweet_type = 'normal'
            
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['to_user'] = to_user
            data['type'] = tweet_type
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data)
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        breakimport scraperwiki
import simplejson
import urllib2
import re

QUERY = '#15m'
RESULTS_PER_PAGE = '900'
LANGUAGE = 'en'
NUM_PAGES = 10
PATTERN_REPLY = r'^@(\w+)'
PATTERN_RT = r'^RT @(\w+)'

for page in range(1, NUM_PAGES):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            reply = re.match(PATTERN_REPLY, result['text'])
            rt = re.match(PATTERN_RT, result['text'])
            if (reply):
                to_user = reply.group(1)
                tweet_type = 'reply'
            elif (rt):
                to_user = rt.group(1)
                tweet_type = 'retweet'
            else:
                to_user = ''
                tweet_type = 'normal'
            
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['to_user'] = to_user
            data['type'] = tweet_type
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data)
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break