import scraperwiki
import urllib2
import time
import datetime
import dateutil.parser 

from time import strftime
from datetime import datetime
from BeautifulSoup import BeautifulSoup

def removeNL(x):
    """cleans a string of new lines and spaces"""
    s = x.split('\n')
    s = [x.strip() for x in s]
    x = " ".join(s)
    return x.lstrip()


# Create/open a file for data storage
f = open('franklin-shiplog.txt', 'w')


#timestamp for this scraping
now = time.time()


# Open source url and load to Beautiful Soup
url = "http://www.charts.gc.ca/announcements-annonces/2012/Franklin-eng.asp"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)


if soup:

    # Find all the tables containing ship data
    shipLocations = soup.findAll('table')

    # Loop thorough individual tables in the found array
    for index in range(len(shipLocations)):

        # Find all the rows in this table
        thisTableRows = shipLocations[index].findAll('tr')

        # Loop through rows, grabbing header and value strings
        for index2 in range(len(thisTableRows)):
            
            # print index2
            thisTableRowHeader = thisTableRows[index2].findAll('th')
            thisTableRowContent = thisTableRows[index2].findAll('td')

            thisRowKey = thisTableRowHeader[0].string
            thisRowValue = thisTableRowContent[0].string 
            thisValue = thisRowValue
            thisDate = ''
            thisData = ''
            thisKVPair = ''
            thisTimestamp = ''


            # check the headers/value pairs and build up the data
            if thisRowKey == 'Location':
                thisKey = 'location'                    
                thisKVPair = "'" + thisKey + "': " + thisValue 
   
            elif thisRowKey == 'Current Vessel Status':
                thisKey = 'vesselStatus'    
                thisKVPair = "'" + thisKey + "': " + thisValue

            elif thisRowKey == 'Daily Plan':
                thisKey = 'dailyPlan'    
                thisKVPair = "'" + thisKey + "': " + thisValue

            elif thisRowKey == 'Weather, Water and Ice Conditions':                
                thisKey = 'conditions'    
                # could split out weather more if needed
                thisKVPair = "'" + thisKey + "': " + thisValue

            elif thisRowKey == 'Helicopter Status':                
                thisKey = 'heliStatus'    
                thisKVPair = "'" + thisKey + "': " + thisValue

            elif thisRowKey == 'Commanding Officer':                 
                thisKey = 'commandingOfficer'    
                thisKVPair = "'" + thisKey + "': " + thisValue

            elif thisRowKey == 'Date and Time of Report':                
                thisKey = 'datetime'    
                thisTimestamp = thisValue
                thisDateTime = thisValue[:-8]
                thisValue = thisDateTime.strip()

                thisDate = time.strptime(thisValue, "%B %d %Y")

                # thisKVPair += "'" + thisKey + "': " + thisValue

        
                # prepare and save data to sqlite
                # thisData += thisKVPair
            


                # thisData = "'timestamp': " + thisTimestamp + ', ' + thisKVPair
                thisData += ', ' + thisKVPair

        if '\n' in thisData:
            thisData = removeNL(thisData)
        thisData  = thisData.replace('  ',' ')


        # print thisDate
        print thisData
        

        # scrapedata = { 'timestamp': thisDate , thisData }
        #scraperwiki.sqlite.save(unique_keys=['thisTimestamp'],data=thisData)





import scraperwiki
import urllib2
import time
import datetime
import dateutil.parser 

from time import strftime
from datetime import datetime
from BeautifulSoup import BeautifulSoup

def removeNL(x):
    """cleans a string of new lines and spaces"""
    s = x.split('\n')
    s = [x.strip() for x in s]
    x = " ".join(s)
    return x.lstrip()


# Create/open a file for data storage
f = open('franklin-shiplog.txt', 'w')


#timestamp for this scraping
now = time.time()


# Open source url and load to Beautiful Soup
url = "http://www.charts.gc.ca/announcements-annonces/2012/Franklin-eng.asp"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)


if soup:

    # Find all the tables containing ship data
    shipLocations = soup.findAll('table')

    # Loop thorough individual tables in the found array
    for index in range(len(shipLocations)):

        # Find all the rows in this table
        thisTableRows = shipLocations[index].findAll('tr')

        # Loop through rows, grabbing header and value strings
        for index2 in range(len(thisTableRows)):
            
            # print index2
            thisTableRowHeader = thisTableRows[index2].findAll('th')
            thisTableRowContent = thisTableRows[index2].findAll('td')

            thisRowKey = thisTableRowHeader[0].string
            thisRowValue = thisTableRowContent[0].string 
            thisValue = thisRowValue
            thisDate = ''
            thisData = ''
            thisKVPair = ''
            thisTimestamp = ''


            # check the headers/value pairs and build up the data
            if thisRowKey == 'Location':
                thisKey = 'location'                    
                thisKVPair = "'" + thisKey + "': " + thisValue 
   
            elif thisRowKey == 'Current Vessel Status':
                thisKey = 'vesselStatus'    
                thisKVPair = "'" + thisKey + "': " + thisValue

            elif thisRowKey == 'Daily Plan':
                thisKey = 'dailyPlan'    
                thisKVPair = "'" + thisKey + "': " + thisValue

            elif thisRowKey == 'Weather, Water and Ice Conditions':                
                thisKey = 'conditions'    
                # could split out weather more if needed
                thisKVPair = "'" + thisKey + "': " + thisValue

            elif thisRowKey == 'Helicopter Status':                
                thisKey = 'heliStatus'    
                thisKVPair = "'" + thisKey + "': " + thisValue

            elif thisRowKey == 'Commanding Officer':                 
                thisKey = 'commandingOfficer'    
                thisKVPair = "'" + thisKey + "': " + thisValue

            elif thisRowKey == 'Date and Time of Report':                
                thisKey = 'datetime'    
                thisTimestamp = thisValue
                thisDateTime = thisValue[:-8]
                thisValue = thisDateTime.strip()

                thisDate = time.strptime(thisValue, "%B %d %Y")

                # thisKVPair += "'" + thisKey + "': " + thisValue

        
                # prepare and save data to sqlite
                # thisData += thisKVPair
            


                # thisData = "'timestamp': " + thisTimestamp + ', ' + thisKVPair
                thisData += ', ' + thisKVPair

        if '\n' in thisData:
            thisData = removeNL(thisData)
        thisData  = thisData.replace('  ',' ')


        # print thisDate
        print thisData
        

        # scrapedata = { 'timestamp': thisDate , thisData }
        #scraperwiki.sqlite.save(unique_keys=['thisTimestamp'],data=thisData)





