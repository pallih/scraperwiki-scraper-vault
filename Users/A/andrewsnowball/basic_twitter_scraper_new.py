# -*- coding: utf-8 -*-

import os
import twitter
import json
import csv

from twitter.oauth import write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance

def login():
    # Go to http://twitter.com/apps/new to create an app and get these items.
    # See also http://dev.twitter.com/pages/oauth_single_token.

    APP_NAME = 'xxx'
    CONSUMER_KEY = 'xxx'
    CONSUMER_SECRET = 'xxx'
    TOKEN_FILE = '/token.txt'

    try:
        (oauth_token, oauth_token_secret) = read_token_file(TOKEN_FILE)
    except IOError, e:
        (oauth_token, oauth_token_secret) = oauth_dance(APP_NAME, CONSUMER_KEY,
                CONSUMER_SECRET)
        print e.errno
        print e

        if not os.path.isdir('out'):
            os.mkdir('out')

        write_token_file(TOKEN_FILE, oauth_token, oauth_token_secret)

    auth=twitter.oauth.OAuth(oauth_token, oauth_token_secret,CONSUMER_KEY, CONSUMER_SECRET)
    return twitter.TwitterStream(auth = auth, secure = True)

if __name__=="__main__":
    t = login()
    res = t.statuses.filter(track = "search text")

    res_list = []
    tweetfields = set()
    for r in res:
        if len(res_list)<100:
            print len(res_list)
            res_list.append(r)
            tweetfields = tweetfields.union(r.keys())
        else:
            break

    fname = '/results.csv'
    f = open(fname,'w')
    dw = csv.DictWriter(f,fieldnames=list(tweetfields))
    dw.writeheader()

    for r in res_list:
        dw.writerow({k:v.encode('utf8') if isinstance(v,unicode) else v for k,v in r.items()})
    f.close()

    print [result['text'] for result in res_list]# -*- coding: utf-8 -*-

import os
import twitter
import json
import csv

from twitter.oauth import write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance

def login():
    # Go to http://twitter.com/apps/new to create an app and get these items.
    # See also http://dev.twitter.com/pages/oauth_single_token.

    APP_NAME = 'xxx'
    CONSUMER_KEY = 'xxx'
    CONSUMER_SECRET = 'xxx'
    TOKEN_FILE = '/token.txt'

    try:
        (oauth_token, oauth_token_secret) = read_token_file(TOKEN_FILE)
    except IOError, e:
        (oauth_token, oauth_token_secret) = oauth_dance(APP_NAME, CONSUMER_KEY,
                CONSUMER_SECRET)
        print e.errno
        print e

        if not os.path.isdir('out'):
            os.mkdir('out')

        write_token_file(TOKEN_FILE, oauth_token, oauth_token_secret)

    auth=twitter.oauth.OAuth(oauth_token, oauth_token_secret,CONSUMER_KEY, CONSUMER_SECRET)
    return twitter.TwitterStream(auth = auth, secure = True)

if __name__=="__main__":
    t = login()
    res = t.statuses.filter(track = "search text")

    res_list = []
    tweetfields = set()
    for r in res:
        if len(res_list)<100:
            print len(res_list)
            res_list.append(r)
            tweetfields = tweetfields.union(r.keys())
        else:
            break

    fname = '/results.csv'
    f = open(fname,'w')
    dw = csv.DictWriter(f,fieldnames=list(tweetfields))
    dw.writeheader()

    for r in res_list:
        dw.writerow({k:v.encode('utf8') if isinstance(v,unicode) else v for k,v in r.items()})
    f.close()

    print [result['text'] for result in res_list]