
# Blank Python
import simplejson
import scraperwiki
import requests

url = "https://api.foursquare.com/v2/venues/search?ll=52.5002,13.3988&oauth_token=ZDPGKZERHSMZDIMLAKQFYLGHHNWJFPFKGXVSNUJSEFV5FFPO&v=20120808&radius=800"

resultsJson = simplejson.loads(scraperwiki.scrape(url))

results = resultsJson['response']['venues']


for item in results:
    
    cName =  None
    address = None
    address = None
    lat = None
    lng = None
    forsquareUrl = None

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

    test = "https://api.foursquare.com/v2/venues/"+id+"?oauth_token=ZDPGKZERHSMZDIMLAKQFYLGHHNWJFPFKGXVSNUJSEFV5FFPO&v=20120812"  
    response = requests.get(test, verify = False).text
    resultsJsonTest = simplejson.loads(response)
    foursquareUrl = resultsJsonTest['response']['venue']['canonicalUrl']
    
    
    data = {'id':  id,         
            'name' : name,
            'address' : address,
            'lat' : lat ,
            'lng' : lng,
            'categoryName' : cName,
            'foursquareUrl' : foursquareUrl
            }

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
