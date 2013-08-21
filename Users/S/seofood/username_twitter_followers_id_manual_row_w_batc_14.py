import scraperwiki
import simplejson
import urllib2
import sys

SCREENNAME = 'tommyrosenqvist' #  - just for reminding, no actual use
c = 0
n = 0
#{'reset_time': 'Thu Apr 05 22:13:14 +0000 2012', 'remaining_hits': 0, 'hourly_limit': 150, 'reset_time_in_seconds': 1333663994}
resetrate_url = 'https://api.twitter.com/1/account/rate_limit_status.json'
resetrate_json = simplejson.loads(scraperwiki.scrape(resetrate_url))
print resetrate_json
print 'You have %s hits left of 150. Reload time is at - %s -' % (resetrate_json['remaining_hits'], resetrate_json['reset_time']) 

#PUT HERE a list of follower's id
lista = [40489066]


###
followers_lista = lista
print "Found %d followers of %s" % (len(followers_lista), SCREENNAME)
#print followers_json
#followers_json = followers_json['ids'] # get earliest followers first for batching
followers_lista.reverse()
print followers_lista 

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
for follower_list in group(followers_lista, 100):
#    print 'Thee batchmode loop in progress.'

    c = c + 1
    if c < batchstart:
        continue
    print "Processing batch number", c, "out of", len(followers_lista) / 100
#    print 'Batch of ids:', follower_list

    url = 'http://api.twitter.com/1/users/lookup.json?user_id=%s' % (urllib2.quote(','.join(map(str, follower_list))))
    print 'Getting url:', url
    details_json = simplejson.loads(scraperwiki.scrape(url))
    for detail in details_json:
        n = n + 1
        data = {'screen_name': detail['screen_name'],
                'id': detail['id'],
                'location': detail['location'], 
                'name': detail['name'], 
                'bio': detail['description'], 
                'created_at': detail['created_at'], 
                'followers_count': detail['followers_count'], 
                'friends_count': detail['friends_count'], 
                'statuses_count': detail['statuses_count'], 
                'listed_count': detail['listed_count'], 
                'url': detail['url'], 
                'time_zone': detail['time_zone']}
        print "Person:", n
        scraperwiki.sqlite.save(unique_keys=['id'], data = data)
    scraperwiki.sqlite.save_var('batchdone', c)
rate_url = 'https://api.twitter.com/1/account/rate_limit_status.json'
rate_json = simplejson.loads(scraperwiki.scrape(rate_url))
print rate_json
print 'You have %s hits left of 150. Reload time will be at - %s -' % (rate_json['remaining_hits'], rate_json['reset_time']) 
c = 0
print "Persons processed:", n
n = 0
