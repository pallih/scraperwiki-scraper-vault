import scraperwiki

#!/usr/bin/python
# -*- coding: utf-8 -*-


import csv
import argparse
import urllib2
import json
import datetime
import time
from urllib import urlencode
from time import mktime
from datetime import date
from math import ceil, floor
from sys import exit

class TwitterScrape(object):
    """    Queries twitter for a given user's tweets.
        - By default 200 of the most recents tweets are returned.
        - Setting _total_tweets, changes the amount of tweets returned.
        - setting _tweet_id will start the search from that tweet and go down 
        from there.
    """
    _tweets = {}

    @property
    def tweets(self):
        return self._tweets

    def textOutput(self, text, message_level=1):
        """ helper function to output text to screen 
            level 0 - no text
            level 1 - some text
            level 2 - all text
        """

        if self._verbose == message_level and message_level == 1: #level 1
            print str(text)
        elif self._verbose == 2: #output all messages
            print str(text)

    def process(self, json_data):
        """ Takes json data from twitter and creates a dict list with the data
            we are looking for - 'id','created_at','text'. see self._tweet_keys

            Keyword arguments:
            json_data     -- json object data retrieved from twitter
            """

        timeDiff = mktime(time.localtime())-mktime(time.gmtime())

        for tweet in json_data:
            newTweet = {}
            for key in self.__tweet_keys:
                if key == 'created_at':
                    ts = mktime(time.strptime(tweet['created_at'], 
                                            '%a %b %d %H:%M:%S +0000 %Y'))
                    dt = datetime.datetime.fromtimestamp(ts+timeDiff)
                    newTweet[key] = dt.strftime("%Y-%m-%d %H:%M:%S")
                elif type(tweet[key]) is str:
                    newTweet[key] = tweet[key].encode('ascii', 'ignore')
                else:
                    newTweet[key] = tweet[key]

            self.textOutput(newTweet)

            self._tweets[str(newTweet['id'])] = newTweet

    def queryTwitter(self, total_tweets=0, tweet_id=0):
        """Queries Twitter for a given users tweets 
            Return a json object.

        Keyword arguments:
        total_tweets    -- total tweets to be returned 
        tweet_id         -- the highest tweet ID. used as a starting point 
                            for getting new tweets
        """

        headers = { 'User-Agent' : 'Mozilla/5.0' }

        #TODO: update to the v1.1 Twitter API
        url = 'https://api.twitter.com/1/statuses/user_timeline.json?' 
        
        #reduced the number of returned tweets, 
        #    if the requested amount is larger than what is allowed
        if total_tweets > self.MAX_TWEETS_PER_CALL:
            total_tweets = self.MAX_TWEETS_PER_CALL

        params = { 'screen_name': self._twitter_handle,
            'include_entities': True,
            'include_rts': 0,
            'trim_user': 1,
            'count': total_tweets
        }

        if tweet_id:
            params['max_id'] = tweet_id
        #elif tweet_id > 0:
        #params['since_id'] = tweet_id

        self.textOutput('Sent ' + url + urlencode(params))

        try:
            req = urllib2.Request(url + urlencode(params), None, headers)
            json_data = urllib2.urlopen(req).read()
        except urllib2.URLError as error:
            print '%s - Bad values' % error
            exit(-1)
        except urllib2.HTTPError as error:
            print '%s' % error 
            exit(-1)

        return json.loads(json_data)

    def writeToCSV(self):
        """Write the tweets to a csv file.
            The Columns are set by self._tweet_keys
        """

        with open(self._file_name, 'wb') as csvfile:
            fw = csv.DictWriter(csvfile, self.__tweet_keys,
                                delimiter=self._delimiter)
            try:
                fw.writer.writerow(fw.fieldnames) 
                for key in sorted(self._tweets.iterkeys()):
                    fw.writerow(self._tweets[key])
            except csv.Error as e:
                exit('file %s: %s' % (self._file_name, e))

    def run(self, total_tweets=None, tweet_id=0):
        """Runs the script
            Queries Twitter for a user's tweets. Tweets are ordered new to old
        """

        #check if tweet_id is a long
        if tweet_id and type(tweet_id) is not long:
            raise Exception("Incorrect tweet ID - tweet ID must be type long")
        
        #if no mount is set, return the maximum amount
        if total_tweets is None:
            total_tweets = self.MAX_TWEETS_PER_CALL

        self.textOutput(total_tweets, 1)

        total_retrieved_tweets = 0
        while len(self._tweets) < total_tweets:
            json_data = self.queryTwitter(total_tweets, tweet_id)
            
            self.textOutput(json_data, 2)

            self.process(json_data)

            #to prevent an inifite loop
            if total_retrieved_tweets  != len(self._tweets):
                total_tweets = len(self._tweets)
            else:
                self.textOutput('no change - no more tweets - exit',1)
                break

            keys = sorted(self._tweets.keys())
            tweet_id = int(self._tweets[keys[0]]['id']) - 1 #previous tweet

        return True

    def __init__(self, twitter_handle, tweet_keys=None, writeCSV=True, keys=['text'], verbose=None):
        """
        Keyword arguments:
        twitter_handle - twitter username - required string
        tweet_keys    -- keys you want returned. default REQUIRED_KEYS
        verbose        -- show output for non-errors, default 0 - no output
        """

        #const values
        self.TWITTER_HANDLE_MAX_LENGTH = 15 #limit set by Twitter
        self.MAX_TWEETS_PER_CALL = 200 #limit set by Twitter
        REQUIRED_KEYS = ['id','created_at']

        #required values
        if twitter_handle is None:
            raise Exception("A twitter handle is required")
        if (len(twitter_handle.replace("@","")) > self.TWITTER_HANDLE_MAX_LENGTH 
            or type(twitter_handle) is not str):
            raise Exception("Bad twitter handle")

        self._twitter_handle = twitter_handle.replace("@","")

        #optional values
        self._verbose = verbose if type(verbose) is int else 0
        self._writeToCSV = writeCSV if writeCSV else True
        
        #set required keys
        self.__tweet_keys = REQUIRED_KEYS
        if type(keys) is list:
            for key in keys:
                self.__tweet_keys.append(key)

        #default values
        self._delimiter = ','
        self._file_name = (datetime.date.today().strftime("%Y-%m-%d") + '_' + 
                            self._twitter_handle + '.csv')


if __name__ == '__main__':
    """Takes input from the users and runs the TwitterScrape class"""

    parser = argparse.ArgumentParser(description='A simple tweet scraper')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('twitter_handle',
                        help='A Twitter handle. MAX 15 characters')
    parser.add_argument('-t', '--total', type=int, dest='total',
                         help='Total number of returned tweets')
    group.add_argument('--tweet-id', type=int, dest='tweet_id',
                        help='Begin search from this ID')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.9')
    args = parser.parse_args()

    try :
        ts = TwitterScrape(args.twitter_handle, verbose=0)
        if ts.run(tweet_id=args.tweet_id, total_tweets=args.total):
            ts.writeToCSV()
        else:
            print 'Error'
    except Exception, err:
        print '%s'% str(err)

import scraperwiki

#!/usr/bin/python
# -*- coding: utf-8 -*-


import csv
import argparse
import urllib2
import json
import datetime
import time
from urllib import urlencode
from time import mktime
from datetime import date
from math import ceil, floor
from sys import exit

class TwitterScrape(object):
    """    Queries twitter for a given user's tweets.
        - By default 200 of the most recents tweets are returned.
        - Setting _total_tweets, changes the amount of tweets returned.
        - setting _tweet_id will start the search from that tweet and go down 
        from there.
    """
    _tweets = {}

    @property
    def tweets(self):
        return self._tweets

    def textOutput(self, text, message_level=1):
        """ helper function to output text to screen 
            level 0 - no text
            level 1 - some text
            level 2 - all text
        """

        if self._verbose == message_level and message_level == 1: #level 1
            print str(text)
        elif self._verbose == 2: #output all messages
            print str(text)

    def process(self, json_data):
        """ Takes json data from twitter and creates a dict list with the data
            we are looking for - 'id','created_at','text'. see self._tweet_keys

            Keyword arguments:
            json_data     -- json object data retrieved from twitter
            """

        timeDiff = mktime(time.localtime())-mktime(time.gmtime())

        for tweet in json_data:
            newTweet = {}
            for key in self.__tweet_keys:
                if key == 'created_at':
                    ts = mktime(time.strptime(tweet['created_at'], 
                                            '%a %b %d %H:%M:%S +0000 %Y'))
                    dt = datetime.datetime.fromtimestamp(ts+timeDiff)
                    newTweet[key] = dt.strftime("%Y-%m-%d %H:%M:%S")
                elif type(tweet[key]) is str:
                    newTweet[key] = tweet[key].encode('ascii', 'ignore')
                else:
                    newTweet[key] = tweet[key]

            self.textOutput(newTweet)

            self._tweets[str(newTweet['id'])] = newTweet

    def queryTwitter(self, total_tweets=0, tweet_id=0):
        """Queries Twitter for a given users tweets 
            Return a json object.

        Keyword arguments:
        total_tweets    -- total tweets to be returned 
        tweet_id         -- the highest tweet ID. used as a starting point 
                            for getting new tweets
        """

        headers = { 'User-Agent' : 'Mozilla/5.0' }

        #TODO: update to the v1.1 Twitter API
        url = 'https://api.twitter.com/1/statuses/user_timeline.json?' 
        
        #reduced the number of returned tweets, 
        #    if the requested amount is larger than what is allowed
        if total_tweets > self.MAX_TWEETS_PER_CALL:
            total_tweets = self.MAX_TWEETS_PER_CALL

        params = { 'screen_name': self._twitter_handle,
            'include_entities': True,
            'include_rts': 0,
            'trim_user': 1,
            'count': total_tweets
        }

        if tweet_id:
            params['max_id'] = tweet_id
        #elif tweet_id > 0:
        #params['since_id'] = tweet_id

        self.textOutput('Sent ' + url + urlencode(params))

        try:
            req = urllib2.Request(url + urlencode(params), None, headers)
            json_data = urllib2.urlopen(req).read()
        except urllib2.URLError as error:
            print '%s - Bad values' % error
            exit(-1)
        except urllib2.HTTPError as error:
            print '%s' % error 
            exit(-1)

        return json.loads(json_data)

    def writeToCSV(self):
        """Write the tweets to a csv file.
            The Columns are set by self._tweet_keys
        """

        with open(self._file_name, 'wb') as csvfile:
            fw = csv.DictWriter(csvfile, self.__tweet_keys,
                                delimiter=self._delimiter)
            try:
                fw.writer.writerow(fw.fieldnames) 
                for key in sorted(self._tweets.iterkeys()):
                    fw.writerow(self._tweets[key])
            except csv.Error as e:
                exit('file %s: %s' % (self._file_name, e))

    def run(self, total_tweets=None, tweet_id=0):
        """Runs the script
            Queries Twitter for a user's tweets. Tweets are ordered new to old
        """

        #check if tweet_id is a long
        if tweet_id and type(tweet_id) is not long:
            raise Exception("Incorrect tweet ID - tweet ID must be type long")
        
        #if no mount is set, return the maximum amount
        if total_tweets is None:
            total_tweets = self.MAX_TWEETS_PER_CALL

        self.textOutput(total_tweets, 1)

        total_retrieved_tweets = 0
        while len(self._tweets) < total_tweets:
            json_data = self.queryTwitter(total_tweets, tweet_id)
            
            self.textOutput(json_data, 2)

            self.process(json_data)

            #to prevent an inifite loop
            if total_retrieved_tweets  != len(self._tweets):
                total_tweets = len(self._tweets)
            else:
                self.textOutput('no change - no more tweets - exit',1)
                break

            keys = sorted(self._tweets.keys())
            tweet_id = int(self._tweets[keys[0]]['id']) - 1 #previous tweet

        return True

    def __init__(self, twitter_handle, tweet_keys=None, writeCSV=True, keys=['text'], verbose=None):
        """
        Keyword arguments:
        twitter_handle - twitter username - required string
        tweet_keys    -- keys you want returned. default REQUIRED_KEYS
        verbose        -- show output for non-errors, default 0 - no output
        """

        #const values
        self.TWITTER_HANDLE_MAX_LENGTH = 15 #limit set by Twitter
        self.MAX_TWEETS_PER_CALL = 200 #limit set by Twitter
        REQUIRED_KEYS = ['id','created_at']

        #required values
        if twitter_handle is None:
            raise Exception("A twitter handle is required")
        if (len(twitter_handle.replace("@","")) > self.TWITTER_HANDLE_MAX_LENGTH 
            or type(twitter_handle) is not str):
            raise Exception("Bad twitter handle")

        self._twitter_handle = twitter_handle.replace("@","")

        #optional values
        self._verbose = verbose if type(verbose) is int else 0
        self._writeToCSV = writeCSV if writeCSV else True
        
        #set required keys
        self.__tweet_keys = REQUIRED_KEYS
        if type(keys) is list:
            for key in keys:
                self.__tweet_keys.append(key)

        #default values
        self._delimiter = ','
        self._file_name = (datetime.date.today().strftime("%Y-%m-%d") + '_' + 
                            self._twitter_handle + '.csv')


if __name__ == '__main__':
    """Takes input from the users and runs the TwitterScrape class"""

    parser = argparse.ArgumentParser(description='A simple tweet scraper')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('twitter_handle',
                        help='A Twitter handle. MAX 15 characters')
    parser.add_argument('-t', '--total', type=int, dest='total',
                         help='Total number of returned tweets')
    group.add_argument('--tweet-id', type=int, dest='tweet_id',
                        help='Begin search from this ID')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.9')
    args = parser.parse_args()

    try :
        ts = TwitterScrape(args.twitter_handle, verbose=0)
        if ts.run(tweet_id=args.tweet_id, total_tweets=args.total):
            ts.writeToCSV()
        else:
            print 'Error'
    except Exception, err:
        print '%s'% str(err)

