import scraperwiki
import lxml.html
from lxml import etree

#define lookup dictionaries for the different codes used
locationTypeLookup = dict()
locationTypeLookup['0'] = "Asset"
locationTypeLookup['1'] = "Project"
locationTypeLookup['2'] = "Asset and Project"

primaryEnergyTypeLookup = dict()
primaryEnergyTypeLookup['0'] = "Thermal"
primaryEnergyTypeLookup['1'] = "Renewables"
primaryEnergyTypeLookup['2'] = "Networks"

secondaryEnergyTypeLookup = dict()
secondaryEnergyTypeLookup['0'] = "Biomass"
secondaryEnergyTypeLookup['1'] = "On-Shore"
secondaryEnergyTypeLookup['2'] = "Off-Shore"
secondaryEnergyTypeLookup['3'] = "Tidal"
secondaryEnergyTypeLookup['4'] = "Hydro"
secondaryEnergyTypeLookup['5'] = "Thermal1"
secondaryEnergyTypeLookup['6'] = "Thermal2"
secondaryEnergyTypeLookup['7'] = "Networks1"
secondaryEnergyTypeLookup['8'] = "Networks2"

countryLookup = dict()
countryLookup['0'] = "Ireland"
countryLookup['1'] = "United Kingdom"

pageURL = "http://www.sse.com/interactivemapxml.aspx"
html = scraperwiki.scrape(pageURL)

#The lxml.html.fromstring function can't be used since this strips out CDATA, which is everywhere in the file
#The XMLParser has to be used instead
parser = etree.XMLParser(strip_cdata=False)
root = etree.fromstring(html, parser)

locations = root.xpath("//locations/location")
for location in locations:
    installationInfo = dict()
    installationInfo['name'] = location.xpath("./@name")[0]
    installationInfo['title'] = location.xpath("./title/@permaLink")[0]
    installationInfo['info'] = location.xpath("./info/text()")[0]
    installationInfo['latitude'] = location.xpath("./latitude/text()")[0]
    installationInfo['longitude'] = location.xpath("./longitude/text()")[0]
    
    installationInfo['type'] = location.xpath("./type/text()")[0]
    installationInfo['currentStatus'] = location.xpath("./currentStatus/text()")[0]
    installationInfo['capacity'] = location.xpath("./capacity/text()")[0]
    installationInfo['homesPowered'] = location.xpath("./homesPowered/text()")[0]
    installationInfo['url'] = location.xpath("./url/text()")[0]

    installationInfo['country'] = countryLookup[location.xpath("./@country")[0]]
    installationInfo['locationType'] = locationTypeLookup[location.xpath("./@locationType")[0]]
    installationInfo['primaryEnergyType'] = primaryEnergyTypeLookup[location.xpath("./@primaryEnergyType")[0]]
    installationInfo['secondaryEnergyType'] = secondaryEnergyTypeLookup[location.xpath("./@secondaryEnergyType")[0]]

    #add reference link
    installationInfo['reference_link'] = 'http://www.sse.com/OurBusiness/AssetsAndProjects/'

    #primary key is based on plantName and location
    scraperwiki.sqlite.save(unique_keys=['title', 'name'], data=installationInfo)import scraperwiki
import lxml.html
from lxml import etree

#define lookup dictionaries for the different codes used
locationTypeLookup = dict()
locationTypeLookup['0'] = "Asset"
locationTypeLookup['1'] = "Project"
locationTypeLookup['2'] = "Asset and Project"

primaryEnergyTypeLookup = dict()
primaryEnergyTypeLookup['0'] = "Thermal"
primaryEnergyTypeLookup['1'] = "Renewables"
primaryEnergyTypeLookup['2'] = "Networks"

secondaryEnergyTypeLookup = dict()
secondaryEnergyTypeLookup['0'] = "Biomass"
secondaryEnergyTypeLookup['1'] = "On-Shore"
secondaryEnergyTypeLookup['2'] = "Off-Shore"
secondaryEnergyTypeLookup['3'] = "Tidal"
secondaryEnergyTypeLookup['4'] = "Hydro"
secondaryEnergyTypeLookup['5'] = "Thermal1"
secondaryEnergyTypeLookup['6'] = "Thermal2"
secondaryEnergyTypeLookup['7'] = "Networks1"
secondaryEnergyTypeLookup['8'] = "Networks2"

countryLookup = dict()
countryLookup['0'] = "Ireland"
countryLookup['1'] = "United Kingdom"

pageURL = "http://www.sse.com/interactivemapxml.aspx"
html = scraperwiki.scrape(pageURL)

#The lxml.html.fromstring function can't be used since this strips out CDATA, which is everywhere in the file
#The XMLParser has to be used instead
parser = etree.XMLParser(strip_cdata=False)
root = etree.fromstring(html, parser)

locations = root.xpath("//locations/location")
for location in locations:
    installationInfo = dict()
    installationInfo['name'] = location.xpath("./@name")[0]
    installationInfo['title'] = location.xpath("./title/@permaLink")[0]
    installationInfo['info'] = location.xpath("./info/text()")[0]
    installationInfo['latitude'] = location.xpath("./latitude/text()")[0]
    installationInfo['longitude'] = location.xpath("./longitude/text()")[0]
    
    installationInfo['type'] = location.xpath("./type/text()")[0]
    installationInfo['currentStatus'] = location.xpath("./currentStatus/text()")[0]
    installationInfo['capacity'] = location.xpath("./capacity/text()")[0]
    installationInfo['homesPowered'] = location.xpath("./homesPowered/text()")[0]
    installationInfo['url'] = location.xpath("./url/text()")[0]

    installationInfo['country'] = countryLookup[location.xpath("./@country")[0]]
    installationInfo['locationType'] = locationTypeLookup[location.xpath("./@locationType")[0]]
    installationInfo['primaryEnergyType'] = primaryEnergyTypeLookup[location.xpath("./@primaryEnergyType")[0]]
    installationInfo['secondaryEnergyType'] = secondaryEnergyTypeLookup[location.xpath("./@secondaryEnergyType")[0]]

    #add reference link
    installationInfo['reference_link'] = 'http://www.sse.com/OurBusiness/AssetsAndProjects/'

    #primary key is based on plantName and location
    scraperwiki.sqlite.save(unique_keys=['title', 'name'], data=installationInfo)