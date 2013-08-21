import scraperwiki
import simplejson
import urllib2
from scraperwiki import swimport

myfollowers = []
twitter_handle = 'AhmadShuja'

base_url = 'https://api.twitter.com/1/followers/ids.json?cursor=-1&screen_name=' + twitter_handle 
results_json = simplejson.loads(scraperwiki.scrape(base_url))
myfollowers = results_json['ids']
myfollowers_str = map(str, myfollowers) 



swimport('twitter_bulk_users_lookup').bulklookup(myfollowers_str)


'''
See https://scraperwiki.com/scrapers/twitter_bulk_users_lookup/ for the code for the script

Still to do
-add parameter for ID and username (usertype)
'''