import scraperwiki
import lxml.html
import re
import json
import htmlentitydefs

#http://effbot.org/zone/re-sub.htm#unescape-html
##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)



link = "http://powerplants.vattenfall.com/#/sort/viewed/view/list"
html = scraperwiki.scrape(link)
root = lxml.html.fromstring(html)


#the data we need is actually stored in javascript
for el in root.cssselect("script[type='text/javascript']"):

    #get the raw code for the javascript
    scriptCode = lxml.html.tostring(el)

    #check if '$GL.parts' is in the script - this contains JSON of the plants and their links
    if '$GL.parts' in scriptCode:
        print "hello"
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

            installationInfo['title'] = unescape(json_object[powerPlantID]['title'])
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
