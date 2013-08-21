###############################################################################
#
# Seattle area 'Hikes of the Week' from the Washington Trails Association.
# 
# Fields:
#      name
#      date
#      shortDescription
#      latitude
#      longitude
#      roundtripDistance
#      elevationGain
#      highestPoint
#      fullDescription
#      url
#
# Made as part of a Code for America hackathon at Stanford University.
#
###############################################################################

import scraperwiki
import BeautifulSoup
import re
import urllib

# set debug to true if you want helpful text to be printed for debugging
debug = False

# retrieve a page
starting_url = 'http://www.wta.org/go-hiking/hikes-of-the-week'
html = scraperwiki.scrape(starting_url)

if (debug):
    print html

soup = BeautifulSoup.BeautifulSoup(html)

# use BeautifulSoup to get all <h4> tags, and the first two <p> tags following a <h4> tag
hikes_div = soup.find('div', {'id':'parent-fieldname-text'})

hikes = hikes_div.findAll('h4')

for hike in hikes:
    name = ''
    date = ''
    shortDescription = ''
    latitude = ''
    longitude = ''
    url = ''
    roundtripDistance = ''
    elevationGain = ''
    highestPoint = ''
    fullDescription = ''

    name = hike.text
    
    p = hike.nextSibling

    # skip white spaces in between <h4> and the first <p> tag
    while (True):
        if (isinstance(p, BeautifulSoup.Tag)):
            break;
        else:
            p = p.nextSibling

    date = p.text

    p = p.nextSibling

    # skip white spaces in between first <p> tag and second <p> tag
    while (True):
        if (isinstance(p, BeautifulSoup.Tag)):
            break;
        else:
            p = p.nextSibling

    # fix this to add space instead of stripping out a
    shortDescription = p.text

    url = p.a['href']

    # follow the hike's URL to get more details about this particular hike
    soup2 = BeautifulSoup.BeautifulSoup(urllib.urlopen(url).read())

    coordinates = soup2.find('div', {'class':'latlong discreet'})

    if (coordinates):
        latitude = coordinates('span')[0].text
        longitude = coordinates('span')[1].text

    statsTable = soup2.find('table', {'class':'stats-table'})

    if (statsTable):
        stats = statsTable.findAll('tr')
    
    length = len(stats)
    if (length > 0):
        roundtripDistance = stats[0]('td')[1].text
    if (length > 1):
        elevationGain = stats[1]('td')[1].text
    if (length > 2):
        highestPoint = stats[2]('td')[1].text

    div = soup2.find('div', {'class':'hike-full-description'})
    if (div):

        # remove any image and image caption in the full description
        img = soup2.find('div', {'id':'first-image'})
        if (img):
            img.extract()

        fullDescription = div.text

    record = { 
            'name' : name,
            'date' : date,
            'short_description' : shortDescription,
            'url' : url,
            'latitude' : latitude,
            'longitude' : longitude,
            'roundtrip_distance' : roundtripDistance,
            'elevation_gain' : elevationGain,
            'highest_point' : highestPoint,
            'full_description' : fullDescription
    }

    # "datastore" is deprecated use "sqlite" instead
    scraperwiki.sqlite.save(['name'],record)
