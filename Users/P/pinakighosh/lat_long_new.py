from geopy import geocoders
g = geocoders.GoogleV3()
place, (lat, lng) = g.geocode("10900 Euclid Ave in Cleveland") 
print "%s: %.5f, %.5f" % (place, lat, lng)
from geopy import geocoders
g = geocoders.GoogleV3()
place, (lat, lng) = g.geocode("10900 Euclid Ave in Cleveland") 
print "%s: %.5f, %.5f" % (place, lat, lng)
