import scraperwiki
import lxml.html
import unicodedata
import re
from lxml import etree

#translate terms or give preferred version
translateDict = dict()
translateDict[u'Energies \xe9oliennes'] = 'Wind'
translateDict[u'Autres \xe9nergies'] = 'Other'
translateDict['Energies solaires'] = 'Solar'
translateDict['Biogaz'] = 'Biogas'
translateDict['france'] = 'France'
translateDict['portugal'] = 'Portugal'
translateDict['espagne'] = 'Spain'
translateDict['gr%C3%A8ce'] = 'Greece'
translateDict['turquie'] = 'Turkey'
translateDict['allemagne'] = 'Germany'
translateDict['royaumeuni'] = 'United Kingdom'
translateDict['italie'] = 'Italy'
translateDict['canada'] = 'Canada'
translateDict['etatsunis'] = 'United States'
translateDict['belgique'] = 'Belgium'
translateDict['bulgarie'] = 'Bulgaria'
translateDict['mexique'] = 'Mexico'
translateDict['Californie'] = 'California'
translateDict['Etat de Washington'] = 'Washingtom'
translateDict['Pennsylvanie'] = 'Pennsylvania'


#function that checks if key exists before translating
def translate(key):
    if key in translateDict:
        return translateDict[key]
    else:
        return key

#regular expression to look for series of consecutive numbers (years)
numberPattern = re.compile('[0-9]+')

#Data from map at http://www.edf-energies-nouvelles.com/en/business/our-realisations
pageURL = "http://www.edf-energies-nouvelles.com/index.php/flash/xml_realisations"
html = scraperwiki.scrape(pageURL)

#The lxml.html.fromstring function can't be used since this strips out CDATA, which is everywhere in the file
#The XMLParser has to be used instead
parser = etree.XMLParser(strip_cdata=False)
root = etree.fromstring(html, parser)

legend = dict()
legendEntries = root.xpath("//legende/item")
for legendEntry in legendEntries:
    legend [ legendEntry.xpath("./@id")[0] ] = legendEntry.xpath("./text()")[0]

countryLinks = root.xpath("//country/countryDetails/text()")
for countryLink in countryLinks:
    countryLink = 'http://www.edf-energies-nouvelles.com' + countryLink
    print countryLink

    #figure out the country from the link
    country = translate(countryLink.replace('http://www.edf-energies-nouvelles.com/index.php/flash/xml_realisations_country/id/', ''))

    html = scraperwiki.scrape(countryLink)
    parser = etree.XMLParser(strip_cdata=False)
    root = etree.fromstring(html, parser)
    plants = root.xpath("//point")
    for plant in plants:
        installationInfo = dict()
        installationInfo['id'] = plant.xpath("./@id")[0]

        installationInfo['country'] = country

        #The name also contains the capacity most of the time
        name = plant.xpath("./title/text()")[0]

        #split by the mysterious circular unicode character
        if u'\u2022' in name:
            nameAndPower = name.split(u'\u2022')
            installationInfo['name'] = nameAndPower[0]
            #capacity is the second value, also replace comma separator with decimal
            #MWc is peak capacity for solar.  Convert to MW to be consistent with the rest
            installationInfo['capacity'] = nameAndPower[1].replace(',', '.').replace(' MWc', ' MW')
        else:        
            installationInfo['name'] = name
        
        #This is not really the date
        installationInfo['location'] = plant.xpath("./date/text()")[0]
        #This tells when the power station first came online
        installationInfo['description'] = plant.xpath("./description/text()")[0]
        #look for the four digits representing the year in this string

        try:
            m = numberPattern.search(installationInfo['description'])
            installationInfo['year_online'] = m.group()
        except:
            print "no year match in " + installationInfo['description']

        installationInfo['power'] = plant.xpath("./power/text()")[0]
        #This is the fuel type
        installationInfo['fuel_type'] = translate(legend [ plant.xpath("./@color")[0] ])

        #add reference link
        installationInfo['reference_link'] = countryLink

        #primary key is based on id
        scraperwiki.sqlite.save(unique_keys=['id'], data=installationInfo)import scraperwiki
import lxml.html
import unicodedata
import re
from lxml import etree

#translate terms or give preferred version
translateDict = dict()
translateDict[u'Energies \xe9oliennes'] = 'Wind'
translateDict[u'Autres \xe9nergies'] = 'Other'
translateDict['Energies solaires'] = 'Solar'
translateDict['Biogaz'] = 'Biogas'
translateDict['france'] = 'France'
translateDict['portugal'] = 'Portugal'
translateDict['espagne'] = 'Spain'
translateDict['gr%C3%A8ce'] = 'Greece'
translateDict['turquie'] = 'Turkey'
translateDict['allemagne'] = 'Germany'
translateDict['royaumeuni'] = 'United Kingdom'
translateDict['italie'] = 'Italy'
translateDict['canada'] = 'Canada'
translateDict['etatsunis'] = 'United States'
translateDict['belgique'] = 'Belgium'
translateDict['bulgarie'] = 'Bulgaria'
translateDict['mexique'] = 'Mexico'
translateDict['Californie'] = 'California'
translateDict['Etat de Washington'] = 'Washingtom'
translateDict['Pennsylvanie'] = 'Pennsylvania'


#function that checks if key exists before translating
def translate(key):
    if key in translateDict:
        return translateDict[key]
    else:
        return key

#regular expression to look for series of consecutive numbers (years)
numberPattern = re.compile('[0-9]+')

#Data from map at http://www.edf-energies-nouvelles.com/en/business/our-realisations
pageURL = "http://www.edf-energies-nouvelles.com/index.php/flash/xml_realisations"
html = scraperwiki.scrape(pageURL)

#The lxml.html.fromstring function can't be used since this strips out CDATA, which is everywhere in the file
#The XMLParser has to be used instead
parser = etree.XMLParser(strip_cdata=False)
root = etree.fromstring(html, parser)

legend = dict()
legendEntries = root.xpath("//legende/item")
for legendEntry in legendEntries:
    legend [ legendEntry.xpath("./@id")[0] ] = legendEntry.xpath("./text()")[0]

countryLinks = root.xpath("//country/countryDetails/text()")
for countryLink in countryLinks:
    countryLink = 'http://www.edf-energies-nouvelles.com' + countryLink
    print countryLink

    #figure out the country from the link
    country = translate(countryLink.replace('http://www.edf-energies-nouvelles.com/index.php/flash/xml_realisations_country/id/', ''))

    html = scraperwiki.scrape(countryLink)
    parser = etree.XMLParser(strip_cdata=False)
    root = etree.fromstring(html, parser)
    plants = root.xpath("//point")
    for plant in plants:
        installationInfo = dict()
        installationInfo['id'] = plant.xpath("./@id")[0]

        installationInfo['country'] = country

        #The name also contains the capacity most of the time
        name = plant.xpath("./title/text()")[0]

        #split by the mysterious circular unicode character
        if u'\u2022' in name:
            nameAndPower = name.split(u'\u2022')
            installationInfo['name'] = nameAndPower[0]
            #capacity is the second value, also replace comma separator with decimal
            #MWc is peak capacity for solar.  Convert to MW to be consistent with the rest
            installationInfo['capacity'] = nameAndPower[1].replace(',', '.').replace(' MWc', ' MW')
        else:        
            installationInfo['name'] = name
        
        #This is not really the date
        installationInfo['location'] = plant.xpath("./date/text()")[0]
        #This tells when the power station first came online
        installationInfo['description'] = plant.xpath("./description/text()")[0]
        #look for the four digits representing the year in this string

        try:
            m = numberPattern.search(installationInfo['description'])
            installationInfo['year_online'] = m.group()
        except:
            print "no year match in " + installationInfo['description']

        installationInfo['power'] = plant.xpath("./power/text()")[0]
        #This is the fuel type
        installationInfo['fuel_type'] = translate(legend [ plant.xpath("./@color")[0] ])

        #add reference link
        installationInfo['reference_link'] = countryLink

        #primary key is based on id
        scraperwiki.sqlite.save(unique_keys=['id'], data=installationInfo)