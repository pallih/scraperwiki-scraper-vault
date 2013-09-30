#!/usr/bin/python

# XXX won't work until can add private data somehow

# Pulls all tweets for a day into local json files called tweets-YYYY-MM-DD.json.
# Stores basic info about users in users.json
# Run it lots on cron.

# Python Twitter OAuth documentation:
# http://jmillerinc.com/2010/05/31/twitter-from-the-command-line-in-python-using-oauth/

import scraperwiki

import os
import re
import sys
import simplejson as json
import dateutil.parser 

scraperwiki.utils.swimport("oauthtwitter")
#import dtlib
import config

# Parameters
login_username = 'frabcus'
users_json_store = 'users.json'
tweets_json_store = 'tweets-%s.json'

# Connect to twitter API
#client = oauthtwitter.OAuthApi(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_KEY, config.ACCESS_SECRET)

# Set up tweets and users we know about
tweets_by_date_dict = {}
if os.path.isfile(users_json_store):
    users_dict = json.loads(open(users_json_store).read())
else:
    users_dict = {}

# Store a new tweet
def save_tweet(when, tweet, user):
    if when not in tweets_by_date_dict:
        fname = tweets_json_store % when
        if os.path.isfile(fname):
            tweets = json.loads(open(fname).read())
        else:
            tweets = {}
        tweets_by_date_dict[when] = tweets

    tweets_by_date_dict[when][tweet['id']] = tweet
    users_dict[user['screen_name']] = user

# Loop through a bunch of recent tweets
tweets = client.GetFriendsTimeline({'count':200, 'include_rts':1, 'include_entities':1})
for d in tweets:
    # get it into the encoding that it will be when loaded from a file, so dictionaries have same keys
    d = json.loads(str(json.dumps(d)))
    d['id'] = unicode(d['id']) # rather than int, so can be used as key nicely in json (not sure why needs to, but seems to)

    u = d['user']
    d['user_screen_name'] = u['screen_name']
    del d['user']

    # XXX should really use local timezone date probably for this, so user gets refresh at midnight. whatever.
    iso_date = dateutil.parser.parse(d['created_at']).date().isoformat()

    save_tweet(iso_date, d, u)

# Save everything out (that we loaded in), trying to be atomic
users_json_store_new = users_json_store + ".new"
open(users_json_store_new, 'w').write(json.dumps(users_dict, indent=4, sort_keys=True))
os.rename(users_json_store_new, users_json_store)

for when, tweets_dict in tweets_by_date_dict.iteritems():
    fname = tweets_json_store % when
    fname_new = fname + ".new"
    open(fname_new, 'w').write(json.dumps(tweets_dict, indent=4, sort_keys=True))
    os.rename(fname_new, fname)








#!/usr/bin/python

# XXX won't work until can add private data somehow

# Pulls all tweets for a day into local json files called tweets-YYYY-MM-DD.json.
# Stores basic info about users in users.json
# Run it lots on cron.

# Python Twitter OAuth documentation:
# http://jmillerinc.com/2010/05/31/twitter-from-the-command-line-in-python-using-oauth/

import scraperwiki

import os
import re
import sys
import simplejson as json
import dateutil.parser 

scraperwiki.utils.swimport("oauthtwitter")
#import dtlib
import config

# Parameters
login_username = 'frabcus'
users_json_store = 'users.json'
tweets_json_store = 'tweets-%s.json'

# Connect to twitter API
#client = oauthtwitter.OAuthApi(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_KEY, config.ACCESS_SECRET)

# Set up tweets and users we know about
tweets_by_date_dict = {}
if os.path.isfile(users_json_store):
    users_dict = json.loads(open(users_json_store).read())
else:
    users_dict = {}

# Store a new tweet
def save_tweet(when, tweet, user):
    if when not in tweets_by_date_dict:
        fname = tweets_json_store % when
        if os.path.isfile(fname):
            tweets = json.loads(open(fname).read())
        else:
            tweets = {}
        tweets_by_date_dict[when] = tweets

    tweets_by_date_dict[when][tweet['id']] = tweet
    users_dict[user['screen_name']] = user

# Loop through a bunch of recent tweets
tweets = client.GetFriendsTimeline({'count':200, 'include_rts':1, 'include_entities':1})
for d in tweets:
    # get it into the encoding that it will be when loaded from a file, so dictionaries have same keys
    d = json.loads(str(json.dumps(d)))
    d['id'] = unicode(d['id']) # rather than int, so can be used as key nicely in json (not sure why needs to, but seems to)

    u = d['user']
    d['user_screen_name'] = u['screen_name']
    del d['user']

    # XXX should really use local timezone date probably for this, so user gets refresh at midnight. whatever.
    iso_date = dateutil.parser.parse(d['created_at']).date().isoformat()

    save_tweet(iso_date, d, u)

# Save everything out (that we loaded in), trying to be atomic
users_json_store_new = users_json_store + ".new"
open(users_json_store_new, 'w').write(json.dumps(users_dict, indent=4, sort_keys=True))
os.rename(users_json_store_new, users_json_store)

for when, tweets_dict in tweets_by_date_dict.iteritems():
    fname = tweets_json_store % when
    fname_new = fname + ".new"
    open(fname_new, 'w').write(json.dumps(tweets_dict, indent=4, sort_keys=True))
    os.rename(fname_new, fname)








