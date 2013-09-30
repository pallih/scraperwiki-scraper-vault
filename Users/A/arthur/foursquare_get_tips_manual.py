# Blank Python
import simplejson
import scraperwiki
import requests

url = "https://api.foursquare.com/v2/venues/4b7ec16bf964a5201bfd2fe3/tips?oauth_token=CJRRXXXINNV5UU0WS4K3C510XTWQ3OACIKHOKOAS3BL5UJU1&v=20130318&limit=100"

resultsJson = simplejson.loads(scraperwiki.scrape(url))

results = resultsJson['response']['tips']['items']

for item in results:
                  
    if item.has_key('id'):
        tipid = item['id']

    tip_id = item['id']

    tip_text = item['text']

    tip_likes = item['likes']['count']

    data = {'tip_id' : tip_id,
            'tip_text' : tip_text,
            'tip_likes' : tip_likes
            }
    
    scraperwiki.sqlite.save(unique_keys=['tip_id'], data=data)
# Blank Python
import simplejson
import scraperwiki
import requests

url = "https://api.foursquare.com/v2/venues/4b7ec16bf964a5201bfd2fe3/tips?oauth_token=CJRRXXXINNV5UU0WS4K3C510XTWQ3OACIKHOKOAS3BL5UJU1&v=20130318&limit=100"

resultsJson = simplejson.loads(scraperwiki.scrape(url))

results = resultsJson['response']['tips']['items']

for item in results:
                  
    if item.has_key('id'):
        tipid = item['id']

    tip_id = item['id']

    tip_text = item['text']

    tip_likes = item['likes']['count']

    data = {'tip_id' : tip_id,
            'tip_text' : tip_text,
            'tip_likes' : tip_likes
            }
    
    scraperwiki.sqlite.save(unique_keys=['tip_id'], data=data)
