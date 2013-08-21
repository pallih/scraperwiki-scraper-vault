import scraperwiki
import simplejson
import urllib2
import sys

#{'reset_time': 'Thu Apr 05 22:13:14 +0000 2012', 'remaining_hits': 0, 'hourly_limit': 150, 'reset_time_in_seconds': 1333663994}
rate_url = 'https://api.twitter.com/1/account/rate_limit_status.json'
rate_json = simplejson.loads(scraperwiki.scrape(rate_url))
print rate_json
print 'You have %s hits left. Reload time is at - %s -' % (rate_json['remaining_hits'], rate_json['reset_time'])       

n = input("Integer? ")#Pick an integer.  And remember, if raw_input is not supported by your OS, use input()
n = int(n)#Defines n as the integer you chose. (Alternatively, you can define n yourself)
if n < 0:
    print ("The absolute value of",n,"is",-n)
else:
    print ("The absolute value of",n,"is",n)
