#fork of Max Richmans script

import scraperwiki

import tweepy



user = tweepy.api.get_user('datahh')
print user.screen_name
print user.followers_count
for friend in user.followers():
    print friend.screen_name