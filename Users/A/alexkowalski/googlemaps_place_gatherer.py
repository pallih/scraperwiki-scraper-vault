import scraperwiki
from lxml import etree
import re
from StringIO import StringIO
from time import sleep

def get_inputs(start_url):
    key = "&key=" #Enter API key
    coordinates = "location=38.900097,-76.984278" #Enter latitude and longitude of central point; be sure to change street in loop below
    radius = "&radius=250"
    sensor = "&sensor=false"
    establishment_type = ['accounting', 'airport' 'amusement_park','aquarium', 'art_gallery', 'atm', 'bakery','bank','bar','beauty_salon','bicycle_store','book_store','bowling_alley','cafe','campground','car_dealer','car_rental','car_repair','car_wash','casino','cemetery',
'church','city_hall','clothing_store','convenience_store','courthouse','dentist','department_store','doctor','electrician','electronics_store',
'embassy','finance','fire_station','florist','food','funeral_home','furniture_store','gas_station','general_contractor','grocery_or_supermarket',
'gym','hair_care','hardware_store','health','hindu_temple','home_goods_store','hospital','insurance_agency','jewelry_store','laundry','lawyer','library','liquor_store',
'local_government_office','locksmith','lodging','meal_delivery','meal_takeaway','mosque','movie_rental','movie_theater','moving_company','museum','night_club','painter'
'park','parking','pet_store','pharmacy','physiotherapist','place_of_worship','plumber','police','post_office','real_estate_agency','restaurant','roofing_contractor','rv_park',
'school','shoe_store','shopping_mall','spa','stadium','storage','store','synagogue','taxi_stand','travel_agency','university','veterinary_care','zoo']

    for item in establishment_type:
        product_url = start_url + coordinates + radius + "&types=" + item + sensor + key
        get_data(product_url)

def get_data(input_url):

    x = 0

    url = input_url

    while x <= 2:
        
        url_data = scrape_url(url)
    
        street_info = url_data.findall('/result')
        
        status = url_data.findtext('/status')

        get_street_data(street_info, status)
    
        page_token = url_data.findtext('/next_page_token')
     
        if page_token != None:
            if "&pagetoken" in url:
                split_url = url.split("&pagetoken")
                url = split_url[0] + "&pagetoken=" + page_token
                sleep(2)
                x += 1
            else:
                url = url + "&pagetoken=" + page_token
                sleep(2)
                x += 1
        else:
            x += 1


def scrape_url(input):

    xml = scraperwiki.scrape(input)

    data = etree.parse(StringIO(xml), parser=etree.XMLParser())

    return data
   

def get_street_data(street_data, establishment_status):

    establishment_data = {}

    establishments = []

    if "OK" in establishment_status:

        for item in street_data:
                if 'H' in item.findtext("vicinity"): #Change street title for each (and `and 'street_type'' if issue)
                    address = item.findtext("vicinity")
                    a = re.split(' |, ', address)
                    establishment_data['Address'] = a[0]
                    establishment_data['Street'] = a[1]
                    establishment_data['Quadrant'] = a[3]
                    establishment_data['Name'] = item.findtext("name")
                    establishment_data['Type'] = item.findtext("type")
                    establishment_data['Rating'] = item.findtext("rating")
                    establishment_data['id'] = item.findtext("id")
                    establishment_data['Age'] = "n/a"
                    establishment_data['Area'] = "n/a"
                    establishment_data['Residential'] = "n/a"
                    establishment_data['Office'] = "n/a"
                    #scraperwiki.sqlite.save(["id"], establishment_data)
                    establishments.append(establishment_data)
                    establishment_data = {}
        print establishments


get_inputs("https://maps.googleapis.com/maps/api/place/search/xml?")


import scraperwiki
from lxml import etree
import re
from StringIO import StringIO
from time import sleep

def get_inputs(start_url):
    key = "&key=" #Enter API key
    coordinates = "location=38.900097,-76.984278" #Enter latitude and longitude of central point; be sure to change street in loop below
    radius = "&radius=250"
    sensor = "&sensor=false"
    establishment_type = ['accounting', 'airport' 'amusement_park','aquarium', 'art_gallery', 'atm', 'bakery','bank','bar','beauty_salon','bicycle_store','book_store','bowling_alley','cafe','campground','car_dealer','car_rental','car_repair','car_wash','casino','cemetery',
'church','city_hall','clothing_store','convenience_store','courthouse','dentist','department_store','doctor','electrician','electronics_store',
'embassy','finance','fire_station','florist','food','funeral_home','furniture_store','gas_station','general_contractor','grocery_or_supermarket',
'gym','hair_care','hardware_store','health','hindu_temple','home_goods_store','hospital','insurance_agency','jewelry_store','laundry','lawyer','library','liquor_store',
'local_government_office','locksmith','lodging','meal_delivery','meal_takeaway','mosque','movie_rental','movie_theater','moving_company','museum','night_club','painter'
'park','parking','pet_store','pharmacy','physiotherapist','place_of_worship','plumber','police','post_office','real_estate_agency','restaurant','roofing_contractor','rv_park',
'school','shoe_store','shopping_mall','spa','stadium','storage','store','synagogue','taxi_stand','travel_agency','university','veterinary_care','zoo']

    for item in establishment_type:
        product_url = start_url + coordinates + radius + "&types=" + item + sensor + key
        get_data(product_url)

def get_data(input_url):

    x = 0

    url = input_url

    while x <= 2:
        
        url_data = scrape_url(url)
    
        street_info = url_data.findall('/result')
        
        status = url_data.findtext('/status')

        get_street_data(street_info, status)
    
        page_token = url_data.findtext('/next_page_token')
     
        if page_token != None:
            if "&pagetoken" in url:
                split_url = url.split("&pagetoken")
                url = split_url[0] + "&pagetoken=" + page_token
                sleep(2)
                x += 1
            else:
                url = url + "&pagetoken=" + page_token
                sleep(2)
                x += 1
        else:
            x += 1


def scrape_url(input):

    xml = scraperwiki.scrape(input)

    data = etree.parse(StringIO(xml), parser=etree.XMLParser())

    return data
   

def get_street_data(street_data, establishment_status):

    establishment_data = {}

    establishments = []

    if "OK" in establishment_status:

        for item in street_data:
                if 'H' in item.findtext("vicinity"): #Change street title for each (and `and 'street_type'' if issue)
                    address = item.findtext("vicinity")
                    a = re.split(' |, ', address)
                    establishment_data['Address'] = a[0]
                    establishment_data['Street'] = a[1]
                    establishment_data['Quadrant'] = a[3]
                    establishment_data['Name'] = item.findtext("name")
                    establishment_data['Type'] = item.findtext("type")
                    establishment_data['Rating'] = item.findtext("rating")
                    establishment_data['id'] = item.findtext("id")
                    establishment_data['Age'] = "n/a"
                    establishment_data['Area'] = "n/a"
                    establishment_data['Residential'] = "n/a"
                    establishment_data['Office'] = "n/a"
                    #scraperwiki.sqlite.save(["id"], establishment_data)
                    establishments.append(establishment_data)
                    establishment_data = {}
        print establishments


get_inputs("https://maps.googleapis.com/maps/api/place/search/xml?")


