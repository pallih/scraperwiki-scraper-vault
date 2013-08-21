###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulStoneSoup
import csv
import urllib

crimeregions = urllib.urlopen('https://spreadsheets.google.com/pub?key=0Agp81FziswcVdGxTc09SWExZMzc2NjNJbjhEbmM2WVE&output=csv')
crimeReader = list(csv.reader(crimeregions))

# retrieve a page
starting_url = 'http://highways.headland.co.uk/GetPointsxml.asp?n=55.91227293006361&e=16.2158203125&s=49.79544988802771&w=-20.54443359375&zoom=6'
html = scraperwiki.scrape(starting_url)
soup = BeautifulStoneSoup(html)
print soup.prettify()

stops = soup.contents[0]
for stop in stops:
    name = stop.find('name').text
    point = stop.find('point')
    cctv = stop.find('cctv').text
    address = stop.find('address').text

    score = 0
    for row in crimeReader:
        if row[0].lower() in address.lower():
            score = row[2]

    lattitude = dict(point.attrs)[u'lat']
    longitude = dict(point.attrs)[u'lng']
    record = { "TruckStop" : name, "Lattitude" : lattitude, "Longitude" : longitude, "CCTV" : cctv, "Score" : score}
    scraperwiki.datastore.save(["TruckStop"], record)
    
