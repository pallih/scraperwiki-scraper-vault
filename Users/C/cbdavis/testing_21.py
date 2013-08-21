#TODO translate dates and fuel types from Spanish
#See http://llts.stanford.edu/months.html for months in Spanish
#filter based on lower case
#ene, feb, mar, abr, may, jun, jul, ago, sep, oct, nov, dic,
#TODO figure out what zona centro means w.r.t. the status of a power station

import unicodedata
import scraperwiki
from BeautifulSoup import BeautifulSoup
import lxml.html

def parseTables(soup, plantType, link):

    #should only be one table for operational power plants
    #second table is for out of service plants, third if for 'zona centro', not sure what that means - no location is mentioned
    tables = soup.findAll('table', 'tabDatos')
    
    #list of the headers, translated from Spanish
    headers = ['Name', 'NumberOfUnits', 'DateOfEntryIntoOperation', 'EffectiveInstalledCapacityMW', 'Location']
    
    #variable to keep track of which table we're on
    #used in combination with rowNumber as a unique key
    tableNumber = 0
    
    for table in tables:
        tableNumber += 1
            
        #get all the rows
        rows = table.findAll('tr')
        
        #counter for row numbers - used as a unique key in the sqlite database
        rowNumber = 0
        
        #create a dictionary to hold the data for a single row in the sqlite db
        installationInfo=dict()

        for row in rows:
            rowNumber += 1
        
            #get all the TD elements
            tableDataElements = row.findAll('td')
        
            #check if we're not on the header row
            if (len(tableDataElements) > 0):
        
                skipThisRow = False
            
                #if the text first cell of the table row is in parenthesis, and then second td is blank, then this means
                #that it is an alternative name for the power plant. We then need to grab the previous entry and update it.
                if (len(tableDataElements[1]) == 0):
                    skipThisRow = True
                    #this doesn't work - unicode issue
                    installationInfo[headers[0]] = unicode(installationInfo[headers[0]]) + ' ' + unicode(tableDataElements[0].text)
        
                #commit the data here
                if (len(installationInfo) > 0):
                    installationInfo['reference_link'] = link
                    installationInfo['tableNumber'] = str(tableNumber)                    
                    installationInfo['rowNumber'] = str(rowNumber)
                    installationInfo['plant_type'] = plantType
                    scraperwiki.sqlite.save(unique_keys=['tableNumber', 'rowNumber', 'plant_type'], data=installationInfo)
        
                #create a dictionary to hold the data for a single row in the sqlite db
                installationInfo=dict()
        
                if (skipThisRow == False):
                    if (len(tableDataElements) == 3): #special case - some columns are missing
                        installationInfo[headers[0]] = tableDataElements[0].text
                        installationInfo[headers[1]] = tableDataElements[1].text
                        installationInfo[headers[3]] = tableDataElements[2].text
                    else: 
                        for i in range(len(tableDataElements)):
                            installationInfo[headers[i]] = tableDataElements[i].text

        #commit the data from the last row
        if (len(installationInfo) > 0):
            #this is the source page for the data
            installationInfo['reference_link'] = link
            installationInfo['tableNumber'] = str(tableNumber)                    
            installationInfo['rowNumber'] = str(rowNumber)
            installationInfo['plant_type'] = plantType
            scraperwiki.sqlite.save(unique_keys=['tableNumber', 'rowNumber', 'plant_type'], data=installationInfo)


def parseOtherFuelTypes(soup):
    #create dictionary for which fuel type is associated with each link
    linkForFuelType = dict()
    linksLocation = soup.findAll('td', 'menuinteriorsuperior')[0].findAll('a')
    for link in linksLocation:
        fullURL = 'http://www.cfe.gob.mx/QuienesSomos/estadisticas/listadocentralesgeneradoras/Paginas/' + link['href']    
        fuelType = link['href'].replace('.aspx', '')
        linkForFuelType[fuelType] = fullURL
    
    #parse the rest of the pages listing the different fuel types
    for item in linkForFuelType:
        #print item
        html = scraperwiki.scrape(linkForFuelType[item])
        soup = BeautifulSoup(html)
        parseTables(soup, item, linkForFuelType[item])


################################### MAIN CODE ###################################

#starting page
link = "http://www.cfe.gob.mx/QuienesSomos/estadisticas/listadocentralesgeneradoras/Paginas/listadohidroelectricas.aspx"
html = scraperwiki.scrape(link)
soup = BeautifulSoup(html)

#gets the data for the hydro plants
parseTables(soup, 'Hydro', link)

parseOtherFuelTypes(soup)