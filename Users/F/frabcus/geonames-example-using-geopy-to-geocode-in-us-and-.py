# This is an example of calling the geopy API.

# It is using the free Geonames service, which is not reliable
# when under any load, so I wouldn't use it yet in a real scraper.

# When we have private scrapers, and/or special ways of putting in 
# API keys, you'll be able to use Google/Yahoo API.

from geopy import geocoders  

gn = geocoders.GeoNames()  

# hmmm, these example addresses don't work now for some reason :(

place, (lat, lng) = gn.geocode("1600 W 93RD ST")  
print "%s: %.5f, %.5f" % (place, lat, lng)  

place, (lat, lng) = gn.geocode("1630 W 93RD ST")  
print "%s: %.5f, %.5f" % (place, lat, lng)  
# This is an example of calling the geopy API.

# It is using the free Geonames service, which is not reliable
# when under any load, so I wouldn't use it yet in a real scraper.

# When we have private scrapers, and/or special ways of putting in 
# API keys, you'll be able to use Google/Yahoo API.

from geopy import geocoders  

gn = geocoders.GeoNames()  

# hmmm, these example addresses don't work now for some reason :(

place, (lat, lng) = gn.geocode("1600 W 93RD ST")  
print "%s: %.5f, %.5f" % (place, lat, lng)  

place, (lat, lng) = gn.geocode("1630 W 93RD ST")  
print "%s: %.5f, %.5f" % (place, lat, lng)  
