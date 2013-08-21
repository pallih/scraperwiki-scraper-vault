import scraperwiki
import requests
import lxml.html
import urllib

def geocode(address):
    try:
        r = requests.get('http://open.mapquestapi.com/nominatim/v1/search.php?format=json&q=' + urllib.quote_plus(address.encode('utf-8')))
        lat = r.json()[0]["lat"]
        lon = r.json()[0]["lon"]
        return [lat, lon]
    except:
        return None

def get_site(url):
    r = requests.get(url, verify=False)
    return lxml.html.fromstring(r.text)

for page in range(10,40):
    print "Scraping page %d" % page
    dom = get_site("https://www.airbnb.se/s/Stockholm--Sweden?page=%d" % page)
    
    results = dom.cssselect('.search_result')
    for result in results:
        apartment_listing = {
          "id": result.get('data-hosting-id'),
          "name": result.cssselect('.name')[0].text_content(),
          "price": result.cssselect('.price_data')[0].text_content().strip()
        }
    
        url = result.cssselect('.name')[0].get('href')
        dom = get_site("https://www.airbnb.se" + url)
        address = dom.cssselect('#display_address')[0].text_content().strip()
        coordinates = geocode(address)
        print coordinates
    
        if coordinates is not None:
            apartment_listing["lat"] = coordinates[0]
            apartment_listing["lon"] = coordinates[1]
            apartment_listing["address"] = address
            scraperwiki.sqlite.save(['id'], apartment_listing)
    
    
    
    
