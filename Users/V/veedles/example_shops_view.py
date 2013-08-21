# The data will be taken from a scraper (in this case - http://scraperwiki.com/scrapers/example_shops)
# We must first set the other here as our sourcescraper
sourcescraper = 'example_shops'

# This pulls in the data api which lets us connect to the datastore in the other scraper (the one that contains the data)
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

# Some basic variables you need to initialize
limit = 5000
offset = 0

# Here we simply use the print statement to build HTML for the view
print '<ul>'
print 'Shop List'

# This is the point where we hit the scraper which is the source of the data and display it in our view
# (in this case we only have one thing in our data - the shop_name)
for row in getData(sourcescraper, limit, offset):
    print '<li>' + row['shop_name'] + '</li>'

print '</ul>'

