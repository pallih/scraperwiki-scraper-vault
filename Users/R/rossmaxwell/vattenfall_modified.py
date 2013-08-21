import scraperwiki
import lxml.html
import re
import json

link = "http://powerplants.vattenfall.com/#/sort/viewed/view/list"
html = scraperwiki.scrape(link)
root = lxml.html.fromstring(html)


#the data we need is actually stored in javascript
for el in root.cssselect("script[type='text/javascript']"):

    #get the raw code for the javascript
    scriptCode = lxml.html.tostring(el)

    #check if '$GL.parts' is in the script - this contains JSON of the plants and their links
    if '$GL.parts' in scriptCode:
        print "Hello Sweden"
        #get all of the data
        items=re.findall("\$GL.parts = {.*$",scriptCode,re.MULTILINE)
        jsonData = items[0].replace('$GL.parts = ', '')
        
        #get rid of scary escape characters
        jsonData = jsonData.replace('\\x26', 'and')
        #get rid of semicolon at the end - this is javascript, not JSON
        jsonData = jsonData[:-1]

        json_object = json.loads(jsonData)

        powerPlantIDs = json_object.keys()        

        for powerPlantID in powerPlantIDs:   
            #create a dictionary to hold the data for a single row in the sqlite db
            installationInfo=dict()

            installationInfo['title'] = json_object[powerPlantID]['title']
            installationInfo['id'] = json_object[powerPlantID]['id']
            installationInfo['text'] = json_object[powerPlantID]['text']
            installationInfo['url'] = "http://powerplants.vattenfall.com" + json_object[powerPlantID]['url']
            installationInfo['electricity'] = json_object[powerPlantID]['electricity']
            installationInfo['capacity'] = json_object[powerPlantID]['capacity']
            installationInfo['commission'] = json_object[powerPlantID]['commission']
            installationInfo['commissioned'] = json_object[powerPlantID]['commissioned']
            installationInfo['thermal'] = json_object[powerPlantID]['thermal']
            installationInfo['thermal_capacity'] = json_object[powerPlantID]['thermal_capacity']
            installationInfo['thermal_capacity_nuclear'] = json_object[powerPlantID]['thermal_capacity_nuclear']
            installationInfo['powerType'] = json_object[powerPlantID]['powerType']
            installationInfo['longitude'] = json_object[powerPlantID]['map']['longitude']
            installationInfo['latitude'] = json_object[powerPlantID]['map']['latitude']

            scraperwiki.sqlite.save(unique_keys=['id'], data=installationInfo)
