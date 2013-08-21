# Blank Python

import scraperwiki
import urlparse
import lxml.html

# scrape_cities function: gets passed an individual MENU page to scrape
def scrape_menus(root, record, cities, restaurants):
    try:
        restaurants = {}
        menu = {}
        only_dishes = []

        if root is not None:
            rest_name = root.cssselect("div#restaurant h1")
            rest_name = rest_name[0].text
            restaurants['name'] = rest_name

            addr = root.cssselect("div#primary_info span#address")
            addr = root.cssselect("span.address_part")
            rest_addr = ""

            if addr:
                for x in addr:
                    rest_addr = rest_addr + ", " + x.text 

                rest_addr = rest_addr.lstrip(', ')
                print rest_addr
                restaurants['addr'] = rest_addr

            rest_contact = root.cssselect("div#primary_info span#phone_number")
            rest_contact = rest_contact[0].text
            restaurants['contact'] = rest_contact

            list_items = root.cssselect("div#menu")
            for item in list_items:
                category = item.cssselect("div.category")
                if category:
                    for heading in category:
                        dish_in_cat = []
                        cat_head = heading.cssselect("div.category_head h3")
                        cat_name = "Unknown"
                        if cat_head:
                            cat_name = heading.cssselect("h3")
                            cat_name = cat_name[0].text
        
                        cat_items = heading.cssselect("ul li")
                        dish_in_cat = []

                        if cat_items:
                            for dish in cat_items:
                                dishes = {}

                                name = dish.cssselect("span.name")
                                dishes['dish_name'] = name[0].text

                                desc = dish.cssselect("p.description")
                                dishes['dish_notes'] = desc[0].text

                                price = dish.cssselect("span.price")
                                dishes['dish_price'] = price[0].text

                                # print dishes
                                # scraperwiki.sqlite.save(["dish_name"], dishes)
                                dish_in_cat.append(dishes)
                                
                        # menu[cat_name] = dish_in_cat
                        only_dishes.extend(dish_in_cat)
    
        #print menu
        print only_dishes
        restaurants['menu'] = only_dishes
        scraperwiki.sqlite.save(["name"], restaurants)
        # scraperwiki.sqlite.save(["only_dishes"], test)
        return only_dishes
    except:
        return None

# scrape_cities function: gets passed an individual RESTAURANT page to scrape
def scrape_restaurants(root, record, cities, city_url):
    try:
        restaurants_in_city = []
    
        if root is not None:
            list_items = root.cssselect("div#restaurant_list ol li")
        
            if list_items:
                for item in list_items:
                    restaurants = {}
                    # Set up our data record - we'll need it later
                    #record = {}
                    links = item.cssselect("div.basics")
                    links = item.cssselect("a")
                    
                    if links:
                        restaurant_link = links[0].attrib.get('href')
                        rest_name = links[0].text
        
                        rest_addr = item.cssselect("p.restaurant_address")
                        rest_addr = rest_addr[0].text
        
                        restaurants['name'] = rest_name
                        restaurants['addr'] = rest_addr
            
                        restaurant_url = urlparse.urljoin(base_url, restaurant_link)
                        restaurants['link'] = restaurant_url
                        print 'Restaurant name:', rest_name, 'Restaurant URL', restaurant_url
            
                        root = get_root(restaurant_url)
                        menu = scrape_menus(root, record, cities, restaurants)
                        restaurants['menu'] = menu
        
                        restaurants_in_city.append(restaurants)
        
            else:        
                city_url = urlparse.urljoin(city_url, '-/')
                print 'CORRECTION: City URL: ', city_url
                root = get_root(city_url)
                scrape_restaurants(root, record, cities, city_url)

        #print restaurants_in_city
        return restaurants_in_city
    except:
        return None

# scrape_top_cities function: gets passed the TOP CITIES page element to scrape
def scrape_top_cities(root):
    try:
        record = {}
        cities = {}
        list_items = root.cssselect("ul.top_cities li")
    
        # print list_items
        for item in list_items:
            # Set up our data record - we'll need it later
            
            restaurants_in_city = []
    
            links = item.cssselect("a")
            if links: 
                city_name = links[0].text                
                cities['city_name'] = city_name
    
                city_link = links[0].attrib.get('href')
                city_url = urlparse.urljoin(base_url, city_link)
                cities['city_url'] = city_url
                print 'city: ', city_name, 'city URL: ', city_url
                record['cities'] = cities # create the record dict to use in the next function
    
                root = get_root(city_url)
                restaurants_in_city = scrape_restaurants(root, record, cities, city_url) # get list of restaurants from each city
                
                cities[city_name] = restaurants_in_city
    
        record["cities"] = cities
        print record
        # Finally, save the state record to the datastore
        # scraperwiki.sqlite.save(["cities"], record)
    except:
        return None

def get_root(url):
    try:
        html = scraperwiki.scrape(url)
        # print html
        root = lxml.html.fromstring(html)
        # print root
        return root
    except:
        return None

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------

base_url = 'http://www.allmenus.com/'
root = get_root(base_url)
scrape_top_cities(root)
