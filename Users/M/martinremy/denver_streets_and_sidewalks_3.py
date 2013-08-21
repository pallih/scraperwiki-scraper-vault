import scraperwiki
import urllib
import urllib2
import re
import simplejson
import time
import datetime
import requests
from bs4 import BeautifulSoup

# TODO -
#   Geocode addresses
#   Parse start/end date
#   Give each entry a unique ID

def get_pdf_link():
    root_url = "http://www.denvergov.org"
    main_page = "/streetclosures"
    closures_page = requests.get(root_url + main_page)

    soup = BeautifulSoup(closures_page.text)
    return root_url + soup.find(id='dnn_ctr499298_HtmlModule_lblContent').find('a').get('href')

def get_dates(date_string):
    re_date = "Start Date:\s+(\d+\/\d+\/\d+)\s+-\s+End Date:\s+(\d+\/\d+\/\d+)"
    regex = re.compile(re_date)
    r = regex.search(date_string)
    return r.groups()

def geocode(location):
    coord = []
    location += ' ,Denver, CO'
    geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote_plus(location)+'&sensor=false&output=json'
    georeq = urllib2.Request(geocode_url)
    geo_response = urllib2.urlopen(georeq)
    geocode = simplejson.loads(geo_response.read())
    # print geocode_url
    # print geocode
    #Google imposes query limits, this lets us pass a failure and have the loop sleep and try again after 2 seconds
    if geocode['status'] == "OVER_QUERY_LIMIT":
        return 0
    if geocode['status'] != 'ZERO_RESULTS':
        coord_lat = geocode['results'][0]['geometry']['location']['lat']
        coord_lon = geocode['results'][0]['geometry']['location']['lng']
        coord.append(coord_lat)
        coord.append(coord_lon)
    # print coord
    return coord

class ClosureBbox:
    def __init__(self, raw_location):
        # the raw location string
        self.raw_location = raw_location
        
    def parse(self):            
        match = re.search('^(.*)--(.*)/(.*)$', self.raw_location, re.IGNORECASE)
        if match:
            print 'RANGE [', self.raw_location, '], anchor=[', match.group(1), '], start=[', match.group(2), '], end=[', match.group(3), ']'
            return

        match = re.search('^([^-:\(,]+)[-:\(,]+(.*?)(?:-|to)(.*)$', self.raw_location, re.IGNORECASE)
        if match:
            print 'RANGE [', self.raw_location, '], anchor=[', match.group(1), '], start=[', match.group(2), '], end=[', match.group(3), ']'
            return

url = get_pdf_link()

xml = scraperwiki.pdftoxml(urllib2.urlopen(url).read())
parsed = BeautifulSoup(xml).text.split("\n")
filtered_list = parsed[parsed.index('Location: '):]
closures = []

i = 0
current_closure = -1

while i < len(filtered_list):
    text = filtered_list[i]
    if text == "Location: ":
        closures.append({})
        current_closure = len(closures) - 1
        i += 1
        closures[current_closure]['location'] = filtered_list[i]
        closure_loc = ClosureBbox(filtered_list[i])
        closure_loc.parse()
        #print filtered_list[i]
        coordinate = geocode(filtered_list[i])
        if(coordinate == 0):
            time.sleep(2)
            coordinate = geocode(filtered_list[i])
        closures[current_closure]['lat'] = coordinate[0]
        closures[current_closure]['lon'] = coordinate[1]
    elif text == "Type: ":
        i += 1
        closures[current_closure]['type'] = filtered_list[i]
    elif text == "Date: ":
        i += 1
        dates = get_dates(filtered_list[i])
        closures[current_closure]['start_date'] = datetime.datetime.strptime(dates[0], '%m/%d/%Y')
        closures[current_closure]['end_date'] = datetime.datetime.strptime(dates[1], '%m/%d/%Y')
    elif text == "Time: ":
        i += 1
        closures[current_closure]['time'] = filtered_list[i]
    elif text == "Purpose: ":
        i += 1
        closures[current_closure]['purpose'] = filtered_list[i]
    elif text == "Contractor: ":
        closures[current_closure]['contractor'] = filtered_list[i]
    
    i+= 1


for closure in closures:
    scraperwiki.sqlite.save(unique_keys=['location'], data=closure)