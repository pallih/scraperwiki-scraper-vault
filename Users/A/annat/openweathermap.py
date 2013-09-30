import scraperwiki
import simplejson
import urllib
import urllib2


#Stations around a point

url = "http://openweathermap.org/data/2.0/find/station?lat=52.52&lon=13.40&cnt=20"
resultsJson = simplejson.loads(urllib.urlopen(url).read())
print len(resultsJson['list'])
for result in resultsJson['list']:
    name = result['name']
    id = result['id']
    lat = result['coord']['lat']
    lng = result['coord']['lon']
    rain1h = None
    rain24h = None
    rainToday = None
    pressure = None
    if result.has_key('rain'):
        if result['rain'].has_key('1h'):
            rain1h = result['rain']['1h']
        if  result['rain'].has_key('24h'):
            rain24h = result['rain']['24h']
        if  result['rain'].has_key('today'):
            rainToday = result['rain']['today']
    windSpeed = result['wind']['speed']
    windDeg = result['wind']['deg']
    temp = result['main']['temp']
    if result['main'].has_key('pressure'):
        pressure = result['main']['pressure']

    url = "http://openweathermap.org/station/" + str(id)
    print url
    data = {'id' : id,
            'name' : name,
            'lat' : lat,
            'long' : lng,
            'rain1h' : rain1h,
            'rain24h' : rain24h,
            'rainToday' : rainToday,
            'windSpeed': windSpeed,
            'windDeg' : windDeg,
            'temp' : temp,
            'pressure' : pressure,
            'url' : url}  

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
import scraperwiki
import simplejson
import urllib
import urllib2


#Stations around a point

url = "http://openweathermap.org/data/2.0/find/station?lat=52.52&lon=13.40&cnt=20"
resultsJson = simplejson.loads(urllib.urlopen(url).read())
print len(resultsJson['list'])
for result in resultsJson['list']:
    name = result['name']
    id = result['id']
    lat = result['coord']['lat']
    lng = result['coord']['lon']
    rain1h = None
    rain24h = None
    rainToday = None
    pressure = None
    if result.has_key('rain'):
        if result['rain'].has_key('1h'):
            rain1h = result['rain']['1h']
        if  result['rain'].has_key('24h'):
            rain24h = result['rain']['24h']
        if  result['rain'].has_key('today'):
            rainToday = result['rain']['today']
    windSpeed = result['wind']['speed']
    windDeg = result['wind']['deg']
    temp = result['main']['temp']
    if result['main'].has_key('pressure'):
        pressure = result['main']['pressure']

    url = "http://openweathermap.org/station/" + str(id)
    print url
    data = {'id' : id,
            'name' : name,
            'lat' : lat,
            'long' : lng,
            'rain1h' : rain1h,
            'rain24h' : rain24h,
            'rainToday' : rainToday,
            'windSpeed': windSpeed,
            'windDeg' : windDeg,
            'temp' : temp,
            'pressure' : pressure,
            'url' : url}  

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
