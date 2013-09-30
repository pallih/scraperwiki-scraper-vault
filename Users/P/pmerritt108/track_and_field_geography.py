import scraperwiki    # Import modules
import lxml.html
import geopy
from geopy import geocoders 

gn = geocoders.GeoNames()  # give the geocoder a name to use later

html = scraperwiki.scrape("http://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=43109")
                                                                 # Grab the HTML webpage
root = lxml.html.fromstring(html)                                # Parse the HTML webpage using lxml

# The webpage presents a list of the top ten D1 NCAA track and field runners in each event.

# We will extract only individual running events (no relays or field events).
# There are 11 men's running events and 11 women's running events.
 
# The dataset we are about to create will be used to join the locations of where these runners train with a shapefile, 
# and explore whether the best runners in the country are concentrated in a particular region of the US.


def getRunners(startRow, stopRow):   # We want to create a function because we need use the same process twice.
                                     # (Once for men runners, and once for women runners.)

    for tr in root.cssselect("table tr")[startRow:stopRow]: # Use a for loop to iterate through each "tr" row in the table.
    
    # The table lists all top men runners for every event, then a few lines of code, and THEN the women's running events. So 
    # we need to specify which part of the table we want to extract by using the startRow and stopRow index as parameters.

        tds = tr.cssselect("td") # a list of all "td"s in the "tr" row.

        if len(tds) == 1:                              # If the "tr" row only has one element in it, then
             event = tds[0].cssselect("a")[0].text     # it's a row with the running event title. There are 22 of these.

        else:                                          # Now we can deal with rows that have a list of elements (aka "td"s): 
            if type(tds[0].text) != type(tds[1].text): # The first element in the rank is the rank (e.g. the #1 runner in the 100m sprint).
                rank = float(rank) + 1                 # Sometimes the rank has <type 'None'>. Because it's difficult to perform any tasks on 
                rank = str(int(rank)) + "."            # something with <tpy 'None'>, we'll compare it to the next element in the list. 
            else:                                      # If it's a different type, we'll replace the <type 'None'> with the correct rank.  
                rank = tds[0].text                

            grade = tds[1].text                        # The other elements in the row will be given a name. 
            name = tds[3].cssselect("a")[0].text
            mark = tds[4].text
            state = tds[6].text
            school = tds[7].cssselect("a")[0].text     # The data will then be added to the dictionary (below) according to its name.
            

            location = gn.geocode(state + ", USA", exactly_one=False)[0]   # Use geopy to find a point in the US state the athlete's 
            place, (lat, lng) = location                                   # college is in (this is a proxy for the actual university address). 
                  
                                                                           # We will then save the data we've just extracted as a dataset in ScraperWiki.
            data = {"rank" : rank, "grade" : grade, "name" : name, "mark" : mark, "state" : state, "school" : school, "event" : event, "lat" : lat, "long" : lng}
            scraperwiki.sqlite.save(unique_keys=["name"], data=data)     

getRunners(4, 125) # Calling this function will extract men runners (and their location, school, etc.)
getRunners(259, 381) # Calling this function will extract women runners (and their location, school, etc.)

import scraperwiki    # Import modules
import lxml.html
import geopy
from geopy import geocoders 

gn = geocoders.GeoNames()  # give the geocoder a name to use later

html = scraperwiki.scrape("http://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=43109")
                                                                 # Grab the HTML webpage
root = lxml.html.fromstring(html)                                # Parse the HTML webpage using lxml

# The webpage presents a list of the top ten D1 NCAA track and field runners in each event.

# We will extract only individual running events (no relays or field events).
# There are 11 men's running events and 11 women's running events.
 
# The dataset we are about to create will be used to join the locations of where these runners train with a shapefile, 
# and explore whether the best runners in the country are concentrated in a particular region of the US.


def getRunners(startRow, stopRow):   # We want to create a function because we need use the same process twice.
                                     # (Once for men runners, and once for women runners.)

    for tr in root.cssselect("table tr")[startRow:stopRow]: # Use a for loop to iterate through each "tr" row in the table.
    
    # The table lists all top men runners for every event, then a few lines of code, and THEN the women's running events. So 
    # we need to specify which part of the table we want to extract by using the startRow and stopRow index as parameters.

        tds = tr.cssselect("td") # a list of all "td"s in the "tr" row.

        if len(tds) == 1:                              # If the "tr" row only has one element in it, then
             event = tds[0].cssselect("a")[0].text     # it's a row with the running event title. There are 22 of these.

        else:                                          # Now we can deal with rows that have a list of elements (aka "td"s): 
            if type(tds[0].text) != type(tds[1].text): # The first element in the rank is the rank (e.g. the #1 runner in the 100m sprint).
                rank = float(rank) + 1                 # Sometimes the rank has <type 'None'>. Because it's difficult to perform any tasks on 
                rank = str(int(rank)) + "."            # something with <tpy 'None'>, we'll compare it to the next element in the list. 
            else:                                      # If it's a different type, we'll replace the <type 'None'> with the correct rank.  
                rank = tds[0].text                

            grade = tds[1].text                        # The other elements in the row will be given a name. 
            name = tds[3].cssselect("a")[0].text
            mark = tds[4].text
            state = tds[6].text
            school = tds[7].cssselect("a")[0].text     # The data will then be added to the dictionary (below) according to its name.
            

            location = gn.geocode(state + ", USA", exactly_one=False)[0]   # Use geopy to find a point in the US state the athlete's 
            place, (lat, lng) = location                                   # college is in (this is a proxy for the actual university address). 
                  
                                                                           # We will then save the data we've just extracted as a dataset in ScraperWiki.
            data = {"rank" : rank, "grade" : grade, "name" : name, "mark" : mark, "state" : state, "school" : school, "event" : event, "lat" : lat, "long" : lng}
            scraperwiki.sqlite.save(unique_keys=["name"], data=data)     

getRunners(4, 125) # Calling this function will extract men runners (and their location, school, etc.)
getRunners(259, 381) # Calling this function will extract women runners (and their location, school, etc.)

