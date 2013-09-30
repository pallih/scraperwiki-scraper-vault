# OK, this is a first attempt to generate Layar AR JSON responses from ScraperWiki data. If it works I hope this will be an example to others, and I *do* have a project for it.
# todo - test.
# it expects you to provide, at the least, the name of a scraper with data in it, a parameterised SQL query to retrieve data from it, a list of which values from the client request you want to pass to the SQL query, and a list of the request field names you want to map  onto your returned database rows. further, the dictionaries layer_defaults and poi_defaults permit you to specify the full range of options provided by the Layar API. if a key in poi_defaults matches a field name, its value is set to whatever was returned from the database and mapped to that key, thus loading data into the fields. layer_defaults permits you to define global settings for the whole project. 

#by default, a simple geographical radius filter is applied to the returned data, but you can override this by providing your own custom filter function as an argument to custom_filter, which must accept the returned row of data and return either True or False. For example, if you want to use visual search you could specify referenceImage in the field mappings and provide a matching function as custom_filter. Obviously if you want to do something that funky you might just subclass it.

# Layar asks you to provide a list of deleted hotspots, and also to distinguish between full refreshes and updates. Unfortunately, the client doesn't tell you which hotspots it's looking at, so you've got to track user state. I've dealt with this using the SQLite rowid field; updates return rowids higher (i.e. more recent) than the last one we logged for that user ID, and the list of rowids served is checked against the database to identify deleted items.

# yes, if you want you can attach to multiple scrapers and do a join! but one of the tables has to be the Shia Source of Emulation for the rowids and you must declare this one first or it won't work.

import scraperwiki
import cgi
import os
import json
from geopy import Point, Distance

class SwLayarPOIServer():
    def _init_(self, source_scraper_name, sqlquery=None, input_fields=[], output_fields=[], layer_defaults={}, poi_defaults={}, alt=0, search_radius=1000, custom_errors={}, custom_filter=None, accuracy=20, refresh_interval=None, refresh_distance=None):
        self.source_scraper_name = source_scraper_name[0]
        self.input_fields = input_fields
        self.output_fields = output_fields
        self.sqlquery = sqlquery
        self.altitude = alt
        self.search_radius = search_radius
        self.errors = {'0': 'OK', '20': 'No POIs found'}
        self.request = {}
        self.defaults = poi_defaults
        self.layer_defaults = layer_defaults
        if custom_errors:
            self.errors.update(custom_errors)
        scraperwiki.sqlite.attach(source_scraper_name)
        if custom_filter:
            self.custom_filter = custom_filter
        
#sourcescraper = '' # obviously, specify the source here
#search_radius = 1000 #can be sent by the user, but a value must be in the response object so a default must be set here
#alt = 0 #altitude may be available but may not. if important, consider setting this param to a suitable value
#errors = {'0': 'OK', '20': 'No POIs found'} # errorCode and errorString are required in the response - edit this dict to set your desired errors other than OK and not-found

    def radius_filter(self, row):
# afaik the DB doesn't have geocapability, so this is a favela-chic way of doing a bounding radius select.
        p = Point(row['lat'], row['lon'], row['alt'])
        me = Point(self.qst['lat'], self.qst['lon'], self.qst['alt'])
        dist = Distance.distance(p, me)
        if dist <= self.qst['search_radius']:
            return True

    def process_requests(self, querystring=None):
        if querystring:
            self.qst = querystring
        else:
            self.qst = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
        data = scraperwiki.sqlite.execute(sqlquery, [k[1] for k in self.qst if k in self.input_fields])
        return data     

    def defaultsmapper(self, row, target):
        for k in self.defaults[(target)]:
            if k in row:
                self.defaults[(target)].update(k=(row[k])
            if isinstance(k[1], dict):
                for k in k[1]:
                    k[1].update(k=row[k])
        return self.defaults[(target)]
    
    def make_hotspot(self, row):
        if not row['alt']:
                row['alt'] = self.altitude
        content = {}
        content['id'] = row['id']
        if row['referenceImage']:
            content['anchor'] = {'referenceImage': (row['referenceImage'])}
        else:
            content['anchor'] = {'geolocation': {'lat': (row['lat']), 'lon': (row['lon']), 'alt': (row['alt'])}}
        content['text'] = {[k, k[1] for k in row if k in [title, description, footnote]]}

        for key in ('actions', 'imageURL', 'icon', 'object', 'transform', 'animations', 'showSmallBiw', 'showBiwOnClick', 'biwStyle', 'scale', 'inFocus',):
             if key in self.defaults:
                content[key] = defaultsmapper(row, key)
        return content

    def find_deleted_hotspots(self):
        ris = scraperwiki.sqlite.select('rowid from ?', self.source_scraper_name)
        served_hotspots = (scraperwiki.get_var(self.qst['userId'])[2])
        deleted_hotspots = [x for x in served_hotspots if x not in ris.values()]
        return deleted_hotspots
        
    def process_response(self, data):
        response = {'layer': (self.request['layer_name']), 'errorCode': 0, 'errorString': (errors["0"])}
        if self.custom_filter:
            filter = self.custom_filter
        else:
            filter = radius_filter

        def track_user_state(self, output)
            rowids = [row['id'] for row in output]
            last = max(rowids)
            scraperwiki.save_var(self.qst['userId'], (last, rowids))

        def update_hotspots(self, data, response, filter):
            user_lastitem = (scraperwiki.get_var(self.qst['userId']))[1]
            output = [dict(zip(self.output_fields, row)) for row in data[1] if filter(row) == True and row['rowid'] > user_lastitem]
            track_user_state(self, output)
            response['FullRefresh'] == false
            return output

        def refresh_all_hotspots(self, data, response, filter):
            output = [dict(zip(self.output_fields, row)) in data[1] if filter(row) == True]
            track_user_state(self, output)          
            response['FullRefresh'] == true
            return output

        if self.qst['action'] == 'update':
            output = update_hotspots(self, data, response, filter)
        else:
            output = refresh_all_hotspots(self, data, response, filter)

        if len(output) == 0:
            response["errorCode"] == 20
            response["errorString"] == errors["20"] # deal with not-found case    
        response['hotspots'] = [make_hotspot(row) for row in output]
        response.update(self.layer_defaults)        
        response.update(deletedHotspots=(find_deleted_hotspots))
        js = json.dumps(response) #generate json
        scraperwiki.utils.httpresponseheader('Content-Type': 'application/json')
        print js #and serve it up        

#any one of the following keys: ['RADIOLIST', 'SEARCHBOX', 'SEARCHBOX_2', 'SEARCHBOX_3', 'CUSTOM_SLIDER', 'CUSTOM_SLIDER_2', 'CUSTOM_SLIDER_3', 'CHECKBOXLIST', 'recognizedReferenceImage', 'pageKey'] may appear in the request or may not. pageKey is used to bind requests for multi-page objects together. recognizedReferenceImage is used to deal with visual search requests. the rest are user input. any present will be in the query dict.

#there is a possibility that the layer might have OAuth enabled, in which case these keys will be present in the query. ['oauth_consumer_key', 'oauth_signature_method', 'oauth_version', 'oauth_timestamp', 'oauth_nonce', 'oauth_body_hash', 'oauth_signature'] can't imagine that a scraper will implement OAuth, but there you go.
 
# more info on the getPOI call here: http://www.layar.com/documentation/browser/api/getpois-request/


# Layar POIs MUST minimally have a unique identifier, a geographical location, and a title. they can also have more things as specified here http://www.layar.com/documentation/browser/api/getpois-response/hotspots/
# as an example, and because this does actually have a use case, we're presuming that there is information about events in a scraper, with geographical locations, some text, a time, and a URI




# OK, this is a first attempt to generate Layar AR JSON responses from ScraperWiki data. If it works I hope this will be an example to others, and I *do* have a project for it.
# todo - test.
# it expects you to provide, at the least, the name of a scraper with data in it, a parameterised SQL query to retrieve data from it, a list of which values from the client request you want to pass to the SQL query, and a list of the request field names you want to map  onto your returned database rows. further, the dictionaries layer_defaults and poi_defaults permit you to specify the full range of options provided by the Layar API. if a key in poi_defaults matches a field name, its value is set to whatever was returned from the database and mapped to that key, thus loading data into the fields. layer_defaults permits you to define global settings for the whole project. 

#by default, a simple geographical radius filter is applied to the returned data, but you can override this by providing your own custom filter function as an argument to custom_filter, which must accept the returned row of data and return either True or False. For example, if you want to use visual search you could specify referenceImage in the field mappings and provide a matching function as custom_filter. Obviously if you want to do something that funky you might just subclass it.

# Layar asks you to provide a list of deleted hotspots, and also to distinguish between full refreshes and updates. Unfortunately, the client doesn't tell you which hotspots it's looking at, so you've got to track user state. I've dealt with this using the SQLite rowid field; updates return rowids higher (i.e. more recent) than the last one we logged for that user ID, and the list of rowids served is checked against the database to identify deleted items.

# yes, if you want you can attach to multiple scrapers and do a join! but one of the tables has to be the Shia Source of Emulation for the rowids and you must declare this one first or it won't work.

import scraperwiki
import cgi
import os
import json
from geopy import Point, Distance

class SwLayarPOIServer():
    def _init_(self, source_scraper_name, sqlquery=None, input_fields=[], output_fields=[], layer_defaults={}, poi_defaults={}, alt=0, search_radius=1000, custom_errors={}, custom_filter=None, accuracy=20, refresh_interval=None, refresh_distance=None):
        self.source_scraper_name = source_scraper_name[0]
        self.input_fields = input_fields
        self.output_fields = output_fields
        self.sqlquery = sqlquery
        self.altitude = alt
        self.search_radius = search_radius
        self.errors = {'0': 'OK', '20': 'No POIs found'}
        self.request = {}
        self.defaults = poi_defaults
        self.layer_defaults = layer_defaults
        if custom_errors:
            self.errors.update(custom_errors)
        scraperwiki.sqlite.attach(source_scraper_name)
        if custom_filter:
            self.custom_filter = custom_filter
        
#sourcescraper = '' # obviously, specify the source here
#search_radius = 1000 #can be sent by the user, but a value must be in the response object so a default must be set here
#alt = 0 #altitude may be available but may not. if important, consider setting this param to a suitable value
#errors = {'0': 'OK', '20': 'No POIs found'} # errorCode and errorString are required in the response - edit this dict to set your desired errors other than OK and not-found

    def radius_filter(self, row):
# afaik the DB doesn't have geocapability, so this is a favela-chic way of doing a bounding radius select.
        p = Point(row['lat'], row['lon'], row['alt'])
        me = Point(self.qst['lat'], self.qst['lon'], self.qst['alt'])
        dist = Distance.distance(p, me)
        if dist <= self.qst['search_radius']:
            return True

    def process_requests(self, querystring=None):
        if querystring:
            self.qst = querystring
        else:
            self.qst = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
        data = scraperwiki.sqlite.execute(sqlquery, [k[1] for k in self.qst if k in self.input_fields])
        return data     

    def defaultsmapper(self, row, target):
        for k in self.defaults[(target)]:
            if k in row:
                self.defaults[(target)].update(k=(row[k])
            if isinstance(k[1], dict):
                for k in k[1]:
                    k[1].update(k=row[k])
        return self.defaults[(target)]
    
    def make_hotspot(self, row):
        if not row['alt']:
                row['alt'] = self.altitude
        content = {}
        content['id'] = row['id']
        if row['referenceImage']:
            content['anchor'] = {'referenceImage': (row['referenceImage'])}
        else:
            content['anchor'] = {'geolocation': {'lat': (row['lat']), 'lon': (row['lon']), 'alt': (row['alt'])}}
        content['text'] = {[k, k[1] for k in row if k in [title, description, footnote]]}

        for key in ('actions', 'imageURL', 'icon', 'object', 'transform', 'animations', 'showSmallBiw', 'showBiwOnClick', 'biwStyle', 'scale', 'inFocus',):
             if key in self.defaults:
                content[key] = defaultsmapper(row, key)
        return content

    def find_deleted_hotspots(self):
        ris = scraperwiki.sqlite.select('rowid from ?', self.source_scraper_name)
        served_hotspots = (scraperwiki.get_var(self.qst['userId'])[2])
        deleted_hotspots = [x for x in served_hotspots if x not in ris.values()]
        return deleted_hotspots
        
    def process_response(self, data):
        response = {'layer': (self.request['layer_name']), 'errorCode': 0, 'errorString': (errors["0"])}
        if self.custom_filter:
            filter = self.custom_filter
        else:
            filter = radius_filter

        def track_user_state(self, output)
            rowids = [row['id'] for row in output]
            last = max(rowids)
            scraperwiki.save_var(self.qst['userId'], (last, rowids))

        def update_hotspots(self, data, response, filter):
            user_lastitem = (scraperwiki.get_var(self.qst['userId']))[1]
            output = [dict(zip(self.output_fields, row)) for row in data[1] if filter(row) == True and row['rowid'] > user_lastitem]
            track_user_state(self, output)
            response['FullRefresh'] == false
            return output

        def refresh_all_hotspots(self, data, response, filter):
            output = [dict(zip(self.output_fields, row)) in data[1] if filter(row) == True]
            track_user_state(self, output)          
            response['FullRefresh'] == true
            return output

        if self.qst['action'] == 'update':
            output = update_hotspots(self, data, response, filter)
        else:
            output = refresh_all_hotspots(self, data, response, filter)

        if len(output) == 0:
            response["errorCode"] == 20
            response["errorString"] == errors["20"] # deal with not-found case    
        response['hotspots'] = [make_hotspot(row) for row in output]
        response.update(self.layer_defaults)        
        response.update(deletedHotspots=(find_deleted_hotspots))
        js = json.dumps(response) #generate json
        scraperwiki.utils.httpresponseheader('Content-Type': 'application/json')
        print js #and serve it up        

#any one of the following keys: ['RADIOLIST', 'SEARCHBOX', 'SEARCHBOX_2', 'SEARCHBOX_3', 'CUSTOM_SLIDER', 'CUSTOM_SLIDER_2', 'CUSTOM_SLIDER_3', 'CHECKBOXLIST', 'recognizedReferenceImage', 'pageKey'] may appear in the request or may not. pageKey is used to bind requests for multi-page objects together. recognizedReferenceImage is used to deal with visual search requests. the rest are user input. any present will be in the query dict.

#there is a possibility that the layer might have OAuth enabled, in which case these keys will be present in the query. ['oauth_consumer_key', 'oauth_signature_method', 'oauth_version', 'oauth_timestamp', 'oauth_nonce', 'oauth_body_hash', 'oauth_signature'] can't imagine that a scraper will implement OAuth, but there you go.
 
# more info on the getPOI call here: http://www.layar.com/documentation/browser/api/getpois-request/


# Layar POIs MUST minimally have a unique identifier, a geographical location, and a title. they can also have more things as specified here http://www.layar.com/documentation/browser/api/getpois-response/hotspots/
# as an example, and because this does actually have a use case, we're presuming that there is information about events in a scraper, with geographical locations, some text, a time, and a URI




