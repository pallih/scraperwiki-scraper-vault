import scraperwiki
import simplejson
import urllib2
import sys

# Needs to be in lower case

SCREENNAME = 'adriandix'

# API help: https://dev.twitter.com/docs/api/1/get/friends/ids
url = 'http://api.twitter.com/1/friends/ids.json?screen_name=%s' % (urllib2.quote(SCREENNAME))
print url
friends_json = simplejson.loads(scraperwiki.scrape(url))
print "Found %d followers of %s" % (len(friends_json), SCREENNAME)
print friends_json
friends_json = friends_json['ids'] # get earliest followers first for batching
friends_json.reverse()
print friends_json 

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
for friends_list in group(friends_json, 30):
    c = c + 1
    if c < batchstart:
        continue
    print "number", c, "out of", len(friends_json) / 30
    print 'batch of ids:', friends_list
    url = 'http://api.twitter.com/1/users/lookup.json?user_id=%s' % (urllib2.quote(','.join(map(str, friends_list))))
    print 'getting url:', url
    details_json = simplejson.loads(scraperwiki.scrape(url))
    for detail in details_json:
        data = {'screen_name': detail['screen_name'],'id': detail['id'],'location': detail['location'], 'bio': detail['description']}
        print "Found person", data
        scraperwiki.sqlite.save(unique_keys=['id'], data = data)
    scraperwiki.sqlite.save_var('batchdone', c)




