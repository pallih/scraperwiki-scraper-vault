# Try out with The Hague restaurants only
import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import urllib

# setup the record format
# scraperwiki.sqlite.save_var('data_columns', ['City', 'Name', 'Address', 'Type', 'Score', 'More'])

## based on http://code.activestate.com/recipes/498128/
def getLatLong(address):
    # Add NL country code for more accuracy
    address = address + ', NL'

    # Encode query string into URL
    query_args = { 'q':address, 'output':'js' }
    encoded_args = urllib.urlencode(query_args)

    url = 'http://maps.google.com/?' + encoded_args
    print '\nGmaps Query: %s' % (url)
    
    xml = scraperwiki.scrape(url)

    if xml:
        if '<error>' in xml:
            return False
        else:
            # Strip lat/long coordinates from XML
            lat,lng = 0.0,0.0
            # example: {center:{lat:52.036596000000003,lng:4.2170610000000002}
            center = xml[xml.find('{center')+9:xml.find('}',xml.find('{center'))]
            center = center.replace('lat:','').replace('lng:','') 
            lat,lng = center.split(',')
            print '\nCoordinates found! (%s, %s) for address: %s' % (lat,lng, address)

    return float(lat),float(lng)


def getFoursquared(name, city):
    
    # Encode query string into URL
    query_args = { 'q': name, 'near': city }
    encoded_args = urllib.urlencode(query_args)

    url = "http://foursquare.com/search?" + encoded_args

    print '\nFoursquare Query: %s' % (url)

    html = scraperwiki.scrape(url)
    
    print html

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_restaurants_for_city(city, restaurants):

    for row in restaurants:
        # Set up our data record - we'll need it later
        record = {}

        # set city for this record
        record['City'] = city

        # get and set the score for this record
        scoreval = 0.0
        score = row.find("td", { "width" : "70" })
        
        #print score

        if score: 
            scoreval = score.find("div").text

        if is_number(scoreval):
            record['Score'] = float(scoreval)
        else:
            record['Score'] = ""

        table_cells = row.findAll("td")
        #print table_cells
        if table_cells: 
            name = table_cells[0].find("span", { "class" : "restname" })
            morelink = table_cells[0].find("a")
            atmp = table_cells[0].find("span", { "class" : "restaddress" })
            #score = table_cells[2].find("div")
            if name and atmp:
                address = atmp.text
                asplit = address.rpartition(",")
                #print asplit
                record['Name'] = name.text
                record['Address'] = asplit[0]
                record['Type'] = asplit[2]
                # for adding linklove back to the Iens website
                record['More'] = 'http://iens.nl' + morelink["href"]
                latlng = (0.0, 0.0)
                try:
                    latlng = getLatLong(asplit[0])
                    #print latlng
                except:
                    print "Google failed to do it's thing"
                
                #try:
                #    fsdata = getFoursquared(name.text, city)
                #except:
                #    print "Could not get anything from Foursquare"
                
                # Finally, save the record to the datastore - 'Name + Address' is our unique key
                record['date'] = datetime.now()
                record['latlng'] = latlng
                scraperwiki.sqlite.save(["Name", "Address"], record)
                # Print out the data we've gathered
                print record

# walk through all pages until we there are no more restaurants on the page
def follow_pages(base_url, num = 1):
    
    query_args = { 'f':num, 'o':'n' }
    encoded_args = urllib.urlencode(query_args)

    url = base_url + '?' + encoded_args

    #print url    

    try:
        html = scraperwiki.scrape(url)
    except URLError:
        pass

    if html:
        soup = BeautifulSoup(html)
        
        rest_links = soup.find("table", { "id" : "restlist" })
        restaurants = rest_links.findAll("tr")
    
        #print restaurants
        
        # we have to count results since there is no 404 returned for empty result pages
        if len(restaurants) > 1:
            get_restaurants_for_city('Den Haag', restaurants)
            num = num + 1
            follow_pages(base_url, num)


base_url = 'http://www.iens.nl/restaurant/denhaag'
follow_pages(base_url)
