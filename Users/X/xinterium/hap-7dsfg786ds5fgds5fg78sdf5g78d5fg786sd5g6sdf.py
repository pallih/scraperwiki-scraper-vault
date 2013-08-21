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

property_content_base_url = "http://hitad.lk/"
property_url = "http://hitad.lk/property/"

property_length=list(range(1,100))

print "HAP base Url " + property_url

idx = 0
for i in property_length:
    current_page_url = property_url + (str(i * 25)) 
    print current_page_url
    html = scraperwiki.scrape(current_page_url)
    print html

    root = lxml.html.fromstring(html)

    
    for table in root.cssselect(".af_box"):
        idx += 1
        row=[]

        ad_type = "FOR_SALE"
        
        adHeader = table.cssselect('.af_heading')[0].text_content()
        print adHeader

        #match for any rent
        rents = re.search("rent",adHeader.lower())
        print rents
        if rents is not None:
            print "RENT DISCOVERED"
            ad_type = "RENT"
        
        thumbnail_url = table.cssselect('.af_image')[0].text_content()
        print thumbnail_url 

        street = table.cssselect('div.af_brand_text span')[2].text_content()
        if street != 'None':
            street = street + ", " + table.cssselect('div.af_brand_text span')[1].text_content()
        else:
            street = table.cssselect('div.af_brand_text span')[1].text_content()
        location = street

        location = location + ", Sri Lanka"
        print location
        
        
        #server side geocoding
        if(geocode_disabled == False):
            print 'sleeping 1 second for geocoding...'
            time.sleep(1)
            geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote_plus(location)+'&sensor=false&output=json'
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
    
            if geocode['status'] == 'OVER_QUERY_LIMIT':
                geocode_disabled = True
                print 'geocoding disabled'
    
            if geocode['status'] != 'ZERO_RESULTS' and geocode['status'] != 'OVER_QUERY_LIMIT':
                data_lat = geocode['results'][0]['geometry']['location']['lat']
                data_lng = geocode['results'][0]['geometry']['location']['lng']
                print data_lat 
                print data_lng
            #server side geocoding ends


        content_url = table.cssselect('.af_more')[0].attrib['href']
        print content_url

        thumbnail_url = table.cssselect('img')[0].attrib['src']
        if 'default' in thumbnail_url:
            thumbnail_url = ""
        print thumbnail_url

        if (not geocode_disabled):    
            scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"HAP", "type":ad_type, "thumbnail_url":thumbnail_url, "lat": data_lat, "lon":data_lng})
        else:
            scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"HAP", "type":ad_type, "thumbnail_url":thumbnail_url})

        #submit to api request start
        submit_url = "http://geolanka-api-beta.appspot.com/add_listing"
        submit_params = {
            "listing_type" :"GL_PROPERTY",
            "header":adHeader.encode('utf-8'),
            "location": location, 
            "content_url":content_url,
            "source":"HAP", 
            "listing_sub_type":"",
            "thumbnail_url":thumbnail_url, 
            "lat":data_lat, 
            "lon": data_lng, 
            "price_in_lkr": ''
        }

        print submit_params
        submit_response = urllib2.urlopen(urllib2.Request(submit_url, urllib.urlencode(submit_params)))
        
        print submit_response
        
        #submit to api request end
            
print "completed scrapping"

