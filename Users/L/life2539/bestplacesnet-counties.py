# This is an attempt to compile all the County areas on bestplaces.net automatically
# 
#
#

print "Running bestplaces.net County Areas list"

# imports

import csv
import scraperwiki


# Function to get the State County Locations
def GetCounties(State):
    
    WebAddress = "http://www.bestplaces.net/find/county.aspx?st="+State
    print "Source " + WebAddress
    
    html = scraperwiki.scrape(WebAddress)
    
    import lxml.html
    root = lxml.html.fromstring(html)
    
    for tr in root.cssselect("[valign='top']"):
        for links in tr.cssselect("a"):
            str = links.text_content()
                    
            data = {
            'County' : str,
            'State' : State 
            }
            scraperwiki.sqlite.save(unique_keys=['County'],data=data)

    return


###############################
# getting all the state codes #
###############################

scraperwiki.sqlite.attach("bestplaces_states", "src")
counter =0

dict = scraperwiki.sqlite.execute("select USPSCode from src.swdata")
for States in dict['data']:
    for State in sorted(set(States)):
        print "Extracting " + State + " data (" + str(counter+1) + "/51)"
        GetCounties(State)
        
    counter += 1
    
###############################
# getting all the state codes #
###############################


