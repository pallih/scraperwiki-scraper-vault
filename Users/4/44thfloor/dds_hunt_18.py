import scraperwiki
import simplejson
import requests
import re
import dateutil.parser

# Only look for tweets that are sent to @ddshunt 
search_term = "@44thfloor"

done_scraping = False
pageNumber = 1

try:
    while not done_scraping:
        print "Processing page %s" % pageNumber
        # Call the twitter API to get a list of tweets sent to @ddshunt
        base_url = 'http://search.twitter.com/search.json?q=%s&rpp=100&page=%s&include_entities=true' % (search_term, pageNumber)
        results_json = simplejson.loads(requests.get(base_url).content)
        
        # Check to see if we got any tweets. If we didn't, we are DONE scraping.
        if len(results_json['results']):
            # If we did get tweets, then loop over every tweet we received
            for result in results_json['results']:
                try:
                    # Collect all the data we need
                    tweet = {
                        'id': result['id'],
                        'text': result['text'],
                        'created_at': dateutil.parser.parse(result['created_at']),
                        'lat': result['geo']['coordinates'][0],
                        'lng': result['geo']['coordinates'][1],
                        'image': result['entities']['media'][0]['media_url'],
                        'user': result['from_user'],
                        'user_name': result['from_user_name']
                    }
                    # Extract the hashtag out of the tweet. This will be the name of the dataset
                    dataset = re.search("#(\w)*", result['text']).group()[1:]
                    print "Found a tweet for the %s dataset by %s" % (dataset, tweet["user_name"])
                    # Save the tweet in the database (It will be saved in a table with the same name as the dataset)
                    scraperwiki.sqlite.save(["id"], tweet, dataset)

                    # Save the tweet again, but in a table containing all of the other datasets people have collected
                    tweet['dataset'] = dataset
                    scraperwiki.sqlite.save(["id"], tweet, "All")
                except:
                    # If an error occurs reading a tweet, skip over that tweet
                    pass
            pageNumber = pageNumber + 1

        else:
            done_scraping = True
except Exception as ex:
    print 'Oh dear, failed to scrape %s' % ex
    raise
