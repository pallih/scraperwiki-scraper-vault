#TODO the map data doesn't align exactly with the capacity data
#The maps describe the power plants, while the other pages describe the units within the power plants

import re
import scraperwiki           
import lxml.html


#Human_Readable_Reference_Link
#http://www.eon-schafft-transparenz.de/kraftwerke/atlas?language=en_US

#Reference_Link
#http://www.eon-schafft-transparenz.com/kraftwerke/map?language=en_US


html = scraperwiki.scrape("http://www.eon-schafft-transparenz.com/kraftwerke/map?language=en_US")
root = lxml.html.fromstring(html)

#get the raw code for the javascript
scriptCode = lxml.html.tostring(root)

plants=re.findall(".*resources/gfx/map/cat_1_icon.*$",scriptCode,re.MULTILINE)
for plant in plants:
    installationInfo = dict()
    
    data = plant.split(' = new Array')[1]
    dataElements = data.split(',')
    installationInfo['Latitude'] = dataElements[0].replace('(', '').replace('"', '')
    installationInfo['Longitude'] = dataElements[1].replace('"', '')
    installationInfo['Name'] = dataElements[2].replace('"', '').strip()
    addressInfo = dataElements[3].replace('"', '')

    #get rid of escapes that don't have to be there
    addressInfo = addressInfo.replace('\\', '')
    addressRoot = lxml.html.fromstring(addressInfo)
    longName = addressRoot.xpath("//div[@class='popup']/h1/text()")[0]
    #print addressInfo
    streetName = addressRoot.xpath("//div[@class='popup']/div[1]/text()")
    if len(streetName) > 0:
        installationInfo['streetName'] = streetName[0]
    installationInfo['postCodeAndCity'] = addressRoot.xpath("//div[@class='popup']/div[3]/text()")[0]

    scraperwiki.sqlite.save(unique_keys=['Name'], data=installationInfo)#TODO the map data doesn't align exactly with the capacity data
#The maps describe the power plants, while the other pages describe the units within the power plants

import re
import scraperwiki           
import lxml.html


#Human_Readable_Reference_Link
#http://www.eon-schafft-transparenz.de/kraftwerke/atlas?language=en_US

#Reference_Link
#http://www.eon-schafft-transparenz.com/kraftwerke/map?language=en_US


html = scraperwiki.scrape("http://www.eon-schafft-transparenz.com/kraftwerke/map?language=en_US")
root = lxml.html.fromstring(html)

#get the raw code for the javascript
scriptCode = lxml.html.tostring(root)

plants=re.findall(".*resources/gfx/map/cat_1_icon.*$",scriptCode,re.MULTILINE)
for plant in plants:
    installationInfo = dict()
    
    data = plant.split(' = new Array')[1]
    dataElements = data.split(',')
    installationInfo['Latitude'] = dataElements[0].replace('(', '').replace('"', '')
    installationInfo['Longitude'] = dataElements[1].replace('"', '')
    installationInfo['Name'] = dataElements[2].replace('"', '').strip()
    addressInfo = dataElements[3].replace('"', '')

    #get rid of escapes that don't have to be there
    addressInfo = addressInfo.replace('\\', '')
    addressRoot = lxml.html.fromstring(addressInfo)
    longName = addressRoot.xpath("//div[@class='popup']/h1/text()")[0]
    #print addressInfo
    streetName = addressRoot.xpath("//div[@class='popup']/div[1]/text()")
    if len(streetName) > 0:
        installationInfo['streetName'] = streetName[0]
    installationInfo['postCodeAndCity'] = addressRoot.xpath("//div[@class='popup']/div[3]/text()")[0]

    scraperwiki.sqlite.save(unique_keys=['Name'], data=installationInfo)