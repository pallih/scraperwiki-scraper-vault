import time
import re
import scraperwiki           
import lxml.html

#!!! Replace NUL characters.  Several of the pages have these, and they cannot be parsed with these in there
html = scraperwiki.scrape("http://www.eon-wasserkraft.com/pages/_Energie-Specials/birdseyeview/index.html").replace('\x00', '')
rootOrig = lxml.html.fromstring(html)

#get the raw code for the javascript
scriptCode = lxml.html.tostring(rootOrig)

coordinateList = []
points=re.findall(".*var point =.*$",scriptCode,re.MULTILINE)
for point in points:
    point = point.replace('var point = new GLatLng(', '')
    point = point.replace(');', '')
    point = point.replace('\r', '')
    point = point.replace(' ', '')
    coordinateList.append(point)

index = 0
markers=re.findall(".*var marker = createMarker.*$",scriptCode,re.MULTILINE)
for marker in markers:
    installationInfo = dict()

    marker = marker.replace('var marker = createMarker(point,', '')
    marker = marker.replace('", "', '","')
    markerInfo = marker.split('","')
    #print markerInfo
    installationInfo['name'] = markerInfo[0].replace('"', '').strip()
    pageURL = 'http://www.eon-wasserkraft.com/pages/_Energie-Specials/birdseyeview/' + markerInfo[3].replace('"', '')
    installationInfo['reference_link'] = pageURL

    #state the obvious
    installationInfo['fuel_type'] = 'Hydro'

    print pageURL

    #don't handle data for the corporate headquarters
    if pageURL == 'http://www.eon-wasserkraft.com/pages/_Energie-Specials/birdseyeview/unternehmensleitung/content.html':
        continue

    #!!! Replace NUL characters.  Several of the pages have these, and they cannot be parsed with these in there
    html = scraperwiki.scrape(pageURL).replace('\x00', '')
    root = lxml.html.fromstring(html)

    points = coordinateList[index].split(',')
    installationInfo['latitude'] = points[0]
    installationInfo['longitude'] = points[1]
    
    #index for matching list of coordinates
    index = index + 1

    #look for the table cell that mentions E.ON
    addressFields = root.xpath("//*[contains(text(),'E.ON Wasserkraft GmbH')]/text()")

    for addressField in addressFields:
        addressField = addressField.strip().replace('\r','') #strip white space
        #skip the first field
        if addressField != 'E.ON Wasserkraft GmbH':
            #TODO this doesn't completely work
            if addressField[4].isdigit():
                installationInfo['cityAndPostCode'] = addressField
            else:
                installationInfo['streetAddress'] = addressField

    #two colons on http://www.eon-wasserkraft.com/pages/_Energie-Specials/birdseyeview/ering/content.html
    #so check for contains text instead of exact match
    try:
        installationInfo['bodyOfWater'] = root.xpath("//td[contains(preceding-sibling::td,'Body of water:')]/text()")[0]
    except:
        print ">>>>>" + html

    try:
        installationInfo['commissioned'] =  root.xpath("//td[contains(preceding-sibling::td,'Commissioned:')]/text()")[0]
    except:
        print ">>>>>" + html

    try:
        installationInfo['systemSize'] = root.xpath("//td[contains(preceding-sibling::td,'System size:')]/text()")[0]
    except:
        print ">>>>>" + html

    scraperwiki.sqlite.save(unique_keys=['name'], data=installationInfo)    import time
import re
import scraperwiki           
import lxml.html

#!!! Replace NUL characters.  Several of the pages have these, and they cannot be parsed with these in there
html = scraperwiki.scrape("http://www.eon-wasserkraft.com/pages/_Energie-Specials/birdseyeview/index.html").replace('\x00', '')
rootOrig = lxml.html.fromstring(html)

#get the raw code for the javascript
scriptCode = lxml.html.tostring(rootOrig)

coordinateList = []
points=re.findall(".*var point =.*$",scriptCode,re.MULTILINE)
for point in points:
    point = point.replace('var point = new GLatLng(', '')
    point = point.replace(');', '')
    point = point.replace('\r', '')
    point = point.replace(' ', '')
    coordinateList.append(point)

index = 0
markers=re.findall(".*var marker = createMarker.*$",scriptCode,re.MULTILINE)
for marker in markers:
    installationInfo = dict()

    marker = marker.replace('var marker = createMarker(point,', '')
    marker = marker.replace('", "', '","')
    markerInfo = marker.split('","')
    #print markerInfo
    installationInfo['name'] = markerInfo[0].replace('"', '').strip()
    pageURL = 'http://www.eon-wasserkraft.com/pages/_Energie-Specials/birdseyeview/' + markerInfo[3].replace('"', '')
    installationInfo['reference_link'] = pageURL

    #state the obvious
    installationInfo['fuel_type'] = 'Hydro'

    print pageURL

    #don't handle data for the corporate headquarters
    if pageURL == 'http://www.eon-wasserkraft.com/pages/_Energie-Specials/birdseyeview/unternehmensleitung/content.html':
        continue

    #!!! Replace NUL characters.  Several of the pages have these, and they cannot be parsed with these in there
    html = scraperwiki.scrape(pageURL).replace('\x00', '')
    root = lxml.html.fromstring(html)

    points = coordinateList[index].split(',')
    installationInfo['latitude'] = points[0]
    installationInfo['longitude'] = points[1]
    
    #index for matching list of coordinates
    index = index + 1

    #look for the table cell that mentions E.ON
    addressFields = root.xpath("//*[contains(text(),'E.ON Wasserkraft GmbH')]/text()")

    for addressField in addressFields:
        addressField = addressField.strip().replace('\r','') #strip white space
        #skip the first field
        if addressField != 'E.ON Wasserkraft GmbH':
            #TODO this doesn't completely work
            if addressField[4].isdigit():
                installationInfo['cityAndPostCode'] = addressField
            else:
                installationInfo['streetAddress'] = addressField

    #two colons on http://www.eon-wasserkraft.com/pages/_Energie-Specials/birdseyeview/ering/content.html
    #so check for contains text instead of exact match
    try:
        installationInfo['bodyOfWater'] = root.xpath("//td[contains(preceding-sibling::td,'Body of water:')]/text()")[0]
    except:
        print ">>>>>" + html

    try:
        installationInfo['commissioned'] =  root.xpath("//td[contains(preceding-sibling::td,'Commissioned:')]/text()")[0]
    except:
        print ">>>>>" + html

    try:
        installationInfo['systemSize'] = root.xpath("//td[contains(preceding-sibling::td,'System size:')]/text()")[0]
    except:
        print ">>>>>" + html

    scraperwiki.sqlite.save(unique_keys=['name'], data=installationInfo)    