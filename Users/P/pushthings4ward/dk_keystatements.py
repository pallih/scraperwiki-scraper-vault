###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import re

# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = [ ('I learn German','Ich lerne Deutsch')]
RESULTS_PER_PAGE = '100'
LANGUAGE = ''
NUM_PAGES = 15

for (q,table) in QUERY:
    for page in range(1, NUM_PAGES+1):
        base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&result_type=recent' \
         % (urllib2.quote(q), RESULTS_PER_PAGE, LANGUAGE, page)
        try:
            results_json = simplejson.loads(scraperwiki.scrape(base_url))
            print results_json
            if len(results_json['results'])==0: break
            for result in results_json['results']:
                #print result
                data = {}
                data['id'] = result['id']
                data['text'] = result['text']
                data['from_user'] = result['from_user']
                data['from_user_id'] = result['from_user_id']
                #data['to_user'] = result['to_user']
                #data['to_user_id'] = result['to_user_id']
                data['created_at'] = result['created_at']
                data['geo'] = result['geo']
                data['source'] = result['source']
                data['profile_image_url'] = result['profile_image_url']
                data['iso_language_code'] = result['iso_language_code']
                 
                thashtags=re.findall("#([a-z0-9]+)", result['text'], re.I)
                data['hashtags']=' | '.join(thashtags)
                
                tuser=re.findall("@([a-z0-9]+)", result['text'], re.I)
                data['user identified']=' | '.join(tuser)
                
                thashtags=re.findall("RT @([a-z0-9]+)", result['text'], re.I)
                data['retweets']=' | '.join(thashtags)

                thashtags=re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", result['text'], re.I)
                data['links']=' | '.join(thashtags)

                thashtags=re.findall("fuck+", result['text'], re.I)
                data['KeyState001']=' | '.join(thashtags)
                
                thashtags=re.findall("German essay+", result['text'], re.I)
                data['KeyState002']=' | '.join(thashtags)
                
                thashtags=re.findall("going to fail+", result['text'], re.I)
                data['KeyState003']=' | '.join(thashtags)
                
                thashtags=re.findall("hard to learn+", result['text'], re.I)
                data['KeyState004']=' | '.join(thashtags)
                
                thashtags=re.findall("I can speak+", result['text'], re.I)
                data['KeyState005']=' | '.join(thashtags)

                thashtags=re.findall("I can't speak+", result['text'], re.I)
                data['KeyState006']=' | '.join(thashtags)
                
                thashtags=re.findall("I hate German+", result['text'], re.I)
                data['KeyState007']=' | '.join(thashtags)
                
                thashtags=re.findall("I have to learn German+", result['text'], re.I)
                data['KeyState008']=' | '.join(thashtags)
                
                thashtags=re.findall("I learn German at school+", result['text'], re.I)
                data['KeyState009']=' | '.join(thashtags)
                
                thashtags=re.findall("I love German+", result['text'], re.I)
                data['KeyState010']=' | '.join(thashtags)
                
                thashtags=re.findall("I love it+", result['text'], re.I)
                data['KeyState011']=' | '.join(thashtags)
                
                thashtags=re.findall("I really need to learn German+", result['text'], re.I)
                data['KeyState012']=' | '.join(thashtags)
                
                thashtags=re.findall("I should learn German+", result['text'], re.I)
                data['KeyState013']=' | '.join(thashtags)
                
                thashtags=re.findall("I study German+", result['text'], re.I)
                data['KeyState014']=' | '.join(thashtags)
                
                thashtags=re.findall("I wanna learn German+", result['text'], re.I)
                data['KeyState015']=' | '.join(thashtags)
                
                thashtags=re.findall("I want to learn German+", result['text'], re.I)
                data['KeyState016']=' | '.join(thashtags)
                
                thashtags=re.findall("I want to learn how to speak German+", result['text'], re.I)
                data['KeyState017']=' | '.join(thashtags)
                
                thashtags=re.findall("I will learn German+", result['text'], re.I)
                data['KeyState018']=' | '.join(thashtags)
                
                thashtags=re.findall("I'd love to learn German+", result['text'], re.I)
                data['KeyState019']=' | '.join(thashtags)
                
                thashtags=re.findall("I'd rather learn German+", result['text'], re.I)
                data['KeyState020']=' | '.join(thashtags)
                
                thashtags=re.findall("I'll learn German+", result['text'], re.I)
                data['KeyState021']=' | '.join(thashtags)
                
                thashtags=re.findall("I'm going to learn German+", result['text'], re.I)
                data['KeyState022']=' | '.join(thashtags)
                
                thashtags=re.findall("I'm gonna learn German+", result['text'], re.I)
                data['KeyState023']=' | '.join(thashtags)
                
                thashtags=re.findall("improve my German+", result['text'], re.I)
                data['KeyState024']=' | '.join(thashtags)
                
                thashtags=re.findall("It's a beautiful language+", result['text'], re.I)
                data['KeyState025']=' | '.join(thashtags)
                
                thashtags=re.findall("need to learn more German+", result['text'], re.I)
                data['KeyState026']=' | '.join(thashtags)
                
                thashtags=re.findall("trying to learn German+", result['text'], re.I)
                data['KeyState027']=' | '.join(thashtags)
                

                print data['from_user'], data['text'], data['iso_language_code'], data['source'], data['geo'], data['profile_image_url']
                scraperwiki.sqlite.save(table_name=table,unique_keys=["id"], data=data)
        except:
            print 'Oh dear, failed to scrape %s' % base_url
            break

###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import re

# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = [ ('I learn German','Ich lerne Deutsch')]
RESULTS_PER_PAGE = '100'
LANGUAGE = ''
NUM_PAGES = 15

for (q,table) in QUERY:
    for page in range(1, NUM_PAGES+1):
        base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&result_type=recent' \
         % (urllib2.quote(q), RESULTS_PER_PAGE, LANGUAGE, page)
        try:
            results_json = simplejson.loads(scraperwiki.scrape(base_url))
            print results_json
            if len(results_json['results'])==0: break
            for result in results_json['results']:
                #print result
                data = {}
                data['id'] = result['id']
                data['text'] = result['text']
                data['from_user'] = result['from_user']
                data['from_user_id'] = result['from_user_id']
                #data['to_user'] = result['to_user']
                #data['to_user_id'] = result['to_user_id']
                data['created_at'] = result['created_at']
                data['geo'] = result['geo']
                data['source'] = result['source']
                data['profile_image_url'] = result['profile_image_url']
                data['iso_language_code'] = result['iso_language_code']
                 
                thashtags=re.findall("#([a-z0-9]+)", result['text'], re.I)
                data['hashtags']=' | '.join(thashtags)
                
                tuser=re.findall("@([a-z0-9]+)", result['text'], re.I)
                data['user identified']=' | '.join(tuser)
                
                thashtags=re.findall("RT @([a-z0-9]+)", result['text'], re.I)
                data['retweets']=' | '.join(thashtags)

                thashtags=re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", result['text'], re.I)
                data['links']=' | '.join(thashtags)

                thashtags=re.findall("fuck+", result['text'], re.I)
                data['KeyState001']=' | '.join(thashtags)
                
                thashtags=re.findall("German essay+", result['text'], re.I)
                data['KeyState002']=' | '.join(thashtags)
                
                thashtags=re.findall("going to fail+", result['text'], re.I)
                data['KeyState003']=' | '.join(thashtags)
                
                thashtags=re.findall("hard to learn+", result['text'], re.I)
                data['KeyState004']=' | '.join(thashtags)
                
                thashtags=re.findall("I can speak+", result['text'], re.I)
                data['KeyState005']=' | '.join(thashtags)

                thashtags=re.findall("I can't speak+", result['text'], re.I)
                data['KeyState006']=' | '.join(thashtags)
                
                thashtags=re.findall("I hate German+", result['text'], re.I)
                data['KeyState007']=' | '.join(thashtags)
                
                thashtags=re.findall("I have to learn German+", result['text'], re.I)
                data['KeyState008']=' | '.join(thashtags)
                
                thashtags=re.findall("I learn German at school+", result['text'], re.I)
                data['KeyState009']=' | '.join(thashtags)
                
                thashtags=re.findall("I love German+", result['text'], re.I)
                data['KeyState010']=' | '.join(thashtags)
                
                thashtags=re.findall("I love it+", result['text'], re.I)
                data['KeyState011']=' | '.join(thashtags)
                
                thashtags=re.findall("I really need to learn German+", result['text'], re.I)
                data['KeyState012']=' | '.join(thashtags)
                
                thashtags=re.findall("I should learn German+", result['text'], re.I)
                data['KeyState013']=' | '.join(thashtags)
                
                thashtags=re.findall("I study German+", result['text'], re.I)
                data['KeyState014']=' | '.join(thashtags)
                
                thashtags=re.findall("I wanna learn German+", result['text'], re.I)
                data['KeyState015']=' | '.join(thashtags)
                
                thashtags=re.findall("I want to learn German+", result['text'], re.I)
                data['KeyState016']=' | '.join(thashtags)
                
                thashtags=re.findall("I want to learn how to speak German+", result['text'], re.I)
                data['KeyState017']=' | '.join(thashtags)
                
                thashtags=re.findall("I will learn German+", result['text'], re.I)
                data['KeyState018']=' | '.join(thashtags)
                
                thashtags=re.findall("I'd love to learn German+", result['text'], re.I)
                data['KeyState019']=' | '.join(thashtags)
                
                thashtags=re.findall("I'd rather learn German+", result['text'], re.I)
                data['KeyState020']=' | '.join(thashtags)
                
                thashtags=re.findall("I'll learn German+", result['text'], re.I)
                data['KeyState021']=' | '.join(thashtags)
                
                thashtags=re.findall("I'm going to learn German+", result['text'], re.I)
                data['KeyState022']=' | '.join(thashtags)
                
                thashtags=re.findall("I'm gonna learn German+", result['text'], re.I)
                data['KeyState023']=' | '.join(thashtags)
                
                thashtags=re.findall("improve my German+", result['text'], re.I)
                data['KeyState024']=' | '.join(thashtags)
                
                thashtags=re.findall("It's a beautiful language+", result['text'], re.I)
                data['KeyState025']=' | '.join(thashtags)
                
                thashtags=re.findall("need to learn more German+", result['text'], re.I)
                data['KeyState026']=' | '.join(thashtags)
                
                thashtags=re.findall("trying to learn German+", result['text'], re.I)
                data['KeyState027']=' | '.join(thashtags)
                

                print data['from_user'], data['text'], data['iso_language_code'], data['source'], data['geo'], data['profile_image_url']
                scraperwiki.sqlite.save(table_name=table,unique_keys=["id"], data=data)
        except:
            print 'Oh dear, failed to scrape %s' % base_url
            break

