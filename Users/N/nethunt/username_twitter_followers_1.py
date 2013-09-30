import scraperwiki
import simplejson
import urllib2
import sys

# Needs to be in lower case

SCREENNAME = 'ullamsaikku'
n = 0

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

# Groups a list in chunks of a given size
def group(lst, n):
    for i in range(0, len(lst), n):
        val = lst[i:i+n]
        if len(val) == n:
            yield tuple(val)

# Where to start? Overlap one batch to increase hit rate if people unfollow etc.
batchdone = scraperwiki.sqlite.get_var('batchdone', 1)
batchstart = batchdone - 1
if batchstart < 1:
    batchstart = 1
print "batchdone:", batchdone #paljonko batcheja on, c:ta varten
print batchstart 
# Take 100 at a time, and do one lookup call for each batch
c = 0
print c
for follower_list in group(followers_json, 100):
    c = c + 1
    if c < batchstart:
        continue
    print "number", c, "out of", len(followers_json) / 100
    print 'batch of ids:', follower_list
    url = 'http://api.twitter.com/1/users/lookup.json?user_id=%s' % (urllib2.quote(','.join(map(str, follower_list))))
    print 'getting url:', url
    details_json = simplejson.loads(scraperwiki.scrape(url))
    for detail in details_json:
        data = {'screen_name': detail['screen_name'],
                'id': detail['id'],'location': detail['location'], 
                'bio': detail['description'], 
                'followers_count': detail['followers_count'], 
                'friends_count': detail['friends_count'], 
                'statuses_count': detail['statuses_count'], 
                'listed_count': detail['listed_count'], 
                'url': detail['url'], 
                'verified': detail['verified'], 
                'time_zone': detail['time_zone']}
        scraperwiki.sqlite.save(unique_keys=['id'], data = data)
    scraperwiki.sqlite.save_var('batchdone', c)

import scraperwiki
import simplejson
import urllib2
import sys

# Needs to be in lower case

SCREENNAME = 'ullamsaikku'
n = 0

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

# Groups a list in chunks of a given size
def group(lst, n):
    for i in range(0, len(lst), n):
        val = lst[i:i+n]
        if len(val) == n:
            yield tuple(val)

# Where to start? Overlap one batch to increase hit rate if people unfollow etc.
batchdone = scraperwiki.sqlite.get_var('batchdone', 1)
batchstart = batchdone - 1
if batchstart < 1:
    batchstart = 1
print "batchdone:", batchdone #paljonko batcheja on, c:ta varten
print batchstart 
# Take 100 at a time, and do one lookup call for each batch
c = 0
print c
for follower_list in group(followers_json, 100):
    c = c + 1
    if c < batchstart:
        continue
    print "number", c, "out of", len(followers_json) / 100
    print 'batch of ids:', follower_list
    url = 'http://api.twitter.com/1/users/lookup.json?user_id=%s' % (urllib2.quote(','.join(map(str, follower_list))))
    print 'getting url:', url
    details_json = simplejson.loads(scraperwiki.scrape(url))
    for detail in details_json:
        data = {'screen_name': detail['screen_name'],
                'id': detail['id'],'location': detail['location'], 
                'bio': detail['description'], 
                'followers_count': detail['followers_count'], 
                'friends_count': detail['friends_count'], 
                'statuses_count': detail['statuses_count'], 
                'listed_count': detail['listed_count'], 
                'url': detail['url'], 
                'verified': detail['verified'], 
                'time_zone': detail['time_zone']}
        scraperwiki.sqlite.save(unique_keys=['id'], data = data)
    scraperwiki.sqlite.save_var('batchdone', c)

