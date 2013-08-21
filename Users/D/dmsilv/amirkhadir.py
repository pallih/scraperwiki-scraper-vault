import scraperwiki
import simplejson
import urllib2
import sys

# Needs to be in lower case

SCREENNAME = 'amirkhadir'

# API help: https://dev.twitter.com/docs/api/1/get/following/ids
url = 'http://api.twitter.com/1/following/ids.json?screen_name=%s' % (urllib2.quote(SCREENNAME))
print url
following_json = simplejson.loads(scraperwiki.scrape(url))
print "Found %d following of %s" % (len(following_json), SCREENNAME)
print following_json
following_json = following_json['ids'] # get earliest following first for batching
following_json.reverse()
print following_json 

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

# Take 100 at a time, and do one lookup call for each batch
c = 0
for follower_list in group(following_json, 100):
    c = c + 1
    if c < batchstart:
        continue
    print "number", c, "out of", len(following_json) / 100
    print 'batch of ids:', follower_list
    url = 'http://api.twitter.com/1/users/lookup.json?user_id=%s' % (urllib2.quote(','.join(map(str, follower_list))))
    print 'getting url:', url
    details_json = simplejson.loads(scraperwiki.scrape(url))
    for detail in details_json:
        data = {'screen_name': detail['screen_name'], 'created_at': detail['created_at'],'id': detail['id'],'location': detail['location'], 'bio': detail['description']}
        print "Found person", data
        scraperwiki.sqlite.save(unique_keys=['id'], data = data)
    scraperwiki.sqlite.save_var('batchdone', c)

