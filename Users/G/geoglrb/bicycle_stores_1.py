import scraperwiki

# Blank Python

# Access website
#html = scraperwiki.scrape("http://www.yelp.com/search?find_desc=bike&find_loc=Seattle%2C+WA&ns=1#cflt=bikes&find_desc=&rpp=40")

html = scraperwiki.scrape("http://www.yelp.com/search?find_desc=bike&find_loc=Seattle%2C+WA&ns=1#cflt=bikes")

# print html
# previous website - "http://www.yelp.com/search?find_desc=bicycle+shop&find_loc=Seattle%2C+WA&ns=1#start=10"
# this one is aproblem because it highlights the search phrases, thus messing up the html and making it difficult to extract the store names. 

# Search through HTML

import lxml.html
root = lxml.html.fromstring(html)

# Set up geocoding

# Define geocode function

def gc():
    address = data.values()[4:6]
    new =  address[1] + " " + address[0]
    #print new
    #print type(new)
    place,(lat, lng) = us.geocode(new)

    coordinates = "%s: %.5f, %.5f" % (place, lat, lng)
    split = coordinates.split(":")

    lat_long = split[1]
    return lat_long

from geopy import geocoders
us = geocoders.GeocoderDotUS()

print html

for elt in root.cssselect("div.businessresult"):
    
    data = {
        'rating' : float(elt.getchildren()[1].getchildren()[0].getchildren()[0].attrib['title'][:3]),
        'number_of_reviews' : int(elt.getchildren()[1].getchildren()[0].getnext().text[:3]),
        'street' : elt.getchildren()[1].getchildren()[0].getnext().getnext().getchildren()[0].text[6:],
        'phone' : elt.getchildren()[1].getchildren()[0].getnext().getnext().getchildren()[0].getnext().text[6:20],
        'city_st_zip' : elt.getchildren()[1].getchildren()[0].getnext().getnext().getchildren()[0].getchildren()[0].tail[:17],
        'name' : elt.getchildren()[0].getchildren()[0].getchildren()[1].getchildren()[0].getchildren()[0].text[3:].replace("\t",""),
        #'latitude' : gc()[0],
        #'longitude' : gc()[1]
                 
    }
    #print data.values()
    
    #for x in range(10):
        #address = data.values()[4:]
        #new =  address[1] + " " + address[0]
        #print new
        #print type(new)
        #place,(lat, lng) = us.geocode(new)

        #coordinates = "%s: %.5f, %.5f" % (place, lat, lng)
        #split = coordinates.split(":")

        #lat_long = split[1]
        #data['latitude'] = lat_long[0]
        #data['longitude'] = lat_long[1]

    scraperwiki.sqlite.save(unique_keys=['name'], data=data)     



#print data




#for elt in root.cssselect("div.rating"):
    
    #data = {
        #'rating' : float(elt.getchildren()[0].attrib['title'][:3]),
        #'number_of_reviews' : int(elt.getnext().text[:3]),
        #'address' : elt.getnext().getnext().text
    #}
    #print data.values()
    #scraperwiki.sqlite.save(unique_keys=['rating'], data=data) 

#store_list = []
#for store in root.cssselect("head"):
    #name = store.getnext()*36






    

import scraperwiki

# Blank Python

# Access website
#html = scraperwiki.scrape("http://www.yelp.com/search?find_desc=bike&find_loc=Seattle%2C+WA&ns=1#cflt=bikes&find_desc=&rpp=40")

html = scraperwiki.scrape("http://www.yelp.com/search?find_desc=bike&find_loc=Seattle%2C+WA&ns=1#cflt=bikes")

# print html
# previous website - "http://www.yelp.com/search?find_desc=bicycle+shop&find_loc=Seattle%2C+WA&ns=1#start=10"
# this one is aproblem because it highlights the search phrases, thus messing up the html and making it difficult to extract the store names. 

# Search through HTML

import lxml.html
root = lxml.html.fromstring(html)

# Set up geocoding

# Define geocode function

def gc():
    address = data.values()[4:6]
    new =  address[1] + " " + address[0]
    #print new
    #print type(new)
    place,(lat, lng) = us.geocode(new)

    coordinates = "%s: %.5f, %.5f" % (place, lat, lng)
    split = coordinates.split(":")

    lat_long = split[1]
    return lat_long

from geopy import geocoders
us = geocoders.GeocoderDotUS()

print html

for elt in root.cssselect("div.businessresult"):
    
    data = {
        'rating' : float(elt.getchildren()[1].getchildren()[0].getchildren()[0].attrib['title'][:3]),
        'number_of_reviews' : int(elt.getchildren()[1].getchildren()[0].getnext().text[:3]),
        'street' : elt.getchildren()[1].getchildren()[0].getnext().getnext().getchildren()[0].text[6:],
        'phone' : elt.getchildren()[1].getchildren()[0].getnext().getnext().getchildren()[0].getnext().text[6:20],
        'city_st_zip' : elt.getchildren()[1].getchildren()[0].getnext().getnext().getchildren()[0].getchildren()[0].tail[:17],
        'name' : elt.getchildren()[0].getchildren()[0].getchildren()[1].getchildren()[0].getchildren()[0].text[3:].replace("\t",""),
        #'latitude' : gc()[0],
        #'longitude' : gc()[1]
                 
    }
    #print data.values()
    
    #for x in range(10):
        #address = data.values()[4:]
        #new =  address[1] + " " + address[0]
        #print new
        #print type(new)
        #place,(lat, lng) = us.geocode(new)

        #coordinates = "%s: %.5f, %.5f" % (place, lat, lng)
        #split = coordinates.split(":")

        #lat_long = split[1]
        #data['latitude'] = lat_long[0]
        #data['longitude'] = lat_long[1]

    scraperwiki.sqlite.save(unique_keys=['name'], data=data)     



#print data




#for elt in root.cssselect("div.rating"):
    
    #data = {
        #'rating' : float(elt.getchildren()[0].attrib['title'][:3]),
        #'number_of_reviews' : int(elt.getnext().text[:3]),
        #'address' : elt.getnext().getnext().text
    #}
    #print data.values()
    #scraperwiki.sqlite.save(unique_keys=['rating'], data=data) 

#store_list = []
#for store in root.cssselect("head"):
    #name = store.getnext()*36






    

