import scraperwiki
import lxml.html


def parseWindFarmResults(link, columnForName):
    html = scraperwiki.scrape(link)
    root = lxml.html.fromstring(html)

    dataHeaders = root.xpath("//table/thead/tr/th/text()")

    #http://stackoverflow.com/questions/2634122/how-to-ignore-first-element-in-xpath
    windFarmEntries = root.xpath("//table/tbody/tr[position()>1]")

    for windFarmEntry in windFarmEntries:
        installationInfo = dict()
        dataElements = windFarmEntry.xpath("./td/text()")
        count=0
        for dataElement in dataElements:
            key = dataHeaders[count].replace(' ', '_').replace('/', 'or').replace('(', '').replace(')', '')
            installationInfo[key] = dataElement
            count = count + 1
    
        installationInfo['Name'] = installationInfo[columnForName]
        scraperwiki.sqlite.save(unique_keys=['Name'], data=installationInfo)

#This company has both Wind Farms and PV Installations
link = "http://www.wkn-ag.de/en/references/wind-farms/"
parseWindFarmResults(link, 'Wind_Farm')
