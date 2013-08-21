#Facebook Places 1

# Blank Python
import simplejson
import scraperwiki
import requests

url = "https://graph.facebook.com/search?q=*&type=place&center=53.00,-2.133&distance=50000&access_token=AAACEdEose0cBAOZCEraT9sZBWzDbao4kvWlKcZA26Ujubl67Mr9SLcbZAXf0jdceKXooc8dHZBfplx4Rm0gjGmk436Y5bMlgedIn2MrgF2QZDZD&limit=500"

resultsJson = simplejson.loads(scraperwiki.scrape(url))

results = resultsJson['data']


for item in results:
    
    street =  None
    cName = None
    latitude = None
    longitude = None
    postcode = None
    category = None
    

    category = item['category']
    #for item2 in category:
        
        #if item2.has_key('name'):
            #cName = category[1]['name']
                  
    if item.has_key('id'):
        id =  item['id']
        
    if item.has_key('name'):
        cName =  item['name']    

    if item['location'].has_key('street'):
        street = item['location']['street']

    if item['location'].has_key('latitude'):
        lat = item['location']['latitude']

    if item['location'].has_key('longitude'):
        lng = item['location']['longitude']
    
    if item['location'].has_key('zip'):
        postcode =item['location']['zip']
    

    #test = "https://api.foursquare.com/v2/venues/"+id+"?oauth_token=SHEATYYM4ZPQRNAJYLNM44BFHCVEUKB25IXBT1BO33OSJJ33"  
    #response = requests.get(test, verify = False).text
    #resultsJsonTest = simplejson.loads(response)
    #foursquareUrl = resultsJsonTest['data']['canonicalUrl']
    
    
    data = {'id':  id,         
            'name' : cName,
            'street' : street,
            'latitude' : lat ,
            'longitude' : lng,
            'zip': postcode,
            'category' : category
            }
  

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

