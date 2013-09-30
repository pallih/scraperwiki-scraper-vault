# Blank Python
import simplejson
import scraperwiki
import requests

url = "https://api.foursquare.com/v2/venues/search?ll=53.02,-2.17&client_id=I0TV2YQ2JCGC0NX0QF0ECZI15SG1CFQKHIW3G5RTC2DLRJJU&client_secret=0IK5ROSZJKKHUPEPA2FK0RVA4FQZRXBBL3ISNSCGKYCVQ0UV&v=20121221"

resultsJson = simplejson.loads(scraperwiki.scrape(url))

results = resultsJson['response']['venues']


for item in results:
    
    cName =  None
    address = None
    address = None
    lat = None
    lng = None
    forsquareUrl = None
    checkins = None
    usersCount = None
    tipCount = None

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
        checkins = item['stats']['checkinsCount']

    if item['stats'].has_key('usersCount'):
        usersCount = item['stats']['usersCount']

    if item['stats'].has_key('tipCount'):
        tipCount = item['stats']['tipCount']

    test = "https://api.foursquare.com/v2/venues/"+id+"?oauth_token=SHEATYYM4ZPQRNAJYLNM44BFHCVEUKB25IXBT1BO33OSJJ33"  
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
            'checkinsCount' : checkins,
            'usersCount' : usersCount,
            'tipCount' : tipCount
            }
  

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

# Blank Python
import simplejson
import scraperwiki
import requests

url = "https://api.foursquare.com/v2/venues/search?ll=53.02,-2.17&client_id=I0TV2YQ2JCGC0NX0QF0ECZI15SG1CFQKHIW3G5RTC2DLRJJU&client_secret=0IK5ROSZJKKHUPEPA2FK0RVA4FQZRXBBL3ISNSCGKYCVQ0UV&v=20121221"

resultsJson = simplejson.loads(scraperwiki.scrape(url))

results = resultsJson['response']['venues']


for item in results:
    
    cName =  None
    address = None
    address = None
    lat = None
    lng = None
    forsquareUrl = None
    checkins = None
    usersCount = None
    tipCount = None

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
        checkins = item['stats']['checkinsCount']

    if item['stats'].has_key('usersCount'):
        usersCount = item['stats']['usersCount']

    if item['stats'].has_key('tipCount'):
        tipCount = item['stats']['tipCount']

    test = "https://api.foursquare.com/v2/venues/"+id+"?oauth_token=SHEATYYM4ZPQRNAJYLNM44BFHCVEUKB25IXBT1BO33OSJJ33"  
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
            'checkinsCount' : checkins,
            'usersCount' : usersCount,
            'tipCount' : tipCount
            }
  

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

