import scraperwiki
import re
import time
import urlparse
from scraperwiki.sqlite import save

base_url = "http://www.timhortons.com/ca/locator/storedirections.html?id="

columns = [
    'Address', 'City', 'Latlong','Phone','Postal Code','Store ID'
]

idcount = 100001

def locationscraper(locationpagesource, idcount):
    address = "not available"
    storeid = "error"
    latlong = "none"
    phone = "none"
    postal = "none"
    city = re.search('BR/>(.+?),', locationpagesource, re.I)
    city = city.group(1)
    city = re.sub("<BR/>", ", ", city)
    storeid = idcount
    latlong = re.search("init\((.+?),'<", locationpagesource)
    latlong = re.sub("'", "", latlong.group(1))
    if re.search('\(\d{3}\) \d{3}-\d{4}', locationpagesource, re.DOTALL|re.S|re.I):
        phone = re.search('\(\d{3}\) \d{3}-\d{4}', locationpagesource, re.DOTALL|re.S|re.I)
        phone = phone.group(0)
    if re.search('\D\d\D \d\D\d', locationpagesource):
        postal = re.search('\D\d\D \d\D\d', locationpagesource)
        postal = postal.group(0)
    row_data = {'Address': city, 'Latlong': latlong, 'Phone': phone, 'Postal Code': postal, 'Store ID': storeid}
    try: 
        save([],row_data)
    except: 
        city = "Address unavailable"
        row_data = {'Address': city, 'Latlong': latlong, 'Phone': phone, 'Postal Code': postal, 'Store ID': storeid}
        save([],row_data)
        
while idcount < 200000: 
    trycount = 0
    while trycount < 3:
        try: 
            locationpage = base_url + str(idcount)
            locationpagesource = scraperwiki.scrape(locationpage)
            if re.search("init\('\d+", locationpagesource):
                locationscraper(locationpagesource, idcount)
            trycount = 4
        except:
            trycount = trycount +1
    idcount = idcount + 1
    time.sleep(1)

    
import scraperwiki
import re
import time
import urlparse
from scraperwiki.sqlite import save

base_url = "http://www.timhortons.com/ca/locator/storedirections.html?id="

columns = [
    'Address', 'City', 'Latlong','Phone','Postal Code','Store ID'
]

idcount = 100001

def locationscraper(locationpagesource, idcount):
    address = "not available"
    storeid = "error"
    latlong = "none"
    phone = "none"
    postal = "none"
    city = re.search('BR/>(.+?),', locationpagesource, re.I)
    city = city.group(1)
    city = re.sub("<BR/>", ", ", city)
    storeid = idcount
    latlong = re.search("init\((.+?),'<", locationpagesource)
    latlong = re.sub("'", "", latlong.group(1))
    if re.search('\(\d{3}\) \d{3}-\d{4}', locationpagesource, re.DOTALL|re.S|re.I):
        phone = re.search('\(\d{3}\) \d{3}-\d{4}', locationpagesource, re.DOTALL|re.S|re.I)
        phone = phone.group(0)
    if re.search('\D\d\D \d\D\d', locationpagesource):
        postal = re.search('\D\d\D \d\D\d', locationpagesource)
        postal = postal.group(0)
    row_data = {'Address': city, 'Latlong': latlong, 'Phone': phone, 'Postal Code': postal, 'Store ID': storeid}
    try: 
        save([],row_data)
    except: 
        city = "Address unavailable"
        row_data = {'Address': city, 'Latlong': latlong, 'Phone': phone, 'Postal Code': postal, 'Store ID': storeid}
        save([],row_data)
        
while idcount < 200000: 
    trycount = 0
    while trycount < 3:
        try: 
            locationpage = base_url + str(idcount)
            locationpagesource = scraperwiki.scrape(locationpage)
            if re.search("init\('\d+", locationpagesource):
                locationscraper(locationpagesource, idcount)
            trycount = 4
        except:
            trycount = trycount +1
    idcount = idcount + 1
    time.sleep(1)

    
