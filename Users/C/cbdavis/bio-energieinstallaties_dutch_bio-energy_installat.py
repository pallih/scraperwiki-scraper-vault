import re
import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://b-i-o.nl/")

root = lxml.html.fromstring(html)

#the data we need is actually stored in javascript
for el in root.cssselect("script[language='javascript']"):
    #get the raw code for the javascript
    scriptCode = lxml.html.tostring(el)

    #create a dictionary to hold the data for a single row in the sqlite db
    installationInfo=dict()

    #check if 'bioinstallaties' is in the script
    if 'bioinstallaties' in scriptCode:
        #get all of the data
        items=re.findall("^item.*$",scriptCode,re.MULTILINE)
        for x in items:
            #remove "item."
            x = x.replace("item.", "")
            #remove quotes
            x = x.replace('"', '')
            #remove semicolon at the end
            x = x[:-1]
            #split data into variable name and value
            rowData = x.split(" = ")
            
            #ID signifies new row
            if rowData[0] == 'ID':
                #write previous data to sqlite (if exists)
                if len(installationInfo.keys()) > 0 :
                    scraperwiki.sqlite.save(unique_keys=['ID'], data=installationInfo)
                #initialize new dictionary for current row
                installationInfo = {'ID': rowData[1]}
            else :
                installationInfo[rowData[0]] = rowData[1]import re
import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://b-i-o.nl/")

root = lxml.html.fromstring(html)

#the data we need is actually stored in javascript
for el in root.cssselect("script[language='javascript']"):
    #get the raw code for the javascript
    scriptCode = lxml.html.tostring(el)

    #create a dictionary to hold the data for a single row in the sqlite db
    installationInfo=dict()

    #check if 'bioinstallaties' is in the script
    if 'bioinstallaties' in scriptCode:
        #get all of the data
        items=re.findall("^item.*$",scriptCode,re.MULTILINE)
        for x in items:
            #remove "item."
            x = x.replace("item.", "")
            #remove quotes
            x = x.replace('"', '')
            #remove semicolon at the end
            x = x[:-1]
            #split data into variable name and value
            rowData = x.split(" = ")
            
            #ID signifies new row
            if rowData[0] == 'ID':
                #write previous data to sqlite (if exists)
                if len(installationInfo.keys()) > 0 :
                    scraperwiki.sqlite.save(unique_keys=['ID'], data=installationInfo)
                #initialize new dictionary for current row
                installationInfo = {'ID': rowData[1]}
            else :
                installationInfo[rowData[0]] = rowData[1]