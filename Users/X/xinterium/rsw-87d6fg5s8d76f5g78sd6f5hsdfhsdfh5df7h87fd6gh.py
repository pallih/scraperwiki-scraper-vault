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


property_content_base_url = "http://riyasewana.com/"
property_url = "http://riyasewana.com/search.php?vcat=Any&vtype=Any&make=Any&model=&page_id="

property_length=list(range(1,10))

print "RSW base Url " + property_url

idx = 0
for i in property_length:
    current_page_url = property_url + (str(i)) 
    print current_page_url
    html = scraperwiki.scrape(current_page_url)
    print html

    root = lxml.html.fromstring(html)

    
    for table in root.cssselect(".item.round"):
        idx += 1
        row=[]

        ad_type = "FOR_SALE"
        
        adHeader = table.cssselect('h3')[0].text_content()
        print adHeader

        #match for any rent
        rents = re.search("rent",adHeader.lower())
        print rents
        if rents is not None:
            print "RENT DISCOVERED"
            ad_type = "RENT"
        
        thumbnail_url = property_content_base_url + table.cssselect('img')[0].attrib['src']
        if 'thumbno_100.jpg' in thumbnail_url: 
            thumbnail_url = ""
        print thumbnail_url 

        location = table.cssselect('.boxintxt')[0].text_content()[len('Location : '):].strip() + ", Sri Lanka"
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


        content_url = table.cssselect('a')[0].attrib['href']
        print content_url


        
        #deep fetch the price
        content_html = scraperwiki.scrape(content_url)
        content = lxml.html.fromstring(content_html)

        priceInLKR = content.cssselect('.moret tr')[4].cssselect('td')[1].text_content()[4:].strip().replace(",","")

        try:
            int(priceInLKR)
        except:
            priceInLKR = ''

        print priceInLKR




        if (not geocode_disabled): 
            scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"RSW", "type":ad_type,"thumbnail_url":thumbnail_url,"lat": data_lat, "lon":data_lng})
        else:
            scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"RSW", "type":ad_type,"thumbnail_url":thumbnail_url})

        #submit to api request start
        submit_url = "http://geolanka-api-beta.appspot.com/add_listing"
        submit_params = {
            "listing_type" :"GL_VEHICLE",
            "header":adHeader.encode('utf-8'),
            "location": location, 
            "content_url":content_url,
            "source":"RSW", 
            "listing_sub_type":'',
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


property_content_base_url = "http://riyasewana.com/"
property_url = "http://riyasewana.com/search.php?vcat=Any&vtype=Any&make=Any&model=&page_id="

property_length=list(range(1,10))

print "RSW base Url " + property_url

idx = 0
for i in property_length:
    current_page_url = property_url + (str(i)) 
    print current_page_url
    html = scraperwiki.scrape(current_page_url)
    print html

    root = lxml.html.fromstring(html)

    
    for table in root.cssselect(".item.round"):
        idx += 1
        row=[]

        ad_type = "FOR_SALE"
        
        adHeader = table.cssselect('h3')[0].text_content()
        print adHeader

        #match for any rent
        rents = re.search("rent",adHeader.lower())
        print rents
        if rents is not None:
            print "RENT DISCOVERED"
            ad_type = "RENT"
        
        thumbnail_url = property_content_base_url + table.cssselect('img')[0].attrib['src']
        if 'thumbno_100.jpg' in thumbnail_url: 
            thumbnail_url = ""
        print thumbnail_url 

        location = table.cssselect('.boxintxt')[0].text_content()[len('Location : '):].strip() + ", Sri Lanka"
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


        content_url = table.cssselect('a')[0].attrib['href']
        print content_url


        
        #deep fetch the price
        content_html = scraperwiki.scrape(content_url)
        content = lxml.html.fromstring(content_html)

        priceInLKR = content.cssselect('.moret tr')[4].cssselect('td')[1].text_content()[4:].strip().replace(",","")

        try:
            int(priceInLKR)
        except:
            priceInLKR = ''

        print priceInLKR




        if (not geocode_disabled): 
            scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"RSW", "type":ad_type,"thumbnail_url":thumbnail_url,"lat": data_lat, "lon":data_lng})
        else:
            scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"RSW", "type":ad_type,"thumbnail_url":thumbnail_url})

        #submit to api request start
        submit_url = "http://geolanka-api-beta.appspot.com/add_listing"
        submit_params = {
            "listing_type" :"GL_VEHICLE",
            "header":adHeader.encode('utf-8'),
            "location": location, 
            "content_url":content_url,
            "source":"RSW", 
            "listing_sub_type":'',
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
