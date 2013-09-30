import scraperwiki
import lxml.html
import unicodedata

link = "http://www.enelgreenpower.com/en-GB/plants/map/Impianti.xml"

html = scraperwiki.scrape(link)
root = lxml.html.fromstring(html)

continents = root.xpath("//continent")
for continent in continents:
    continentName = continent.xpath("./@name")[0]
    countries = continent.xpath("./country")
    for country in countries:
        countryName = country.xpath("./@name")[0]
        regions = country.xpath("./region")
        for region in regions:
            regionName = region.xpath("./@name")[0]
            plants = region.xpath("./impianto")
            for plant in plants:
                installationInfo = dict()

                installationInfo['Continent'] = continentName.title()
                installationInfo['Country'] = countryName.title()
                installationInfo['Region'] = regionName.title()

                #TODO translate these
                installationInfo['id'] = plant.xpath("./@id")[0]
                #installationInfo['PR'] = plant.xpath("./@pr")[0]
                installationInfo['City'] = plant.xpath("./@comune")[0]
                installationInfo['Address'] = plant.xpath("./@indirizzo")[0]
                installationInfo['Coordinates'] = plant.xpath("./@coordinate")[0]
                installationInfo['Name'] = plant.xpath("./@denominazione")[0].title()
                installationInfo['Fuel_Type'] = plant.xpath("./@fonte")[0].title()
                installationInfo['Capacity'] = plant.xpath("./@capacity")[0].replace(',', '.') #change comma to period

                #is this the main owner, of which Enel is the parent?  What does the participant mean?
                installationInfo['Partecipazione_Enel'] = plant.xpath("./@partecipazione_enel")[0]
                installationInfo['Perc'] = plant.xpath("./@perc")[0] #seems to be the Capacity in kW
                installationInfo['Plants_number'] = plant.xpath("./@plants_number")[0] #what is this?  'id' seems to be enough
                
                #add reference link
                installationInfo['Human_Readable_Reference_Link'] = 'http://www.enelgreenpower.com/en-GB/plants/map/'
                installationInfo['Reference_Link'] = 'http://www.enelgreenpower.com/en-GB/plants/map/Impianti.xml'

                #primary key is based on id
                scraperwiki.sqlite.save(unique_keys=['id'], data=installationInfo)
import scraperwiki
import lxml.html
import unicodedata

link = "http://www.enelgreenpower.com/en-GB/plants/map/Impianti.xml"

html = scraperwiki.scrape(link)
root = lxml.html.fromstring(html)

continents = root.xpath("//continent")
for continent in continents:
    continentName = continent.xpath("./@name")[0]
    countries = continent.xpath("./country")
    for country in countries:
        countryName = country.xpath("./@name")[0]
        regions = country.xpath("./region")
        for region in regions:
            regionName = region.xpath("./@name")[0]
            plants = region.xpath("./impianto")
            for plant in plants:
                installationInfo = dict()

                installationInfo['Continent'] = continentName.title()
                installationInfo['Country'] = countryName.title()
                installationInfo['Region'] = regionName.title()

                #TODO translate these
                installationInfo['id'] = plant.xpath("./@id")[0]
                #installationInfo['PR'] = plant.xpath("./@pr")[0]
                installationInfo['City'] = plant.xpath("./@comune")[0]
                installationInfo['Address'] = plant.xpath("./@indirizzo")[0]
                installationInfo['Coordinates'] = plant.xpath("./@coordinate")[0]
                installationInfo['Name'] = plant.xpath("./@denominazione")[0].title()
                installationInfo['Fuel_Type'] = plant.xpath("./@fonte")[0].title()
                installationInfo['Capacity'] = plant.xpath("./@capacity")[0].replace(',', '.') #change comma to period

                #is this the main owner, of which Enel is the parent?  What does the participant mean?
                installationInfo['Partecipazione_Enel'] = plant.xpath("./@partecipazione_enel")[0]
                installationInfo['Perc'] = plant.xpath("./@perc")[0] #seems to be the Capacity in kW
                installationInfo['Plants_number'] = plant.xpath("./@plants_number")[0] #what is this?  'id' seems to be enough
                
                #add reference link
                installationInfo['Human_Readable_Reference_Link'] = 'http://www.enelgreenpower.com/en-GB/plants/map/'
                installationInfo['Reference_Link'] = 'http://www.enelgreenpower.com/en-GB/plants/map/Impianti.xml'

                #primary key is based on id
                scraperwiki.sqlite.save(unique_keys=['id'], data=installationInfo)
