import scraperwiki
import simplejson
import urllib2
import sys

x = -1 # number of id's on array
n = 0 # number of processed id's
d = 0 # rate limit

# fuction: check available rate limit 150 / hour {'reset_time': 'Thu Apr 05 22:13:14 +0000 2012', 'remaining_hits': 0, 'hourly_limit': 150, 'reset_time_in_seconds': 1333663994}
rate_url = 'https://api.twitter.com/1/account/rate_limit_status.json'
rate_json = simplejson.loads(scraperwiki.scrape(rate_url))
print rate_json
print 'You have %s hits left. Reload time is at - %s -' % (rate_json['remaining_hits'], rate_json['reset_time'])       #Get the remaining hits for the hour

wasted = rate_json['remaining_hits']
#Put target id's here on the 'lista'
lista = [12578882,14079118,14273044,15487001,17152448,19399906,21329567,21472089,22010171,23483819,24043586,25065931,28796179,34709013,35749513,38011034,38136838,39216615,40453503,41320544,41798186,42020943,44945145,46343892,50744958,51991093,52433735,61616586,64992410,65971046,72370342,84671043,85822997,96961276,106721139,108905689,110670265,112703168,113082933,123967892,143805896,151440150,160500115,169421250,185148186,203576917,208045380,214111412,224943395,233943822,238677255,239361386,274107624,293614015,303631084,326245467,364180014,371180171,376274548,380880643,396811941,409773530,428412274,452249877,460159130,462789896,483655928,483721529,520288725,522152953,526169146,526670940,526707733,531013976,531269236,531684273,532889579,534635941,534636443,534717825,534719040,534724515,537076431,537222739,539883940]

while x <len(lista):
    SCREENID = lista[x]
    print "Processing node %d of %d, ID number %d" % (x, len(lista), lista[x])
    wasted = wasted - 1
    n = n + 1
    x = x + 1
    url = 'http://api.twitter.com/1/followers/ids.json?user_id=%d' % (SCREENID)
#    print 'getting url:', url
    print "Only %d hits to waste" % (wasted)

    details_json = simplejson.loads(scraperwiki.scrape(url))
    print details_json
    for detail in details_json:
# All the possible details to fetch are listed in Twitter API help: https://dev.twitter.com/docs/api/1/get/users/lookup
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
print 'You have %s hits left. Reload time is at - %s -' % (rate_json['remaining_hits'], rate_json['reset_time'])       #Get the remaining hits for the hour
print "Persons processed:", n