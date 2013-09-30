#The other scraper gets the data from the map, this one gets the capacity
#The names are not directly comparable since the map talks about the actual 
#site of the power plant, while this one details the units.

import re
import scraperwiki           
import lxml.html

fuelLinks = ['http://www.eon-schafft-transparenz.de/kraftwerke/kern?language=en_US', 
                'http://www.eon-schafft-transparenz.de/kraftwerke/braunkohle?language=en_US', 
                'http://www.eon-schafft-transparenz.de/kraftwerke/steinkohle?language=en_US', 
                'http://www.eon-schafft-transparenz.de/kraftwerke/gas?language=en_US', 
                'http://www.eon-schafft-transparenz.de/kraftwerke/oel?language=en_US']

fuelLookup = dict()
fuelLookup['http://www.eon-schafft-transparenz.de/kraftwerke/kern?language=en_US'] = 'Nuclear'
fuelLookup['http://www.eon-schafft-transparenz.de/kraftwerke/braunkohle?language=en_US'] = 'Lignite'
fuelLookup['http://www.eon-schafft-transparenz.de/kraftwerke/steinkohle?language=en_US'] = 'Hard Coal'
fuelLookup['http://www.eon-schafft-transparenz.de/kraftwerke/gas?language=en_US'] = 'Natural Gas'
fuelLookup['http://www.eon-schafft-transparenz.de/kraftwerke/oel?language=en_US'] = 'Fuel Oil'

#get the data for the capacity and commissioning date
for fuelLink in fuelLinks:
    html = scraperwiki.scrape(fuelLink)
    root = lxml.html.fromstring(html)

    rows = root.xpath("//table[@class='info']/tbody/tr")
    for row in rows:
        installationInfo = dict()        

        #make sure that there is data here
        if len(row.xpath("./td[2]/text()")) > 0:
            installationInfo['Name'] = row.xpath("./td[1]/text()")[0].strip()
            installationInfo['Capacity'] = row.xpath("./td[2]/text()")[0]
            installationInfo['Fuel_Type'] = fuelLookup[fuelLink]
            installationInfo['Commissioning_Date'] = row.xpath("./td[3]/text()")[0]
            scraperwiki.sqlite.save(unique_keys=['Name'], data=installationInfo)
#The other scraper gets the data from the map, this one gets the capacity
#The names are not directly comparable since the map talks about the actual 
#site of the power plant, while this one details the units.

import re
import scraperwiki           
import lxml.html

fuelLinks = ['http://www.eon-schafft-transparenz.de/kraftwerke/kern?language=en_US', 
                'http://www.eon-schafft-transparenz.de/kraftwerke/braunkohle?language=en_US', 
                'http://www.eon-schafft-transparenz.de/kraftwerke/steinkohle?language=en_US', 
                'http://www.eon-schafft-transparenz.de/kraftwerke/gas?language=en_US', 
                'http://www.eon-schafft-transparenz.de/kraftwerke/oel?language=en_US']

fuelLookup = dict()
fuelLookup['http://www.eon-schafft-transparenz.de/kraftwerke/kern?language=en_US'] = 'Nuclear'
fuelLookup['http://www.eon-schafft-transparenz.de/kraftwerke/braunkohle?language=en_US'] = 'Lignite'
fuelLookup['http://www.eon-schafft-transparenz.de/kraftwerke/steinkohle?language=en_US'] = 'Hard Coal'
fuelLookup['http://www.eon-schafft-transparenz.de/kraftwerke/gas?language=en_US'] = 'Natural Gas'
fuelLookup['http://www.eon-schafft-transparenz.de/kraftwerke/oel?language=en_US'] = 'Fuel Oil'

#get the data for the capacity and commissioning date
for fuelLink in fuelLinks:
    html = scraperwiki.scrape(fuelLink)
    root = lxml.html.fromstring(html)

    rows = root.xpath("//table[@class='info']/tbody/tr")
    for row in rows:
        installationInfo = dict()        

        #make sure that there is data here
        if len(row.xpath("./td[2]/text()")) > 0:
            installationInfo['Name'] = row.xpath("./td[1]/text()")[0].strip()
            installationInfo['Capacity'] = row.xpath("./td[2]/text()")[0]
            installationInfo['Fuel_Type'] = fuelLookup[fuelLink]
            installationInfo['Commissioning_Date'] = row.xpath("./td[3]/text()")[0]
            scraperwiki.sqlite.save(unique_keys=['Name'], data=installationInfo)
