import scraperwiki
import simplejson
 # The Twitter API is the Schr ö dinger ’ s cat of web service APIs. Until you call it, you 
#never know if it ’ s alive or dead. Sometimes the mere act of calling it is enough to 
#kill it. 
#—  Scott Koon, Witty

#twitter api docs here: https://dev.twitter.com/docs/using-search

base_url = 'http://search.twitter.com/search.json?q='
num_tweets = '&rrp=5'
#Chrysi Avgi

result_type='&result_type=recent'

query = '%22I%20heard%20voices%22'
#query = 'Obama'
include_entities= 'include_entities=true'
possibly_senitive= 'possibly_sensitive:true'

include_entities='&include_entities=true'



#print results
#print results['results'] 

page_number = 1

while page_number <= 5:

    page='&page='+str(page_number)

    url=base_url+query+include_entities+page+num_tweets+result_type
    results = simplejson.loads(scraperwiki.scrape(url))
    print results
    for item in results['results']:
                #print item['text'] 
                data = {'text': item['text'] ,'time': item['created_at']}
                scraperwiki.sqlite.save(unique_keys=['text'], data = data) 
                
                #print item['profile_image_url']
                #print item['source']
                #print item['geo']
    page_number += 1
