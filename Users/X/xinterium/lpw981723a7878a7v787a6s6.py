import scraperwiki
import mechanize
import re
import lxml.html
import string

import time
import urllib
import urllib2
import simplejson
geocode_disabled = False

property_content_base_url = "http://www.lankapropertyweb.com"
property_url = "http://www.lankapropertyweb.com/index.php?page="

property_length=list(range(1,100))

print "Property base Url " + property_url

idx = 0
for i in property_length:
    current_page_url = property_url + (str(i)) 
    print current_page_url
    html = scraperwiki.scrape(current_page_url)
    print html

    root = lxml.html.fromstring(html)

    
    for table in root.cssselect("#pty_box"):
        idx += 1
        row=[]
        adHeader = table.cssselect("#pty_heading_gold")[0].text_content()
        print adHeader

        location = table.cssselect("#pty_location")[0].text_content()[10:].strip()+", Sri Lanka" ##adding the country name to help the geocoder
        print location
    
        prices = table.cssselect(".pty_pr")

        if not prices:
            priceinLKR = ''
        else :
            priceInLKR = float(prices[0].text_content().replace(',','')) * 1000000
        print priceInLKR

        #server side geocoding
        if(geocode_disabled == False):
            print 'sleeping 1 second for geocoding...'
            time.sleep(1)
            #geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote(location.encode('utf-8'))+'&sensor=false&output=json'
            geocode_url = 'http://georexon.appspot.com/geojson?a=' +urllib.quote(location.encode('utf-8'))
            print geocode_url
            georeq = urllib2.Request(geocode_url)
            geo_response = urllib2.urlopen(georeq)
            geocode = simplejson.loads(geo_response.read())
            print geocode
    
            if geocode['status'] == 'OVER_QUERY_LIMIT':
                print 'sleeping to maintain query limit'
                time.sleep(2)
                print 'reattempting after wait'
                georeq = urllib2.Request(geocode_url)
                geo_response = urllib2.urlopen(georeq)
                geocode = simplejson.loads(geo_response.read())

            if geocode['status'] == 'ZERO_RESULTS':
                continue 

            if geocode['status'] == 'INVALID_REQUEST':
                continue 
    
            if geocode['status'] == 'OVER_QUERY_LIMIT':
                geocode_disabled = True
                print 'geocoding disabled'
    
            if geocode['status'] != 'ZERO_RESULTS' and geocode['status'] != 'OVER_QUERY_LIMIT':
                data_lat = geocode['results'][0]['geometry']['location']['lat']
                data_lng = geocode['results'][0]['geometry']['location']['lng']
                print data_lat 
                print data_lng
            #server side geocoding ends

        if(len(table.cssselect(".ad_pr")) > 0):    
            price = table.cssselect(".ad_pr")[0].text_content()
            print price #todo extract price

        content_url = property_content_base_url + table.cssselect("a")[0].attrib['href']
        print content_url

        thumbnail_url = property_content_base_url + table.cssselect("img")[0].attrib['src'][2:]
        print thumbnail_url


        if (not geocode_disabled):
            scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"LPW","thumbnail_url":thumbnail_url, "lat":data_lat, "lon": data_lng, "price_in_lkr": priceInLKR })
        else:
            scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"LPW","thumbnail_url":thumbnail_url, "price_in_lkr": priceInLKR})
    
        #submit to api request start
        submit_url = "http://geolanka-api-beta.appspot.com/add_listing"
        submit_params = {
            "listing_type" :"GL_PROPERTY",
            "header":adHeader.encode('utf-8'),
            "location": location, 
            "content_url":content_url,
            "source":"LPW", 
            "listing_sub_type":"",
            "thumbnail_url":thumbnail_url, 
            "lat":data_lat, 
            "lon": data_lng, 
            "price_in_lkr":priceInLKR
        }

        print submit_params
        submit_response = urllib2.urlopen(urllib2.Request(submit_url, urllib.urlencode(submit_params)))
        
        print submit_response
        
        #submit to api request end

print "completed scrapping"
