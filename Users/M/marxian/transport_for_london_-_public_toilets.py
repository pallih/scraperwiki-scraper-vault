import scraperwiki
from geopy import geocoders 
from geopy.geocoders.google import GQueryError
import xlrd
import urllib2
import csv
import string


xlbin = scraperwiki.scrape("http://publicloo.neontribe.co.uk/data/tfl-public-toilets-gla.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0)    
ONS_CODE = "TfL"

locations = [x for x in csv.DictReader(urllib2.urlopen("http://publicloo.neontribe.co.uk/data/StationLocation.csv"))]

def getLocation(name):
    for station in locations:
        if name.startswith(station['Station Name']):
            return {"lat": station['Latitude'][2:],
                    "lng": station['Longitude'].replace("E ", "+").replace("W ", "-")}

# We need to transform most of this data through 90 degrees...
# Make a store of header values  - which we find in column B
fields = sheet.col_values(1, 1) # grab the values from the field column (omit the header)

for loodex in range (4, sheet.ncols):
    rawloo = {}
    col = sheet.col_values(loodex, 1)
    for fdex, field in enumerate(fields):
        if col[fdex]: # Column has data for this field
            val = col[fdex]
            if val == 'y' or val == 'Y':
                val = True
            if val == 'n' or val == 'N':
                val = False
            rawloo[field] = val

    cleaned_data = {'ons_code': ONS_CODE }
    cleaned_data['name'] = rawloo[u'Name of building / park / location']    
    cleaned_data['address'] = ', '.join([cleaned_data['name'].split('(')[0]])
        
    #Horrid Hack
    cleaned_data['postcode'] = cleaned_data['address']
        
       
    # Geocoding is tricky here since there's no explicit locational data
    # We know all of these are libraries so:
    #g = geocoders.Google(api_key="AIzaSyBrWEbkKvx4B7TOHi1Ye0BtWzgJXFFcQG0", domain='maps.google.co.uk')    
    #place, (lat, lng) = g.geocode(cleaned_data['address'])
    try:
        point = getLocation(cleaned_data['address'])
        cleaned_data['WGS84_lat'] = point['lat']
        cleaned_data['WGS84_long'] = point['lng']
        cleaned_data['disabled'] = rawloo.get('Is it wheelchair accessible?', False)
        cleaned_data['babychanging'] = rawloo.get('Does it have babychange facilities?', False)
        scraperwiki.sqlite.save(unique_keys=['name', 'address'], data=cleaned_data)
    except:
        print "FAILED: " + cleaned_data['name']
    


import scraperwiki
from geopy import geocoders 
from geopy.geocoders.google import GQueryError
import xlrd
import urllib2
import csv
import string


xlbin = scraperwiki.scrape("http://publicloo.neontribe.co.uk/data/tfl-public-toilets-gla.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0)    
ONS_CODE = "TfL"

locations = [x for x in csv.DictReader(urllib2.urlopen("http://publicloo.neontribe.co.uk/data/StationLocation.csv"))]

def getLocation(name):
    for station in locations:
        if name.startswith(station['Station Name']):
            return {"lat": station['Latitude'][2:],
                    "lng": station['Longitude'].replace("E ", "+").replace("W ", "-")}

# We need to transform most of this data through 90 degrees...
# Make a store of header values  - which we find in column B
fields = sheet.col_values(1, 1) # grab the values from the field column (omit the header)

for loodex in range (4, sheet.ncols):
    rawloo = {}
    col = sheet.col_values(loodex, 1)
    for fdex, field in enumerate(fields):
        if col[fdex]: # Column has data for this field
            val = col[fdex]
            if val == 'y' or val == 'Y':
                val = True
            if val == 'n' or val == 'N':
                val = False
            rawloo[field] = val

    cleaned_data = {'ons_code': ONS_CODE }
    cleaned_data['name'] = rawloo[u'Name of building / park / location']    
    cleaned_data['address'] = ', '.join([cleaned_data['name'].split('(')[0]])
        
    #Horrid Hack
    cleaned_data['postcode'] = cleaned_data['address']
        
       
    # Geocoding is tricky here since there's no explicit locational data
    # We know all of these are libraries so:
    #g = geocoders.Google(api_key="AIzaSyBrWEbkKvx4B7TOHi1Ye0BtWzgJXFFcQG0", domain='maps.google.co.uk')    
    #place, (lat, lng) = g.geocode(cleaned_data['address'])
    try:
        point = getLocation(cleaned_data['address'])
        cleaned_data['WGS84_lat'] = point['lat']
        cleaned_data['WGS84_long'] = point['lng']
        cleaned_data['disabled'] = rawloo.get('Is it wheelchair accessible?', False)
        cleaned_data['babychanging'] = rawloo.get('Does it have babychange facilities?', False)
        scraperwiki.sqlite.save(unique_keys=['name', 'address'], data=cleaned_data)
    except:
        print "FAILED: " + cleaned_data['name']
    


