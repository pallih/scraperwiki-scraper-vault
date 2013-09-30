import scraperwiki
import lxml.html
import unicodedata


def processPowerPlantData(linkToPlant):
    #create new dictionary for this entry
    installationInfo = dict()

    print linkToPlant
    installationInfo['reference'] = linkToPlant
    html = scraperwiki.scrape(linkToPlant)
    plantroot = lxml.html.fromstring(html)
    dataRows = plantroot.xpath("//div[@class='tableContainer']/table/tbody/tr")
    for dataRow in dataRows:
        key = dataRow.xpath("./td[1]/span/text()")[0]
        value = lxml.html.tostring(dataRow.xpath("./td[2]")[0])
        value = value.replace('<td>', '').replace('</td>', '')
        value = value.replace('<br>', ',')
        value = value.replace('<td class="noBorder">', '')
        value = value.replace('</li>', ',').replace('<li>', '')
        value = value.replace('</ul>', '')
        value = value.replace('<ul class="coal">', '')
        value = value.replace('&#8211;', '-')
        value = value.replace('<p>', '').replace('</p>', '')
        #fix unicode issues, u'\xa0 encountered for https://www.clpgroup.com/ouroperations/assetsandservices/powergeneraton/naturalgaspowerplants/Pages/blackpointpowerstation.aspx
        #can't seem to find this in the source of the page
        key = key.replace(u'\xa0', '_') 
        value = value.replace(u'\xa0', ',') 
        key = key.replace(' ', '_')
        installationInfo[key] = value
    scraperwiki.sqlite.save(unique_keys=['Title'], data=installationInfo)    



link = "https://www.clpgroup.com/ouroperations/assetsandservices/powergeneraton/Pages/powergeneration.aspx"
html = scraperwiki.scrape(link)
root = lxml.html.fromstring(html)

#don't look at purchase agreements
plantCategories = root.xpath("//div[@class='euql_opp_title']/a[text()!='Coal-fired power purchase' and text()!='Natural gas power purchase']")

for plantsInCategory in plantCategories:
    plantType = plantsInCategory.xpath("../a/text()")[0]
    plantsInCategory.xpath("../a/text()")[0]

    if plantType != 'Renewable energy': 
        listOfPlants = plantsInCategory.xpath("../../div[position()=2]/ul/li/a/@href")
        for plantLink in listOfPlants:
            linkToPlant = 'https://www.clpgroup.com' + plantLink
            processPowerPlantData(linkToPlant)
            

    else: #special case - traverse down an extra level
        renewableEnergyTypes = plantsInCategory.xpath("../../div[position()=2]/ul/li")
        for renewableEnergyType in renewableEnergyTypes:
            plantType = renewableEnergyType.xpath("./a/text()")[0]
            listOfPlants = renewableEnergyType.xpath("./div/ul/li/a/@href")
            for plantLink in listOfPlants:
                linkToPlant = 'https://www.clpgroup.com' + plantLink
                processPowerPlantData(linkToPlant)
import scraperwiki
import lxml.html
import unicodedata


def processPowerPlantData(linkToPlant):
    #create new dictionary for this entry
    installationInfo = dict()

    print linkToPlant
    installationInfo['reference'] = linkToPlant
    html = scraperwiki.scrape(linkToPlant)
    plantroot = lxml.html.fromstring(html)
    dataRows = plantroot.xpath("//div[@class='tableContainer']/table/tbody/tr")
    for dataRow in dataRows:
        key = dataRow.xpath("./td[1]/span/text()")[0]
        value = lxml.html.tostring(dataRow.xpath("./td[2]")[0])
        value = value.replace('<td>', '').replace('</td>', '')
        value = value.replace('<br>', ',')
        value = value.replace('<td class="noBorder">', '')
        value = value.replace('</li>', ',').replace('<li>', '')
        value = value.replace('</ul>', '')
        value = value.replace('<ul class="coal">', '')
        value = value.replace('&#8211;', '-')
        value = value.replace('<p>', '').replace('</p>', '')
        #fix unicode issues, u'\xa0 encountered for https://www.clpgroup.com/ouroperations/assetsandservices/powergeneraton/naturalgaspowerplants/Pages/blackpointpowerstation.aspx
        #can't seem to find this in the source of the page
        key = key.replace(u'\xa0', '_') 
        value = value.replace(u'\xa0', ',') 
        key = key.replace(' ', '_')
        installationInfo[key] = value
    scraperwiki.sqlite.save(unique_keys=['Title'], data=installationInfo)    



link = "https://www.clpgroup.com/ouroperations/assetsandservices/powergeneraton/Pages/powergeneration.aspx"
html = scraperwiki.scrape(link)
root = lxml.html.fromstring(html)

#don't look at purchase agreements
plantCategories = root.xpath("//div[@class='euql_opp_title']/a[text()!='Coal-fired power purchase' and text()!='Natural gas power purchase']")

for plantsInCategory in plantCategories:
    plantType = plantsInCategory.xpath("../a/text()")[0]
    plantsInCategory.xpath("../a/text()")[0]

    if plantType != 'Renewable energy': 
        listOfPlants = plantsInCategory.xpath("../../div[position()=2]/ul/li/a/@href")
        for plantLink in listOfPlants:
            linkToPlant = 'https://www.clpgroup.com' + plantLink
            processPowerPlantData(linkToPlant)
            

    else: #special case - traverse down an extra level
        renewableEnergyTypes = plantsInCategory.xpath("../../div[position()=2]/ul/li")
        for renewableEnergyType in renewableEnergyTypes:
            plantType = renewableEnergyType.xpath("./a/text()")[0]
            listOfPlants = renewableEnergyType.xpath("./div/ul/li/a/@href")
            for plantLink in listOfPlants:
                linkToPlant = 'https://www.clpgroup.com' + plantLink
                processPowerPlantData(linkToPlant)
