from geopy import geocoders 
import lxml.html
import scraperwiki

PAGE_URL = "http://www.walthamforest.gov.uk/index/transport/public-conveniences/community-toilet-scheme.htm"
ONS_CODE = "E09000031"
           
html = scraperwiki.scrape(PAGE_URL) 

root = lxml.html.fromstring(html) 

for tr in root.cssselect("div#content table.datatable tbody tr"):
    cleaned_data = {'ons_code' : ONS_CODE}
    cleaned_data['name'] = tr.cssselect('td')[0].text_content().strip()
    cleaned_data['address'] = tr.cssselect('td')[1].text_content().strip()
    
    try:
        # Perform Geocode
    
        g = geocoders.Google(domain='maps.google.co.uk')    
        place, (lat, lng) = g.geocode(cleaned_data['name'] + ', ' + cleaned_data['address'])
        cleaned_data['WGS84_lat'] = lat
        cleaned_data['WGS84_long'] = lng

        # Horrid hack
        cleaned_data['postcode'] = cleaned_data['address']

        scraperwiki.sqlite.save(unique_keys=['name', 'address'], data=cleaned_data) 
    except:
        pass   

from geopy import geocoders 
import lxml.html
import scraperwiki

PAGE_URL = "http://www.walthamforest.gov.uk/index/transport/public-conveniences/community-toilet-scheme.htm"
ONS_CODE = "E09000031"
           
html = scraperwiki.scrape(PAGE_URL) 

root = lxml.html.fromstring(html) 

for tr in root.cssselect("div#content table.datatable tbody tr"):
    cleaned_data = {'ons_code' : ONS_CODE}
    cleaned_data['name'] = tr.cssselect('td')[0].text_content().strip()
    cleaned_data['address'] = tr.cssselect('td')[1].text_content().strip()
    
    try:
        # Perform Geocode
    
        g = geocoders.Google(domain='maps.google.co.uk')    
        place, (lat, lng) = g.geocode(cleaned_data['name'] + ', ' + cleaned_data['address'])
        cleaned_data['WGS84_lat'] = lat
        cleaned_data['WGS84_long'] = lng

        # Horrid hack
        cleaned_data['postcode'] = cleaned_data['address']

        scraperwiki.sqlite.save(unique_keys=['name', 'address'], data=cleaned_data) 
    except:
        pass   

