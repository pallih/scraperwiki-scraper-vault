# Authors: Erika Deal, Anne Nguyen, Phoebe Merritt
# Date: 5/7/2013
# Name: Farmer's Market Scraper
# Description: This script scrapes data from the Broadway Farmers Market Vendor List
# and prints the data
# The data is stored in a dictionary with four value pairs -- 'Farm,' 
# 'County,' 'Products,' and 'Season'



# Import system modules
import scraperwiki
import urllib
import lxml.html

# Download HTML from the web
html = scraperwiki.scrape("http://www.seattlefarmersmarkets.org/vendors/broadway-sunday-farmers-market-list-of-vendors-products")


# Set variables for data extraction
root = lxml.html.fromstring(html)
paras = root.cssselect("div.plain p")

# Select all the p in <div class="plain">. For each p, it selects and extracts 
# individual strings of text based on the HTML tags (i.e. <em> and <strong>).
# Data is then stored in a dictionary named 'data.'
# The exception catches strings for which the tag may or may not exist.
for p in paras:    
    farm = p.text
    
    try:
        county = p.cssselect("em")[0].text.strip(",")
    except IndexError:
        continue

    products = p.cssselect("strong")[0].text
    season = p.cssselect("strong")[0].tail

    if farm == None:
        farm = "Farm"

    if county == None or county == ", County,":
        county = "County"

    if products == None:
        products = "Products"

    if season == None:
        season = "Season"

    data = {
        "Farm": farm,
        "County": county,
        "Products": products,
        "Season": season 
    }
    # Print data
    print data
    # Save and store data to the ScraperWiki datastore
    scraperwiki.sqlite.save(unique_keys=["Farm"], data=data)
# Authors: Erika Deal, Anne Nguyen, Phoebe Merritt
# Date: 5/7/2013
# Name: Farmer's Market Scraper
# Description: This script scrapes data from the Broadway Farmers Market Vendor List
# and prints the data
# The data is stored in a dictionary with four value pairs -- 'Farm,' 
# 'County,' 'Products,' and 'Season'



# Import system modules
import scraperwiki
import urllib
import lxml.html

# Download HTML from the web
html = scraperwiki.scrape("http://www.seattlefarmersmarkets.org/vendors/broadway-sunday-farmers-market-list-of-vendors-products")


# Set variables for data extraction
root = lxml.html.fromstring(html)
paras = root.cssselect("div.plain p")

# Select all the p in <div class="plain">. For each p, it selects and extracts 
# individual strings of text based on the HTML tags (i.e. <em> and <strong>).
# Data is then stored in a dictionary named 'data.'
# The exception catches strings for which the tag may or may not exist.
for p in paras:    
    farm = p.text
    
    try:
        county = p.cssselect("em")[0].text.strip(",")
    except IndexError:
        continue

    products = p.cssselect("strong")[0].text
    season = p.cssselect("strong")[0].tail

    if farm == None:
        farm = "Farm"

    if county == None or county == ", County,":
        county = "County"

    if products == None:
        products = "Products"

    if season == None:
        season = "Season"

    data = {
        "Farm": farm,
        "County": county,
        "Products": products,
        "Season": season 
    }
    # Print data
    print data
    # Save and store data to the ScraperWiki datastore
    scraperwiki.sqlite.save(unique_keys=["Farm"], data=data)
