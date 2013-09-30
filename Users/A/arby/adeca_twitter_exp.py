print "Hello, coding in the cloud!"

import scraperwiki 
import simplejson
import urllib2
import datetime

# Based on Nicola's Twitter Scraper -view-source:https://scraperwiki.com/editor/raw/mozfest_twitter_scraper_1  

# Change QUERY to your search term of choice.  
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight' 
QUERY = 'from:ADECA_News' 
RESULTS_PER_PAGE = '100' 
LANGUAGE = 'en' 
NUM_PAGES = 1000   

for page in range(1, NUM_PAGES+1):
     
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)     
    try:         
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:             
            data = {}             
            data['id'] = result['id']             
            data['text'] = result['text'].replace("&quot;", "'")             
            data['from_user'] = result['from_user']             
            data['date'] = datetime.datetime.today()             
            print data['from_user'], data['text']             
            scraperwiki.sqlite.save(["id"], data)      

    except:         
        print 'Oh dear, failed to scrape %s' % base_url         
        break              




          

# Tutorial  
# html =  scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm") 
#print  html


# import lxml.html            
# root = lxml.html.fromstring(html) 
# for tr in root.cssselect("div[align='left'] tr"):     
#    tds = tr.cssselect("td")     
#     if len(tds)==12:         
 #       data = {             
 #           'country' : tds[0].text_content(),             
 #            'years_in_school' : int(tds[4].text_content())         
 #       }         
 #       print data
 #        scraperwiki.sqlite.save(unique_keys=['country'], data=data)



print "Hello, coding in the cloud!"

import scraperwiki 
import simplejson
import urllib2
import datetime

# Based on Nicola's Twitter Scraper -view-source:https://scraperwiki.com/editor/raw/mozfest_twitter_scraper_1  

# Change QUERY to your search term of choice.  
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight' 
QUERY = 'from:ADECA_News' 
RESULTS_PER_PAGE = '100' 
LANGUAGE = 'en' 
NUM_PAGES = 1000   

for page in range(1, NUM_PAGES+1):
     
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)     
    try:         
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:             
            data = {}             
            data['id'] = result['id']             
            data['text'] = result['text'].replace("&quot;", "'")             
            data['from_user'] = result['from_user']             
            data['date'] = datetime.datetime.today()             
            print data['from_user'], data['text']             
            scraperwiki.sqlite.save(["id"], data)      

    except:         
        print 'Oh dear, failed to scrape %s' % base_url         
        break              




          

# Tutorial  
# html =  scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm") 
#print  html


# import lxml.html            
# root = lxml.html.fromstring(html) 
# for tr in root.cssselect("div[align='left'] tr"):     
#    tds = tr.cssselect("td")     
#     if len(tds)==12:         
 #       data = {             
 #           'country' : tds[0].text_content(),             
 #            'years_in_school' : int(tds[4].text_content())         
 #       }         
 #       print data
 #        scraperwiki.sqlite.save(unique_keys=['country'], data=data)



