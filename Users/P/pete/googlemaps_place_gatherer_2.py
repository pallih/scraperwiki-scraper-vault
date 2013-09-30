import scraperwiki
from lxml import etree
import re
from StringIO import StringIO
from time import sleep

def get_inputs(start_url):
    key = "&key=AIzaSyCrmKDAuSEI0gV1CCjOjYj16hyqKOdBFmU" #Enter API key
    coordinates = "location=40.797177,-73.963497" #Enter latitude and longitude of central point; be sure to change street in loop below
    radius = "&radius=1500"
    sensor = "&sensor=false"
    establishment_type = ['accounting']

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
                    scraperwiki.sqlite.save(["id"], establishment_data)
                    establishments.append(establishment_data)
                    establishment_data = {}
        #print establishments


get_inputs("https://maps.googleapis.com/maps/api/place/search/xml?")


import scraperwiki
from lxml import etree
import re
from StringIO import StringIO
from time import sleep

def get_inputs(start_url):
    key = "&key=AIzaSyCrmKDAuSEI0gV1CCjOjYj16hyqKOdBFmU" #Enter API key
    coordinates = "location=40.797177,-73.963497" #Enter latitude and longitude of central point; be sure to change street in loop below
    radius = "&radius=1500"
    sensor = "&sensor=false"
    establishment_type = ['accounting']

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
                    scraperwiki.sqlite.save(["id"], establishment_data)
                    establishments.append(establishment_data)
                    establishment_data = {}
        #print establishments


get_inputs("https://maps.googleapis.com/maps/api/place/search/xml?")


