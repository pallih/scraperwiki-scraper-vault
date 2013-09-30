#import scraperwiki
#import requests
#import lxml.html
#import urllib

#def geocode(address):
#    try:
#       r = requests.get("http://open.mapquestapi.com/nominatim/v1/search.php?format=json&q=" + urllib.quote_plus(address.encode(utf-8)))
#      lat = r.json()[0]["lat"]
#     lon = r.json()[0]["lon"]
#    return [lat, lon]
#except:
#   return None


#def get_site(url):
#   r = requests.get(url, verify=False)
#  return lxml.html.fromstring(r.text)
## make a function of a returning request, in this case to make the url into a dom and text


## Get the data
#for page in range(1,10):
#   print "Scraping page %d" % page
#  dom = get_site("https://airbnb.se/s/Stockholm--Sweden?page=%d" % page)
    #r= requests.get("https://airbnb.se/s/Stockholm--Sweden?page=%d" % page, verify=False)
    ## you need verify=False because it's a https site
    ## print.r to check if any data is included in your request. if response is 200 it's ok
    ## if you do r.text you will actually see all of the html
    
    ## convert the HTML into a dom file
    #dom = lxml.html.fromstring(r.text)
    #dom.cssselect(".name")
    
    # for element in dom.cssselect(".name"):
    #    print element.text_content()
    
    # for element in dom.cssselect(".price"):
    #    print element.text_content()
    
    ## or
    # names = dom.cssselect(".name")
    # for name in names:
    #    print name.text_content()
    
#   results = dom.cssselect(".search_result")
#    for result in results:
#     apartment_listing = {
#          "id": result.get("data-hosting-id"),
#           "name": result.cssselect(".name")[0].text_content().strip(),
#            "price": result.cssselect(".price_data")[0].text_content().strip()
#       }
    
        #url = result.cssselect(".name")[0].get("href")
        #r   = requests.get("https://www.airbnb.se" + url, verify=False)
        #dom = lxml.html.fromstring(r.text)
## because we made a def up to change the dom, we can use:
        #dom = get_site("https://www.airbnb.se" + url)
        #address = dom.cssselect("#display_address")[0].text_content().strip()
        #coordinates = geocode(address)
        #print r
    
    ##.strip() is to clean out all the /n or spaces in strings
    ## price.data is more correct and narrow, it takes out all the kr or € signs
    
        #if coordinates is not None:
            #apartment_listing["lat"] = coordinates[0]
            #apartment_listing["lon"] = coordinates[1]
            #apartment_listing["address"] = address
            #scraperwiki.sqlite.save(["id"], apartment_listing)
            
        #print apartment_listing
    
        #print result.cssselect(".name")[0].text_content()
        #print result.cssselect(".price")[0].text_content()

import scraperwiki
import requests
import lxml.html
import urllib

def geocode(address):
    try:
        r = requests.get('http://open.mapquestapi.com/nominatim/v1/search.php?format=json&q=' + urllib.quote_plus(address.encode('utf-8')))
        lat = r.json()[0]["lat"]
        lon = r.json()[0]["lon"]
        return [lat, lon]
    except:
        return None

def get_site(url):
    r = requests.get(url, verify=False)
    return lxml.html.fromstring(r.text)

for page in range(1,10):
    print "Scraping page %d" % page
    dom = get_site("https://www.airbnb.se/s/Stockholm--Sweden?page=%d" % page)
    
    results = dom.cssselect('.search_result')
    for result in results:
        apartment_listing = {
          "id": result.get('data-hosting-id'),
          "name": result.cssselect('.name')[0].text_content(),
          "price": result.cssselect('.price_data')[0].text_content().strip()
        }
    
        url = result.cssselect('.name')[0].get('href')
        dom = get_site("https://www.airbnb.se" + url)
        address = dom.cssselect('#display_address')[0].text_content().strip()
        coordinates = geocode(address)
        print coordinates
    
        if coordinates is not None:
            apartment_listing["lat"] = coordinates[0]
            apartment_listing["lon"] = coordinates[1]
            apartment_listing["address"] = address
            scraperwiki.sqlite.save(['id'], apartment_listing)
    
    
    
    








#import scraperwiki
#import requests
#import lxml.html
#import urllib

#def geocode(address):
#    try:
#       r = requests.get("http://open.mapquestapi.com/nominatim/v1/search.php?format=json&q=" + urllib.quote_plus(address.encode(utf-8)))
#      lat = r.json()[0]["lat"]
#     lon = r.json()[0]["lon"]
#    return [lat, lon]
#except:
#   return None


#def get_site(url):
#   r = requests.get(url, verify=False)
#  return lxml.html.fromstring(r.text)
## make a function of a returning request, in this case to make the url into a dom and text


## Get the data
#for page in range(1,10):
#   print "Scraping page %d" % page
#  dom = get_site("https://airbnb.se/s/Stockholm--Sweden?page=%d" % page)
    #r= requests.get("https://airbnb.se/s/Stockholm--Sweden?page=%d" % page, verify=False)
    ## you need verify=False because it's a https site
    ## print.r to check if any data is included in your request. if response is 200 it's ok
    ## if you do r.text you will actually see all of the html
    
    ## convert the HTML into a dom file
    #dom = lxml.html.fromstring(r.text)
    #dom.cssselect(".name")
    
    # for element in dom.cssselect(".name"):
    #    print element.text_content()
    
    # for element in dom.cssselect(".price"):
    #    print element.text_content()
    
    ## or
    # names = dom.cssselect(".name")
    # for name in names:
    #    print name.text_content()
    
#   results = dom.cssselect(".search_result")
#    for result in results:
#     apartment_listing = {
#          "id": result.get("data-hosting-id"),
#           "name": result.cssselect(".name")[0].text_content().strip(),
#            "price": result.cssselect(".price_data")[0].text_content().strip()
#       }
    
        #url = result.cssselect(".name")[0].get("href")
        #r   = requests.get("https://www.airbnb.se" + url, verify=False)
        #dom = lxml.html.fromstring(r.text)
## because we made a def up to change the dom, we can use:
        #dom = get_site("https://www.airbnb.se" + url)
        #address = dom.cssselect("#display_address")[0].text_content().strip()
        #coordinates = geocode(address)
        #print r
    
    ##.strip() is to clean out all the /n or spaces in strings
    ## price.data is more correct and narrow, it takes out all the kr or € signs
    
        #if coordinates is not None:
            #apartment_listing["lat"] = coordinates[0]
            #apartment_listing["lon"] = coordinates[1]
            #apartment_listing["address"] = address
            #scraperwiki.sqlite.save(["id"], apartment_listing)
            
        #print apartment_listing
    
        #print result.cssselect(".name")[0].text_content()
        #print result.cssselect(".price")[0].text_content()

import scraperwiki
import requests
import lxml.html
import urllib

def geocode(address):
    try:
        r = requests.get('http://open.mapquestapi.com/nominatim/v1/search.php?format=json&q=' + urllib.quote_plus(address.encode('utf-8')))
        lat = r.json()[0]["lat"]
        lon = r.json()[0]["lon"]
        return [lat, lon]
    except:
        return None

def get_site(url):
    r = requests.get(url, verify=False)
    return lxml.html.fromstring(r.text)

for page in range(1,10):
    print "Scraping page %d" % page
    dom = get_site("https://www.airbnb.se/s/Stockholm--Sweden?page=%d" % page)
    
    results = dom.cssselect('.search_result')
    for result in results:
        apartment_listing = {
          "id": result.get('data-hosting-id'),
          "name": result.cssselect('.name')[0].text_content(),
          "price": result.cssselect('.price_data')[0].text_content().strip()
        }
    
        url = result.cssselect('.name')[0].get('href')
        dom = get_site("https://www.airbnb.se" + url)
        address = dom.cssselect('#display_address')[0].text_content().strip()
        coordinates = geocode(address)
        print coordinates
    
        if coordinates is not None:
            apartment_listing["lat"] = coordinates[0]
            apartment_listing["lon"] = coordinates[1]
            apartment_listing["address"] = address
            scraperwiki.sqlite.save(['id'], apartment_listing)
    
    
    
    








