import scraperwiki, json, re, sys
from urllib import urlopen

#scraperwiki.sqlite.execute("DELETE FROM swdata WHERE link_id NOT IN (SELECT MIN(link_id) FROM swdata GROUP BY atm_id)")


#sys.exit()

scraperwiki.sqlite.attach('uk_postcodes_from_codepoint', 'postcodes')

unicode_re = re.compile(r'\\x([A-Fa-f0-9]{2})')

default_distance = 10000

geocoder = "http://clients.multimap.com/API/geocode/1.2/linkapi?output=json&callback=MMGeocoder.prototype._GeneralJSONCallback&" 
geocoder += "locale=en-us&qs=%s&countryCode=GB&deliveryID=2011051916223016758&identifier=0"

atm_url = "http://clients.multimap.com/API/search/1.2/linkapi?"
atm_url += "output=json&callback=MMSearchRequester.prototype._GeneralJSONCallback&deliveryID=2011051916223016758&identifier=1&dataSource=mm.clients.linkapi&" 
atm_url += "orderByFields=distance&orderByOrder=asc&locale=en-us&"
atm_url += "count=100&lat=%(lat)s&lon=%(lon)s&maxDistance=15000"


def get_atms(postcode):
    response = urlopen(geocoder % postcode).read()
    data_str = response[response.find("{"):].rstrip().rstrip(')')

    data = json.loads(data_str)

    if not len(data["result_set"]):
        return []

    point = data["result_set"][0]["point"]
    response = urlopen(atm_url % point).read()

    #The response is a small javascript, there's one method call where a parameter is quite usable as json, strip out the rest.
    response = response[response.find('['):response.rfind(']')+1]

    # The feed contained invalid escape characters, using hexadecimal \xNN notation instead of \uNNNN
    response = unicode_re.sub(r'\\u00\1', response)
    
    return json.loads(response)

def tidy_data(atm):
    atm["link_id"] = atm["id"]
    atm["lat"] = atm["point"]["lat"]
    atm["lon"] = atm["point"]["lon"]
    atm["postcode"] = atm["pc"]

    del atm["id"]
    del atm["point"]
    del atm["pc"]        
    del atm["distance"] #distance from the searched postcode, not worth keeping

    return atm

#Prepare to scrape
print("Select postcodes")
postcodes = scraperwiki.sqlite.select('distinct substr(Postcode, -3, -10) as outcode from postcodes.swdata')
print("Get outcode")
outcode = scraperwiki.sqlite.get_var('outcode', False)



    for atm in get_atms(outcode):
        scraperwiki.sqlite.save(["atm_id"], tidy_data(atm))

scraperwiki.sqlite.save_var('outcode', False)import scraperwiki, json, re, sys
from urllib import urlopen

#scraperwiki.sqlite.execute("DELETE FROM swdata WHERE link_id NOT IN (SELECT MIN(link_id) FROM swdata GROUP BY atm_id)")


#sys.exit()

scraperwiki.sqlite.attach('uk_postcodes_from_codepoint', 'postcodes')

unicode_re = re.compile(r'\\x([A-Fa-f0-9]{2})')

default_distance = 10000

geocoder = "http://clients.multimap.com/API/geocode/1.2/linkapi?output=json&callback=MMGeocoder.prototype._GeneralJSONCallback&" 
geocoder += "locale=en-us&qs=%s&countryCode=GB&deliveryID=2011051916223016758&identifier=0"

atm_url = "http://clients.multimap.com/API/search/1.2/linkapi?"
atm_url += "output=json&callback=MMSearchRequester.prototype._GeneralJSONCallback&deliveryID=2011051916223016758&identifier=1&dataSource=mm.clients.linkapi&" 
atm_url += "orderByFields=distance&orderByOrder=asc&locale=en-us&"
atm_url += "count=100&lat=%(lat)s&lon=%(lon)s&maxDistance=15000"


def get_atms(postcode):
    response = urlopen(geocoder % postcode).read()
    data_str = response[response.find("{"):].rstrip().rstrip(')')

    data = json.loads(data_str)

    if not len(data["result_set"]):
        return []

    point = data["result_set"][0]["point"]
    response = urlopen(atm_url % point).read()

    #The response is a small javascript, there's one method call where a parameter is quite usable as json, strip out the rest.
    response = response[response.find('['):response.rfind(']')+1]

    # The feed contained invalid escape characters, using hexadecimal \xNN notation instead of \uNNNN
    response = unicode_re.sub(r'\\u00\1', response)
    
    return json.loads(response)

def tidy_data(atm):
    atm["link_id"] = atm["id"]
    atm["lat"] = atm["point"]["lat"]
    atm["lon"] = atm["point"]["lon"]
    atm["postcode"] = atm["pc"]

    del atm["id"]
    del atm["point"]
    del atm["pc"]        
    del atm["distance"] #distance from the searched postcode, not worth keeping

    return atm

#Prepare to scrape
print("Select postcodes")
postcodes = scraperwiki.sqlite.select('distinct substr(Postcode, -3, -10) as outcode from postcodes.swdata')
print("Get outcode")
outcode = scraperwiki.sqlite.get_var('outcode', False)



    for atm in get_atms(outcode):
        scraperwiki.sqlite.save(["atm_id"], tidy_data(atm))

scraperwiki.sqlite.save_var('outcode', False)