import scraperwiki
import mechanize
import re
import lxml.html
import string
import json
import time
from datetime import date
import urllib
import urllib2
import simplejson
geocode_disabled = False

property_content_base_url = "http://ikman.lk/"
property_url = "http://ikman.lk/property-in-sri-lanka?page="

property_length=list(range(1,2))

print "IKM base Url " + property_url

idx = 0
for i in property_length:
    current_page_url = property_url + (str(i)) 
    print current_page_url
    html = scraperwiki.scrape(current_page_url)
    print html

    root = lxml.html.fromstring(html)
    
    for table in root.cssselect("li.item"):
        idx += 1
        row=[]

        adHeader = table.cssselect('h2')[0].text_content()
        print adHeader
        
        print table.attrib

        data_str = table.attrib['data-item']
        data_object = json.loads(data_str)
            

        if not (data_object['show_image'] is None):    
            thumbnail_url = "http://ctim.saltsidecdn.net/ikman/thumb/" + data_object['show_image'] + ".jpg"
            print thumbnail_url
        else:
            thumbnail_url = ''
            print "no thumbnail url found"

        location = data_object['location'] + ', Sri Lanka'
        print location

        #server side geocoding
        if(geocode_disabled == False):
            print 'sleeping 1 second for geocoding...'
            time.sleep(1)
            #geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote_plus(location)+'&sensor=false&output=json'
            geocode_url = 'http://georexon.appspot.com/geojson?a=' +urllib.quote(location.encode('utf-8'))
            print geocode_url
            georeq = urllib2.Request(geocode_url)
            geo_response = urllib2.urlopen(georeq)
            geocode = simplejson.loads(geo_response.read())
            print geocode
    
            if geocode['status'] == 'OVER_QUERY_LIMIT':
                print 'sleeping to maintain query limit'
                time.sleep(1)
                print 'reattempting after wait'
                georeq = urllib2.Request(geocode_url)
                geo_response = urllib2.urlopen(georeq)
                geocode = simplejson.loads(geo_response.read())
    
            if geocode['status'] == 'OVER_QUERY_LIMIT':
                geocode_disabled = True
                print 'geocoding disabled'
    
            if geocode['status'] != 'ZERO_RESULTS' and geocode['status'] != 'OVER_QUERY_LIMIT':
                data_lat = geocode['results'][0]['geometry']['location']['lat']
                data_lng = geocode['results'][0]['geometry']['location']['lng']
                print data_lat 
                print data_lng
            #server side geocoding ends

        priceInLKR = data_object['show_attr']['value'][4:].replace(",","");
        
        content_url = property_content_base_url + table.cssselect('a')[0].attrib['href'][0:]
        print content_url

        if("for-sale" in content_url):
            ad_type = "SALE"
        elif ('for-rent' in content_url):
            ad_type = "RENT"

    
        added_date = str(date.fromtimestamp(data_object['created_at']));
        print added_date;

        #submit to api request start
        submit_url = "http://3gx3.localtunnel.com/add_listing"
        submit_params = {
            "listing_type" :"GL_PROPERTYX",
            "header":adHeader.encode('utf-8'),
            "location": location, 
            "content_url":content_url,
            "source":"IKM", 
            "listing_sub_type":ad_type,
            "thumbnail_url":thumbnail_url,
            "price_in_lkr":priceInLKR, 
            "added_date": added_date
        }

        print submit_params
        submit_response = urllib2.urlopen(urllib2.Request(submit_url, urllib.urlencode(submit_params)))
        
        print submit_response
        
        #submit to api request end


print "completed scrapping"
