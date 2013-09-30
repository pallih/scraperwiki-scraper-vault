import scraperwiki
import lxml.html


def parseWindFarmResults(link):

    html = scraperwiki.scrape(link)
    root = lxml.html.fromstring(html)
    #data is stored under two different li classes
    windFarmEntries = root.xpath("//li[@class='impar itemlistado' or @class='par itemlistado']")
    
    #loop over the entries for each wind farm
    for windFarmEntry in windFarmEntries:
        #create new dictionary for this entry
        installationInfo = dict()
        name = windFarmEntry.xpath("./div/strong[@class='nombre']/text()")
        installationInfo['name'] = name[0]
    
        #these are the individual data fields (keys and values)
        dataItems = windFarmEntry.xpath("./div/ul[@class='tipo1']/li")
        for dataItem in dataItems:
    
            #the problem here is that some of the data fields are separated by a '|' and not by html elements - need to parse the raw text
            #get the raw string and start cleaning it up
            dataString = lxml.html.tostring(dataItem).replace('<strong>','').replace('</strong>','').replace('<li>','').replace('</li>','').replace(': ', ':').replace('&#13;', '')
    
            #split up the string
            dataElements = dataString.split('|')
            for dataElement in dataElements:
                dataElement = dataElement.strip()
                keyValuePair = dataElement.split(':')
                key = keyValuePair[0]
                value = keyValuePair[1]
                installationInfo[key] = value
    
        scraperwiki.sqlite.save(unique_keys=['name'], data=installationInfo)

    #find the next page
    nextPageLink = root.xpath("//li[@class='sigpag']/a/@href")
    if (len(nextPageLink) > 0): #check if there is a next page link
        nextPageLink = nextPageLink[0]
        nextPageLink = 'http://www.gamesacorp.com' + nextPageLink
        print nextPageLink
        parseWindFarmResults(nextPageLink)
    else: #nothing more to see
        print 'end'
    

#start page
link = "http://www.gamesacorp.com/en/tratarAplicacionParqueEolico.do"
parseWindFarmResults(link)import scraperwiki
import lxml.html


def parseWindFarmResults(link):

    html = scraperwiki.scrape(link)
    root = lxml.html.fromstring(html)
    #data is stored under two different li classes
    windFarmEntries = root.xpath("//li[@class='impar itemlistado' or @class='par itemlistado']")
    
    #loop over the entries for each wind farm
    for windFarmEntry in windFarmEntries:
        #create new dictionary for this entry
        installationInfo = dict()
        name = windFarmEntry.xpath("./div/strong[@class='nombre']/text()")
        installationInfo['name'] = name[0]
    
        #these are the individual data fields (keys and values)
        dataItems = windFarmEntry.xpath("./div/ul[@class='tipo1']/li")
        for dataItem in dataItems:
    
            #the problem here is that some of the data fields are separated by a '|' and not by html elements - need to parse the raw text
            #get the raw string and start cleaning it up
            dataString = lxml.html.tostring(dataItem).replace('<strong>','').replace('</strong>','').replace('<li>','').replace('</li>','').replace(': ', ':').replace('&#13;', '')
    
            #split up the string
            dataElements = dataString.split('|')
            for dataElement in dataElements:
                dataElement = dataElement.strip()
                keyValuePair = dataElement.split(':')
                key = keyValuePair[0]
                value = keyValuePair[1]
                installationInfo[key] = value
    
        scraperwiki.sqlite.save(unique_keys=['name'], data=installationInfo)

    #find the next page
    nextPageLink = root.xpath("//li[@class='sigpag']/a/@href")
    if (len(nextPageLink) > 0): #check if there is a next page link
        nextPageLink = nextPageLink[0]
        nextPageLink = 'http://www.gamesacorp.com' + nextPageLink
        print nextPageLink
        parseWindFarmResults(nextPageLink)
    else: #nothing more to see
        print 'end'
    

#start page
link = "http://www.gamesacorp.com/en/tratarAplicacionParqueEolico.do"
parseWindFarmResults(link)