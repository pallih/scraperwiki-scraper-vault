import scraperwiki
import lxml.html
import urllib   
import simplejson
import urllib2
import datetime
import operator
from operator import itemgetter, attrgetter
from urllib import urlencode
from json import loads, dumps
import time


#data = scraperwiki.scrape('https://gist.github.com/raw/****')
#import csv 
#reader = csv.DictReader(data.splitlines())
#for row in reader: 
#    scraperwiki.sqlite.save(['id'],data=row)

#scraperwiki.sqlite.execute("CREATE TABLE `data3` (`id` text,`sourceurl` text,  `result` text,`geolocation_type` text,`sitename` text, `number` text,`subunit` text, `building` text, `intersection` text, `street` text, `town_sub` text, `town` text, `state` text,`country` text, `full_address` text)")
#scraperwiki.sqlite.commit()

scraperwiki.sqlite.execute("DELETE FROM data3 where result='Try Again'")
scraperwiki.sqlite.commit()

linklist = scraperwiki.sqlite.select("id,sourceurl from swdata where id not in (select id from data3) order by id")

for l in linklist:
    record={}
    record['id']=l['id']
    id=l['id']
    record['sourceurl']=l['sourceurl']+'&region=AU'

    # Google maps
    # - Works world wide (at least in the countries listed here: http://gmaps-samples.googlecode.com/svn/trunk/mapcoverage_filtered.html)
    # - limited to 2,500 requests in a 24 hour period (more details here: http://code.google.com/apis/maps/faq.html#geocoder_limit)
    geocode_url =l['sourceurl']+'&region=AU'
    #print geocode_url
    georeq = urllib2.Request(geocode_url)
    geo_response = urllib2.urlopen(georeq)
    geocode = simplejson.loads(geo_response.read())

    print geocode['status'],' : ',geocode_url

    if geocode['status'] == 'ZERO_RESULTS':
        record['result']='No address found'
    elif geocode['status'] == 'OVER_QUERY_LIMIT':
        record['result']='Try Again'
    else:
        record['result']='OK'       

        #print geocode['results'][0]['types']
        record ['geolocation_type']=geocode['results'][0]['types'][0]

        #print geocode['results'][0]['formatted_address']
        record['full_address']=geocode['results'][0]['formatted_address']
        
        li=geocode['results'][0]['address_components']
        #print li
        for n in li:
            if n['types'][0]=='country':
                record['country']=n['long_name']
            elif n['types'][0]=='administrative_area_level_1':
                record['state']=n['short_name']
            elif n['types'][0]=='postal_code':
                record['postcode']=n['long_name']
            elif n['types'][0]=='locality':
                record['town']=n['long_name']
            elif n['types'][0]=='sublocality':
                record['town_sub']=n['long_name']
            elif n['types'][0]=='intersection':
                record['intersection']=n['long_name']
            elif n['types'][0]=='route':
                record['street']=n['long_name']
            elif n['types'][0]=='street_number':
                record['number']=n['long_name']
            elif n['types'][0]=='subpremise':
                record['subunit']=n['long_name']
            elif n['types'][0]=='premise':
                record['building']=n['long_name']
            elif n['types'][0]=='point_of_interest' or n['types'][0]=='establishment' or n['types'][0]=='university':
                record['sitename']=n['long_name']

    scraperwiki.sqlite.save(['id'],record, 'data3')
    time.sleep(0.5)


import scraperwiki
import lxml.html
import urllib   
import simplejson
import urllib2
import datetime
import operator
from operator import itemgetter, attrgetter
from urllib import urlencode
from json import loads, dumps
import time


#data = scraperwiki.scrape('https://gist.github.com/raw/****')
#import csv 
#reader = csv.DictReader(data.splitlines())
#for row in reader: 
#    scraperwiki.sqlite.save(['id'],data=row)

#scraperwiki.sqlite.execute("CREATE TABLE `data3` (`id` text,`sourceurl` text,  `result` text,`geolocation_type` text,`sitename` text, `number` text,`subunit` text, `building` text, `intersection` text, `street` text, `town_sub` text, `town` text, `state` text,`country` text, `full_address` text)")
#scraperwiki.sqlite.commit()

scraperwiki.sqlite.execute("DELETE FROM data3 where result='Try Again'")
scraperwiki.sqlite.commit()

linklist = scraperwiki.sqlite.select("id,sourceurl from swdata where id not in (select id from data3) order by id")

for l in linklist:
    record={}
    record['id']=l['id']
    id=l['id']
    record['sourceurl']=l['sourceurl']+'&region=AU'

    # Google maps
    # - Works world wide (at least in the countries listed here: http://gmaps-samples.googlecode.com/svn/trunk/mapcoverage_filtered.html)
    # - limited to 2,500 requests in a 24 hour period (more details here: http://code.google.com/apis/maps/faq.html#geocoder_limit)
    geocode_url =l['sourceurl']+'&region=AU'
    #print geocode_url
    georeq = urllib2.Request(geocode_url)
    geo_response = urllib2.urlopen(georeq)
    geocode = simplejson.loads(geo_response.read())

    print geocode['status'],' : ',geocode_url

    if geocode['status'] == 'ZERO_RESULTS':
        record['result']='No address found'
    elif geocode['status'] == 'OVER_QUERY_LIMIT':
        record['result']='Try Again'
    else:
        record['result']='OK'       

        #print geocode['results'][0]['types']
        record ['geolocation_type']=geocode['results'][0]['types'][0]

        #print geocode['results'][0]['formatted_address']
        record['full_address']=geocode['results'][0]['formatted_address']
        
        li=geocode['results'][0]['address_components']
        #print li
        for n in li:
            if n['types'][0]=='country':
                record['country']=n['long_name']
            elif n['types'][0]=='administrative_area_level_1':
                record['state']=n['short_name']
            elif n['types'][0]=='postal_code':
                record['postcode']=n['long_name']
            elif n['types'][0]=='locality':
                record['town']=n['long_name']
            elif n['types'][0]=='sublocality':
                record['town_sub']=n['long_name']
            elif n['types'][0]=='intersection':
                record['intersection']=n['long_name']
            elif n['types'][0]=='route':
                record['street']=n['long_name']
            elif n['types'][0]=='street_number':
                record['number']=n['long_name']
            elif n['types'][0]=='subpremise':
                record['subunit']=n['long_name']
            elif n['types'][0]=='premise':
                record['building']=n['long_name']
            elif n['types'][0]=='point_of_interest' or n['types'][0]=='establishment' or n['types'][0]=='university':
                record['sitename']=n['long_name']

    scraperwiki.sqlite.save(['id'],record, 'data3')
    time.sleep(0.5)


