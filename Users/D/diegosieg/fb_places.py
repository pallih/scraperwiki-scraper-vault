# Blank Python
import simplejson
import scraperwiki
import requests

url = "https://graph.facebook.com/search?q=*&type=place&center=-23.564125,-46.702816&distance=40000&access_token=AAACEdEose0cBAAGgmIkGV8U0znfmkKHfIZBfwaowHyNi1DRPwE2d36ZAWQoZBoJA3duFf9swsEWGxtPA1Vo9CwafxFzYzzZAWBYaPjkdRgZDZD&limit=500"
#trocar token, coordenadas e distancia menor que 50000

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
    
    
    
    data = {'id':  id,         
            'name' : cName,
            'street' : street,
            'latitude' : lat ,
            'longitude' : lng,
            'zip': postcode,
            'category' : category
            }
  

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

