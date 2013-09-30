import re
import scraperwiki
import lxml.html

#starting page
html = scraperwiki.scrape("http://www.canwea.ca/farms/wind-farms_e.php")

root = lxml.html.fromstring(html)

#fill in data from the big data and then try to update it later with information from the individual pages if available
#skip first row - it's the table headers
tableRows = root.xpath("//table[@width='520']/tr[position()>1]")

for tableRow in tableRows:
    td = tableRow.cssselect("td")

    #create a dictionary to hold the data for a single row in the sqlite db
    installationInfo=dict()

    #get the id for the wind farm
    installationInfo['id'] = td[0].xpath("./a/@href")[0].split('=')[1]
    #the name is part of the link
    installationInfo['name'] = td[0].xpath("./a/text()")[0].strip()
    installationInfo['province'] = td[1].text.strip()
    installationInfo['dateInstalled'] = td[2].text.strip()
    installationInfo['turbinesAndTotalCapacity'] = td[3].text.strip()
    installationInfo['company'] = td[4].text.strip()
    
    link = td[0].xpath("./a/@href")[0]
    link = link.replace('../', 'http://www.canwea.ca/')
    #try to get coordinates
    try:
        windFarmHtml = scraperwiki.scrape(link)
        rootWindFarm = lxml.html.fromstring(windFarmHtml)    
        
        point=re.findall("^var point0 = new GPoint.*$",windFarmHtml,re.MULTILINE)
        if len(point) > 0:
            point = point[0].replace('var point0 = new GPoint(', '')
            point = point.replace(')', '')
            coords = point.split(',')
            #retrieve the row from the database, and insert the coordinates
            installationInfo['lat'] = coords[1].strip()
            installationInfo['lon'] = coords[0].strip()

    except: #wind farm with ID 8 can't be scraped for some reason
        print link
        print 'something has gone wrong'

    #store the data in the sqlite database
    scraperwiki.sqlite.save(unique_keys=['id'], data=installationInfo)import re
import scraperwiki
import lxml.html

#starting page
html = scraperwiki.scrape("http://www.canwea.ca/farms/wind-farms_e.php")

root = lxml.html.fromstring(html)

#fill in data from the big data and then try to update it later with information from the individual pages if available
#skip first row - it's the table headers
tableRows = root.xpath("//table[@width='520']/tr[position()>1]")

for tableRow in tableRows:
    td = tableRow.cssselect("td")

    #create a dictionary to hold the data for a single row in the sqlite db
    installationInfo=dict()

    #get the id for the wind farm
    installationInfo['id'] = td[0].xpath("./a/@href")[0].split('=')[1]
    #the name is part of the link
    installationInfo['name'] = td[0].xpath("./a/text()")[0].strip()
    installationInfo['province'] = td[1].text.strip()
    installationInfo['dateInstalled'] = td[2].text.strip()
    installationInfo['turbinesAndTotalCapacity'] = td[3].text.strip()
    installationInfo['company'] = td[4].text.strip()
    
    link = td[0].xpath("./a/@href")[0]
    link = link.replace('../', 'http://www.canwea.ca/')
    #try to get coordinates
    try:
        windFarmHtml = scraperwiki.scrape(link)
        rootWindFarm = lxml.html.fromstring(windFarmHtml)    
        
        point=re.findall("^var point0 = new GPoint.*$",windFarmHtml,re.MULTILINE)
        if len(point) > 0:
            point = point[0].replace('var point0 = new GPoint(', '')
            point = point.replace(')', '')
            coords = point.split(',')
            #retrieve the row from the database, and insert the coordinates
            installationInfo['lat'] = coords[1].strip()
            installationInfo['lon'] = coords[0].strip()

    except: #wind farm with ID 8 can't be scraped for some reason
        print link
        print 'something has gone wrong'

    #store the data in the sqlite database
    scraperwiki.sqlite.save(unique_keys=['id'], data=installationInfo)