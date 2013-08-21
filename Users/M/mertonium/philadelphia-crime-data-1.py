###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import urllib
import urllib2
import simplejson
import datetime
from BeautifulSoup import BeautifulSoup
from datetime import timedelta
import sys


# define the order our columns are displayed in the datastore
scraperwiki.sqlite.save_var('data_columns', ['crimeclass','Dc_key', 'Ucr', 'Ucr_text', 'Location', 'Dispatch_date_time', 'Dc_dist', 'Sector','Premise_text', 'X_coord', 'Y_coord'])

# Create a function to return a list of crime types
def get_crime_categories(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)

    options = soup.find("select", { "id" : "ctl00_ContentPlaceHolder1_ddlCrimeType" }).findAll("option")
    crime_categories= []
    for option in options:
        val = option['value']
        if val != '':
            crime_categories.append(val)

    return crime_categories

def normalize_address(address):
    return (address or '').replace('BLOCK', '')

# retrieve the starting page
starting_url = 'http://citymaps.phila.gov/CrimeMap/StepByStep.aspx'

# collect all the different types of crimes
crime_cats = get_crime_categories(starting_url)

# Setup our dates
now = datetime.datetime.now()
end_date = now.strftime("%m/%d/%Y")
tdelta = timedelta(days=1);  # set the start & end dates to be one day apart
start_date = (now-tdelta).strftime("%m/%d/%Y")


# query the page with each one of the crime categories
for crime_cat in crime_cats:
    crime_url = 'http://citymaps.phila.gov/CrimeMap/MappingServices.asmx/GetIncidentsByCriteria'
    values = '{"crimeclass":'+crime_cat+',"from":"'+start_date+'","to":"'+end_date+'","bounds":"2606470.5,211682,2812260.5,289682"}'
    
    # The page is expecting json data so we need to change our POST header
    headers = { 'Content-type' : 'application/json', 'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16','Referer':'http://citymaps.phila.gov/CrimeMap/map.aspx'}    
    req = urllib2.Request(crime_url, values, headers)
    print crime_url
    print values
    print headers
    print req.headers
#    try:
    response = urllib2.urlopen(req)


    # Get our list of crimes of this particular type over the selected time period
    crime_list = simplejson.loads(response.read())

    # Set up our data record - we'll need it later
    record = {}

    # Loop through each type of crime
    for crime in crime_list:
        record['crimeclass'] = crime_cat
        record['Dc_key'] = crime['Dc_key']
        record['Ucr'] = crime['Ucr']
        record['Ucr_text'] = crime['Ucr_text']
        record['Location'] = crime['Location']
        # Strip the js 'Date' function & convert the timestamp
        dispatch_date = crime['Dispatch_date_time']
        dispatch_date = dispatch_date.replace('/Date(','');
        dispatch_date = dispatch_date.replace(')/','');
        record['Dispatch_date_time'] = datetime.datetime.fromtimestamp(float(dispatch_date)//1000)
        record['Dc_dist'] = crime['Dc_dist']
        record['Sector'] = crime['Sector']
        record['Premise_text'] = crime['Premise_text']
        record['X_coord'] = crime['X_coord']
        record['Y_coord'] = crime['Y_coord']

        # Geocode the address
        #geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote_plus(normalize_address(record['Location']))+'+Philadelphia,+PA&sensor=false&output=json'
        #print geocode_url
        #georeq = urllib2.Request(geocode_url)
        #geo_response = urllib2.urlopen(georeq)
        #geocode = simplejson.loads(geo_response.read())
        #if geocode['status'] != 'ZERO_RESULTS':
        #    crime_lat = geocode['results'][0]['geometry']['location']['lat']
        #    crime_lng = geocode['results'][0]['geometry']['location']['lng']

        # ESRI Locator service
        # - Currently USA addresses only
        # - Unlimited geocoding using the method below (there are restrictions on batch geocoding: http://www.arcgis.com/home/item.html?id=41e621023bed4304b2a78e9d8b5ce67d )
        geocode_url = 'http://tasks.arcgisonline.com/ArcGIS/rest/services/Locators/TA_Streets_US_10/GeocodeServer/findAddressCandidates?Single+Line+Input='+urllib.quote_plus(normalize_address(record['Location']))+'+Philadelphia,+PA&outFields=&outSR=&f=json'
        print geocode_url
        georeq = urllib2.Request(geocode_url)
        geo_response = urllib2.urlopen(georeq)
        geocode = simplejson.loads(geo_response.read())
        print geocode
        if len(geocode['candidates']):
            crime_lat = geocode['candidates'][0]['location']['y']
            crime_lng = geocode['candidates'][0]['location']['x']
        
        print crime_lat 
        print crime_lng

        # backwards-compat only
        record['date'] = record['Dispatch_date_time']
        record['latlng_lat'] = crime_lat
        record['latlng_lng'] = crime_lng

        # Finally, save the record to the datastore - 'Dc_key' is our unique key
        scraperwiki.sqlite.save(unique_keys=['Dc_key'], data=record)
#    except:
#        print "Error: ",sys.exc_info()[0]