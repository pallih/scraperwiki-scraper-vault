import scraperwiki
import lxml.html
import requests

#base_url = "http://houseprices.landregistry.gov.uk/sold-prices/st119rf"


scraperwiki.sqlite.attach("st_postcodes_doogal")
#pull in postcodes from array for scraper
postcode_array = scraperwiki.sqlite.select("Postcode from st_postcodes_doogal.swdata")

postcode_len = len(postcode_array)

for el in postcode_array:
    postcode_bit = el['Postcode']
    postcode_bit = postcode_bit.lower()
    postcode_bit = postcode_bit.replace(" ", "")

    
    url = "http://houseprices.landregistry.gov.uk/sold-prices/"+postcode_bit
    r = requests.get(url)
    root_content = r.content
    root = lxml.html.fromstring(root_content)
    
    address = root.cssselect(".lr_results ul")
    for place in address:
        
        record = {}
        address_property = place.cssselect("li a")[0].text
        record['address_property'] = address_property
        house_type = place.cssselect("li")[1].text
        record['house_type'] = house_type
        house_sell_price = place.cssselect("li")[2].text
        record['house_sell_price'] = house_sell_price
        house_sell_date = place.cssselect("li")[3].text
        record['house_sell_date'] = house_sell_date
        record['postcode'] = postcode_bit
        if place.cssselect("li img"):
            record['new_house'] = "true"
        else:
            record['new_house'] = "false"
        print record
        scraperwiki.sqlite.save(['address_property'], record)





import scraperwiki
import lxml.html
import requests

#base_url = "http://houseprices.landregistry.gov.uk/sold-prices/st119rf"


scraperwiki.sqlite.attach("st_postcodes_doogal")
#pull in postcodes from array for scraper
postcode_array = scraperwiki.sqlite.select("Postcode from st_postcodes_doogal.swdata")

postcode_len = len(postcode_array)

for el in postcode_array:
    postcode_bit = el['Postcode']
    postcode_bit = postcode_bit.lower()
    postcode_bit = postcode_bit.replace(" ", "")

    
    url = "http://houseprices.landregistry.gov.uk/sold-prices/"+postcode_bit
    r = requests.get(url)
    root_content = r.content
    root = lxml.html.fromstring(root_content)
    
    address = root.cssselect(".lr_results ul")
    for place in address:
        
        record = {}
        address_property = place.cssselect("li a")[0].text
        record['address_property'] = address_property
        house_type = place.cssselect("li")[1].text
        record['house_type'] = house_type
        house_sell_price = place.cssselect("li")[2].text
        record['house_sell_price'] = house_sell_price
        house_sell_date = place.cssselect("li")[3].text
        record['house_sell_date'] = house_sell_date
        record['postcode'] = postcode_bit
        if place.cssselect("li img"):
            record['new_house'] = "true"
        else:
            record['new_house'] = "false"
        print record
        scraperwiki.sqlite.save(['address_property'], record)





