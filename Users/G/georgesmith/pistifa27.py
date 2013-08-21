import scraperwiki 
import simplejson 
import urllib2 
import re 
 
QUERY = 'tayipistifa'
UNTIL_DATE = '2013-05-27'
RESULTS_PER_PAGE = '100' 
NUM_PAGES = 8 
 
LEGAL = """ 
/* 
Dataset Repository: OpenData | Open DataSets Source Respository 
Dataset Name: #oyunagelmeturkiyem  
Dataset URI: https://github.com/PatrickMcGee/OpenData 
Author: Patrick McGee 
Author URI: http://www.patrickmcgee.co.uk 
Description: hashtag used for this dataset: #oyunagelmeturkiyem Dataset of tweets that are collected for further analysis and visualisation. 
dataset is in relation to the protests in Turkey. 
Version: 1.1 
License: Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License 
License URI: http://creativecommons.org/licenses/by-nc-sa/3.0/ 
Tags:  #direngeziparki #direntaksim #direnankara #direnturkiye #tayipistifa #oyunagelmeturkiyem 
Text Domain: http://www.patrickmcgee.co.uk 
 
 
Use it to make something cool, have fun, and share what you've learned with others. 
*/ 
 
""" 

for page in range(1, NUM_PAGES+1): 
    base_url = 'http://search.twitter.com/search.json?q=%s&ud=%s&rpp=%s&page=%s' \
        % (urllib2.quote(QUERY),UNTIL_DATE, RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            print result
            scraperwiki.sqlite.save(["id"], result) 
    
    
    except:
        print 'something went wrong and the scraper %s failed to complete' % base_url
        break 

