import os
import glob
import lxml.html
from lxml import etree
import datetime
import scraperwiki
import unicodedata
import time
import sys

# these fields don't contain any data
# too many fields also cause a SqliteError: sqliteexecute: sqlite3.Error: too many SQL variables
# This seems to occur when ever 1000 columns become used
def removeBogusColumnsFromDict(d):
    #delete all keys that start with these patterns
    keyPatternsToDelete = ["Add_Another_", "Add_Associated_", "ai", "Color", "Levels", "LinesCount", "NumberOf", "Num_Levels", "Opacity", "Overlay_", "Zoom_Factor", "Weight"]
    for key in d.keys():
        okToDelete = False
        for keyPattern in keyPatternsToDelete:
            if key.startswith(keyPattern):
                okToDelete = True
        if okToDelete:
            del d[key]

    return d

def checkForValue(value):
        if len(value) > 0:
                return str(value[0].encode("utf-8"))
        else:
                return ""

#remove problem characters that don't work as sql column names
def makeNiceKey(value):

        value = value.replace('(', '')
        value = value.replace(')', '')
        value = value.replace('%', 'Percent')
        value = value.replace('-', '_')
        value = value.replace('/', '__')
        value = value.replace('###', '___')
        value = value.replace(':_', '__')
        value = value.replace('         ', '')
        value = value.replace('&#9;', '')
        value = value.replace('\t', '')
        value = value.replace('enumfield', '')
        while value.find('__') > 0:
            value = value.replace('__', '_')
        return value

scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS powerplants (Name TEXT, Type TEXT, Country TEXT, State TEXT, Type_of_Plant_rng1 TEXT, Type_of_Fuel_rng1_Primary TEXT, Type_of_Fuel_rng2_Secondary TEXT, Design_Capacity_MWe_nbr NUMBER)")

# figure out what's already been downloaded
knownIDs = scraperwiki.scrape("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=global_energy_observatory_power_plants&query=select%20distinct%20replace(CurrentPage_sys%2C%20'%2Fgeoid%2F'%2C%20'')%20as%20id%20from%20%60powerplants%60")
knownIDs = knownIDs.split("\r\n")
del knownIDs[0] # first element is the header
print knownIDs

fuelTypes = ["Coal", "Gas", "Oil", "Hydro", "Geothermal", "Nuclear", "Solar_PV", "Solar_Thermal", "Waste", "Wind"]

for fuelType in fuelTypes:
    fuelTypeURL = "http://globalenergyobservatory.org/list.php?db=PowerPlants&type=" + fuelType
    print fuelTypeURL
    html = scraperwiki.scrape(fuelTypeURL)
    root = lxml.html.fromstring(html)

    links = root.xpath("//tr[@class='odd_perf' or @class='even_perf']/td[1]/a/@href")
    for link in links:

        plantID = link.replace("geoid/", "")

        plantURL = "http://globalenergyobservatory.org/" + link

        # only download plants not currently in the database
        if plantID not in knownIDs:
            print plantURL
            try:
                html = scraperwiki.scrape(plantURL)
                root = lxml.html.fromstring(html)    
            except:
                print "Error downloading " + plantURL

            installationInfo = dict()
            unitList = list()
            id = -1

            inputFields = root.xpath("//input | //select")
            for inputField in inputFields:
    
                #TODO how to deal with checkboxes?
                typeVal = checkForValue(inputField.xpath("./@type"))
                idVal = checkForValue(inputField.xpath("./@id"))
                classVal = checkForValue(inputField.xpath("./@class"))
                valueVal = checkForValue(inputField.xpath("./@value"))
                nameVal = checkForValue(inputField.xpath("./@name"))
                chkVal = checkForValue(inputField.xpath("./@checked"))
                catVal = checkForValue(inputField.xpath("ancestor::div[h1]/@id"))
                selOptVal = checkForValue(inputField.xpath("./option[@selected]/@value"))

                if ((typeVal == "text" or typeVal == "hidden") or ((typeVal == "radio" or typeVal == "checkbox") and len(chkVal) > 0)) and len(valueVal) > 0 and len(idVal) > 0:
                    if idVal == "GEO_Assigned_Identification_Number":
                        id = valueVal
                    if catVal <> 'UnitDescription_Block':
                        installationInfo[makeNiceKey(idVal)] = valueVal
                    else:  # use different table for unit details to avoid having too many fields in main table
                        parts = makeNiceKey(idVal).rpartition('_')
                        while int(parts[2]) > len(unitList):
                            unitList.append({'GEO_Assigned_Identification_Number':id, 'Unit_Nbr':len(unitList)+1})
                        unitList[int(parts[2])-1][parts[0]] = valueVal
                elif len(selOptVal) > 0 and not(selOptVal.startswith("Please Select")) and len(idVal) > 0:
                    installationInfo[makeNiceKey(idVal)] = selOptVal

            #add in fuel type
            #installationInfo["Fuel_type"] = fuelType

            installationInfo = removeBogusColumnsFromDict(installationInfo)

            # TODO Description_ID does not always correspond to the actual page URL, need to contact Rajan Gupta of GEO as he's probably not aware of this.
            # select Description_ID, CurrentPage_sys, GEO_Assigned_Identification_Number from `swdata` where Description_ID != GEO_Assigned_Identification_Number OR replace(CurrentPage_sys, "/geoid/", "") != GEO_Assigned_Identification_Number
            # Using GEO_Assigned_Identification_Number, it corresponds to CurrentPage_sys except in one case

            try:
                #primary key is based on id
                scraperwiki.sqlite.save(unique_keys=["GEO_Assigned_Identification_Number"], data=installationInfo, table_name="powerplants")
                if len(unitList) > 0:
                    scraperwiki.sqlite.save(unique_keys=["GEO_Assigned_Identification_Number","Unit_Nbr"], data=unitList, table_name="ppl_units")
            except:
                print "Error saving to DB" + ": " + str(sys.exc_info()[1])

            time.sleep(5) #sleep a little to be kind to the server, running into "Temporary failure in name resolution"
        #else:
            # add in the fuel type since we forgot to put it in the first time around, it's not actually on the page usually
            # Nono: Wasn't it already in the Type field? (hidden field within HTML source)
            # Chris: I think you're correct, and I only noticed this field much later.

            #currentEntry = dict()
            #currentEntry = scraperwiki.sqlite.execute("select * from swdata where Description_ID = " + str(plantID))
            #scraperwiki.sqlite.execute("UPDATE swdata SET Fuel_type='" + fuelType + "' WHERE Description_ID=" + str(plantID))
            #print "UPDATE swdata SET Fuel_type='" + fuelType + "' WHERE Description_ID=" + str(plantID)
            #currentEntry["Fuel_Type"] = fuelType
            #scraperwiki.sqlite.save(unique_keys=["Description_ID"], data=currentEntry)