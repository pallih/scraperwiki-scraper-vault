# Blank Python
import simplejson
import scraperwiki
import requests

url = "https://api.foursquare.com/v2/venues/search?intent=browse&sw=51.55017800,5.06263733&ne=51.56085115,5.08049011&oauth_token=HQFRZSOGA4N5C5CYIIZPEGMHX1OGENDTYKWL3DJZMH2GUNYN&v=20120920&categoryId=4d4b7105d754a06376d81259&limit=100"

resultsJson = simplejson.loads(scraperwiki.scrape(url))

results = resultsJson['response']['venues']


for item in results:
    
    cName =  None
    address = None
    address = None
    lat = None
    lng = None
    forsquareUrl = None
    Tipcount = None
    Checkins = None
    Users = None

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

    if item['stats'].has_key('tipCount'):
        Tipcount = item['stats']['tipCount']

    if item['stats'].has_key('checkinsCount'):
        Checkins = item['stats']['checkinsCount']

    if item['stats'].has_key('usersCount'):
        Users = item['stats']['usersCount']
    

    test = "https://api.foursquare.com/v2/venues/"+id+"?oauth_token=HQFRZSOGA4N5C5CYIIZPEGMHX1OGENDTYKWL3DJZMH2GUNYN&v=20120920"  
    response = requests.get(test, verify = False).text
    resultsJsonTest = simplejson.loads(response)
    foursquareUrl = resultsJsonTest['response']['venue']['canonicalUrl']

    

    
    data = {'id':  id,         
            'name' : name,
            'address' : address,
            'lat' : lat ,
            'lng' : lng,
            'categoryName' : cName,
            'foursquareUrl' : foursquareUrl,
            'Tipcount' : Tipcount,
            'Checkins' : Checkins,
            'Users': Users,
            }
  

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)


# Blank Python
import simplejson
import scraperwiki
import requests

url = "https://api.foursquare.com/v2/venues/search?intent=browse&sw=51.55017800,5.06263733&ne=51.56085115,5.08049011&oauth_token=HQFRZSOGA4N5C5CYIIZPEGMHX1OGENDTYKWL3DJZMH2GUNYN&v=20120920&categoryId=4d4b7105d754a06376d81259&limit=100"

resultsJson = simplejson.loads(scraperwiki.scrape(url))

results = resultsJson['response']['venues']


for item in results:
    
    cName =  None
    address = None
    address = None
    lat = None
    lng = None
    forsquareUrl = None
    Tipcount = None
    Checkins = None
    Users = None

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

    if item['stats'].has_key('tipCount'):
        Tipcount = item['stats']['tipCount']

    if item['stats'].has_key('checkinsCount'):
        Checkins = item['stats']['checkinsCount']

    if item['stats'].has_key('usersCount'):
        Users = item['stats']['usersCount']
    

    test = "https://api.foursquare.com/v2/venues/"+id+"?oauth_token=HQFRZSOGA4N5C5CYIIZPEGMHX1OGENDTYKWL3DJZMH2GUNYN&v=20120920"  
    response = requests.get(test, verify = False).text
    resultsJsonTest = simplejson.loads(response)
    foursquareUrl = resultsJsonTest['response']['venue']['canonicalUrl']

    

    
    data = {'id':  id,         
            'name' : name,
            'address' : address,
            'lat' : lat ,
            'lng' : lng,
            'categoryName' : cName,
            'foursquareUrl' : foursquareUrl,
            'Tipcount' : Tipcount,
            'Checkins' : Checkins,
            'Users': Users,
            }
  

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)


