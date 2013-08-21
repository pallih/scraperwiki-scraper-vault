# a library of functions dealing with geographical location defined by postcode and latitude/longitude

# Note in a full UK postcode, a space in the middle is irrelevant (occurs before the final 3 chars) and some sites ask for it to be stripped
# However for partial postcodes the space separator is significant e.g. 'N15' vs 'N1 5'

import scraperwiki
import urllib2, urllib
import time
import json
import sys
import re
from datetime import datetime
from datetime import timedelta
from lxml import etree
from cStringIO import StringIO

scraperwiki.sqlite.attach('adaptive_uk_postcode_lookup', 'postcodes')

# these are openstreetmap boundary line identifiers and postcode prefixes for national parks
# not used at the moment
brecon_beacons = '357283'  # LD, CF, NP, SA and HR
broads = ''   # NR
cairngorms = '1947603' #  PH, AB, DD
dartmoor = '1928125' # PL, EX and TQ
exmoor = '86909' # EX and TA
lake_district = '287917'  # CA and LA
loch_lomond = '1957067'  #  PA, FK, G, KA
new_forest = '129493402' # way not relation # BH, SP and SO
northumberland = '1168821' # NE, TD, CA
north_york_moors = '409150' # YO, DL, TS
peak_district = '2176657'  # SK, DE, S, HD and OL
pembrokeshire_coast = '165598' # multiple polygons # SA
snowdonia = '287245'  # LL and SY
south_downs = '1596374'  #  PO, SO, GU, RH, BN
yorkshire_dales = '307985'  # CA, LA, BD, DL, HG and LS


# postcode lookup sources listed in order of preference based on feature richness
main_list = [
    'mapit', # most features incl. local authority information
    'ukpostcodes', # next best
    'geopostcode', 
    'scraperwiki', # maybe fastest from here?
    'jamiethompson', # does not include Northern Ireland but does have some authority information - data source may not be codepoint
]

# postcode lookup sources for partial postcodes e.g. WC1E (input field) or N16 5 (sector code)
partial_list = [
    'geopostcode',
    'mapit', # no local authority info for partial codes and only does short partial codes of form N16 but not N16 5
    'yahoo',
    'google', 
]

# postcode lookup sources for crown dependency postcodes - Jersey, Guernsey, Isle of Man
crowndep_list = [
    'geopostcode',
    'yahoo',
    'google', 
]

# lookup sources for reverse geocoding via latitude and longitude to produce nearest postcode
reverse_list = [
    'mapit',
    'ukpostcodes',
    'google', 
]

# lookup sources for geocoding from address
geocode_list = [
    'google', 
    'yahoo'
]

EXTRACT_FULL_REGEX = re.compile(r'\b([A-Z][A-Z]?\d(?:\d|[A-Z])?)\s*(\d[ABDEFGHJLNPQRSTUWXYZ]{2})\b', re.I) # ignore case
EXTRACT_PARTIAL_REGEX = re.compile(r'\b([A-Z][A-Z]?\d(?:\d|[A-Z])?)(?:\s+(\d))?\b', re.I) # ignore case
POSTCODE_REGEX = re.compile(r'^\s*([A-Z][A-Z]?\d(?:\d|[A-Z])?)\s*(\d[ABDEFGHJLNPQRSTUWXYZ]{2})\s*$', re.I) # ignore case
PARTIAL_REGEX = re.compile(r'^\s*([A-Z][A-Z]?\d(?:\d|[A-Z])?)(?:\s+(\d)\s*)?$', re.I) # ignore case
CROWNDEP_REGEX = re.compile(r'^\s*(IM|JE|GY)', re.I) # ignore case
GAPS_REGEX = re.compile(r'\s+', re.U) # unicode spaces include html &nbsp;
GEO_TIMEOUT = 10 # max time to wait for a response from any source in seconds
DEBUG = False
FULL_CODE = 'Full'
PARTIAL_CODE = 'Partial'

# test for presence of a postcode
def test_postcode(text):
    if not text: return ''
    if EXTRACT_FULL_REGEX.search(text):
        return FULL_CODE
    elif EXTRACT_PARTIAL_REGEX.search(text):
        return PARTIAL_CODE
    return ''

# extract a normalised full postcode
def extract_postcode(text):
    if not text: return None
    postcode_match = EXTRACT_FULL_REGEX.search(text)
    if postcode_match and postcode_match.lastindex >= 2:
        return postcode_match.group(1).upper() + ' ' + postcode_match.group(2).upper()
    return None

# extract a normalised partial postcode
def extract_partial_postcode(text):
    if not text: return None
    postcode_match = EXTRACT_PARTIAL_REGEX.search(text)
    if postcode_match and postcode_match.lastindex >= 2:
        return postcode_match.group(1).upper() + ' ' + postcode_match.group(2).upper()
    elif postcode_match and postcode_match.lastindex == 1:
        return postcode_match.group(1).upper()
    return None

# normalise postcode - normalise spaces and force upper case
# note returns None if the postcode is not recognised
def postcode_norm(postcode):
    norm_code = extract_postcode(postcode)
    if norm_code:
        return norm_code
    return extract_partial_postcode(postcode) 

# uses location based data attributes within a dict to derive any missing latitude/longitude and postcode values
# note includes a nested call to postcode_lookup(), which updates the adaptive postcode database
def set_latlngpost(data):

    if data.get('postcode') and (data.get('lng') or data.get('lat')):
        return

    postcode = None
    if data.get('postcode'):
        postcode = extract_postcode(data['postcode']) # note full postcodes only
    if not postcode and data.get('address'):
        postcode = extract_postcode(data['address']) # note full postcodes only
        
    if postcode:
        data['postcode'] = postcode
        # replace the existing postcode version if we have a verified full valid postcode

    # now try to get lat and lng from easting, northing or OS grid ref values if they exist
    # NB need extra information to say whether it is on the Irish or GB grids
    # By default assume GB grid
    if not data.get('lng') and not data.get('lat'):
        east = None; north = None
        if data.get('easting') and data.get('northing'):
            east = float(data['easting'])
            north = float(data['northing'])
        elif data.get('os_grid_ref'):
            if ',' in data['os_grid_ref']: # sometimes easting, northing are put in the os_grid_ref field by mistake
                coords = data['os_grid_ref'].split(',')
                east = float(trim(coords[0]))
                north = float(trim(coords[1]))
            else:
                try:
                    east, north = scraperwiki.geo.osgb_to_eastnorth(data['os_grid_ref'])
                except:
                    east = None; north = None
    
        if east or north:
            grid = 'GB'
            if postcode and postcode.startswith('BT') and not data.get('os_grid_ref'): 
                grid = 'IE' # Northern Ireland easting/northing values are relative to Irish grid
            result = scraperwiki.geo.os_easting_northing_to_latlng(east, north, grid)
            if result:
                data['lat'] = str(result[0])
                data['lng'] = str(result[1])
                if postcode:
                    return

    # if there is still a postcode only, we use it to get the location from the adaptive postcode database and exit here
    if postcode and not data.get('lng') and not data.get('lat'):
        result = postcode_lookup(postcode) 
        if result:
            data['lat'] = str(result['lat'])
            data['lng'] = str(result['lng'])
            return

    # if there is a location only, we do a reverse lookup of the postcode and exit
    if not postcode and (data.get('lng') or data.get('lat')):
        result = postcode_reverse(data['lng'], data['lat'])
        if result and test_postcode(result['postcode']) == FULL_CODE:
            # only use the returned postcode if it is a full valid postcode
            data['postcode'] = extract_postcode(result['postcode'])
            return

    # last resort is an attempt to reverse geocode using the address
    if data.get('address'):
        result = geocode(data['address'])
        if result:
            if not data.get('lng') and not data.get('lat'):
                data['lat'] = str(result['lat'])
                data['lng'] = str(result['lng'])
            if not postcode and test_postcode(result['postcode']) == FULL_CODE:
                # only use the returned postcode if it is a full valid postcode
                data['postcode'] = extract_postcode(result['postcode'])
                return

# get the ideal source for lookup of a postcode
def get_postcode_best_source(postcode):
    ptype = test_postcode(postcode)
    if ptype and CROWNDEP_REGEX.search(postcode): #crown dependencies
        return crowndep_list[0]
    elif ptype == FULL_CODE:
        return main_list[0]
    elif ptype == PARTIAL_CODE:
        return partial_list[0]
    return ''

# direct fetch of location from postcode using  external lookup source list
def geocode_postcode(postcode, end_sources_before = None, only_source = None):
    ptype = test_postcode(postcode)
    if ptype == FULL_CODE:
        if DEBUG: print "Full postcode found"
        if CROWNDEP_REGEX.search(postcode): #crown dependencies
            source_list = crowndep_list
        else:
            source_list = main_list
    elif ptype == PARTIAL_CODE:
        if DEBUG: print "Partial postcode found"
        if CROWNDEP_REGEX.search(postcode): #crown dependencies
            source_list = crowndep_list
        else:
            source_list = partial_list
    else:
        return None
    result = None
    for i in source_list:
        if end_sources_before and i == end_sources_before:
            break
        if only_source and i <> only_source:
            continue
        start_time = time.time()
        result = eval( i + "_postcode('" + postcode + "')" )
        if result:
            result['lookup_time'] = time.time() - start_time
            result['source'] = i
            if not result.get('region'):
                postcode = postcode_norm(postcode)
                if postcode:
                    if postcode.startswith('JE') or postcode.startswith('GY'):
                        result['region'] = 'Channel Islands'
                    elif postcode.startswith('IM'):
                        result['region'] = 'Isle of Man'
                    elif postcode.startswith('BT'):
                        result['region'] = 'Northern Ireland'
            if not result.get('district'):
                postcode = postcode_norm(postcode)
                if postcode:
                    if postcode.startswith('JE'):
                        result['district'] = 'Jersey'
                    elif postcode.startswith('GY9'):
                        result['district'] = 'Alderney'
                    elif postcode.startswith('GY10'):
                        result['district'] = 'Sark'
                    elif postcode.startswith('GY'):
                        result['district'] = 'Guernsey'
                    elif postcode.startswith('IM'):
                        result['district'] = 'Isle of Man'
            if DEBUG: print "Valid geocode postcode response from", i
            break
        else:
            if DEBUG: print "No geocode postcode response from", i
    return result

# get indirect location from postcode using 
# 1. directly attached postcodes table if it exists
# 2. request to get same data via scraperwiki view (which will update the tables)
def postcode_lookup(postcode):
    # first try to get the postcode directly from the database
    sql = "* from postcodes.postcodes where postcode = '%s'" % postcode_norm(postcode)
    try:
        result = scraperwiki.sqlite.select(sql)
        return result[0]
    except:
        pass
    # if it's not found, do an external request via scraperwiki view which updates the database for next time
    url = 'https://views.scraperwiki.com/run/adaptive_uk_postcode_lookup/?fmt=json&postcode=' + urllib.quote_plus(postcode)
    try:
        return json.load(urllib2.urlopen(url, None, GEO_TIMEOUT))  # 10 sec timeout
    except:
        return None

# get location from address
def geocode(address):
    result = None
    for i in geocode_list:
        start_time = time.time()
        func = i + "_geocode('" + address.replace("'", "''") + "')"
        func = func.replace("('''", "(' ''")
        func = func.replace("''')", "'' ')")
        result = eval( func )
        if result:
            result['lookup_time'] = time.time() - start_time
            result['source'] = i
            if DEBUG: print "Valid geocode response from", i
            break
        else:
            if DEBUG: print "No geocode response from", i
    return result

# nearest postcode lookup from lng/lat location using reverse geocoding sources
def postcode_reverse(lng, lat):
    result = None
    for i in reverse_list:
        start_time = time.time()
        result = eval( i + "_reverse('" + str(lng) + "', '" + str(lat) + "')" )
        if result:
            result['lookup_time'] = time.time() - start_time
            result['source'] = i
            if DEBUG: print "Valid reverse response from", i
            break
        else:
            if DEBUG: print "No reverse response from", i
    return result

# reverse Geocode via mapit
def mapit_reverse(x, y, grid='GB'):
    strx = str(x)
    stry = str(y)
    if '.' in strx or '.' in stry:
        url = 'http://mapit.mysociety.org/nearest/4326/%s,%s' % (strx, stry) # lon/lat
    elif grid and grid.upper() == 'IE':
        url = 'http://mapit.mysociety.org/nearest/29902/%s,%s' % (strx, stry) # easting/northing (NB Ireland)
    else:
        url = 'http://mapit.mysociety.org/nearest/27700/%s,%s' % (strx, stry) # easting/northing (NB GB)
    try:
        result = json.load(urllib2.urlopen(url, None, GEO_TIMEOUT))  
    except:
        return None
    if DEBUG: print 'Result', result
    if result:
        if 'easting' not in result['postcode']  and 'northing' not in result['postcode']: # ignore postcodes found outside the British Isles
            return None
        return { 'lat': result['postcode']['wgs84_lat'],
            'lng': result['postcode']['wgs84_lon'],
            'easting': result['postcode']['easting'],
            'northing': result['postcode']['northing'],
            'postcode': result['postcode']['postcode'],
            'url': url }
    else:
        return None

def mapit_postcode(postcode):
    ptype = test_postcode(postcode)
    if ptype == FULL_CODE:
        url = 'http://mapit.mysociety.org/postcode/' + urllib.quote_plus(postcode)
    elif ptype == PARTIAL_CODE: # NB works with partial postcodes of form N16 but not N16 5
        url = 'http://mapit.mysociety.org/postcode/partial/' + urllib.quote_plus(postcode)
    else:
        return None
    try:
        result = json.load(urllib2.urlopen(url, None, GEO_TIMEOUT))  
    except:
        return None
    if DEBUG: print 'Result', result
    if result:
        if result.get('shortcuts') and result.get('areas'):
            region = None; region_gss = None; region_snac = None
            district = None; district_gss = None; district_snac = None
            county = None; county_gss = None; county_snac = None
            council_id = result['shortcuts']['council']
            if isinstance(council_id, dict):
                district = result['areas'][str(council_id['district'])]['name']
                district_snac = result['areas'][str(council_id['district'])]['codes']['ons']
                county = result['areas'][str(council_id['county'])]['name']
                county_snac = result['areas'][str(council_id['county'])]['codes']['ons']
                try:
                    district_gss = result['areas'][str(council_id['district'])]['codes']['gss']
                    county_gss = result['areas'][str(council_id['county'])]['codes']['gss']
                except:
                    district_gss = None
                    county_gss = None
            else:
                district = result['areas'][str(council_id)]['name']
                try:
                    district_gss = result['areas'][str(council_id)]['codes']['gss']
                except:
                    district_gss = None
                district_snac = result['areas'][str(council_id)]['codes']['ons']
            for k, v in result['areas'].items():
                if v['type'] == 'EUR':
                    region = v['name']
                    region_gss = v['codes']['gss']
                    region_snac = v['codes']['ons']
                    break
            return { 'lat': result['wgs84_lat'],
                'lng': result['wgs84_lon'],
                'easting': result['easting'],
                'northing': result['northing'],
                'district': district,
                'county': county,
                'district_gss': district_gss,
                'county_gss': county_gss,
                'district_snac': district_snac,
                'county_snac': county_snac,
                'region': region,
                'region_gss': region_gss,
                'region_snac': region_snac,
                'postcode': result['postcode'],
                'url': url }
        else:
            return { 'lat': result['wgs84_lat'],
                'lng': result['wgs84_lon'],
                'easting': result['easting'],
                'northing': result['northing'],
                'postcode': result['postcode'],
                'url': url }
    else:
        return None

def jamiethompson_postcode(postcode): # uses http://jamiethompson.co.uk/projects/2010/04/30/an-open-free-uk-postcode-geocoding-web-service/
    url = 'http://geo.jamiethompson.co.uk/' + urllib.quote_plus(postcode) + '.json'
    try:
        result = json.load(urllib2.urlopen(url, None, GEO_TIMEOUT))
    except:
        return None
    if DEBUG: print 'Result', result
    if result and result['status'] == 200:
        district = result['address']['district'],
        county = result['address']['county'],
        if county == 'Greater London':
            county = None
        if not district and county:
            district = county
            county = None
        if isinstance(district, list): district = district[0]
        if isinstance(county, list): county = county[0]
        return { 'lat': float(result['geo']['lat']),
                'lng': float(result['geo']['lng']),
                'easting': int(result['geo']['os_x']),
                'northing': int(result['geo']['os_y']),
                'district': district,
                'county': county,
                'postcode': result['postcode'],
                'url': url  }
                # 'gridref': result['geo']['landranger'],
    else:
        return None

def scraperwiki_postcode(postcode):
    url = 'https://views.scraperwiki.com/run/uk_postcode_lookup/?postcode=' + urllib.quote_plus(postcode)
    try:
        result = json.load(urllib2.urlopen(url, None, GEO_TIMEOUT))
    except:
        return None
    if DEBUG: print 'Result', result
    if result and 'error' not in result:
        return { 'lat': result['lat'],
                'lng': result['lng'],
                'easting': result['Eastings'],
                'northing': result['Northings'],
                'postcode': result['Postcode'],
                'url': url  }
    else:
        return None

def ukpostcodes_postcode(postcode):
    postcode = GAPS_REGEX.sub('', postcode) # need to strip any internal spaces
    url = 'http://www.uk-postcodes.com/postcode/' + urllib.quote_plus(postcode) + '.json'
    try:
        result = json.load(urllib2.urlopen(url, None, GEO_TIMEOUT))
    except:
        return None
    if DEBUG: print 'Result', result
    if result:
        try:
            county = result['administrative']['county']['title']
            county_snac = result['administrative']['county']['snac']
        except:
            county = None
            county_snac = None
        return { 'lat': float(result['geo']['lat']),
                'lng': float(result['geo']['lng']),
                'easting': int(result['geo']['easting']),
                'northing': int(result['geo']['northing']),
                'district': result['administrative']['district']['title'],
                'county': county,
                'district_snac': result['administrative']['district']['snac'],
                'county_snac': county_snac,
                'postcode': result['postcode'],
                'url': url  }
    else:
        return None

# reverse Geocode via ukpostcodes
def ukpostcodes_reverse(x, y):
    url = 'http://www.uk-postcodes.com/latlng/' + str(y) + ',' + str(x) + '.json'
    try:
        result = json.load(urllib2.urlopen(url, None, GEO_TIMEOUT))
    except:
        return None
    if DEBUG: print 'Result', result
    if result:
        if 'easting' not in result['geo']  and 'northing' not in result['geo']: # ignore postcodes found outside the British Isles
            return None
        return { 'lat': float(result['geo']['lat']),
                'lng': float(result['geo']['lng']),
                'easting': int(result['geo']['easting']),
                'northing': int(result['geo']['northing']),
                'postcode': result['postcode'],
                'url': url  }
    else:
        return None

def geopostcode_postcode(postcode):
    url = 'http://www.geopostcode.org.uk/api/' + urllib.quote_plus(postcode) + '.json'
    try:
        result = json.load(urllib2.urlopen(url, None, GEO_TIMEOUT))
    except:
        return None
    if DEBUG: print 'Result', result
    if result:
        postcode = postcode_norm(postcode)
        if postcode and postcode.startswith('BT'): # Northern Ireland eastings/northings supplied relative to Irish grid
            easting = int(result['osie']['east'])
            northing = int(result['osie']['north'])
        else:
            easting = int(result['osgb36']['east'])
            northing = int(result['osgb36']['north'])
        return { 'lat': float(result['wgs84']['lat']),
                'lng': float(result['wgs84']['lon']),
                'easting': easting,
                'northing': northing,             
                'postcode': result['code'],
                'url': url  }
    else:
        return None

def google_postcode(postcode):
    result = google_geocode(postcode)
    if not result or not result.get('postcode'):
        return None
    else:
        return result

#reverse Geocode
def google_reverse(x, y):
    location = str(y) + ',' + str(x)
    geo_args = {
        'sensor': 'false',
        'latlng': location,
        'region': 'uk'
    }
    url = 'http://maps.googleapis.com/maps/api/geocode/json?' + urllib.urlencode(geo_args)
    try:
        result = json.load(urllib2.urlopen(url, None, GEO_TIMEOUT))
    except:
        return None
    if DEBUG: print 'Result', result
    if result and result['status'] == 'OK':
        for res in result['results']:
            if len(res['types']) == 1 and 'postal_code' in res['types']:
                postcode = None
                for comp in res['address_components']:
                    if 'postal_code' in comp['types']:
                        postcode = comp['long_name']
                if not postcode:
                    return None
                else:
                    return { 'lat': res['geometry']['location']['lat'],
                        'lng': res['geometry']['location']['lng'],
                        'postcode': postcode,
                        'url': url  }
    else:
        return None

def yahoo_postcode(postcode, region = None):
    result = yahoo_geocode(postcode, region)
    if not result or not result.get('postcode'):
        return None
    else:
        return result

# Yahoo reverse geocode - DO NOT USE - only returns truncated postcode
def yahoo_reverse(x, y):
    location = str(y) + ' ' + str(x)
    geo_args = {
        'location': location.encode('utf-8'),
        'locale': 'en_GB',
        'flags': 'GJ', # JSON
        'gflags': 'LR' # limit to locale, reverse geocode
    }
    url = 'http://where.yahooapis.com/geocode?' + urllib.urlencode(geo_args)
    try:
        result = json.load(urllib2.urlopen(url, None, GEO_TIMEOUT))
    except:
        return None
    if DEBUG: print 'Result', result
    if result and result['ResultSet']['Found'] > 0:
        try:
            postcode = result['ResultSet']['Results'][0]['uzip']
            if not postcode: 
                postcode = result['ResultSet']['Results'][0]['postal']
        except:
            return None
        if not postcode:
            return None
        else:
            return { 'lat': float(result['ResultSet']['Results'][0]['latitude']),
                'lng': float(result['ResultSet']['Results'][0]['longitude']),
                'postcode': postcode,
                'url': url  }
    else:
        return None

# not very comprehensive and doesn't like no spaces in postcode
def nominatim_postcode(postcode):
    geo_args = {
        'q': postcode,
        'countrycodes': 'GB',  'polygon': '0',
        'format': 'json',
        'addressdetails': '1'
    }
    url = 'http://nominatim.openstreetmap.org/search/?' + urllib.urlencode(geo_args)
    try:
        result = json.load(urllib2.urlopen(url, None, GEO_TIMEOUT))
    except:
        return None
    if DEBUG: print 'Result', result
    if result:
        found = None
        for place in result:
            if place['type'] == 'postcode' and postcode_norm(place['address']['postcode']) == postcode_norm(postcode):
                found = place
                break
        if not found:
            return None
        else:
            return { 'lat': float(found['lat']),
                'lng': float(found['lon']),
                'postcode': found['address']['postcode'],
                'url': url  }
    else:
        return None

def google_geocode(address): # uses Google to geocode from address
    try:
        geo_args = {
            'sensor': 'false',
            'address': address, # was address.encode('utf-8')
            'region': 'uk'
        }
        url = 'http://maps.googleapis.com/maps/api/geocode/json?' + urllib.urlencode(geo_args)
        result = json.load(urllib2.urlopen(url, None, GEO_TIMEOUT))  # 10 sec timeout
    except:
        result = None
    if DEBUG: print 'Result', result
    if result and result['status'] == 'OK' and result.get('results'):
        postcode = None
        district = None
        county = None
        for comp in result['results'][0]['address_components']:
            if not postcode and len(comp['types']) > 1 and 'postal_code' in comp['types']:
                postcode = comp['long_name'] # can be a partial postcode
            if len(comp['types']) == 1 and 'postal_code' in comp['types']:
                postcode = comp['long_name'] # can only be a full postcode
            if 'administrative_area_level_3' in comp['types']:
                district = comp['long_name']
            if 'administrative_area_level_2' in comp['types']:
                county = comp['long_name']
        if county == 'Greater London':
            county = None
        if not district and county:
            district = county
            county = None
        return { 'lat': result['results'][0]['geometry']['location']['lat'],
            'lng': result['results'][0]['geometry']['location']['lng'],
            'district': district,
            'county': county,    
            'postcode': postcode,
            'url': url  }
    else:
        return None

def yahoo_geocode(address, region = None): # uses Yahoo to geocode from address - only returns partial postcode?
    try:
        geo_args = {
            'location': address, # was address.encode('utf-8')
            'locale': 'en_GB',
            'flags': 'GJ', # JSON
            'gflags': 'L' # limit to locale
        }
        url = 'http://where.yahooapis.com/geocode?' + urllib.urlencode(geo_args)
        result = json.load(urllib2.urlopen(url, None, GEO_TIMEOUT))  # 10 sec timeout
    except:
        result = None
    if DEBUG: print 'Result', result
    if result and result.get('ResultSet') and result['ResultSet'].get('Results') and result['ResultSet']['Found'] > 0:
        count = result['ResultSet']['Found']
        lat = result['ResultSet']['Results'][0]['latitude']
        lng = result['ResultSet']['Results'][0]['longitude']
        postal = result['ResultSet']['Results'][0]['uzip']
        if not postal: postal = result['ResultSet']['Results'][0]['postal']
        if region and count > 1:
            for i in result['ResultSet']['Results']:
                if i['city'] == region or i['county'] == region or i['state'] == region:
                    lat = i['latitude']
                    lng = i['longitude']
                    postal = i['uzip']
                    if not postal: postal = i['postal']
                    break
        if not postal: postal = None
        return { 'lat': float(lat),
            'lng': float(lng),
            'postcode': postal,
            'url': url  }
    else:
        return None

# determine if a point is inside a given polygon or not
# poly is a list of (x,y) pairs.
# source http://www.ariel.com.au/a/python-point-int-poly.html
def point_inside_polygon(x,y,poly):
    n = len(poly)
    inside =False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

# takes a gpx string and return all points in routes or tracksegs as a list of (xlon,ylat) pairs.
def gpx_route(gpx):
    poly = []
    tree = etree.parse(StringIO(gpx))
    root = tree.getroot()
    ns = root.nsmap[None] # get namespace
    #print '\nxmlns = %s' %ns
    if ns: ns = '{' + ns + '}'
    points=tree.findall('.//'+ns+'trkseg/'+ns+'trkpt')
    if not points:
        points=tree.findall('.//'+ns+'rte/'+ns+'rtept')
    if points:
        for point in points:
            poly.append( (float(point.get('lon')), float(point.get('lat')) ))
    return poly

if __name__ == 'scraper':

    #print yahoo_geocode('FIVEOAK BOARDING, HILL FARRANCE')
    #sys.exit()

    print postcode_reverse('-1.354', '53.430')
    res = geocode_postcode('S60 2LT')
    print res
    res = geocode('24 Haydon Grove Flanderwell Rotherham')
    print res
    #test = { 'address': '24 Haydon Grove Flanderwell Rotherham' }
    #test = { 'lng': '-1.354', 'lat': '53.430' }
    test = { 'postcode': 'LD3 8ER' }
    set_latlngpost(test)
    print test

    print get_postcode_best_source(' N16    5') 
    print get_postcode_best_source(' N16    5JE')
    print get_postcode_best_source(' JE5 6Xu')

    url = 'http://osmrm.openstreetmap.de/gpx.jsp?relation=357283' 
    response = urllib2.urlopen(url, None, GEO_TIMEOUT)
    gpx = response.read()
    brecpoly = gpx_route(gpx)
    print brecpoly[:10]
    print point_inside_polygon(-1.354, 53.429, brecpoly) # outside
    print point_inside_polygon(-3.48856562759, 51.924984776, brecpoly) # inside
    



