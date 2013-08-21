import scraperwiki
import urlparse
import lxml.html

# scrape_cities function: gets passed an individual MENU page to scrape
def scrape_menus(root, restaurants, rest_id, rest_name):
    try:
        menu = {}
        if root is not None:
            rest_website = root.cssselect("div#restaurant div#primary_info span#website")
            if rest_website:
                rest_website = rest_website[0].cssselect("a")
                rest_website = rest_website[0].text
                restaurants['website'] = rest_website
                # print "Restaurant website is:", rest_website

            rest_contact = root.cssselect("div#restaurant div#primary_info span#phone_number")            
            if rest_contact:
                rest_contact = rest_contact[0].text
                restaurants['contact_number'] = rest_contact

                # print "Restaurant contact is:", rest_contact

            rest_latlong = root.cssselect("div#restaurant div#primary_info meta")
            if rest_latlong:
                rest_lat = rest_latlong[0].attrib.get('content')
                restaurants['location_latitude'] = rest_lat
                rest_long = rest_latlong[1].attrib.get('content')
                restaurants['location_longitude'] = rest_long

                # print "Lat-Long is:", rest_lat,rest_long

            list_items = root.cssselect("div#menu")
            for item in list_items:
                category = item.cssselect("div.category")
                if category:
                    for heading in category:
                        dish_in_cat = []

                        cat_head = heading.cssselect("div.category_head h3")
                        if cat_head:
                            cat_name = heading.cssselect("h3")
                            cat_name = cat_name[0].text
                        else:
                            cat_name = "Unknown"

                        cat_items = heading.cssselect("ul li")
                        if cat_items:
                            for dish in cat_items:
                                dishes = {}

                                name = dish.cssselect("span.name")
                                if name:
                                    dishes['name'] = name[0].text

                                desc = dish.cssselect("p.description")
                                if desc:
                                    dishes['content'] = desc[0].text

                                price = dish.cssselect("span.price")
                                if price:
                                    price_range = price[0].text
                                    if "-" in price_range:
                                        price_range = price_range.replace('$','')
                                        price_range = price_range.split('-')
                                        dishes['price_min'] = price_range[0]
                                        dishes['price_max'] = price_range[1]
                                    
                                dishes['category'] = cat_name 
                                dishes['restaurant_id'] = rest_id
                                dishes['restaurant_name'] = rest_name
                                dishes['cuisine'] = restaurants['cuisines']
                                
                                dishes['is standalone'] = True
                                if 'side' in cat_name.lower() or 'extra' in cat_name.lower():
                                    dishes['is_standalone'] = False

                                # print dishes
                                
                                dish_in_cat.append(dishes)
                        menu[cat_name] = dish_in_cat
                        scraperwiki.sqlite.save(["name", "restaurant_name"], dish_in_cat, table_name="menu", verbose = 0)
        return
    except scraperwiki.Error as e:
        print e
        scraperwiki.sqlite.save(["name", "restaurant_name"], dish_in_cat, table_name="menu", verbose = 0)
        print 'uh-oh! error happened while scraping menus!'
        return

# scrape_cities function: gets passed an individual CITY page to scrape
def scrape_restaurants(root, rest_id, base_url, city_url):
    try:    
        if root is not None:
            list_items = root.cssselect("div#restaurant_list ol li.restaurant")
        
            if list_items:
                for item in list_items:
                    restaurants = {}
                    links = item.cssselect("div.basics")
                    if links:
                        cuisines = item.cssselect("ul.restaurant_cuisines li")
                        rest_cuisines = ""
                        for cuisine in cuisines:
                            rest_cuisines += cuisine.text
                        # print rest_cuisines

                        links = item.cssselect("a")
                        restaurant_link = links[0].attrib.get('href')
                        rest_name = links[0].text
        
                        rest_addr = item.cssselect("p.restaurant_address")
                        rest_addr = rest_addr[0].text

                        rest_ext_id = restaurant_link.split('-')
                        rest_ext_id = rest_ext_id[0].split('/')
                        rest_ext_id = rest_ext_id[len(rest_ext_id)-1]
                        restaurants['external_id'] = rest_ext_id

                        restaurants['restaurant_id'] = rest_id
                        restaurants['name'] = rest_name
                        restaurants['location_address'] = rest_addr
                        restaurants['cuisines'] = rest_cuisines
                        restaurants['providestakeaway'] = True
                        restaurants['ext_id_type'] = "allmenus"
            
                        restaurant_url = urlparse.urljoin(base_url, restaurant_link)
                        restaurants['link'] = restaurant_url
                        print rest_id, 'Restaurant name:', rest_name, 'Restaurant URL', restaurant_url
                        
                        root = get_root(restaurant_url)
                        scrape_menus(root, restaurants, rest_id,  rest_name)

                        scraperwiki.sqlite.save_var('last_scraped_id', rest_id, verbose=0)
                        scraperwiki.sqlite.save(["link"], restaurants, table_name="restaurants", verbose = 0)

                        rest_id += 1

                        # restaurants_in_city.append(restaurants)
            else:        
                cuisine_list = root.cssselect("div#cuisines ul#all_cuisines li")
                if cuisine_list:
                    for cuisine in cuisine_list:
                        cuisine_url = cuisine.cssselect("a")
                        if cuisine_url and cuisine_url[0].attrib.get('href'):
                            cuisine_url = cuisine_url[0].attrib.get('href')
                            rest_list_url = urlparse.urljoin(city_url, cuisine_url)
                            new_root = get_root(rest_list_url)
                            rest_id = scrape_restaurants(new_root, rest_id, base_url, rest_list_url)
        return rest_id
    except scraperwiki.Error as e:
        print 'uh-oh! error happened while scraping restaurants!'
        print e
        scraperwiki.sqlite.save_var('last_scraped_id', rest_id, verbose=0)
        scraperwiki.sqlite.save(["link"], restaurants, table_name="restaurants", verbose = 0)
        return rest_id

def get_root(url):
    try:
        html = scraperwiki.scrape(url)
        # print html
        root = lxml.html.fromstring(html)
        # print root
        return root
    except scraperwiki.Error as e:
        print e
        return None

def createIndexes():
    scraperwiki.sqlite.execute("CREATE INDEX res_links_manual_index on restaurants (link);")
    scraperwiki.sqlite.execute("CREATE INDEX name_restaurant_manual_index on menu (name, restaurant);")

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------

base_url = 'http://www.allmenus.com/'
city_url = 'http://www.allmenus.com/ma/boston/'
root = get_root(city_url)

rest_id = scraperwiki.sqlite.get_var('last_scraped_id')
rest_id = max(1,rest_id)
scrape_restaurants(root, rest_id, base_url, city_url)

'''dish_in_cat = []
restaurants = {}

try:
    print "Starting run..."
    rest_id = scrape_restaurants(root, rest_id, base_url, city_url)
    print "...run finished without errors!!"
except scraperwiki.Error as e:
    print "Some errors were encountered during the run!"
    print e
finally:
    if len(dish_in_cat)!=0 and len(restaurants)!=0:
        scraperwiki.sqlite.save(["name", "restaurant_name"], dish_in_cat, table_name="menu", verbose = 0)   
        scraperwiki.sqlite.save(["link"], restaurants, table_name="restaurants", verbose = 0)
        scraperwiki.sqlite.save_var('last_scraped_id', rest_id, verbose=0)'''

createIndexes()
