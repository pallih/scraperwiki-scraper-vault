import scraperwiki

# Attach to my list of UK towns, along with their lat/lng
scraperwiki.sqlite.attach("uktowns")

# Find my nearest town, for me this is Chester
my_town = scraperwiki.sqlite.select("* from uktowns.towns where town='Chester'")

lat,lng = my_town[0]['lat'], my_town[0]['lng']

# distance(%s,%s,cast(lat as real),cast(lng as real))
# Returns the KM distance between the passed in lat/lng and the lat/lng fields of each record
# so the following query will return the town, and distance from Chester (above) ordered 
# by the closest town first.
print scraperwiki.sqlite.select("town, distance(%s,%s,cast(lat as real),cast(lng as real)) as distance_km from uktowns.towns order by distance_km" % (lat,lng,))
