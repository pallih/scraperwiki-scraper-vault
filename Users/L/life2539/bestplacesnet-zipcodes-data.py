# This is an attempt to compile all the ZipCode areas on bestplaces.net automatically
# 
#
#

print "Running bestplaces.net ZipCode Areas list"

# imports

import csv
import scraperwiki

# Function to get the Zipcode Locations
def GetZipCodes(State, City, Zip):
    #establishing categories
    Categories = [ '_' ,'People', 'Health', 'Economy', 'Housing', 'Crime', 'Climate', 'Education', 'Transportation', 'Cost of Living', 'Religion', 'Voting']
    
    # Go Through all the statistic categories
    CatCounter = 0
    SubsectionCounter = 0
    KeyPrefix = ""
    for cat in Categories:
        if Categories[CatCounter]== '_':
            WebAddress = "http://www.bestplaces.net/zip-code/" + State + "/" + CityTown + "/" + Zip
        else:
            WebAddress = "http://www.bestplaces.net/" + Categories[CatCounter].replace(" ","_")+ "/zip-code/" + State + "/" + CityTown + "/" + Zip
        print "Source " + WebAddress
        
        html = scraperwiki.scrape(WebAddress)
        
        import lxml.html
        root = lxml.html.fromstring(html)

        for tr in root.cssselect("table[rules='cols']>tr :not([class='header'])"):
            
            tds = tr.cssselect("td")
            
            # statcategory
            if Categories[CatCounter] == "_":
                statcategory = "Overview"
            else : 
                statcategory = Categories[CatCounter]
            
            # statkey
            statkey = tds[0].text_content().replace(":","")
            # statvalue
            statvalue = tds[1].text_content()
                        
            # converting subsection
            if statkey == "ESTIMATED HOUSEHOLDS BY HOUSEHOLD INCOME":
                SubsectionCounter = 11
                KeyPrefix = "HOUSEHOLD BY INCOME"
                statvalue = "skip"

            elif statkey == "POPULATION BY OCCUPATION":
                SubsectionCounter = 8
                KeyPrefix = "POPULATION BY OCCUPATION"
                statvalue = "skip"

            elif statkey == "OWNER-OCCUPIED HOUSING UNITS BY VALUEClick Links Below to see Properties":
                SubsectionCounter = 14
                KeyPrefix = "OWNER-OCCUPIED HOUSING UNITS"
                statvalue = "skip"

            elif statkey == "HOUSING UNITS BY YEAR STRUCTURE BUILTClick Links Below to see Properties":
                SubsectionCounter = 10
                KeyPrefix = "HOUSING AGE"
                statvalue = "skip"

            elif statkey == "COMMUTE MODE":
                SubsectionCounter = 5
                KeyPrefix = "COMMUTE MODE"
                statvalue = "skip"

            elif statkey == "COMMUTE TIME TO WORK":            
                SubsectionCounter = 6
                KeyPrefix = "COMMUTE TIME TO WORK"
                statvalue = "skip"

            if SubsectionCounter == 0:
                KeyPrefix = ""

             
##############
# Store Data #
##############
            if statvalue == "skip":
                pass
            else :
                data = {
                  'statcategory' : statcategory,
                  'statsubcategory' : KeyPrefix,
                  'statkey' : statkey,
                  'value' : statvalue,
                  'zipcode' : Zip,
                  'citytown' : City,
                  'state' : State 
                  }
                scraperwiki.sqlite.save(unique_keys=['zipcode','statkey'],data=data)
                
            SubsectionCounter -= 1
                
        CatCounter += 1

    return


###############################
# getting all the state codes #
###############################

scraperwiki.sqlite.attach("bestplaces_zipcodes", "src")
dict = scraperwiki.sqlite.execute("select Zipcode, CityTown, State  from src.swdata")

counter =0
for States in dict['data']:
    Zipcode = str(States[0])
    CityTown = str(States[1])
    State = str(States[2])
    
    CityTown = CityTown.replace(" ","_")
    #for State in sorted(set(States)):
    print "Extracting " + CityTown + ", " + State + " " + Zipcode + " data"
    GetZipCodes(State, CityTown, Zipcode)
        
    counter += 1
    
###############################
# getting all the state codes #
###############################


