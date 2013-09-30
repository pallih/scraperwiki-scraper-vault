import scraperwiki
import lxml.html
import unicodedata

#gets the first element of the list.  If no elements, return empty string
def getFirstElement(resultSet):
    value = ""
    if len(resultSet) > 0:
        value = resultSet[0]
    return value


#data is from http://www.edison.it/it/contatti/impianti-e-centrali.shtml
#this is the xml data used by the map on the link above:
pageURL = "http://www.edison.it/it/data/mappe.xml"
html = scraperwiki.scrape(pageURL)
root = lxml.html.fromstring(html)

#These are the icons to search for which indicate that we're looking at a power station
#The map contains other data such as LNG terminals, oil & gas fields, etc.
iconXPathQuery = "text()='/media/biomassa.jpg'"
iconXPathQuery += " or text()='/media/eolico.jpg'"
iconXPathQuery += " or text()='/media/fotovoltaico.jpg'"
iconXPathQuery += " or text()='/media/Centrale_generica.jpg'"
iconXPathQuery += " or text()='/media/centrale_idro.jpg'"

powerPlants = root.xpath("//contents/imagepath[" + iconXPathQuery + "]/..")

for powerPlant in powerPlants:
    plantType = getFirstElement(powerPlant.xpath("./title/text()"))
    plantName = getFirstElement(powerPlant.xpath("./subtitle/text()"))
    keys = powerPlant.xpath("./description/strong/text()")
    values = powerPlant.xpath("./description/text()")
    
    #the data (probably) isn't parseable by xpath.  The keys are surrounded by <strong> tags
    #but there are no tags surrounding the values
    #the most reliable way is to just chop up the html data
    powerPlantDescription = lxml.html.tostring(powerPlant.xpath("./description")[0])
    powerPlantDescription = powerPlantDescription.replace('<description>', '')
    powerPlantDescription = powerPlantDescription.replace('</description>', '')
    descriptionItems = powerPlantDescription.split('<strong>')

    installationInfo = dict()
    installationInfo['plantType'] = plantType
    installationInfo['plantName'] = plantName
    installationInfo['Location'] = '' #default value for location, ideally should be overwritten below. 
                                      #Location is used as a primary key in combination with the plantName, since some of the plants don't have names (wind parks, etc)
    for descriptionItem in descriptionItems:
        descriptionItem = descriptionItem.replace('<br>', '')
        keyValuePair = descriptionItem.split('</strong> ')
        if len(keyValuePair) > 1:
            key = keyValuePair[0].replace(':','').strip()
            value = keyValuePair[1].replace(']]&gt;', '').strip()
            #check if a valid value exists
            if value != "-":
                key = key.replace('Societ&#224;', 'Owner')
                key = key.replace('Localit&#224;', 'Location')
                key = key.replace('Potenza massima', 'Potenza installata')
                key = key.replace('Tipologia impianto', 'Tipologia')    

                #parse the the value of the website if needed
                if key == "Sito":
                    value = lxml.html.fromstring(value).xpath("//a/@href")[0]
                    value = value.replace('%5C', '/')
                    value = value.replace('%20', '')

                #key needs to be simple text - http://stackoverflow.com/questions/6968329/python-utf-8-accents-problem
                #TODO this doesn't do anything due to the current encoding
                #key = unicodedata.normalize('NFD', key.decode('utf-8')).encode('ascii', 'ignore')
                #print plantName + "\t\tkey=" + key + "\t\t value=" + value

                installationInfo[key] = value

    #add reference link
    installationInfo['reference_link'] = 'http://www.edison.it/it/contatti/impianti-e-centrali.shtml'

    #primary key is based on plantName and location
    scraperwiki.sqlite.save(unique_keys=['plantName', 'Location'], data=installationInfo)
import scraperwiki
import lxml.html
import unicodedata

#gets the first element of the list.  If no elements, return empty string
def getFirstElement(resultSet):
    value = ""
    if len(resultSet) > 0:
        value = resultSet[0]
    return value


#data is from http://www.edison.it/it/contatti/impianti-e-centrali.shtml
#this is the xml data used by the map on the link above:
pageURL = "http://www.edison.it/it/data/mappe.xml"
html = scraperwiki.scrape(pageURL)
root = lxml.html.fromstring(html)

#These are the icons to search for which indicate that we're looking at a power station
#The map contains other data such as LNG terminals, oil & gas fields, etc.
iconXPathQuery = "text()='/media/biomassa.jpg'"
iconXPathQuery += " or text()='/media/eolico.jpg'"
iconXPathQuery += " or text()='/media/fotovoltaico.jpg'"
iconXPathQuery += " or text()='/media/Centrale_generica.jpg'"
iconXPathQuery += " or text()='/media/centrale_idro.jpg'"

powerPlants = root.xpath("//contents/imagepath[" + iconXPathQuery + "]/..")

for powerPlant in powerPlants:
    plantType = getFirstElement(powerPlant.xpath("./title/text()"))
    plantName = getFirstElement(powerPlant.xpath("./subtitle/text()"))
    keys = powerPlant.xpath("./description/strong/text()")
    values = powerPlant.xpath("./description/text()")
    
    #the data (probably) isn't parseable by xpath.  The keys are surrounded by <strong> tags
    #but there are no tags surrounding the values
    #the most reliable way is to just chop up the html data
    powerPlantDescription = lxml.html.tostring(powerPlant.xpath("./description")[0])
    powerPlantDescription = powerPlantDescription.replace('<description>', '')
    powerPlantDescription = powerPlantDescription.replace('</description>', '')
    descriptionItems = powerPlantDescription.split('<strong>')

    installationInfo = dict()
    installationInfo['plantType'] = plantType
    installationInfo['plantName'] = plantName
    installationInfo['Location'] = '' #default value for location, ideally should be overwritten below. 
                                      #Location is used as a primary key in combination with the plantName, since some of the plants don't have names (wind parks, etc)
    for descriptionItem in descriptionItems:
        descriptionItem = descriptionItem.replace('<br>', '')
        keyValuePair = descriptionItem.split('</strong> ')
        if len(keyValuePair) > 1:
            key = keyValuePair[0].replace(':','').strip()
            value = keyValuePair[1].replace(']]&gt;', '').strip()
            #check if a valid value exists
            if value != "-":
                key = key.replace('Societ&#224;', 'Owner')
                key = key.replace('Localit&#224;', 'Location')
                key = key.replace('Potenza massima', 'Potenza installata')
                key = key.replace('Tipologia impianto', 'Tipologia')    

                #parse the the value of the website if needed
                if key == "Sito":
                    value = lxml.html.fromstring(value).xpath("//a/@href")[0]
                    value = value.replace('%5C', '/')
                    value = value.replace('%20', '')

                #key needs to be simple text - http://stackoverflow.com/questions/6968329/python-utf-8-accents-problem
                #TODO this doesn't do anything due to the current encoding
                #key = unicodedata.normalize('NFD', key.decode('utf-8')).encode('ascii', 'ignore')
                #print plantName + "\t\tkey=" + key + "\t\t value=" + value

                installationInfo[key] = value

    #add reference link
    installationInfo['reference_link'] = 'http://www.edison.it/it/contatti/impianti-e-centrali.shtml'

    #primary key is based on plantName and location
    scraperwiki.sqlite.save(unique_keys=['plantName', 'Location'], data=installationInfo)
