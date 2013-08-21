import scraperwiki
import lxml.html
import re, mechanize, time

# mechanize:
# br = mechanize.Browser()
# r = br.open("http://www.somewebsite.com")
# br.find_link(text='Click this link')
# req = br.click_link(text='Click this link')
# br.open(req)
# print br.response().read()

flag = True
flag_2 = True
flag_3 = True

# Counter initializations:
record_id = 1

# Province URL:
cities_url = "http://www.yellowpages.ca/locations/Ontario/"

# double-space check function:
def space_checker(title_string):
    print title_string
    try:
        error_checker = re.search('\s\s', title_string, re.I|re.M|re.S) 
        if error_checker:
            fixed_title = title_string.replace('  ', ' ')
            return fixed_title 
        else:
            return title_string
    except:
        return title_string

# Initialize scraping tools:
cities_page = scraperwiki.scrape(cities_url)
root = lxml.html.fromstring(cities_page)
mech = mechanize.Browser()
mech.open(cities_url)

# grab ypgCategory.text make list of links.
cities = root.cssselect('.ypgLocation')
cities.pop()

city_count = len(cities)
print "Number of cities: " + str(city_count)

for city in cities:
    print "City: " + city.text_content()
    if flag:
            if city.text_content() != "Brampton":
                continue
            else:
                flag = False

    mech.find_link(text=city.text_content())
    city_results = mech.click_link(text=city.text_content())
    mech.open(city_results)
    categories_page = lxml.html.fromstring(mech.response().read())    
    categories = categories_page.cssselect('.ypgCatTitle')
    for category in categories:
        print "Category: " + category.text_content()
        
        if flag_2:
                if category.text_content() != "Shopping & Specialty Stores":
                    continue
                else:
                    flag_2 = False

        mech.find_link(text=category.text_content())
        category_results = mech.click_link(text=category.text_content())
        mech.open(category_results)
        subcategories_page = lxml.html.fromstring(mech.response().read())
        subcategories = subcategories_page.cssselect('.ypgCatTitle')
        for subcategory in subcategories:
            print "Subcategory: " + subcategory.text_content()
            
            if flag_3:
                if subcategory.text_content() != "Florists":
                    continue
                else:
                    flag_3 = False

            error_link = re.search('^Adhesives', subcategory.text_content(), re.I|re.M|re.S)
            error_link_2 = re.search('Cooling', subcategory.text_content(), re.I|re.M|re.S)
            if error_link:
                mech.find_link(url="/locations/Ontario/" + city.text_content() + "/90019009.html")
                subcategory_results = mech.click_link(url="/locations/Ontario/" + city.text_content() + "/90019009.html")
            elif error_link_2:
                mech.find_link(url="/locations/Ontario/" + city.text_content() + "/90011004.html")
                subcategory_results = mech.click_link(url="/locations/Ontario/" + city.text_content() + "/90011004.html")
            else:
                subcat = space_checker(subcategory.text_content())
                print subcat
                mech.find_link(text=subcat)
                subcategory_results = mech.click_link(text=subcat)               

            mech.open(subcategory_results)
            minicategories_page = lxml.html.fromstring(mech.response().read())
            minicategories = minicategories_page.cssselect('.ypgCategory')
            for minicategory in minicategories:
                print "Minicategory: " + minicategory.text_content()
                try:
                    mech.find_link(text=minicategory.text_content())
                    listings_results = mech.click_link(text=minicategory.text_content())
                except:
                    minicat = space_checker(minicategory.text_content())
                    mech.find_link(text=minicat)
                    listings_results = mech.click_link(text=minicat)  
                
                mech.open(listings_results)
                listings_page = lxml.html.fromstring(mech.response().read())    
                page = 1 # Reset in each new minicategory
                try:
                    last_page = re.search('Page\s1\sof\s(\d{1,})', listings_page.text_content(), re.I|re.M|re.S).group(1)
                except:
                    last_page = 1
                print "Pages: " + str(last_page)
                last_page = int(last_page)
                
                while page <= last_page:
                    try:
                        error = re.search("(find\sany\sbusiness\slistings\smatching)", mech.response().read(), re.I|re.M|re.S).group(1)
                        print error
                        page = last_page + 1
                        continue
                    except:
                        listings_page = lxml.html.fromstring(mech.response().read())
                        listing_block = listings_page.cssselect('#geoListings')[0]
                        listings = listing_block.cssselect('.listingDetail')
                    for listing in listings:
                        try:
                            name = listing.cssselect('.listingTitleLine')[0]
                            name = name.text_content()
                        except:
                            name = 'NAME NOT RECORDED'
                        try:
                            address = listing.cssselect('.address')[0]
                            address = address.text_content()
                        except:
                            address = 'Multiple locations'
                        try:
                            phone = listing.cssselect('.phoneLink')[0]
                            phone = phone.text_content()
                        except:
                            phone = 'No phone'
                
                        scraperwiki.sqlite.save(unique_keys=["id"], data={"id": record_id, "name": name, "address": address, "phone": phone, 
                                                "subcategory": subcategory.text_content(), "category": category.text_content(), 
                                                "city": city.text_content() })
                        record_id+=1
                    
                    if page != last_page:
                        mech.find_link(text='Next')
                        n = mech.click_link(text='Next')
                        mech.open(n)
                        print "Page: "+ str(page) + " complete."
                        page+=1
                    else:
                        print "Page: "+ str(page) + " complete."
                        page+=1
                time.sleep(2)
                mech.open(subcategory_results)
            mech.open(category_results)
        mech.open(city_results)
    mech.open(cities_url)
