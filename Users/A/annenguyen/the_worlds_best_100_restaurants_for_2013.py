# Author: Anne Nguyen
# Date: 5/12/2013
# Name: The World's Best 100 Restaurants for 2013
# Description: This script scrapes data from the world's 50 best list for 2013 website and
# puts them into four fields: 'name', 'url', 'position', 'city', 'country'


# Import system modules
import scraperwiki
import urllib
import lxml.html
from geopy import geocoders  


# Download HTML from the web
html = scraperwiki.scrape("http://www.theworlds50best.com/list/1-50-winners/#t1-10")

# Set variables for data extraction
root = lxml.html.fromstring(html)
bullets = root.cssselect("div.col-wide li")

# Select all the li in <div class="col-wide">. For each li, it selects and extracts 
# individual strings of text based on the HTML tag <a> and tags within <a>.
# Data is then stored in a dictionary named 'data.'
for li in bullets:    
    
    aaa = li.cssselect("a")
    
    restauranturl = aaa[0].attrib['href']
    restaurantposition = aaa[0].cssselect("p")[0].text.strip("No.")
    restaurantname = aaa[0].cssselect("h2")[0].text
    city_country = aaa[0].cssselect("h3")[0].text
    city = (city_country.split(",")[0])
    country = (city_country.split(",")[-1])


# Put the extracted data into a dictionary. As mentioned earlier, I was unable to 
# get APIs to work and so the lat, long and geocoder result are commented out.
    data = {
        'name': restaurantname,
        'url': "http://www.theworlds50best.com/" + restauranturl,
        'position': restaurantposition,
        'city': city,
        'country': country,
#       'lat': lat,
#       'long': lng,
#       'geocoder result': place
    }
    # Print data
    print data

    # Save and store data to the ScraperWiki datastore
    scraperwiki.sqlite.save(unique_keys=["name"], data=data)