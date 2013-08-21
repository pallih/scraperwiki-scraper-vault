import scraperwiki
import re
import time
import urlparse
from scraperwiki.sqlite import save

base_url = "http://www.starbucks.ca/store/"

columns = [
    'Address', 'City', 'Country', 'Lat', 'long','Phone','Store ID'
]

idcount = 1

def locationscraper(locationpagesource, idcount):
    address = "not available"
    storeid = "error"
    lat = "none"
    longitude = "none"
    phone = "None available"
    country = "Not listed"
    city = re.search('class="locality">(.+?)<', locationpagesource, re.DOTALL|re.S)
    city = re.sub('&nbsp;', '', city.group(1))
    city = re.sub(',', '', city)
    if re.search('class="street-address"', locationpagesource):
        address = re.search('class="street-address">(.+?)<', locationpagesource, re.DOTALL|re.S)
        address = address.group(1)
    if re.search('class="country-name">(.+?)<', locationpagesource):
        country = re.search('class="country-name">(.+?)<', locationpagesource)
        country = country.group(1)
    storeid = idcount
    lat = re.search('data-store-lat="(.+?)"', locationpagesource)
    lat = lat.group(1)
    longitude = re.search('data-store-lon="(.+?)"', locationpagesource)
    longitude = longitude.group(1)
    if re.search('\d{3}-\d{3}-\d{4}', locationpagesource, re.DOTALL|re.S|re.I):
        phone = re.search('\d{3}-\d{3}-\d{4}', locationpagesource, re.DOTALL|re.S|re.I)
        phone = phone.group(0)
    row_data = {'Address': address, 'City': city, 'Country': country, 'Lat': lat, 'Long': longitude, 'Phone': phone, 'Store ID': storeid}
    save([],row_data)

while idcount < 20001: 
    locationpage = base_url + str(idcount)
    locationpagesource = scraperwiki.scrape(locationpage)
    if re.search('class="locality">(.+?)<', locationpagesource, re.DOTALL|re.S):
        if not re.search('\(Closed\)', locationpagesource):
            locationscraper(locationpagesource, idcount)
    idcount = idcount + 1
    time.sleep(2)

    
