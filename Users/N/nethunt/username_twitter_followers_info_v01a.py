import scraperwiki
import simplejson
import urllib2
import sys

# Needs to be in lower case
SCREENNAME = 'tasalampo'
x = 0

#{'reset_time': 'Thu Apr 05 22:13:14 +0000 2012', 'remaining_hits': 0, 'hourly_limit': 150, 'reset_time_in_seconds': 1333663994}
rate_url = 'https://api.twitter.com/1/account/rate_limit_status.json'
rate_json = simplejson.loads(scraperwiki.scrape(rate_url))
print rate_json
print 'You have %s hits left. Reload time is at - %s -' % (rate_json['remaining_hits'], rate_json['reset_time'])       

# API help: https://dev.twitter.com/docs/api/1/get/followers/ids
url = 'http://api.twitter.com/1/followers/ids.json?&screen_name=%s' % (urllib2.quote(SCREENNAME))
print url
followers_json = simplejson.loads(scraperwiki.scrape(url))
print "Found %d followers of %s" % (len(followers_json), SCREENNAME)
followers_json = followers_json['ids'] # get earliest followers first for batching
followers_json.reverse()
print followers_json
while x <len(followers_json):
    SCREENID = followers_json[x]
    print 'Processing ID number: ', followers_json[x]
    print "Processing node %d of total %d" % (x, len(followers_json))
    x = x + 1
    url = 'http://api.twitter.com/1/users/lookup.json?user_id=%d' % (SCREENID)
    print 'getting url:', url
    details_json = simplejson.loads(scraperwiki.scrape(url))
    print details_json
    for detail in details_json:
# All the details are listed in Twitter API help: https://dev.twitter.com/docs/api/1/get/users/lookup
        data = {'screen_name': detail['screen_name'],
                'id': detail['id'],
                'location': detail['location'], 
                'bio': detail['description'], 
                'followers_count': detail['followers_count'], 
                'friends_count': detail['friends_count'], 
                'statuses_count': detail['statuses_count'], 
                'listed_count': detail['listed_count'], 
                'url': detail['url'], 
                'verified': detail['verified'], 
                'time_zone': detail['time_zone']}
        scraperwiki.sqlite.save(unique_keys=['id'], data = data)
#{'reset_time': 'Thu Apr 05 22:13:14 +0000 2012', 'remaining_hits': 0, 'hourly_limit': 150, 'reset_time_in_seconds': 1333663994}
rate_url = 'https://api.twitter.com/1/account/rate_limit_status.json'
rate_json = simplejson.loads(scraperwiki.scrape(rate_url))
print rate_json
print 'You have %s hits left. Reload time is at - %s -' % (rate_json['remaining_hits'], rate_json['reset_time'])
import scraperwiki
import simplejson
import urllib2
import sys

# Needs to be in lower case
SCREENNAME = 'tasalampo'
x = 0

#{'reset_time': 'Thu Apr 05 22:13:14 +0000 2012', 'remaining_hits': 0, 'hourly_limit': 150, 'reset_time_in_seconds': 1333663994}
rate_url = 'https://api.twitter.com/1/account/rate_limit_status.json'
rate_json = simplejson.loads(scraperwiki.scrape(rate_url))
print rate_json
print 'You have %s hits left. Reload time is at - %s -' % (rate_json['remaining_hits'], rate_json['reset_time'])       

# API help: https://dev.twitter.com/docs/api/1/get/followers/ids
url = 'http://api.twitter.com/1/followers/ids.json?&screen_name=%s' % (urllib2.quote(SCREENNAME))
print url
followers_json = simplejson.loads(scraperwiki.scrape(url))
print "Found %d followers of %s" % (len(followers_json), SCREENNAME)
followers_json = followers_json['ids'] # get earliest followers first for batching
followers_json.reverse()
print followers_json
while x <len(followers_json):
    SCREENID = followers_json[x]
    print 'Processing ID number: ', followers_json[x]
    print "Processing node %d of total %d" % (x, len(followers_json))
    x = x + 1
    url = 'http://api.twitter.com/1/users/lookup.json?user_id=%d' % (SCREENID)
    print 'getting url:', url
    details_json = simplejson.loads(scraperwiki.scrape(url))
    print details_json
    for detail in details_json:
# All the details are listed in Twitter API help: https://dev.twitter.com/docs/api/1/get/users/lookup
        data = {'screen_name': detail['screen_name'],
                'id': detail['id'],
                'location': detail['location'], 
                'bio': detail['description'], 
                'followers_count': detail['followers_count'], 
                'friends_count': detail['friends_count'], 
                'statuses_count': detail['statuses_count'], 
                'listed_count': detail['listed_count'], 
                'url': detail['url'], 
                'verified': detail['verified'], 
                'time_zone': detail['time_zone']}
        scraperwiki.sqlite.save(unique_keys=['id'], data = data)
#{'reset_time': 'Thu Apr 05 22:13:14 +0000 2012', 'remaining_hits': 0, 'hourly_limit': 150, 'reset_time_in_seconds': 1333663994}
rate_url = 'https://api.twitter.com/1/account/rate_limit_status.json'
rate_json = simplejson.loads(scraperwiki.scrape(rate_url))
print rate_json
print 'You have %s hits left. Reload time is at - %s -' % (rate_json['remaining_hits'], rate_json['reset_time'])
