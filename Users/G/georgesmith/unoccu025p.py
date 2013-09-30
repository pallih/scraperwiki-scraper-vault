import scraperwiki 
import simplejson 
import urllib2 
import re 
 
QUERY = 'occupygezi%20-rt%20-RT%20-direngeziparki%20-direntaksim%20-direnankara%20-direnturkiye%20-tayipistifa%20-oyunagelmeturkiyem'

since = '2013-06-01'
until = '2013-06-02'
lang = 'tr'
RESULTS_PER_PAGE = '100' 
NUM_PAGES = 10 

 
LEGAL = """ 
/* 
Dataset Repository: OpenData | Open DataSets Source Respository 
Dataset Name: #occupygezi  
Dataset URI: https://github.com/PatrickMcGee/OpenData 
Author: Patrick McGee 
Author URI: http://www.patrickmcgee.co.uk 
Description: hashtag used for this dataset: #oyunagelmeturkiyem Dataset of tweets that are collected for further analysis and visualisation. 
dataset is in relation to the protests in Turkey. 
Version: 1.1 
License: Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License 
License URI: http://creativecommons.org/licenses/by-nc-sa/3.0/ 
Tags:  #direngeziparki #direntaksim #direnankara #direnturkiye #tayipistifa #oyunagelmeturkiyem #occupygezi
Text Domain: http://www.patrickmcgee.co.uk 
 
 
Use it to make something cool, have fun, and share what you've learned with others. 
*/ 
 
""" 

for page in range(1, NUM_PAGES+1): 
    base_url = 'http://search.twitter.com/search.json?q=%s&since=%s&until=%s&lang=%s&rpp=%s&page=%s' \
        % (urllib2.quote(QUERY), since, until, lang, RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            print result
            scraperwiki.sqlite.save(["id"], result)
            #data = {}
            #data['id'] = result['id']
            #data['text'] = result['text']
            #data['location'] = result['iso_language_code']
            #data['from_user'] = result['from_user']
            #data['created_at'] = result['created_at']
            #if data['location']:
                #print data['location'], data['from_user']
                #scraperwiki.sqlite.save(["id"], data)            
    

             
    
    
    except:
        print 'something went wrong and the scraper %s failed to complete' % base_url
        break 
import scraperwiki 
import simplejson 
import urllib2 
import re 
 
QUERY = 'occupygezi%20-rt%20-RT%20-direngeziparki%20-direntaksim%20-direnankara%20-direnturkiye%20-tayipistifa%20-oyunagelmeturkiyem'

since = '2013-06-01'
until = '2013-06-02'
lang = 'tr'
RESULTS_PER_PAGE = '100' 
NUM_PAGES = 10 

 
LEGAL = """ 
/* 
Dataset Repository: OpenData | Open DataSets Source Respository 
Dataset Name: #occupygezi  
Dataset URI: https://github.com/PatrickMcGee/OpenData 
Author: Patrick McGee 
Author URI: http://www.patrickmcgee.co.uk 
Description: hashtag used for this dataset: #oyunagelmeturkiyem Dataset of tweets that are collected for further analysis and visualisation. 
dataset is in relation to the protests in Turkey. 
Version: 1.1 
License: Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License 
License URI: http://creativecommons.org/licenses/by-nc-sa/3.0/ 
Tags:  #direngeziparki #direntaksim #direnankara #direnturkiye #tayipistifa #oyunagelmeturkiyem #occupygezi
Text Domain: http://www.patrickmcgee.co.uk 
 
 
Use it to make something cool, have fun, and share what you've learned with others. 
*/ 
 
""" 

for page in range(1, NUM_PAGES+1): 
    base_url = 'http://search.twitter.com/search.json?q=%s&since=%s&until=%s&lang=%s&rpp=%s&page=%s' \
        % (urllib2.quote(QUERY), since, until, lang, RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            print result
            scraperwiki.sqlite.save(["id"], result)
            #data = {}
            #data['id'] = result['id']
            #data['text'] = result['text']
            #data['location'] = result['iso_language_code']
            #data['from_user'] = result['from_user']
            #data['created_at'] = result['created_at']
            #if data['location']:
                #print data['location'], data['from_user']
                #scraperwiki.sqlite.save(["id"], data)            
    

             
    
    
    except:
        print 'something went wrong and the scraper %s failed to complete' % base_url
        break 
