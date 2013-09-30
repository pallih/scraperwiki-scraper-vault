import scraperwiki
import requests
import lxml.html

#get the data
r = requests.get("https://www.airbnb.se/s/Stockholm--Sweden", verify=False)

#convert the HTML string into a DOM
dom = lxml.html.fromstring(r.text)

results = dom.cssselect(".search_result") 
for result in results:
    apartment_listing = {
        "id" : result.get('data-hosting-id'),
        "name" : result.cssselect('.name')[0].text_content(),
        "price" : result.cssselect('.price_data')[0].text_content().strip()
    }

    scraperwiki.sqlite.save(['id'], apartment_listing)



import scraperwiki
import requests
import lxml.html

#get the data
r = requests.get("https://www.airbnb.se/s/Stockholm--Sweden", verify=False)

#convert the HTML string into a DOM
dom = lxml.html.fromstring(r.text)

results = dom.cssselect(".search_result") 
for result in results:
    apartment_listing = {
        "id" : result.get('data-hosting-id'),
        "name" : result.cssselect('.name')[0].text_content(),
        "price" : result.cssselect('.price_data')[0].text_content().strip()
    }

    scraperwiki.sqlite.save(['id'], apartment_listing)



