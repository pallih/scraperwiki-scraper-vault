# Blank Python
import simplejson
import scraperwiki
import requests

near = "Moscow"
auth = "ZDPGKZERHSMZDIMLAKQFYLGHHNWJFPFKGXVSNUJSEFV5FFPO"
#auth = "NN3TBSPRBCVJMWCDPN1WELO1LOQLXAA31Q40WHW2L1BI5L1X"
#auth = "ACCESS_TOKEN"
date = "20120509"
url = "https://api.foursquare.com/v2/venues/search?near="+near+"&oauth_token="+auth+"&v="+date
#url = "https://api.foursquare.com/v2/venues/search?near="+near+"&oauth_token="+auth

scraperwiki.sqlite.delete

resultsJson = simplejson.loads(scraperwiki.scrape(url))

results = resultsJson['response']['venues']


for item in results:
    
    cName =  None
    address = None
    address = None
    lat = None
    lng = None
    forsquareUrl = None
    stats= 0

    category = item['categories']
    for item2 in category:
        
        if item2.has_key('name'):
            cName = category[0]['name']
                  
    if item.has_key('id'):
        id =  item['id']
        
    if item.has_key('name'):
        name =  item['name']    

    if item['location'].has_key('address'):
        address = item['location']['address']

    if item['location'].has_key('lat'):
        lat = item['location']['lat']

    if item['location'].has_key('lng'):
        lng = item['location']['lng']

    if item['stats'].has_key('checkinsCount'):
        count = item['stats']['checkinsCount']

    test = "https://api.foursquare.com/v2/venues/"+id+"?oauth_token="+auth+"&v="+date  
    response = requests.get(test, verify = False).text
    resultsJsonTest = simplejson.loads(response)
    foursquareUrl = resultsJsonTest['response']['venue']['canonicalUrl']

    likes =  resultsJsonTest['response']['venue']['likes']['count']
    
    data = {'id':  id,         
            'name' : name,
            'address' : address,
            'lat' : lat ,
            'lng' : lng,
            'categoryName' : cName,
            'count' : count,
            'likes' : likes}

    if count > 100 :
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

