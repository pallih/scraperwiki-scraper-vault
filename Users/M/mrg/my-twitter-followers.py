import scraperwiki
import simplejson
import urllib2
from scraperwiki import swimport

def get_followers(twitter_handle):
    base_url = 'https://api.twitter.com/1/followers/ids.json?cursor=-1&screen_name=' + twitter_handle
    results_json = simplejson.loads(scraperwiki.scrape(base_url))
    return results_json['ids']

followers = get_followers("gormno")

myfollowers_str = map(str, followers)

swimport('twitter_bulk_users_lookup_3').bulklookup("gormno", myfollowers_str)

followers = get_followers("gormer")

myfollowers_str = map(str, followers)

swimport('twitter_bulk_users_lookup_3').bulklookup("gormer", myfollowers_str)
