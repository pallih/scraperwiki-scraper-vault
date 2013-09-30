import scraperwiki
import lxml.html
import re
import urllib2

###############
html =scraperwiki.scrape("http://www.menulog.com.au/himalaya_pakistani_indian_restaurant_rockdale")
run = 2 #1 for menu, 2 for modifiers

#Change according to whatever computer is being used:
#Jimylig's 13" MBP:
    #Google Chrome:
#heads = {"Cookie":"PHPSESSID=l0mitdgj226hdp3utlc3unpbu7; SERVERID=www_mlweb6_1; __utma=159154086.1347556771.1349857474.1349857474.1349857474.1; __utmb=159154086.3.10.1349857474; __utmc=159154086; __utmz=159154086.1349857474.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)"}

#Phil's MBP:
    #Google Chrome:
#heads = {"Cookie":"PHPSESSID=d4kqbd5mekri2lnqfegtnvvoe3; SERVERID=www_mlweb6_1; WRUID=4849193.508293249; WRIgnore=true; __utma=159154086.1610577125.1346980519.1348626424.1349225596.30; __utmb=159154086.6.9.1349225614480; __utmc=159154086; __utmz=159154086.1346980519.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)"}

#Andrew's 13" inch MBP:
    #Chrome:
heads = {"Cookie":"PHPSESSID=a1bc0beb29e66a360e792ea540483598; SERVERID=www_mlweb6_1; WRUID=1213540462.1681966284; WRIgnore=true; __utma=159154086.1900219217.1337396703.1348626277.1349225008.6; __utmb=159154086.7.9.1349225085076; __utmc=159154086; __utmz=159154086.1341031985.4.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)"}


###############


if run is 1:
    print "Getting menu"
elif run is 2:
    print "Getting modifiers"
else:
    print "no flag given"

root = lxml.html.fromstring(html)


restaurantId = ""
restaurantScripts = root.cssselect("script[type='text/javascript']")

for script in restaurantScripts:
    scriptContent = script.text_content()
    restaurantIdPattern = re.compile(r'restaurantId: \d+,')
    restIdMatch = restaurantIdPattern.search(scriptContent)
    if restIdMatch:
        restaurantId = restIdMatch.group().lstrip('restaurantId: ')
        restaurantId = restaurantId.rstrip(',')    
        #print "restaurantId: ", restaurantId
        break
if restaurantId == "":
    print "ERROR: no restaurant Id found on page. Cannot get modifiers."
#####


menu = root.cssselect("ul[class='foodItems']")
menuGroups = root.cssselect("li[class='course']")
#print len(menuGroups)

itemSizeNameKey = 'itemSizeName'
itemSizePriceKey = 'itemSizePrice'
itemSizeIdKey = 'itemSizeId'

menuGroupPosition = -1
currentSku = 0
modifierId = 0

dataList = []
id = 0
modifierGroupPosition = -1
modifierGroupDict = {}
for menuGroup in menuGroups:
    menuGroupPosition += 1    

    heading = menuGroup.cssselect("h3")
    menuGroupName = heading[0].text_content()
    menuGroupName = menuGroupName.strip()
    #print "Menu Group: ", menuGroupName
    menuItems = menuGroup.cssselect("ul")[0].cssselect("li")
    #print "Menu Group Size: ", len(menuItems)

    menuItemPosition = -1
    modifierGroupCount = 1
    for menuItem in menuItems:
        menuItemPosition += 1
        menuItemName = menuItem.cssselect("h4")[0].text_content()
        menuItemDescElement = menuItem.cssselect("p")
        menuItemDescription = ""
        if len(menuItemDescElement) > 0:
            menuItemDescription = menuItemDescElement[0].text_content()

        #get rid of newlines:
        descLines = menuItemDescription.splitlines()
        menuItemDescription = ""
        for descLine in descLines:
            menuItemDescription += descLine + " "
        
    #Check for multiple item sizes and prices
        price =""
        itemSizePricesList = []
        itemSizeNamesList = []
        itemSizeList = []

        itemSizeId = ""
        itemSizesElement = menuItem.cssselect("div[class='varieties singleVariety']")
        if len(itemSizesElement) > 0:
            #single item size:
            price = itemSizesElement[0].text_content()
            price = price.strip()
            
            #Get itemSize Id:
            inputElement = itemSizesElement[0].cssselect("input")[0]
            itemSizeId = inputElement.attrib['value']
            #print "itemSizeId: ", itemSizeId
            
            itemSizeDict = {
                            itemSizeNameKey : "",
                            itemSizePriceKey : price,
                            itemSizeIdKey : itemSizeId
                            }
            itemSizeList.append(itemSizeDict)
                    
        else:
            #multiple item sizes:
            itemSizesElement = menuItem.cssselect("div[class='varieties jsBrowserVer']")
            if len(itemSizesElement) > 0:
                
                for itemSize in itemSizesElement[0].cssselect("label"):
                    nextItemSizeString = itemSize.text_content()
                    
                    pattern = re.compile(r'\$.+')
                    match = pattern.search(nextItemSizeString)
                    nextItemSizePrice = match.group()

                    nextItemSizeName = nextItemSizeString.rstrip(nextItemSizePrice)
                    nextItemSizeName = nextItemSizeName.strip()
                    #print "-- Item Size Name: ", nextItemSizeName


                    #Get itemSize Id:
                    inputElement = itemSize.cssselect("input")[0]
                    itemSizeId = inputElement.attrib['value']
                    #print "Multiple itemSizeId: ", itemSizeId
                    
                    itemSizeDict = {
                                    itemSizeNameKey : nextItemSizeName,
                                    itemSizePriceKey : nextItemSizePrice,
                                    itemSizeIdKey : itemSizeId
                                    }

                    itemSizeList.append(itemSizeDict)
            else:
                itemSizeDict = {itemSizeNameKey : "", itemSizePriceKey : "", itemSizeIdKey : ""}
                itemSizeList.append(itemSizeDict)
                print "ERROR: No price found for item: ", menuItemName

        es = "" #empty string
        SKUs=[es,es,es,es,es,es]
        menuItemSizeNames=[es,es,es,es,es,es]
        menuItemPrices=[es,es,es,es,es,es]
        modifierGroupStrings=[es,es,es,es,es,es]
        mealSuggestions=[es,es,es,es,es,es]


        #print menuItemName
        #print itemSizeList
        sizeCount = 0
        for nextItemSize in itemSizeList:
            SKUs[sizeCount] = currentSku
            currentSku += 1
            
            menuItemSizeNames[sizeCount] = nextItemSize[itemSizeNameKey]
            menuItemPrices[sizeCount] = nextItemSize[itemSizePriceKey]


            
############################################################################################################################################
#MODIFIERS:
            
            itemSizeId = nextItemSize[itemSizeIdKey]
            modifierFormRequest = "varietyId="+ itemSizeId + "&action=add&restaurantId=" + restaurantId
            request = urllib2.Request("http://www.menulog.com.au/takeaway/ajax_update_cart.php", data=modifierFormRequest, headers=heads)
            
            page = urllib2.urlopen(request)
            response = page.read()
#            print "Response: ", response

            errorPattern = re.compile("error")
            errorMatch = errorPattern.search(response)

#            responseErrorMessage = '[["error","Sorry, a problem has occurred. Please try again later"]]'
            if errorMatch:
                print "ERROR: HTTP response for modifiers is incorrect for menu item; ",menuItemName,", in menu group; ",menuGroupName,". Try inputting delivery details for the current restaurant and menu item on the ML website"

            popupHtml = lxml.html.fromstring(response)
#            print "menu item: ", menuItemName
            modifierClumpElement = popupHtml.cssselect("h5")
            if modifierClumpElement:
                modifierClump = modifierClumpElement[0].text_content()
    
                #print "modifierClump: ", modifierClump
                
                modifierGroups = modifierClump.split("Choice(s)")
                modGroupsHtml = response.split("Choice(s)")
                #print "modifierGroups: ", modifierGroups
                #print "modGroupsHtml: ", modGroupsHtml
                
               
                modifierNameLists = []
                modifierPriceLists = []
                
                index = 0
                modifierGroupsString = ""
                for modifierGroup in modifierGroups:
                    #print "Modifier Group: ", modifierGroup
                    if modifierGroup.strip() != "":
                        modifierPattern = re.compile(r'\\n[^\\]+\\n')
                        matches = modifierPattern.findall(modifierGroup)
                        modifiers = []
                        for match in matches:
                            modifiers.append((match.lstrip(r'\\n')).rstrip(r'\\n'))
                        #print "Modifiers: ", modifiers
                        #print "Number of modifiers for current group: ", len(modifiers)
                        
                        modifierGroupName = menuGroupName + "-" + menuItemSizeNames[sizeCount] + str(modifierGroupCount)
                        modifierGroupCount+=1
                        #Check if modifier group already exists:
                        modifierGroupKey = modifiers[0] 
                        #Assume if the first modifier exists, the rest of the modifiers match the same group
                        if modifierGroupKey in modifierGroupDict:
                            #if it does, add modifier group to comma-seperated list of modifiers and skip creation of modifiers
                            modifierGroupsString += modifierGroupDict[modifierGroupKey] + ","
                            continue
                        #Add to dictionary of existing modifier Groups. Map all modifier items to modifier Group
                        for modifier in modifiers:
                            modifierGroupDict[modifier] = modifierGroupName
                        modifierGroupPosition+=1
                        
                        #extract names and prices:
                        namePattern = re.compile(r'.*\+')
                        pricePattern = re.compile(r'\+.*')
                        
                        modifierNames = []
                        modifierPrices = []
                        for modifier in modifiers:
                            nameMatch = namePattern.search(modifier)
                            if nameMatch:
                                modifierName = nameMatch.group().rstrip("+")
                                modifierName = modifierName.strip()
                                modifierNames.append(modifierName)
                                
                                #if modifier name and price exist, add price:
                                priceMatch = pricePattern.search(modifier)
                                if priceMatch:
                                    modifierPrice = priceMatch.group().lstrip("+")
                                    modifierPrice = modifierPrice.strip()
                                    modifierPrice = modifierPrice.lstrip("$")
                                    modifierPrices.append(modifierPrice)
                                else:
                                    modifierPrices.append("")
                                
                            else: #if no price:
                                modifierName = modifier.strip()
                                modifierNames.append(modifierName)
                                modifierPrices.append("")

                        


                
                        #print "modifier names: ", modifierNames
                        #print "modifier prices: ", modifierPrices
                        modifierNameLists.append(modifierNames)
                        modifierPriceLists.append(modifierPrices)
                
                
                        #set radio or checkbox type:
                
                        firstModifier = modifierNames[0]
                        checkboxPattern = re.compile(r'core-ignoreTransformInput checkbox\\" \\/>\\n' + firstModifier)
                        radioPattern = re.compile(r'core-ignoreTransformInput radio\\" \\/>\\n' + firstModifier)
                        modifierGroupHtml = modGroupsHtml[index]
                        checkboxMatch = checkboxPattern.search(modifierGroupHtml)
                        radioMatch = radioPattern.search(modifierGroupHtml)
                        radio = "radio"
                        checkbox = "checkbox"
                        selectionType = radio
                
                        if checkboxMatch:
                            #print checkboxMatch.group()
                            selectionType = checkbox
                        elif radioMatch:
                            #print radioMatch.group()
                            pass
                        else:
                            #print "No checkbox type pattern found"
                            pass
                
                        #print "Selection type: ", selectionType

                        #Save modifier groups in comma seperated string:
                        
                        
                        modifierGroupsString += modifierGroupName + ","
                        
                        

                        #default radio
                        modifierMinSelect = "1"
                        modifierMaxSelect = "1"
                        if selectionType == radio:
                            modifierMinSelect = "1"
                            modifierMaxSelect = "1"
                        elif selectionType == checkbox:
                            modifierMinSelect = "0"
                            modifierMaxSelect = ""
                        else:
                            print "No Check Box type found for menu item: ", menItemName, " in modifier group: " , modifierGroupName ,", defaulting to radio type"
                            pass
                            
                        #modifierNames = []
                        #modifierPrices = []
                        modifierCount = 0
                        for nextModifierName in modifierNames:
                            nextModifierPrice = modifierPrices[modifierCount]

                            if run == 2:
                                #Save Modifier Data:
                                modifierData = {
                                                    'modifierId' : modifierId,
                                                    'ModifierGroup': modifierGroupName,
                                                    'ModifierGroupPosition' : modifierGroupPosition,
                                                    'ModifierMinSelect' : modifierMinSelect,
                                                    'ModifierMaxSelect' : modifierMaxSelect,
                                                    'ModifierPosition' : modifierCount,
                                                    'ItemSizeSKU' : "",
                                                    'ItemSizeName' : nextModifierName,
                                                    'AdditivePrice' : nextModifierPrice,
                                                }
                                modifierCount += 1
                                modifierId += 1
        
                                dataList.append(modifierData)
                                id += 1
                        
                        
                        
                    else:
                        #print "Empty Modifier Group"
                        pass
                    index += 1
                modifierString = (modifierGroupsString.strip()).rstrip(",")
                modifierGroupStrings[sizeCount] = modifierString
                
                #print "modifierNameLists: ", modifierNameLists
                #print "modifierPriceLists: ", modifierPriceLists
                
                #print "Names: ", modifierNames
                #print "Prices: ", modifierPrices
            else:
                #no modifiers:
                pass

            sizeCount += 1
            


############################################################################################################################################
        if run== 1:
            menuItemData = {
                            'ID' : id,
                            'MenuGroupName' : menuGroupName,
                            'MenuGroupDescription' : '',
                            'MenuGroupStartTime' : '',
                            'MenuGroupEndTime' : '',
                            'MenuGroupIncludingDays' : '',
                            'MenuGroupPosition' : menuGroupPosition,
                            'MenuGroupVisible' : 'TRUE',

                            'MenuItemName' : menuItemName,
                            'MenuItemPosition' : menuItemPosition,
                            'MenuItemDescription' : menuItemDescription,
                            'MenuItemVisible' : 'TRUE',
    
                            'MenuItemSize_1_SKU' : SKUs[0],
                            'MenuItemSize_1_Name' : menuItemSizeNames[0],
                            'MenuItemSize_1_Price' : menuItemPrices[0],
                            'MenuItemSize_1_Modifiers' : modifierGroupStrings[0],
                            'MenuItemSize_1_NutritionalKJ' : "",
                            'MenuItemSize_1_Position' : 0,
                            'MenuItemSize_1_Suggestions' : mealSuggestions[0],
    
                            'MenuItemSize_2_SKU' : SKUs[1],
                            'MenuItemSize_2_Name' : menuItemSizeNames[1],
                            'MenuItemSize_2_Price' : menuItemPrices[1],
                            'MenuItemSize_2_Modifiers' : modifierGroupStrings[1],
                            'MenuItemSize_2_NutritionalKJ' : "",
                            'MenuItemSize_2_Position' : 0,
                            'MenuItemSize_2_Suggestions' : mealSuggestions[1],
    
                            'MenuItemSize_3_SKU' : SKUs[2],
                            'MenuItemSize_3_Name' : menuItemSizeNames[2],
                            'MenuItemSize_3_Price' : menuItemPrices[2],
                            'MenuItemSize_3_Modifiers' : modifierGroupStrings[2],
                            'MenuItemSize_3_NutritionalKJ' : "",
                            'MenuItemSize_3_Position' : 0,
                            'MenuItemSize_3_Suggestions' : mealSuggestions[2],
    
                            'MenuItemSize_4_SKU' : SKUs[3],
                            'MenuItemSize_4_Name' : menuItemSizeNames[3],
                            'MenuItemSize_4_Price' : menuItemPrices[3],
                            'MenuItemSize_4_Modifiers' : modifierGroupStrings[3],
                            'MenuItemSize_4_NutritionalKJ' : "",
                            'MenuItemSize_4_Position' : 0,
                            'MenuItemSize_4_Suggestions' : mealSuggestions[3],
    
                            'MenuItemSize_5_SKU' : SKUs[4],
                            'MenuItemSize_5_Name' : menuItemSizeNames[4],
                            'MenuItemSize_5_Price' : menuItemPrices[4],
                            'MenuItemSize_5_Modifiers' : modifierGroupStrings[4],
                            'MenuItemSize_5_NutritionalKJ' : "",
                            'MenuItemSize_5_Position' : 0,
                            'MenuItemSize_5_Suggestions' : mealSuggestions[4],
                            
                            'MenuItemSize_6_SKU' : SKUs[5],
                            'MenuItemSize_6_Name' : menuItemSizeNames[5],
                            'MenuItemSize_6_Price' : menuItemPrices[5],
                            'MenuItemSize_6_Modifiers' : modifierGroupStrings[5],
                            'MenuItemSize_6_NutritionalKJ' : "",
                            'MenuItemSize_6_Position' : 0,
                            'MenuItemSize_6_Suggestions' : mealSuggestions[5],
                            
                            }
    
            dataList.append(menuItemData)
            id += 1

if run == 1:
    uniqueKey = 'MenuItemSize_1_SKU'
if run == 2:
    uniqueKey = 'modifierId'
for dataEntry in dataList:
    scraperwiki.sqlite.save(unique_keys=[uniqueKey], data=dataEntry)
    
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################










import scraperwiki
import lxml.html
import re
import urllib2

###############
html =scraperwiki.scrape("http://www.menulog.com.au/himalaya_pakistani_indian_restaurant_rockdale")
run = 2 #1 for menu, 2 for modifiers

#Change according to whatever computer is being used:
#Jimylig's 13" MBP:
    #Google Chrome:
#heads = {"Cookie":"PHPSESSID=l0mitdgj226hdp3utlc3unpbu7; SERVERID=www_mlweb6_1; __utma=159154086.1347556771.1349857474.1349857474.1349857474.1; __utmb=159154086.3.10.1349857474; __utmc=159154086; __utmz=159154086.1349857474.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)"}

#Phil's MBP:
    #Google Chrome:
#heads = {"Cookie":"PHPSESSID=d4kqbd5mekri2lnqfegtnvvoe3; SERVERID=www_mlweb6_1; WRUID=4849193.508293249; WRIgnore=true; __utma=159154086.1610577125.1346980519.1348626424.1349225596.30; __utmb=159154086.6.9.1349225614480; __utmc=159154086; __utmz=159154086.1346980519.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)"}

#Andrew's 13" inch MBP:
    #Chrome:
heads = {"Cookie":"PHPSESSID=a1bc0beb29e66a360e792ea540483598; SERVERID=www_mlweb6_1; WRUID=1213540462.1681966284; WRIgnore=true; __utma=159154086.1900219217.1337396703.1348626277.1349225008.6; __utmb=159154086.7.9.1349225085076; __utmc=159154086; __utmz=159154086.1341031985.4.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)"}


###############


if run is 1:
    print "Getting menu"
elif run is 2:
    print "Getting modifiers"
else:
    print "no flag given"

root = lxml.html.fromstring(html)


restaurantId = ""
restaurantScripts = root.cssselect("script[type='text/javascript']")

for script in restaurantScripts:
    scriptContent = script.text_content()
    restaurantIdPattern = re.compile(r'restaurantId: \d+,')
    restIdMatch = restaurantIdPattern.search(scriptContent)
    if restIdMatch:
        restaurantId = restIdMatch.group().lstrip('restaurantId: ')
        restaurantId = restaurantId.rstrip(',')    
        #print "restaurantId: ", restaurantId
        break
if restaurantId == "":
    print "ERROR: no restaurant Id found on page. Cannot get modifiers."
#####


menu = root.cssselect("ul[class='foodItems']")
menuGroups = root.cssselect("li[class='course']")
#print len(menuGroups)

itemSizeNameKey = 'itemSizeName'
itemSizePriceKey = 'itemSizePrice'
itemSizeIdKey = 'itemSizeId'

menuGroupPosition = -1
currentSku = 0
modifierId = 0

dataList = []
id = 0
modifierGroupPosition = -1
modifierGroupDict = {}
for menuGroup in menuGroups:
    menuGroupPosition += 1    

    heading = menuGroup.cssselect("h3")
    menuGroupName = heading[0].text_content()
    menuGroupName = menuGroupName.strip()
    #print "Menu Group: ", menuGroupName
    menuItems = menuGroup.cssselect("ul")[0].cssselect("li")
    #print "Menu Group Size: ", len(menuItems)

    menuItemPosition = -1
    modifierGroupCount = 1
    for menuItem in menuItems:
        menuItemPosition += 1
        menuItemName = menuItem.cssselect("h4")[0].text_content()
        menuItemDescElement = menuItem.cssselect("p")
        menuItemDescription = ""
        if len(menuItemDescElement) > 0:
            menuItemDescription = menuItemDescElement[0].text_content()

        #get rid of newlines:
        descLines = menuItemDescription.splitlines()
        menuItemDescription = ""
        for descLine in descLines:
            menuItemDescription += descLine + " "
        
    #Check for multiple item sizes and prices
        price =""
        itemSizePricesList = []
        itemSizeNamesList = []
        itemSizeList = []

        itemSizeId = ""
        itemSizesElement = menuItem.cssselect("div[class='varieties singleVariety']")
        if len(itemSizesElement) > 0:
            #single item size:
            price = itemSizesElement[0].text_content()
            price = price.strip()
            
            #Get itemSize Id:
            inputElement = itemSizesElement[0].cssselect("input")[0]
            itemSizeId = inputElement.attrib['value']
            #print "itemSizeId: ", itemSizeId
            
            itemSizeDict = {
                            itemSizeNameKey : "",
                            itemSizePriceKey : price,
                            itemSizeIdKey : itemSizeId
                            }
            itemSizeList.append(itemSizeDict)
                    
        else:
            #multiple item sizes:
            itemSizesElement = menuItem.cssselect("div[class='varieties jsBrowserVer']")
            if len(itemSizesElement) > 0:
                
                for itemSize in itemSizesElement[0].cssselect("label"):
                    nextItemSizeString = itemSize.text_content()
                    
                    pattern = re.compile(r'\$.+')
                    match = pattern.search(nextItemSizeString)
                    nextItemSizePrice = match.group()

                    nextItemSizeName = nextItemSizeString.rstrip(nextItemSizePrice)
                    nextItemSizeName = nextItemSizeName.strip()
                    #print "-- Item Size Name: ", nextItemSizeName


                    #Get itemSize Id:
                    inputElement = itemSize.cssselect("input")[0]
                    itemSizeId = inputElement.attrib['value']
                    #print "Multiple itemSizeId: ", itemSizeId
                    
                    itemSizeDict = {
                                    itemSizeNameKey : nextItemSizeName,
                                    itemSizePriceKey : nextItemSizePrice,
                                    itemSizeIdKey : itemSizeId
                                    }

                    itemSizeList.append(itemSizeDict)
            else:
                itemSizeDict = {itemSizeNameKey : "", itemSizePriceKey : "", itemSizeIdKey : ""}
                itemSizeList.append(itemSizeDict)
                print "ERROR: No price found for item: ", menuItemName

        es = "" #empty string
        SKUs=[es,es,es,es,es,es]
        menuItemSizeNames=[es,es,es,es,es,es]
        menuItemPrices=[es,es,es,es,es,es]
        modifierGroupStrings=[es,es,es,es,es,es]
        mealSuggestions=[es,es,es,es,es,es]


        #print menuItemName
        #print itemSizeList
        sizeCount = 0
        for nextItemSize in itemSizeList:
            SKUs[sizeCount] = currentSku
            currentSku += 1
            
            menuItemSizeNames[sizeCount] = nextItemSize[itemSizeNameKey]
            menuItemPrices[sizeCount] = nextItemSize[itemSizePriceKey]


            
############################################################################################################################################
#MODIFIERS:
            
            itemSizeId = nextItemSize[itemSizeIdKey]
            modifierFormRequest = "varietyId="+ itemSizeId + "&action=add&restaurantId=" + restaurantId
            request = urllib2.Request("http://www.menulog.com.au/takeaway/ajax_update_cart.php", data=modifierFormRequest, headers=heads)
            
            page = urllib2.urlopen(request)
            response = page.read()
#            print "Response: ", response

            errorPattern = re.compile("error")
            errorMatch = errorPattern.search(response)

#            responseErrorMessage = '[["error","Sorry, a problem has occurred. Please try again later"]]'
            if errorMatch:
                print "ERROR: HTTP response for modifiers is incorrect for menu item; ",menuItemName,", in menu group; ",menuGroupName,". Try inputting delivery details for the current restaurant and menu item on the ML website"

            popupHtml = lxml.html.fromstring(response)
#            print "menu item: ", menuItemName
            modifierClumpElement = popupHtml.cssselect("h5")
            if modifierClumpElement:
                modifierClump = modifierClumpElement[0].text_content()
    
                #print "modifierClump: ", modifierClump
                
                modifierGroups = modifierClump.split("Choice(s)")
                modGroupsHtml = response.split("Choice(s)")
                #print "modifierGroups: ", modifierGroups
                #print "modGroupsHtml: ", modGroupsHtml
                
               
                modifierNameLists = []
                modifierPriceLists = []
                
                index = 0
                modifierGroupsString = ""
                for modifierGroup in modifierGroups:
                    #print "Modifier Group: ", modifierGroup
                    if modifierGroup.strip() != "":
                        modifierPattern = re.compile(r'\\n[^\\]+\\n')
                        matches = modifierPattern.findall(modifierGroup)
                        modifiers = []
                        for match in matches:
                            modifiers.append((match.lstrip(r'\\n')).rstrip(r'\\n'))
                        #print "Modifiers: ", modifiers
                        #print "Number of modifiers for current group: ", len(modifiers)
                        
                        modifierGroupName = menuGroupName + "-" + menuItemSizeNames[sizeCount] + str(modifierGroupCount)
                        modifierGroupCount+=1
                        #Check if modifier group already exists:
                        modifierGroupKey = modifiers[0] 
                        #Assume if the first modifier exists, the rest of the modifiers match the same group
                        if modifierGroupKey in modifierGroupDict:
                            #if it does, add modifier group to comma-seperated list of modifiers and skip creation of modifiers
                            modifierGroupsString += modifierGroupDict[modifierGroupKey] + ","
                            continue
                        #Add to dictionary of existing modifier Groups. Map all modifier items to modifier Group
                        for modifier in modifiers:
                            modifierGroupDict[modifier] = modifierGroupName
                        modifierGroupPosition+=1
                        
                        #extract names and prices:
                        namePattern = re.compile(r'.*\+')
                        pricePattern = re.compile(r'\+.*')
                        
                        modifierNames = []
                        modifierPrices = []
                        for modifier in modifiers:
                            nameMatch = namePattern.search(modifier)
                            if nameMatch:
                                modifierName = nameMatch.group().rstrip("+")
                                modifierName = modifierName.strip()
                                modifierNames.append(modifierName)
                                
                                #if modifier name and price exist, add price:
                                priceMatch = pricePattern.search(modifier)
                                if priceMatch:
                                    modifierPrice = priceMatch.group().lstrip("+")
                                    modifierPrice = modifierPrice.strip()
                                    modifierPrice = modifierPrice.lstrip("$")
                                    modifierPrices.append(modifierPrice)
                                else:
                                    modifierPrices.append("")
                                
                            else: #if no price:
                                modifierName = modifier.strip()
                                modifierNames.append(modifierName)
                                modifierPrices.append("")

                        


                
                        #print "modifier names: ", modifierNames
                        #print "modifier prices: ", modifierPrices
                        modifierNameLists.append(modifierNames)
                        modifierPriceLists.append(modifierPrices)
                
                
                        #set radio or checkbox type:
                
                        firstModifier = modifierNames[0]
                        checkboxPattern = re.compile(r'core-ignoreTransformInput checkbox\\" \\/>\\n' + firstModifier)
                        radioPattern = re.compile(r'core-ignoreTransformInput radio\\" \\/>\\n' + firstModifier)
                        modifierGroupHtml = modGroupsHtml[index]
                        checkboxMatch = checkboxPattern.search(modifierGroupHtml)
                        radioMatch = radioPattern.search(modifierGroupHtml)
                        radio = "radio"
                        checkbox = "checkbox"
                        selectionType = radio
                
                        if checkboxMatch:
                            #print checkboxMatch.group()
                            selectionType = checkbox
                        elif radioMatch:
                            #print radioMatch.group()
                            pass
                        else:
                            #print "No checkbox type pattern found"
                            pass
                
                        #print "Selection type: ", selectionType

                        #Save modifier groups in comma seperated string:
                        
                        
                        modifierGroupsString += modifierGroupName + ","
                        
                        

                        #default radio
                        modifierMinSelect = "1"
                        modifierMaxSelect = "1"
                        if selectionType == radio:
                            modifierMinSelect = "1"
                            modifierMaxSelect = "1"
                        elif selectionType == checkbox:
                            modifierMinSelect = "0"
                            modifierMaxSelect = ""
                        else:
                            print "No Check Box type found for menu item: ", menItemName, " in modifier group: " , modifierGroupName ,", defaulting to radio type"
                            pass
                            
                        #modifierNames = []
                        #modifierPrices = []
                        modifierCount = 0
                        for nextModifierName in modifierNames:
                            nextModifierPrice = modifierPrices[modifierCount]

                            if run == 2:
                                #Save Modifier Data:
                                modifierData = {
                                                    'modifierId' : modifierId,
                                                    'ModifierGroup': modifierGroupName,
                                                    'ModifierGroupPosition' : modifierGroupPosition,
                                                    'ModifierMinSelect' : modifierMinSelect,
                                                    'ModifierMaxSelect' : modifierMaxSelect,
                                                    'ModifierPosition' : modifierCount,
                                                    'ItemSizeSKU' : "",
                                                    'ItemSizeName' : nextModifierName,
                                                    'AdditivePrice' : nextModifierPrice,
                                                }
                                modifierCount += 1
                                modifierId += 1
        
                                dataList.append(modifierData)
                                id += 1
                        
                        
                        
                    else:
                        #print "Empty Modifier Group"
                        pass
                    index += 1
                modifierString = (modifierGroupsString.strip()).rstrip(",")
                modifierGroupStrings[sizeCount] = modifierString
                
                #print "modifierNameLists: ", modifierNameLists
                #print "modifierPriceLists: ", modifierPriceLists
                
                #print "Names: ", modifierNames
                #print "Prices: ", modifierPrices
            else:
                #no modifiers:
                pass

            sizeCount += 1
            


############################################################################################################################################
        if run== 1:
            menuItemData = {
                            'ID' : id,
                            'MenuGroupName' : menuGroupName,
                            'MenuGroupDescription' : '',
                            'MenuGroupStartTime' : '',
                            'MenuGroupEndTime' : '',
                            'MenuGroupIncludingDays' : '',
                            'MenuGroupPosition' : menuGroupPosition,
                            'MenuGroupVisible' : 'TRUE',

                            'MenuItemName' : menuItemName,
                            'MenuItemPosition' : menuItemPosition,
                            'MenuItemDescription' : menuItemDescription,
                            'MenuItemVisible' : 'TRUE',
    
                            'MenuItemSize_1_SKU' : SKUs[0],
                            'MenuItemSize_1_Name' : menuItemSizeNames[0],
                            'MenuItemSize_1_Price' : menuItemPrices[0],
                            'MenuItemSize_1_Modifiers' : modifierGroupStrings[0],
                            'MenuItemSize_1_NutritionalKJ' : "",
                            'MenuItemSize_1_Position' : 0,
                            'MenuItemSize_1_Suggestions' : mealSuggestions[0],
    
                            'MenuItemSize_2_SKU' : SKUs[1],
                            'MenuItemSize_2_Name' : menuItemSizeNames[1],
                            'MenuItemSize_2_Price' : menuItemPrices[1],
                            'MenuItemSize_2_Modifiers' : modifierGroupStrings[1],
                            'MenuItemSize_2_NutritionalKJ' : "",
                            'MenuItemSize_2_Position' : 0,
                            'MenuItemSize_2_Suggestions' : mealSuggestions[1],
    
                            'MenuItemSize_3_SKU' : SKUs[2],
                            'MenuItemSize_3_Name' : menuItemSizeNames[2],
                            'MenuItemSize_3_Price' : menuItemPrices[2],
                            'MenuItemSize_3_Modifiers' : modifierGroupStrings[2],
                            'MenuItemSize_3_NutritionalKJ' : "",
                            'MenuItemSize_3_Position' : 0,
                            'MenuItemSize_3_Suggestions' : mealSuggestions[2],
    
                            'MenuItemSize_4_SKU' : SKUs[3],
                            'MenuItemSize_4_Name' : menuItemSizeNames[3],
                            'MenuItemSize_4_Price' : menuItemPrices[3],
                            'MenuItemSize_4_Modifiers' : modifierGroupStrings[3],
                            'MenuItemSize_4_NutritionalKJ' : "",
                            'MenuItemSize_4_Position' : 0,
                            'MenuItemSize_4_Suggestions' : mealSuggestions[3],
    
                            'MenuItemSize_5_SKU' : SKUs[4],
                            'MenuItemSize_5_Name' : menuItemSizeNames[4],
                            'MenuItemSize_5_Price' : menuItemPrices[4],
                            'MenuItemSize_5_Modifiers' : modifierGroupStrings[4],
                            'MenuItemSize_5_NutritionalKJ' : "",
                            'MenuItemSize_5_Position' : 0,
                            'MenuItemSize_5_Suggestions' : mealSuggestions[4],
                            
                            'MenuItemSize_6_SKU' : SKUs[5],
                            'MenuItemSize_6_Name' : menuItemSizeNames[5],
                            'MenuItemSize_6_Price' : menuItemPrices[5],
                            'MenuItemSize_6_Modifiers' : modifierGroupStrings[5],
                            'MenuItemSize_6_NutritionalKJ' : "",
                            'MenuItemSize_6_Position' : 0,
                            'MenuItemSize_6_Suggestions' : mealSuggestions[5],
                            
                            }
    
            dataList.append(menuItemData)
            id += 1

if run == 1:
    uniqueKey = 'MenuItemSize_1_SKU'
if run == 2:
    uniqueKey = 'modifierId'
for dataEntry in dataList:
    scraperwiki.sqlite.save(unique_keys=[uniqueKey], data=dataEntry)
    
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################










