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


property_content_base_url = "http://autolanka.com/"
property_url = "http://autolanka.com/Buy.asp?ad_category_id=&search=&Page="

property_length=list(range(1,10))

print "ALK base Url " + property_url

idx = 0
for i in property_length:
    current_page_url = property_url + (str(i)) 
    print current_page_url
    html = scraperwiki.scrape(current_page_url)
    print html

    root = lxml.html.fromstring(html)

    
    for table in root.cssselect("font.BuyDataFONT strong a"):
        idx += 1
        row=[]
        
        content_url = table.attrib['href']

        if (content_url == "http://cloudflare.com/email-protection.html"):
            continue #skip if cloudflare is caught
        
        content_url = property_content_base_url + content_url
        print content_url

        m = re.search(r"=(?P<content_id>\w+)",content_url)
        content_id = m.group('content_id')

        thumbnail_url = "http://www.autolanka.com/adss/" + content_id.zfill(9)+ "_s.jpg"
        print thumbnail_url 

        #dive into the content
        content_html = scraperwiki.scrape(content_url)
        content = lxml.html.fromstring(content_html)

        adHeader = content.cssselect('td.GeneralLinksFormHeaderTD')[0].text_content()
        print adHeader

        location = content.cssselect('tr')[20].text_content()[len('Location'):].strip()
        print location

        if(location == 'Other' or location == ""):
            continue
        else:
            location = location + ", Sri Lanka"

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


        priceInLKR = content.cssselect('tr')[21].text_content()[len('Price '):].strip()
        
        if priceInLKR == 'Highest Offer':
            priceInLKR = ''
        else:
            print priceInLKR            
            priceInLKR = priceInLKR.replace('Rs. ', '').replace(',', '').replace('/=', '').strip()

        print priceInLKR
        
        if (not geocode_disabled):    
            scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"ALK", "type":"FOR_SALE","thumbnail_url":thumbnail_url,"lat": data_lat, "lon":data_lng,"price_in_lkr" : priceInLKR})
        else:
            scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"ALK", "type":"FOR_SALE","thumbnail_url":thumbnail_url,"price_in_lkr" : priceInLKR})

        #submit to api request start
        submit_url = "http://geolanka-api-beta.appspot.com/add_listing"
        submit_params = {
            "listing_type" :"GL_VEHICLE",
            "header":adHeader.encode('utf-8'),
            "location": location, 
            "content_url":content_url,
            "source":"ALK", 
            "listing_sub_type":"",
            "thumbnail_url":thumbnail_url, 
            "lat":data_lat, 
            "lon": data_lng, 
            "price_in_lkr":priceInLKR
        }

        print submit_params
        submit_response = urllib2.urlopen(urllib2.Request(submit_url, urllib.urlencode(submit_params)))
        
        print submit_response.read()
        
        #submit to api request end

print "completed scrapping"

