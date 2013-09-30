import scraperwiki
import simplejson
 # The Twitter API is the Schr ö dinger ’ s cat of web service APIs. Until you call it, you 
#never know if it ’ s alive or dead. Sometimes the mere act of calling it is enough to 
#kill it. 
#—  Scott Koon, Witty

#twitter api docs here: https://dev.twitter.com/docs/using-search

base_url = 'http://search.twitter.com/search.json?q='
num_tweets = '&rpp=70'
#Chrysi Avgi

result_type='&result_type=recent'

#query = 'Chrysi%20Avgi'

query = 'Obama'

#query = 'Obama'
include_entities= '&include_entities=true'

#...


#print results
#print results['results'] 

page_number = 1

while page_number <= 1:

    page='&page='+str(page_number)

    url=base_url+query+num_tweets
    print url
    results = simplejson.loads(scraperwiki.scrape(url))
    #print results
    counter = 0
    for item in results['results']:
                #print item['text'] 
                data = {'text': item['text'] ,'source': item['source']}
                scraperwiki.sqlite.save(unique_keys=['text'], data = data)
                
                #print item['profile_image_url']
                print item['text']
                #print item['geo']
                counter+=1
    page_number += 1
    print 'num tweets = ',counter
import scraperwiki
import simplejson
 # The Twitter API is the Schr ö dinger ’ s cat of web service APIs. Until you call it, you 
#never know if it ’ s alive or dead. Sometimes the mere act of calling it is enough to 
#kill it. 
#—  Scott Koon, Witty

#twitter api docs here: https://dev.twitter.com/docs/using-search

base_url = 'http://search.twitter.com/search.json?q='
num_tweets = '&rpp=70'
#Chrysi Avgi

result_type='&result_type=recent'

#query = 'Chrysi%20Avgi'

query = 'Obama'

#query = 'Obama'
include_entities= '&include_entities=true'

#...


#print results
#print results['results'] 

page_number = 1

while page_number <= 1:

    page='&page='+str(page_number)

    url=base_url+query+num_tweets
    print url
    results = simplejson.loads(scraperwiki.scrape(url))
    #print results
    counter = 0
    for item in results['results']:
                #print item['text'] 
                data = {'text': item['text'] ,'source': item['source']}
                scraperwiki.sqlite.save(unique_keys=['text'], data = data)
                
                #print item['profile_image_url']
                print item['text']
                #print item['geo']
                counter+=1
    page_number += 1
    print 'num tweets = ',counter
