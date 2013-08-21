# Blank Python

import scraperwiki
import urlparse
import lxml.html
import time

# scrape_cities function: gets passed an individual MENU page to scrape
def scrape_menus(root):
    only_dishes = []

    if root is not None:
        list_items = root.cssselect("div.category")
        for item in list_items:
            cat_name = root.cssselect("div.category_head h3")
            if cat_name:
                cat_name = cat_name[0].text

            cat_items = item.cssselect("ul li")
            dish_in_cat = []

            if cat_items:
                for dish in cat_items:
                    dishes = {}

                    name = dish.cssselect("span.name")
                    if name:
                        dishes['name'] = name[0].text

                    desc = dish.cssselect("p.description")
                    if desc:
                        desc = desc[0].text
                        if cat_name:
                            desc= "%s (Category: %s)" % (desc, cat_name)
                        dishes['notes'] = desc

                    price = dish.cssselect("span.price")
                    if price:
                        dishes['price'] = price[0].text

                    scraperwiki.sqlite.save(["name"], dishes, verbose = 0)
                    # scraperwiki.sqlite.execute('''CREATE INDEX IF NOT EXISTS dish_name_index ON dishes (name)''')

# scrape_cities function: gets passed an individual RESTAURANT page to scrape
def scrape_restaurants(root, city_url):
    if root is not None:
        list_items = root.cssselect("div#restaurant_list ol li")
    
        if list_items:
            #counter = 1
            for item in list_items:
                restaurants = {}
                # Set up our data record - we'll need it later
                #record = {}
                links = item.cssselect("div.basics")
                links = item.cssselect("a")
                
                if links:
                    restaurant_link = links[0].attrib.get('href')
                    rest_name = links[0].text

                    # rest_addr = item.cssselect("p.restaurant_address")
                    # rest_addr = rest_addr[0].text
        
                    restaurant_url = urlparse.urljoin(base_url, restaurant_link)
                    print 'Restaurant name:', rest_name, 'Restaurant URL', restaurant_url
                    root = get_root(restaurant_url)
                    scrape_menus(root)

                    #if counter%10 == 0:
                        #"Taking a short break..."
                        #time.sleep(15)
                    #counter += 1
    
        else:        
            city_url = urlparse.urljoin(city_url, '-/')
            print 'CORRECTION: City URL: ', city_url
            root = get_root(city_url)
            scrape_restaurants(root, city_url)
    

# scrape_top_cities function: gets passed the TOP CITIES page element to scrape
def scrape_top_cities(root):
    list_items = root.cssselect("ul.top_cities li")

    # print list_items
    for item in list_items:
        # Set up our data record - we'll need it later
        
        restaurants_in_city = []

        links = item.cssselect("a")
        if links: 
            city_name = links[0].text
            city_link = links[0].attrib.get('href')
            city_url = urlparse.urljoin(base_url, city_link)

            print 'city: ', city_name, 'city URL: ', city_url

            root = get_root(city_url)
            scrape_restaurants(root, city_url) # get list of restaurants from each city
            
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
