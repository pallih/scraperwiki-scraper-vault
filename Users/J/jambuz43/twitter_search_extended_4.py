import scraperwiki
import simplejson
import urllib2
import requests
import dateutil.parser

def search(queries = [], results_per_page = 100, language = 'en', num_pages = 15, save_author_info = True ):
    '''
    Get results from the Twitter API! Change QUERY to your search term of choice. 
    Example queries: 'newsnight', '#newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
    '''
    for query in queries:
        for page in range(1, num_pages + 1):
            tweets = [#ReplacetaglinewithJokowi]
            usernames = []
            users = []

            base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' % (urllib2.quote(query), str(results_per_page), language, str(page))
            try:
                results_json = simplejson.loads(requests.get(base_url).content)
                if 'results' in results_json:
                    for result in results_json['results']:
                        tweet = {
                            'id': result['id'],
                            'text': result['text'],
                            'created_at': dateutil.parser.parse(result['created_at']),
                            'location': None,
                            'lat': None,
                            'lng': None,
                            'from_user': result['from_user'],
                            'from_user_id': result['from_user_id'],
                            'from_user_name': result['from_user_name'],
                            'to_user': result['to_user'],
                            'to_user_id': result['to_user_id'],
                            'to_user_name': result['to_user_name']
                        }
                        try:
                            tweet['lat'] = result['geo']['coordinates'][0]
                            tweet['lng'] = result['geo']['coordinates'][1]
                        except:
                            pass
                        try:
                            tweet['location'] = result['location']
                        except:
                            pass
                        tweets.append(tweet)
                        usernames.append(result['from_user'])
                    #print tweets
                    #print usernames
                    if len(tweets):
                        scraperwiki.sqlite.save(["id"], tweets, 'tweets')
                        print query, '-', 'scraped', len(tweets), 'tweets'
                    else:
                        print query, '-', 'no more tweets returned'
                else:
                    print 'no results returned for query:', query, ' - ', results_json
            except:
                print 'Oh dear, failed to scrape %s' % base_url
                raise
            
            if len(usernames):
                base_url = 'http://api.twitter.com/1/users/lookup.json'
                try:
                    results_json = simplejson.loads(requests.post(base_url, data={'screen_name':','.join(list(set(usernames)))}).content)
                    for result in results_json:
                        user = {
                            'id': result['id'],
                            'screen_name': result['screen_name'],
                            'created_at': dateutil.parser.parse(result['created_at']),
                            'location': None,
                            'lat': None,
                            'lng': None,
                            'followers_count': result['followers_count'],
                            'friends_count': result['friends_count'],
                            'description': result['description']
                        }
                        try:
                            user['lat'] = result['geo']['coordinates'][0]
                            user['lng'] = result['geo']['coordinates'][1]
                        except:
                            pass
                        try:
                            user['location'] = result['location']
                        except:
                            pass
                        users.append(user)
                    #print users
                    scraperwiki.sqlite.save(["id"], users, 'users')
                    print query, '-', 'scraped', len(users), 'users'
                except:
                    print 'Oh dear, failed to scrape %s' % base_url
                    raise
            else:
                print query, '-', 'no more users to scrape'
import scraperwiki
import simplejson
import urllib2
import requests
import dateutil.parser

def search(queries = [], results_per_page = 100, language = 'en', num_pages = 15, save_author_info = True ):
    '''
    Get results from the Twitter API! Change QUERY to your search term of choice. 
    Example queries: 'newsnight', '#newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
    '''
    for query in queries:
        for page in range(1, num_pages + 1):
            tweets = [#ReplacetaglinewithJokowi]
            usernames = []
            users = []

            base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' % (urllib2.quote(query), str(results_per_page), language, str(page))
            try:
                results_json = simplejson.loads(requests.get(base_url).content)
                if 'results' in results_json:
                    for result in results_json['results']:
                        tweet = {
                            'id': result['id'],
                            'text': result['text'],
                            'created_at': dateutil.parser.parse(result['created_at']),
                            'location': None,
                            'lat': None,
                            'lng': None,
                            'from_user': result['from_user'],
                            'from_user_id': result['from_user_id'],
                            'from_user_name': result['from_user_name'],
                            'to_user': result['to_user'],
                            'to_user_id': result['to_user_id'],
                            'to_user_name': result['to_user_name']
                        }
                        try:
                            tweet['lat'] = result['geo']['coordinates'][0]
                            tweet['lng'] = result['geo']['coordinates'][1]
                        except:
                            pass
                        try:
                            tweet['location'] = result['location']
                        except:
                            pass
                        tweets.append(tweet)
                        usernames.append(result['from_user'])
                    #print tweets
                    #print usernames
                    if len(tweets):
                        scraperwiki.sqlite.save(["id"], tweets, 'tweets')
                        print query, '-', 'scraped', len(tweets), 'tweets'
                    else:
                        print query, '-', 'no more tweets returned'
                else:
                    print 'no results returned for query:', query, ' - ', results_json
            except:
                print 'Oh dear, failed to scrape %s' % base_url
                raise
            
            if len(usernames):
                base_url = 'http://api.twitter.com/1/users/lookup.json'
                try:
                    results_json = simplejson.loads(requests.post(base_url, data={'screen_name':','.join(list(set(usernames)))}).content)
                    for result in results_json:
                        user = {
                            'id': result['id'],
                            'screen_name': result['screen_name'],
                            'created_at': dateutil.parser.parse(result['created_at']),
                            'location': None,
                            'lat': None,
                            'lng': None,
                            'followers_count': result['followers_count'],
                            'friends_count': result['friends_count'],
                            'description': result['description']
                        }
                        try:
                            user['lat'] = result['geo']['coordinates'][0]
                            user['lng'] = result['geo']['coordinates'][1]
                        except:
                            pass
                        try:
                            user['location'] = result['location']
                        except:
                            pass
                        users.append(user)
                    #print users
                    scraperwiki.sqlite.save(["id"], users, 'users')
                    print query, '-', 'scraped', len(users), 'users'
                except:
                    print 'Oh dear, failed to scrape %s' % base_url
                    raise
            else:
                print query, '-', 'no more users to scrape'
