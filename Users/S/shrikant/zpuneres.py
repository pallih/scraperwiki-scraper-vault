import scraperwiki
import urlparse
import lxml.html

# scrape_restaurants: Scrape restaurants on the page and then move to next page
def scrape_restaurants(root, rest_id, base_url, city_url):
    try:
        print "Starting scrape of page: ", city_url
        if root is not None:
            restaurant_list  = root.cssselect("div.search_results section#search-results-container ol li.resZS")
            if restaurant_list:
                restaurants_in_city = []
                for each_restaurant in restaurant_list:
                    restaurants = {}

                    res_link = each_restaurant.cssselect("div.search-name")

                    if res_link:
                        res_name = res_link[0].cssselect("h3 a")
                        res_name = res_name[0].text
                        print res_name

                        res_cuisines = res_link[0].cssselect("p.ln24")
                        res_cuisines = res_cuisines[0].attrib.get('title')
                        # print res_cuisines

                        res_addr = res_link[0].cssselect("p.ln24")
                        res_addr = res_addr[1].attrib.get('title')
                        # print res_addr

                        restaurants['id'] = rest_id
                        restaurants['name'] = res_name
                        restaurants['addr'] = res_addr
                        restaurants['cuisines'] = res_cuisines

                        rest_id += 1
                        restaurants_in_city.append(restaurants)
        # print restaurants_in_city
        scraperwiki.sqlite.save(["id"], restaurants_in_city, table_name="restaurants", verbose=0)
        return rest_id
    except scraperwiki.Error as e:
        scraperwiki.sqlite.save(["id"], restaurants_in_city, table_name="restaurants", verbose=0)
        print 'uh-oh! error happened while scraping restaurants!', e
        return None

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url, rest_id):
    try:
        html = scraperwiki.scrape(url)
    except scraperwiki.Error:
        print "Sleeping for 10 seconds..."
        time.sleep(10)
        html = scraperwiki.scrape(url)
    
    # print html
    root = lxml.html.fromstring(html)
    rest_id = scrape_restaurants(root, rest_id, base_url, city_url)
    scraperwiki.sqlite.save_var('last_rest_id', rest_id) 
    next_links = root.cssselect("ul.pagination-control li.active a")

    for link in next_links:
        if "Next" in link.text:
            next_link = link.attrib.get('href')
        else:
            next_link = None
    
    if next_link is not None:
        next_url = urlparse.urljoin(base_url, next_link)
        print next_url
        scraperwiki.sqlite.save_var('last_url_scraped', next_url) 
        scrape_and_look_for_next_link(next_url, rest_id)
    else:
        print "Finished scraping!"

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------

base_url = 'http://www.zomato.com/'
city_url = 'http://www.zomato.com/ncr/restaurants'

rest_id = max(scraperwiki.sqlite.get_var('last_rest_id'), 1)
url_to_scrape = scraperwiki.sqlite.get_var('last_url_scraped')

if url_to_scrape is not None:
    scrape_and_look_for_next_link(url_to_scrape, rest_id)
else:
    scrape_and_look_for_next_link(city_url, rest_id)