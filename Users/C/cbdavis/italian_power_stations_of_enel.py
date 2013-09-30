import scraperwiki
import lxml.html
import unicodedata
import sys #used for debugging - program stops if preferred term is not found


#there are misspellings and variations on the terms
#here we create a dictionary to retrive the prefered term
def createPreferredTermsDict():
    #TODO should just have the preferred term in English, not sure yet what everything means yet
    preferredTermsLookup = dict()
    preferredTermsLookup['anno automazione'] = 'anno automazione'
    preferredTermsLookup['anno di automazione:'] = 'anno automazione'
    preferredTermsLookup['anno di automazione'] = 'anno automazione'
    preferredTermsLookup['anno di automizzazione'] = 'anno automazione'
    preferredTermsLookup['anno di costruzione'] = 'anno di costruzione'
    preferredTermsLookup['combustibile'] = 'combustibile'
    preferredTermsLookup['combustibile gruppi'] = 'combustibile'
    preferredTermsLookup['combustibile.gruppi'] = 'combustibile'
    preferredTermsLookup['combustibili'] = 'combustibile'
    preferredTermsLookup['comune'] = 'comune'
    preferredTermsLookup['impianto am'] = 'impianto amis'
    preferredTermsLookup['impianto amis'] = 'impianto amis'
    preferredTermsLookup['n.aerogeneratori'] = 'n aerogeneratori'
    preferredTermsLookup['n. aerogeneratori'] = 'n aerogeneratori'
    preferredTermsLookup['n aerogeneratori'] = 'n aerogeneratori'
    preferredTermsLookup['n. gruppi'] = 'n gruppi'
    preferredTermsLookup['n.gruppo'] = 'n gruppi'
    preferredTermsLookup['n.gruppi'] = 'n gruppi'
    preferredTermsLookup['n gruppi'] = 'n gruppi'
    preferredTermsLookup['n  gruppi'] = 'n gruppi'
    preferredTermsLookup['n gruppo'] = 'n gruppi'
    preferredTermsLookup['ombustibile'] = 'combustibile'
    preferredTermsLookup['portata'] = 'portata'
    preferredTermsLookup['portenza'] = 'potenza'
    preferredTermsLookup['potenza'] = 'potenza'
    preferredTermsLookup['potenza:'] = 'potenza'
    preferredTermsLookup['potenza in pompaggio'] = 'potenza'
    preferredTermsLookup['potenza installata'] = 'potenza'
    preferredTermsLookup['producibilità'] = 'producibilità'
    preferredTermsLookup['produbilità'] = 'producibilità'
    preferredTermsLookup['producibilità'] = 'producibilità'
    preferredTermsLookup['producibilità anno 2008'] = 'producibilità'
    preferredTermsLookup['producibilità tot'] = 'producibilità'
    preferredTermsLookup['producibilità tot.'] = 'producibilità'
    preferredTermsLookup['producibilità tot:'] = 'producibilità'
    preferredTermsLookup['producibilità tot '] = 'producibilità'
    preferredTermsLookup['produciblità'] = 'producibilità'
    preferredTermsLookup['proucibilità tot'] = 'producibilità'
    preferredTermsLookup['provincia'] = 'provincia'
    preferredTermsLookup['regione'] = 'regione'
    preferredTermsLookup['ritenute'] = 'ritenute'
    preferredTermsLookup['salto'] = 'salto'
    preferredTermsLookup['superficie'] = 'superficie'
    preferredTermsLookup['tecnologia'] = 'tecnologia'
    preferredTermsLookup['tipi macchinario'] = 'tipologia macchinario'
    preferredTermsLookup['tipo amis'] = 'tipo amis'
    preferredTermsLookup['tipo di amcchinario'] = 'tipologia macchinario'
    preferredTermsLookup['tipo di macchinario'] = 'tipologia macchinario'
    preferredTermsLookup['tipologia:'] = 'tipologia'
    preferredTermsLookup['tipologia'] = 'tipologia'
    preferredTermsLookup['tipologia macchinario'] = 'tipologia macchinario'
    preferredTermsLookup['tipo macchinario'] = 'tipologia macchinario'
    preferredTermsLookup['toi macchinario'] = 'tipologia macchinario'
    preferredTermsLookup['torri di raffreddamento'] = 'torri di raffreddamento'
    preferredTermsLookup['tprri di raffreddamento'] = 'torri di raffreddamento'
    return preferredTermsLookup


#starting page, a page for any region in Italy will do
link = "http://www.enel.it/it-IT/impianti/mappa/abruzzo/"
html = scraperwiki.scrape(link)
root = lxml.html.fromstring(html)

#this finds the links to the different regions
links = root.xpath("//div[@class='menu_tendina']//ul//li//a/@href")

#The links are only relative, build up the full URL here
linksToAllRegions = ['http://www.enel.it'+x for x in links]

#these are links to pages describing all the power plants using a particular fuel type in a region
linksToFuelTypeInARegion = []
for regionLink in linksToAllRegions:

    try:
        #parse the page for a region
        regionHtml = scraperwiki.scrape(regionLink)
        regionRoot = lxml.html.fromstring(regionHtml)
        
        
        #Get the tabs on the pages.  Need to find id of 'tab' followed by a number
        #It is important to check for the presence of a number, otherwise other elements of the document will be retrieved
        #http://stackoverflow.com/questions/597944/xpath-expression-for-regex-like-matching
        tabs = regionRoot.xpath("//li[starts-with(@id,'tab') and substring(@id, 4) >= 0 and substring(@id, 4) <= 99999999]")
        
        for tab in tabs:
            #These are the links to pages describing all the power stations of a particular fuel type in a region
            tabLink = tab.xpath("./a/@href")
            #check if empty
            if tabLink != []:
                #if we've found something, create the full URL
                linksToFuelTypeInARegion.append(regionLink + tabLink[0])
    except:
        print "Can't download " + regionLink
    

#add the list of links to all regions - this is because every region page by default shows a fuel type also
#i.e. the Abruzzo page shows Hydro by default, and this isn't picked up by the code above that looks for links within the tabs
linksToFuelTypeInARegion.extend(linksToAllRegions)

#get the dictionary for looking up the preferred terms
#the tables contain misspellings and variations
preferredTermsLookup = createPreferredTermsDict()


#this is where we get the links to individual power stations
for pageDescribingFuelTypeInARegion in linksToFuelTypeInARegion:

    #this is a page that would, for example, list all the hydro stations in a region
    fuelTypeHtml = scraperwiki.scrape(pageDescribingFuelTypeInARegion)
    fuelTypeRoot = lxml.html.fromstring(fuelTypeHtml)

    #these are the links to all the power stations using a particular fuel type within a region
    linksTemp = fuelTypeRoot.xpath("//div[@class='articoli']/ul/li/a/@href")

    #The links are only relative, build up the full URL here
    linksToIndividualPowerStations = ['http://www.enel.it'+x for x in linksTemp]

    #get the data for the individual power stations
    for powerStationPage in linksToIndividualPowerStations:
        
        powerPlantRoot = ""

        try:
            powerPlantHtml = scraperwiki.scrape(powerStationPage)
            powerPlantRoot = lxml.html.fromstring(powerPlantHtml)
        except:
            #have a problem with downloading:
            #http://www.enel.it/it-IT/impianti/mappa/piemonte/fedio_demonte.aspx
            #httplib.BadStatusLine
            #should be ok to rerun the code to update this, since the primary key is based on the URL
            print sys.exc_info()[0]
            print "couldn't download " + powerStationPage

        #only parse if we've found something
        if powerPlantRoot != "":
    
            #Now for the fun part:
            #1) There are alternative versions of the same terms (plural?  misspellings?)
            #2) Some of the terms appear twice but refer to different concepts - 
                #Some of these are just duplicates, for example 2x mentions gas as fuel type: http://www.enel.it/it-IT/impianti/mappa/sicilia/archimede_priolo_gargallo.aspx
                    #For "combustibile", "portata", "producibilità", "regione", and "tipo macchinario" this seems to be the case
                    #For "tipologia", this seems to be (mostly) used for hydro plants.  The first appearance is to mention that it's hydro, the second is to describe the type of hydro
    
    
            powerPlantName = powerPlantRoot.xpath("//h3[@class='h3large']/text()")
            if len(powerPlantName) > 0:
                powerPlantName = powerPlantName[0]
            else: 
                powerPlantName = ""

            #this lists if it's Hydro, Wind, etc.
            powerPlantType = powerPlantRoot.xpath("//div[@class='editorialihp']/p/text()")
            if len(powerPlantType) > 0:
                powerPlantType = powerPlantType[0]
            else: 
                powerPlantType = ""
    
            powerPlantDataRows = powerPlantRoot.xpath("//table[@class='tabella_scheda_impianto']/tr")
    
            installationInfo=dict()
            installationInfo['powerPlantName'] = powerPlantName
            installationInfo['powerPlantType'] = powerPlantType
            #record where we got this information
            installationInfo['reference_link'] = powerStationPage
            
            for dataRow in powerPlantDataRows:
                #there should always be a key so don't check if it exists
                key = dataRow.xpath("./th/text()")[0]
                value = dataRow.xpath("./td/text()")
                if len(value) > 0:
                    value = value[0]
                else:
                    value = ""

                key = key.strip().lower().replace(':','')

                #get the preferred term
                if key.encode("utf-8") in preferredTermsLookup:
                    key = preferredTermsLookup[key.encode("utf-8")]
        
                    #special case check in case have encountered "tipologia" - assume 1st instance is the general technology, the 2nd is the more specific type of technology
                    #1st instance of the key stays the same, 2nd instance is renamed to 'technology type'
                    if key == 'tipologia' and 'tipologia' in installationInfo:
                        key = 'technology type'
    
                    #strip white space
                    value = value.strip()
    
                    #key needs to be simple text - http://stackoverflow.com/questions/6968329/python-utf-8-accents-problem
                    key = unicodedata.normalize('NFD', key.decode('utf-8')).encode('ascii', 'ignore')
    
                    #store to the dictionary
                    installationInfo[key] = value
    
                else: #don't save data for this key/value
                    print "ERROR: No preferred term known for " + key
                    print key.encode("utf-8")
                    print preferredTermsLookup
                    #stop the program until we've figured out what's wrong
                    #there should be a preferred term defined for everything
                    #Exit with an error code to indicate that the scraper is "broken" and in need of attention
                    #It's not that hard to add a new term to a lookup table, but it's harder to realize that there's a term that we missed.
                    sys.exit(1)
    
            #save to the database
            scraperwiki.sqlite.save(unique_keys=['reference_link'], data=installationInfo)import scraperwiki
import lxml.html
import unicodedata
import sys #used for debugging - program stops if preferred term is not found


#there are misspellings and variations on the terms
#here we create a dictionary to retrive the prefered term
def createPreferredTermsDict():
    #TODO should just have the preferred term in English, not sure yet what everything means yet
    preferredTermsLookup = dict()
    preferredTermsLookup['anno automazione'] = 'anno automazione'
    preferredTermsLookup['anno di automazione:'] = 'anno automazione'
    preferredTermsLookup['anno di automazione'] = 'anno automazione'
    preferredTermsLookup['anno di automizzazione'] = 'anno automazione'
    preferredTermsLookup['anno di costruzione'] = 'anno di costruzione'
    preferredTermsLookup['combustibile'] = 'combustibile'
    preferredTermsLookup['combustibile gruppi'] = 'combustibile'
    preferredTermsLookup['combustibile.gruppi'] = 'combustibile'
    preferredTermsLookup['combustibili'] = 'combustibile'
    preferredTermsLookup['comune'] = 'comune'
    preferredTermsLookup['impianto am'] = 'impianto amis'
    preferredTermsLookup['impianto amis'] = 'impianto amis'
    preferredTermsLookup['n.aerogeneratori'] = 'n aerogeneratori'
    preferredTermsLookup['n. aerogeneratori'] = 'n aerogeneratori'
    preferredTermsLookup['n aerogeneratori'] = 'n aerogeneratori'
    preferredTermsLookup['n. gruppi'] = 'n gruppi'
    preferredTermsLookup['n.gruppo'] = 'n gruppi'
    preferredTermsLookup['n.gruppi'] = 'n gruppi'
    preferredTermsLookup['n gruppi'] = 'n gruppi'
    preferredTermsLookup['n  gruppi'] = 'n gruppi'
    preferredTermsLookup['n gruppo'] = 'n gruppi'
    preferredTermsLookup['ombustibile'] = 'combustibile'
    preferredTermsLookup['portata'] = 'portata'
    preferredTermsLookup['portenza'] = 'potenza'
    preferredTermsLookup['potenza'] = 'potenza'
    preferredTermsLookup['potenza:'] = 'potenza'
    preferredTermsLookup['potenza in pompaggio'] = 'potenza'
    preferredTermsLookup['potenza installata'] = 'potenza'
    preferredTermsLookup['producibilità'] = 'producibilità'
    preferredTermsLookup['produbilità'] = 'producibilità'
    preferredTermsLookup['producibilità'] = 'producibilità'
    preferredTermsLookup['producibilità anno 2008'] = 'producibilità'
    preferredTermsLookup['producibilità tot'] = 'producibilità'
    preferredTermsLookup['producibilità tot.'] = 'producibilità'
    preferredTermsLookup['producibilità tot:'] = 'producibilità'
    preferredTermsLookup['producibilità tot '] = 'producibilità'
    preferredTermsLookup['produciblità'] = 'producibilità'
    preferredTermsLookup['proucibilità tot'] = 'producibilità'
    preferredTermsLookup['provincia'] = 'provincia'
    preferredTermsLookup['regione'] = 'regione'
    preferredTermsLookup['ritenute'] = 'ritenute'
    preferredTermsLookup['salto'] = 'salto'
    preferredTermsLookup['superficie'] = 'superficie'
    preferredTermsLookup['tecnologia'] = 'tecnologia'
    preferredTermsLookup['tipi macchinario'] = 'tipologia macchinario'
    preferredTermsLookup['tipo amis'] = 'tipo amis'
    preferredTermsLookup['tipo di amcchinario'] = 'tipologia macchinario'
    preferredTermsLookup['tipo di macchinario'] = 'tipologia macchinario'
    preferredTermsLookup['tipologia:'] = 'tipologia'
    preferredTermsLookup['tipologia'] = 'tipologia'
    preferredTermsLookup['tipologia macchinario'] = 'tipologia macchinario'
    preferredTermsLookup['tipo macchinario'] = 'tipologia macchinario'
    preferredTermsLookup['toi macchinario'] = 'tipologia macchinario'
    preferredTermsLookup['torri di raffreddamento'] = 'torri di raffreddamento'
    preferredTermsLookup['tprri di raffreddamento'] = 'torri di raffreddamento'
    return preferredTermsLookup


#starting page, a page for any region in Italy will do
link = "http://www.enel.it/it-IT/impianti/mappa/abruzzo/"
html = scraperwiki.scrape(link)
root = lxml.html.fromstring(html)

#this finds the links to the different regions
links = root.xpath("//div[@class='menu_tendina']//ul//li//a/@href")

#The links are only relative, build up the full URL here
linksToAllRegions = ['http://www.enel.it'+x for x in links]

#these are links to pages describing all the power plants using a particular fuel type in a region
linksToFuelTypeInARegion = []
for regionLink in linksToAllRegions:

    try:
        #parse the page for a region
        regionHtml = scraperwiki.scrape(regionLink)
        regionRoot = lxml.html.fromstring(regionHtml)
        
        
        #Get the tabs on the pages.  Need to find id of 'tab' followed by a number
        #It is important to check for the presence of a number, otherwise other elements of the document will be retrieved
        #http://stackoverflow.com/questions/597944/xpath-expression-for-regex-like-matching
        tabs = regionRoot.xpath("//li[starts-with(@id,'tab') and substring(@id, 4) >= 0 and substring(@id, 4) <= 99999999]")
        
        for tab in tabs:
            #These are the links to pages describing all the power stations of a particular fuel type in a region
            tabLink = tab.xpath("./a/@href")
            #check if empty
            if tabLink != []:
                #if we've found something, create the full URL
                linksToFuelTypeInARegion.append(regionLink + tabLink[0])
    except:
        print "Can't download " + regionLink
    

#add the list of links to all regions - this is because every region page by default shows a fuel type also
#i.e. the Abruzzo page shows Hydro by default, and this isn't picked up by the code above that looks for links within the tabs
linksToFuelTypeInARegion.extend(linksToAllRegions)

#get the dictionary for looking up the preferred terms
#the tables contain misspellings and variations
preferredTermsLookup = createPreferredTermsDict()


#this is where we get the links to individual power stations
for pageDescribingFuelTypeInARegion in linksToFuelTypeInARegion:

    #this is a page that would, for example, list all the hydro stations in a region
    fuelTypeHtml = scraperwiki.scrape(pageDescribingFuelTypeInARegion)
    fuelTypeRoot = lxml.html.fromstring(fuelTypeHtml)

    #these are the links to all the power stations using a particular fuel type within a region
    linksTemp = fuelTypeRoot.xpath("//div[@class='articoli']/ul/li/a/@href")

    #The links are only relative, build up the full URL here
    linksToIndividualPowerStations = ['http://www.enel.it'+x for x in linksTemp]

    #get the data for the individual power stations
    for powerStationPage in linksToIndividualPowerStations:
        
        powerPlantRoot = ""

        try:
            powerPlantHtml = scraperwiki.scrape(powerStationPage)
            powerPlantRoot = lxml.html.fromstring(powerPlantHtml)
        except:
            #have a problem with downloading:
            #http://www.enel.it/it-IT/impianti/mappa/piemonte/fedio_demonte.aspx
            #httplib.BadStatusLine
            #should be ok to rerun the code to update this, since the primary key is based on the URL
            print sys.exc_info()[0]
            print "couldn't download " + powerStationPage

        #only parse if we've found something
        if powerPlantRoot != "":
    
            #Now for the fun part:
            #1) There are alternative versions of the same terms (plural?  misspellings?)
            #2) Some of the terms appear twice but refer to different concepts - 
                #Some of these are just duplicates, for example 2x mentions gas as fuel type: http://www.enel.it/it-IT/impianti/mappa/sicilia/archimede_priolo_gargallo.aspx
                    #For "combustibile", "portata", "producibilità", "regione", and "tipo macchinario" this seems to be the case
                    #For "tipologia", this seems to be (mostly) used for hydro plants.  The first appearance is to mention that it's hydro, the second is to describe the type of hydro
    
    
            powerPlantName = powerPlantRoot.xpath("//h3[@class='h3large']/text()")
            if len(powerPlantName) > 0:
                powerPlantName = powerPlantName[0]
            else: 
                powerPlantName = ""

            #this lists if it's Hydro, Wind, etc.
            powerPlantType = powerPlantRoot.xpath("//div[@class='editorialihp']/p/text()")
            if len(powerPlantType) > 0:
                powerPlantType = powerPlantType[0]
            else: 
                powerPlantType = ""
    
            powerPlantDataRows = powerPlantRoot.xpath("//table[@class='tabella_scheda_impianto']/tr")
    
            installationInfo=dict()
            installationInfo['powerPlantName'] = powerPlantName
            installationInfo['powerPlantType'] = powerPlantType
            #record where we got this information
            installationInfo['reference_link'] = powerStationPage
            
            for dataRow in powerPlantDataRows:
                #there should always be a key so don't check if it exists
                key = dataRow.xpath("./th/text()")[0]
                value = dataRow.xpath("./td/text()")
                if len(value) > 0:
                    value = value[0]
                else:
                    value = ""

                key = key.strip().lower().replace(':','')

                #get the preferred term
                if key.encode("utf-8") in preferredTermsLookup:
                    key = preferredTermsLookup[key.encode("utf-8")]
        
                    #special case check in case have encountered "tipologia" - assume 1st instance is the general technology, the 2nd is the more specific type of technology
                    #1st instance of the key stays the same, 2nd instance is renamed to 'technology type'
                    if key == 'tipologia' and 'tipologia' in installationInfo:
                        key = 'technology type'
    
                    #strip white space
                    value = value.strip()
    
                    #key needs to be simple text - http://stackoverflow.com/questions/6968329/python-utf-8-accents-problem
                    key = unicodedata.normalize('NFD', key.decode('utf-8')).encode('ascii', 'ignore')
    
                    #store to the dictionary
                    installationInfo[key] = value
    
                else: #don't save data for this key/value
                    print "ERROR: No preferred term known for " + key
                    print key.encode("utf-8")
                    print preferredTermsLookup
                    #stop the program until we've figured out what's wrong
                    #there should be a preferred term defined for everything
                    #Exit with an error code to indicate that the scraper is "broken" and in need of attention
                    #It's not that hard to add a new term to a lookup table, but it's harder to realize that there's a term that we missed.
                    sys.exit(1)
    
            #save to the database
            scraperwiki.sqlite.save(unique_keys=['reference_link'], data=installationInfo)