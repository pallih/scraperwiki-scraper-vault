import scraperwiki
import re
import time
import urlparse
from scraperwiki.sqlite import save

base_url = "http://parking.greenp.com/parking-info/carpark-info.html?page="
base_number = 1

columns = [
    'Address', 'Facility Type','Capacity','Bike Racks','Payment Options','Accepted Payment','LatLong','Rates Halfhour','Rates Day','Rates Night'
]

def subscraper(suburl):
    subpage = scraperwiki.scrape(suburl)
    relevantpage = re.search('lot-summary(.+?)Location Information', subpage, re.DOTALL|re.S)
    relevantpage = relevantpage.group(0)
    address = re.search('Address:(.+?)<', relevantpage)
    address = re.sub('</strong>', "", address.group(1))
    address = re.sub('<', "", address)
    facility = re.search('Facility Type:(.+?)<', relevantpage)
    facility = re.sub('</strong>', "", facility.group(1))
    facility = re.sub('<', "", facility)
    capacity = re.search('Capacity:(.+?)<', relevantpage)
    capacity = re.sub('</strong>', "", capacity.group(1))
    capacity = re.sub('<', "", capacity)
    capacity = re.sub(' Spaces', "", capacity)
    bikes = "Not Available"
    halfhour = "None"        
    night = "undefined"
    day = "undefined"
    if re.search('Bike Racks:(.+?)<', relevantpage):
        bikes = re.search('Bike Racks:(.+?)<', relevantpage)
        bikes = re.sub('</strong>', "", bikes.group(1))
        bikes = re.sub('<', "", bikes)
    payment = re.search('Payment Options:(.+?)<', relevantpage)
    payment = re.sub('</strong>', "", payment.group(1))
    payment = re.sub('<', "", payment)
    accepted = re.search('Accepted Forms of Payment:(.+?)<', relevantpage)
    accepted = re.sub('</strong>', "", accepted.group(1))
    accepted = re.sub('<', "", accepted)
    latlong = re.search('var point = new GLatLng\((.+?)\);', subpage)
    latlong = re.sub("'", "", latlong.group(1))
    if re.search('half-hour-rate', relevantpage): 
        halfhour = re.search('half-hour-rate(.+?)<', relevantpage)
        halfhour = re.sub('">\$', "", halfhour.group(1))
        halfhour = re.sub(' / Half Hour', "", halfhour)
    if re.search('Any \d+ ho?u?r Period', relevantpage):
        day = re.search('Any \d+ ho?u?r Period(.+?)\$(.+?)<', relevantpage)
        day = re.sub('<', "", day.group(2))
        night = day
        relevantpage = "already processed"
    if re.search('\([0-9]pm(.+?)[0-9]pm\):(.+?);(.+?)<', relevantpage):
        night = re.search('[0-9]pm(.+?)-(.+?)[0-9]pm(.+?); (.+?)<', relevantpage)
        night = re.sub('<', "", night.group(4))
        night = re.sub('&nbsp;', "", night)
        night = re.sub('\$', "", night)
        day = night
        relevantpage = "already processed"
    if re.search('\([0-9]am(.+?)[0-9]pm\)', relevantpage, re.DOTALL|re.S):
        day = re.search('[0-9]am(.+?)[0-9]pm\):(.+?);(.+?)<', relevantpage)
        day = re.sub('<', "", day.group(3))
        day = re.sub('&nbsp;', "", day)
        day = re.sub('\$', "", day)
    if re.search('[0-9]pm(.+?)[0-9](&nbsp;)?am\):(.+?);(.+?)<', relevantpage, re.DOTALL|re.S):
        night = re.search('[0-9]pm(.+?)[0-9](&nbsp;)?am\):(.+?);(.+?)<', relevantpage)
        night = re.sub('<', "", night.group(4)) 
        night = re.sub('&nbsp;', "", night)
        night = re.sub('\$', "", night)
        relevantpage = "already processed"
    if re.search('\([0-9]am(.+?)[0-9]am\):(.+?);(.+?)<', relevantpage):
        day = re.search('[0-9]am(.+?)[0-9]am(.+?); (.+?)<', relevantpage)
        day = re.sub('<', "", day.group(3))
        day = re.sub('&nbsp;', "", day)
        day = re.sub('\$', "", day)
        night = day
        relevantpage = "already processed"
    if night == "undefined":
         night = day
    if day == "undefined":
         day = night
    row_data = {'Address': address, 'Facility Type': facility, 'Capacity': capacity, 'Bike Racks': bikes, 'Payment Options': payment, 'Accepted Payment': accepted, 'LatLong': latlong, 'Rates Halfhour': halfhour, 'Rates Day': day, 'Rates Night': night}
    save([],row_data)

def lot_scraper(page_url):
    the_page = scraperwiki.scrape(page_url)
    base_suburl = "http://parking.greenp.com/"
    base_subnumber = 1
    for every_post in re.finditer('carpark-name(.+?)">', the_page, re.DOTALL|re.S):
        suburl = every_post.group(1)
        suburl = re.sub('"><a href="', "", suburl)
        suburl = "http://parking.greenp.com" + suburl
        subscraper(suburl)
        time.sleep(10)

while base_number < 18: 
    page_url = base_url + str(base_number)
    lot_scraper(page_url)
    base_number = base_number + 1
    time.sleep(10)
import scraperwiki
import re
import time
import urlparse
from scraperwiki.sqlite import save

base_url = "http://parking.greenp.com/parking-info/carpark-info.html?page="
base_number = 1

columns = [
    'Address', 'Facility Type','Capacity','Bike Racks','Payment Options','Accepted Payment','LatLong','Rates Halfhour','Rates Day','Rates Night'
]

def subscraper(suburl):
    subpage = scraperwiki.scrape(suburl)
    relevantpage = re.search('lot-summary(.+?)Location Information', subpage, re.DOTALL|re.S)
    relevantpage = relevantpage.group(0)
    address = re.search('Address:(.+?)<', relevantpage)
    address = re.sub('</strong>', "", address.group(1))
    address = re.sub('<', "", address)
    facility = re.search('Facility Type:(.+?)<', relevantpage)
    facility = re.sub('</strong>', "", facility.group(1))
    facility = re.sub('<', "", facility)
    capacity = re.search('Capacity:(.+?)<', relevantpage)
    capacity = re.sub('</strong>', "", capacity.group(1))
    capacity = re.sub('<', "", capacity)
    capacity = re.sub(' Spaces', "", capacity)
    bikes = "Not Available"
    halfhour = "None"        
    night = "undefined"
    day = "undefined"
    if re.search('Bike Racks:(.+?)<', relevantpage):
        bikes = re.search('Bike Racks:(.+?)<', relevantpage)
        bikes = re.sub('</strong>', "", bikes.group(1))
        bikes = re.sub('<', "", bikes)
    payment = re.search('Payment Options:(.+?)<', relevantpage)
    payment = re.sub('</strong>', "", payment.group(1))
    payment = re.sub('<', "", payment)
    accepted = re.search('Accepted Forms of Payment:(.+?)<', relevantpage)
    accepted = re.sub('</strong>', "", accepted.group(1))
    accepted = re.sub('<', "", accepted)
    latlong = re.search('var point = new GLatLng\((.+?)\);', subpage)
    latlong = re.sub("'", "", latlong.group(1))
    if re.search('half-hour-rate', relevantpage): 
        halfhour = re.search('half-hour-rate(.+?)<', relevantpage)
        halfhour = re.sub('">\$', "", halfhour.group(1))
        halfhour = re.sub(' / Half Hour', "", halfhour)
    if re.search('Any \d+ ho?u?r Period', relevantpage):
        day = re.search('Any \d+ ho?u?r Period(.+?)\$(.+?)<', relevantpage)
        day = re.sub('<', "", day.group(2))
        night = day
        relevantpage = "already processed"
    if re.search('\([0-9]pm(.+?)[0-9]pm\):(.+?);(.+?)<', relevantpage):
        night = re.search('[0-9]pm(.+?)-(.+?)[0-9]pm(.+?); (.+?)<', relevantpage)
        night = re.sub('<', "", night.group(4))
        night = re.sub('&nbsp;', "", night)
        night = re.sub('\$', "", night)
        day = night
        relevantpage = "already processed"
    if re.search('\([0-9]am(.+?)[0-9]pm\)', relevantpage, re.DOTALL|re.S):
        day = re.search('[0-9]am(.+?)[0-9]pm\):(.+?);(.+?)<', relevantpage)
        day = re.sub('<', "", day.group(3))
        day = re.sub('&nbsp;', "", day)
        day = re.sub('\$', "", day)
    if re.search('[0-9]pm(.+?)[0-9](&nbsp;)?am\):(.+?);(.+?)<', relevantpage, re.DOTALL|re.S):
        night = re.search('[0-9]pm(.+?)[0-9](&nbsp;)?am\):(.+?);(.+?)<', relevantpage)
        night = re.sub('<', "", night.group(4)) 
        night = re.sub('&nbsp;', "", night)
        night = re.sub('\$', "", night)
        relevantpage = "already processed"
    if re.search('\([0-9]am(.+?)[0-9]am\):(.+?);(.+?)<', relevantpage):
        day = re.search('[0-9]am(.+?)[0-9]am(.+?); (.+?)<', relevantpage)
        day = re.sub('<', "", day.group(3))
        day = re.sub('&nbsp;', "", day)
        day = re.sub('\$', "", day)
        night = day
        relevantpage = "already processed"
    if night == "undefined":
         night = day
    if day == "undefined":
         day = night
    row_data = {'Address': address, 'Facility Type': facility, 'Capacity': capacity, 'Bike Racks': bikes, 'Payment Options': payment, 'Accepted Payment': accepted, 'LatLong': latlong, 'Rates Halfhour': halfhour, 'Rates Day': day, 'Rates Night': night}
    save([],row_data)

def lot_scraper(page_url):
    the_page = scraperwiki.scrape(page_url)
    base_suburl = "http://parking.greenp.com/"
    base_subnumber = 1
    for every_post in re.finditer('carpark-name(.+?)">', the_page, re.DOTALL|re.S):
        suburl = every_post.group(1)
        suburl = re.sub('"><a href="', "", suburl)
        suburl = "http://parking.greenp.com" + suburl
        subscraper(suburl)
        time.sleep(10)

while base_number < 18: 
    page_url = base_url + str(base_number)
    lot_scraper(page_url)
    base_number = base_number + 1
    time.sleep(10)
