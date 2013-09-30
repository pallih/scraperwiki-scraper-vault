# Blank Python
# This scraper collects all tips for all venues from particular list
# Last edit: 18 / 03/ 2013 @ 20:50 - Tested and works
import simplejson
import scraperwiki
import requests

url = "https://api.foursquare.com/v2/lists/4ef2f5058b81368cf8e84bd6?oauth_token=CJRRXXXINNV5UU0WS4K3C510XTWQ3OACIKHOKOAS3BL5UJU1&v=20130318"

resultsJson = simplejson.loads(scraperwiki.scrape(url))

results = resultsJson['response']['list']['listItems']['items']


for item in results:

    category = item['venue']['categories']
    for item0 in category:
        
        if item0.has_key('name'):
            cName = category[0]['name']
                  
    if item['venue'].has_key('id'):
        vid = item['venue']['id']
        
    if item['venue'].has_key('name'):
        name = item['venue']['name']    

    if item['venue']['location'].has_key('lat'):
        lat = item['venue']['location']['lat']

    if item['venue']['location'].has_key('lng'):
        lng = item['venue']['location']['lng']

    url2 = "https://api.foursquare.com/v2/venues/"+vid+"/tips?oauth_token=CJRRXXXINNV5UU0WS4K3C510XTWQ3OACIKHOKOAS3BL5UJU1&v=20130318"  
    resultsJson2 = simplejson.loads(scraperwiki.scrape(url2))
    tips = resultsJson2['response']['tips']['items']

    for item2 in tips:

        if item2.has_key('id'):
            tipid = item2['id']

        url3 = "https://api.foursquare.com/v2/tips/"+tipid+"?oauth_token=CJRRXXXINNV5UU0WS4K3C510XTWQ3OACIKHOKOAS3BL5UJU1&v=20130318"
        resultsJson3 = simplejson.loads(scraperwiki.scrape(url3))        
        tip = resultsJson3['response']['tip']

        tip_id = tip['id']

        tip_text = tip['text']

        v_name = tip['venue']['name']

        data = {'tip_id' : tip_id,
                'tip_text' : tip_text,
                'v_name' : v_name,
                }
    
        scraperwiki.sqlite.save(unique_keys=['tip_id'], data=data)
# Blank Python
# This scraper collects all tips for all venues from particular list
# Last edit: 18 / 03/ 2013 @ 20:50 - Tested and works
import simplejson
import scraperwiki
import requests

url = "https://api.foursquare.com/v2/lists/4ef2f5058b81368cf8e84bd6?oauth_token=CJRRXXXINNV5UU0WS4K3C510XTWQ3OACIKHOKOAS3BL5UJU1&v=20130318"

resultsJson = simplejson.loads(scraperwiki.scrape(url))

results = resultsJson['response']['list']['listItems']['items']


for item in results:

    category = item['venue']['categories']
    for item0 in category:
        
        if item0.has_key('name'):
            cName = category[0]['name']
                  
    if item['venue'].has_key('id'):
        vid = item['venue']['id']
        
    if item['venue'].has_key('name'):
        name = item['venue']['name']    

    if item['venue']['location'].has_key('lat'):
        lat = item['venue']['location']['lat']

    if item['venue']['location'].has_key('lng'):
        lng = item['venue']['location']['lng']

    url2 = "https://api.foursquare.com/v2/venues/"+vid+"/tips?oauth_token=CJRRXXXINNV5UU0WS4K3C510XTWQ3OACIKHOKOAS3BL5UJU1&v=20130318"  
    resultsJson2 = simplejson.loads(scraperwiki.scrape(url2))
    tips = resultsJson2['response']['tips']['items']

    for item2 in tips:

        if item2.has_key('id'):
            tipid = item2['id']

        url3 = "https://api.foursquare.com/v2/tips/"+tipid+"?oauth_token=CJRRXXXINNV5UU0WS4K3C510XTWQ3OACIKHOKOAS3BL5UJU1&v=20130318"
        resultsJson3 = simplejson.loads(scraperwiki.scrape(url3))        
        tip = resultsJson3['response']['tip']

        tip_id = tip['id']

        tip_text = tip['text']

        v_name = tip['venue']['name']

        data = {'tip_id' : tip_id,
                'tip_text' : tip_text,
                'v_name' : v_name,
                }
    
        scraperwiki.sqlite.save(unique_keys=['tip_id'], data=data)
