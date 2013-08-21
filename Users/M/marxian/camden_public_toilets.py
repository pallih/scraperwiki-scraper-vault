from geopy import geocoders 
import lxml.html
import scraperwiki

PAGE_URL = "http://www.camden.gov.uk/ccm/content/contacts/categories/public-toilets-in-camden.en"
ONS_CODE = "E09000007"
           
html = scraperwiki.scrape(PAGE_URL) 

root = lxml.html.fromstring(html) 

for h2 in root.cssselect("div.contact-last h2"):
    cleaned_data = {'ons_code' : ONS_CODE}
    cleaned_data['name'] = h2.text_content().strip()

    cleaned_data['opening'] = h2.getnext().getnext().find('div').text_content().strip()

    details = h2.getnext().getnext().getnext().find('div').text_content().strip()
    cleaned_data['babychanging'] = ('baby changing' in details.lower())
    cleaned_data['disabled'] = ('wheelchair' in details.lower() or 'disabled' in details.lower())

    cleaned_data['address'] = ', '.join([x.strip() for x in h2.getnext().cssselect('div.second')[0].itertext()])
    try:
        cleaned_data['postcode'] = h2.getnext().getnext().getnext().getnext().cssselect('div.fifth p a')[0].get('href').split('q=')[-1]
    except:
        cleaned_data['postcode'] = cleaned_data['address'].split(', ')[-1]

    # Perform Geocode
    
    g = geocoders.Google(domain='maps.google.co.uk')    
    place, (lat, lng) = g.geocode(cleaned_data['postcode'])
    cleaned_data['WGS84_lat'] = lat
    cleaned_data['WGS84_long'] = lng

    scraperwiki.sqlite.save(unique_keys=['name', 'address'], data=cleaned_data)    
     
