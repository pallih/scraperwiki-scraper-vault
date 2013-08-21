from geopy import geocoders

loc = 'HR1 3RN'
g = geocoders.Google()
print g.geocode(loc)