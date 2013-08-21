import scraperwiki
import urllib2
import tweepy
import oauth2
import re
from datetime import datetime
import time
import sys

# API Authentication (for RepsGunTweets handle)
consumer_key = "d2ERzAgQJ8m9LRHjOxcdg"
consumer_secret = "uJ4PAb89K9sq1thbWdLfLJ2czLMAZG1lZ4gxoPdBlpY"
access_token = "1096062824-Q30bxWSX0nipq2CzHBi1wfvedZ81XC8acZRNFaF"
access_token_secret = "QmZD49quPQTa5ZU9VZVYh76mvbHsP8Cpm5yZszCVyl4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# meta variables
list_name = "members-of-congress"
owner = "cspan"
per_page = "150"
regex = "(gun safety)|(firearm)|(assault weapon)|(theydeserveavote)|(gunviolence)|(gun control)|(gun violence)|(nra )|( gun)|(^guns )|(^gun)|(AWB)|(2nd ammendment)|(gun show)|(handgun)|(right to carry)|(rifle)|(2nd amend)|(second ammendment)|(second amend)|(skeet shooting)|(hunting)|(brady campaign)|(carry permit)|(concealed weapon)|(sandy hook)|(sandyhook)|(sandy hook)|(newtown)|(aurora)|(sikh temple shooting)|(gabrielle giffords)|(gabby giffords)|(newtown massacre)|(2ndammend)|(2ndammendment)"


# page through list and filter out relevant tweets
print "paging through recent tweets..."
for page in [5,4,3,2,1]:
    list_url = "http://api.twitter.com/1/lists/statuses.json?slug=%s&owner_screen_name=%s&per_page=%s&page=%s&include_entities=true" % (list_name, owner, per_page, page)

    # fetch the url
    print "fetching page", page, "of", owner +"'s", list_name, "list"
    json = urllib2.urlopen(list_url).read()

    # convert to a native python object
    (true,false,null) = (True,False,None)
    list_tweets = eval(json)

    # # extract relevant tweets
    for lt in list_tweets:
        id_str = lt['id_str'].encode('utf-8')
        name = lt['user']['screen_name'].encode('utf-8')
        text = lt['text'].encode('utf-8')
        in_reply_to_status_id_str = lt['in_reply_to_status_id_str']
        if in_reply_to_status_id_str is None:
            in_reply_to_status_id_str = "NA"
        in_reply_to_user_id_str = lt['in_reply_to_user_id_str']
        if in_reply_to_user_id_str is None:
            in_reply_to_user_id_str = 'NA'
        coordinates = lt['coordinates']
        if coordinates is None:
            coordniates = 'NA'
        created_at = lt['created_at']
        if created_at is None:
            created_at = 'NA'

        # apply the regular expression to the tweet text
        if re.search(regex, text.lower()):
            print "saving", id_str, "to file"
            scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id_str, "handle":name, "tweet":text, "in_reply_to_status_id_str":in_reply_to_status_id_str, "in_reply_to_user_id_str": in_reply_to_user_id_str, "coordinates": coordinates, "created_at": created_at })





