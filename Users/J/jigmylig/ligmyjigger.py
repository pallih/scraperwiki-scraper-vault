import scraperwiki
import lxml.html
import re

html =scraperwiki.scrape("http://www.deliveryhero.com.au/sydney/malabar-darlinghurst/")
root = lxml.html.fromstring(html)


run = 1
# run is 1 or 2
##Keys linking food items to ingredients:

keyDict = {}
menuList = root.cssselect("div#menu_list_actual")
scripts = menuList[0].cssselect("script")
#print len(scripts)
for script in scripts:
    content = script.text_content()
#    print content
    
    keyPattern = re.compile(r"\'[\w-]+\'")
    p = re.compile(r"if \( ! ingSetsForItem")
    m = p.findall(content)
    if len(m) > 0:

        ##get ingredient keys linking to ingredient items:
        
        modifierKeyPattern = re.compile("ingredientsets\[\'[\w-]+\'")
        modifierKeyMatch = modifierKeyPattern.search(content)
        modifierKeyQ = keyPattern.search(modifierKeyMatch.group())
        #get rid of quotation marks on both ends:
        modifierKey = modifierKeyQ.group().split("\'")[1]
        #print "Ingredient Item Key: ",modifierKey

        
        ##get item keys linking to food items:
        pattern1 = re.compile(r"if \( ! ingSetsForItem[\'[\w-]+\'")
        roughItemKeys = pattern1.finditer(content)
        
        ingredientKeys = []
        for roughItemKey in roughItemKeys:
            itemKeyQ = keyPattern.search(roughItemKey.group())
            #get rid of quotation marks on both ends:
            menuItemKey = itemKeyQ.group().split("\'")[1]
            #print "Food Item Key: ", itemKey

            ##look up list of modifier keys from menu item key:
            modifierGroupKeys = keyDict.get(menuItemKey)
            if modifierGroupKeys is not None:
                #print "LIST ALREADY EXISTS"
                pass
            ##if it does not exist, create it and add to dictionary:
            if modifierGroupKeys is None:
                #print "CREATING NEW LIST"
                modifierGroupKeys = []
                keyDict[menuItemKey] = modifierGroupKeys
            ##Add modifierGroupKey to list 
            modifierGroupKeys.append(modifierKey)
            
            
            #print "modifierGroupKeys: ", keyDict.get(menuItemKey)
            #print "menuItemKey: ", menuItemKey




##Food items:
sku = 0
menuItemKeyDict = {}
menuItemsSKUDict = {}
menuGroupPosition = -1
for sections in root.cssselect("div.menu_row"):

    for menuGroup in sections.cssselect("div[class='section']"):
        menuGroupPosition = menuGroupPosition + 1
        menuGroupName = menuGroup.cssselect("h3")[0].text_content()
        #print "Menu Name: ", menuGroupName

        menuItemPosition = 0
        for menuItem in menuGroup.cssselect("ul li"):

            menuItemName = menuItem.cssselect("div.name")[0].text_content()
            menuItemPrice = menuItem.cssselect("span.price")[0].text_content()
            #print "- Menu Item: ", menuItemName , menuItemPrice

            listItem = menuItem.attrib['onclick']
            array = listItem.split(',')
            menuItemKey = array[1].split("\'")[1]
            #print  "--- key: ", menuItemKey

            menuItemKeyDict[sku] = menuItemKey
            descriptionElement = menuItem.cssselect("p")
            if (len(descriptionElement) > 0):
                menuItemDescription = descriptionElement[0].text_content()
                #print "--- Description: ", menuItemDescription
            else:
                menuItemDescription = ""

########################get modifiers:

            #menuItemKey = menuItemKeyDict.get(skuKey)
            modifierGroupList = []

            # Look up List of modifierGroupKeys from menuItemKey:
            modifierGroupKeyList = keyDict.get(menuItemKey)
        
            if modifierGroupKeyList is not None:
                #Go through modifierGroupKeys one by one:
                for modifierGroupName in modifierGroupKeyList:
                    #save modifierGroupName:
                    modifierGroupList.append(modifierGroupName)
        
            modifierGroupString = ""
            ##put into a comma-seperated string:
            for modifierGroupName in modifierGroupList:
                modifierGroupString = modifierGroupString + modifierGroupName + ","
        
            #remove last comma if it's there:
            modifierGroupString = modifierGroupString.rstrip(",")
        
######################

            ##Edit and trim values:
            menuGroupName = menuGroupName.strip()
            menuItemName = menuItemName.strip()

            """
            Save menu item names to dictionary mapped to SKUs.
            If this menu item already exists when used as an 
            additional side order/modifier in the Ingredients loop, 
            link it from the modifier group to this menu item with the SKU
            """
            menuItemsSKUDict[menuItemName] = sku

            data = {
                    'MenuGroupName' : menuGroupName,
                    'MenuGroupPosition' : menuGroupPosition,
                    'MenuGroupVisible' : 'TRUE',
                    'MenuItemName' : menuItemName,
                    'MenuItemPosition' : menuItemPosition,
                    'MenuItemDescription' : menuItemDescription,
                    'MenuItemVisible' : 'TRUE',
                    'MenuItemSize_1_SKU' : sku,
                    'MenuItemSize_1_Name' : "",
                    'MenuItemSize_1_Price' : menuItemPrice,
                    'MenuItemSize_1_NutritionalKJ' : "",
                    'MenuItemSize_1_Position' : 0,
                    'MenuItemSize_1_Modifiers' : modifierGroupString,
                    }
            menuItemPosition = menuItemPosition + 1
            sku = sku + 1
            if run is 1:
                scraperwiki.sqlite.save(unique_keys=['MenuItemSize_1_SKU'], data=data)




##Ingredients:
modifierGroupPosition = -1
ID = 1 
modifierGroupIngredientDict = {}
ingredientCategories = root.cssselect("div[class='lightboxcomponent fliesstextL']")
for ingredientCategory in ingredientCategories:
    modifierGroupPosition = modifierGroupPosition + 1
    headingQuestion = ingredientCategory.cssselect("h3")[0].text_content()
    #print "Heading question: " , headingQuestion

    ingredients = ingredientCategory.cssselect("div.ingredient")    
    modifierGroupKey = ingredients[0].cssselect("input")[0].attrib['name']
    #print "modifierGroupKey: ", modifierGroupKey

    ##create list of Ingredients
    ingredientsList = []
    modifierGroupIngredientDict[modifierGroupKey] = ingredientsList
    
    modifierPosition = 0
    for ingredient in ingredients:
        
        ingredientLabel = ingredient.cssselect("label") 
        ingredientName = ingredientLabel[0].text_content()

        ##strip off white space and dashes, if any:
        ingredientName = ingredientName.strip()
        ingredientName = ingredientName.rstrip("-")

        ingredientPriceSpan = ingredientLabel[0].cssselect("span")
        #assume if there is a price, that this ingredient/modifier is a size:
        ingredientPrice = ""


        #Check whether ingredient is mandatory radio or optional checkbox
        modifierMinSelect = "1"
        modifierMaxSelect = "1"
        
        selectionType = ingredient.cssselect("input")[0].attrib['type']
        selectionType = selectionType.strip()
        #print "selectionType: ", selectionType
        if selectionType == 'checkbox':
            modifierMinSelect = "0"
            modifierMaxSelect = ""
            #print ingredientName, " is a checkbox type"
        elif selectionType == 'radio':
            #print ingredientName, " is a radio type"
            pass
        else:
            #print ingredientName, " unrecognised type"
            pass


        overrideFlag = "FALSE"
        extraIngredientPrice = ""
        if len(ingredientPriceSpan) > 0:
            ingredientPriceString = ingredientPriceSpan[0].text_content()
            p = re.compile(r'\$.+')
            m = p.search(ingredientPriceString)
            if m is not None:
                price = m.group()
                ingredientPricePattern = re.compile(r"[\d]+\.[\d]+")
                extraIngredientPrice = ingredientPricePattern.findall(price)[0]
                #print "Ingredient price: ", ingredientPrice
#                overrideFlag = "TRUE"
                ingredientName = ingredientName.rstrip(price)
                ingredientName = ingredientName.strip()
                ingredientName = ingredientName.rstrip("+")
                ingredientName = ingredientName.strip()
#        print "Ingredient name: ", ingredientName


        #print "Ingredient name: ", ingredientName
        ###map names to their categories/keys:
        ingredientsList.append(ingredientName)
        
        #print "modifierGroupKey: ", modifierGroupKey
        #print "ingredientName: ", ingredientName
        #print "ID: ", ID

        #Check if current ingredient exists as a menuItem and link it with SKU if it does
        itemSizeSKU = menuItemsSKUDict.get(ingredientName)
        if itemSizeSKU is None:
           itemSizeSKU = ""
        else:
            print "Modifier: ", ingredientName ,", exists as menu item, ItemSizeSKU: ", itemSizeSKU
            ingredientName = ""
            pass


        data2 = {
                'ID' : ID,
                'ModifierGroup' : modifierGroupKey,
                'ModifierGroupPosition' : modifierGroupPosition,
                'ModifierMinSelect' : modifierMinSelect,
                'ModifierMaxSelect' : modifierMaxSelect,
                'ModifierPosition' : modifierPosition,
                'ItemSizeSKU' : itemSizeSKU,
                'ItemSizeName' : ingredientName,
                #'ItemSizePrice' : "",
                'AdditivePrice' : extraIngredientPrice,
                #'OverridePrice' : overrideFlag,
                }
        modifierPosition = modifierPosition+1
        ID = ID+1
        if run is 2: 
            scraperwiki.sqlite.save(unique_keys=['ID'], data=data2)


"""
-map SKU to menuItemKey
-map menuItemKey to List of modifierGroupKeys
-map modifierGroupKey to List of ingredientNames
Go through SKUs one by one:
    Look up menuItemKey from SKU
    Look up List of modifierGroupKeys from menuItemKey
    Go through modifierGroupKeys one by one:
        Look up List of ingredientNames from modifierGroupKey
        Go through List of ingredientNames one by one:
            add next ingredientName to comma-seperated list of modifierGroups entries
        


i = 0
for skuKey in menuItemKeyDict:
    
    i = i+1
    modifierGroupList = []
    #Look up menuItemKey from SKU:
    menuItemKey = menuItemKeyDict.get(skuKey)

    # Look up List of modifierGroupKeys from menuItemKey:
    modifierGroupKeyList = keyDict.get(menuItemKey)

    if modifierGroupKeyList is not None:
        #Go through modifierGroupKeys one by one:
        for modifierGroupName in modifierGroupKeyList:
            #save modifierGroupName:
            modifierGroupList.append(modifierGroupName)

    modifierGroupString = ""
    ##put into a comma-seperated string:
    for modifierGroupName in modifierGroupList:
        modifierGroupString = modifierGroupString + modifierGroupName + ","

    #remove last comma if it's there:
    modifierGroupString = modifierGroupString.rstrip(",")

    data3 = {
            'MenuItemSize_1_SKU' : skuKey,
            'MenuItemSize_1_Modifiers' : modifierGroupString,
            }

    #scraperwiki.sqlite.save(unique_keys=['MenuItemSize_1_SKU'], data=data3)







i = 0
for skuKey in menuItemKeyDict:
    
    i = i+1
    modifierGroupList = []
    #Look up menuItemKey from SKU:
    menuItemKey = menuItemKeyDict.get(skuKey)

    # Look up List of modifierGroupKeys from menuItemKey:
    modifierGroupKeyList = keyDict.get(menuItemKey)
    #print "menuItemKey: ", menuItemKey
    #print "modifierGroupKeyList: ", modifierGroupKeyList
    
    if modifierGroupKeyList is not None:
        #Go through modifierGroupKeys one by one:
        for modifierGroupKey in modifierGroupKeyList:
            #Look up List of ingredientNames from modifierGroupKey
            ingredientNamesList = modifierGroupIngredientDict.get(modifierGroupKey)
            #print "modifierGroupKey: ", modifierGroupKey
            #print "ingredientNamesList: ", ingredientNamesList
            for ingredientName in ingredientNamesList:
                modifierGroupList.append(ingredientName)
    
    modifierGroupString = ""
    ##put into a comma-seperated string:
    for modifierGroupName in modifierGroupList:
        modifierGroupString = modifierGroupString + modifierGroupName + ","

    #remove last comma if it's there:
    modifierGroupString = modifierGroupString.rstrip(",")

    data3 = {
            'MenuItemSize_1_SKU' : skuKey,
            'MenuItemSize_1_Modifiers' : modifierGroupString,
            }

    #scraperwiki.sqlite.save(unique_keys=['MenuItemSize_1_SKU'], data=data3)


"""



import scraperwiki
import lxml.html
import re

html =scraperwiki.scrape("http://www.deliveryhero.com.au/sydney/malabar-darlinghurst/")
root = lxml.html.fromstring(html)


run = 1
# run is 1 or 2
##Keys linking food items to ingredients:

keyDict = {}
menuList = root.cssselect("div#menu_list_actual")
scripts = menuList[0].cssselect("script")
#print len(scripts)
for script in scripts:
    content = script.text_content()
#    print content
    
    keyPattern = re.compile(r"\'[\w-]+\'")
    p = re.compile(r"if \( ! ingSetsForItem")
    m = p.findall(content)
    if len(m) > 0:

        ##get ingredient keys linking to ingredient items:
        
        modifierKeyPattern = re.compile("ingredientsets\[\'[\w-]+\'")
        modifierKeyMatch = modifierKeyPattern.search(content)
        modifierKeyQ = keyPattern.search(modifierKeyMatch.group())
        #get rid of quotation marks on both ends:
        modifierKey = modifierKeyQ.group().split("\'")[1]
        #print "Ingredient Item Key: ",modifierKey

        
        ##get item keys linking to food items:
        pattern1 = re.compile(r"if \( ! ingSetsForItem[\'[\w-]+\'")
        roughItemKeys = pattern1.finditer(content)
        
        ingredientKeys = []
        for roughItemKey in roughItemKeys:
            itemKeyQ = keyPattern.search(roughItemKey.group())
            #get rid of quotation marks on both ends:
            menuItemKey = itemKeyQ.group().split("\'")[1]
            #print "Food Item Key: ", itemKey

            ##look up list of modifier keys from menu item key:
            modifierGroupKeys = keyDict.get(menuItemKey)
            if modifierGroupKeys is not None:
                #print "LIST ALREADY EXISTS"
                pass
            ##if it does not exist, create it and add to dictionary:
            if modifierGroupKeys is None:
                #print "CREATING NEW LIST"
                modifierGroupKeys = []
                keyDict[menuItemKey] = modifierGroupKeys
            ##Add modifierGroupKey to list 
            modifierGroupKeys.append(modifierKey)
            
            
            #print "modifierGroupKeys: ", keyDict.get(menuItemKey)
            #print "menuItemKey: ", menuItemKey




##Food items:
sku = 0
menuItemKeyDict = {}
menuItemsSKUDict = {}
menuGroupPosition = -1
for sections in root.cssselect("div.menu_row"):

    for menuGroup in sections.cssselect("div[class='section']"):
        menuGroupPosition = menuGroupPosition + 1
        menuGroupName = menuGroup.cssselect("h3")[0].text_content()
        #print "Menu Name: ", menuGroupName

        menuItemPosition = 0
        for menuItem in menuGroup.cssselect("ul li"):

            menuItemName = menuItem.cssselect("div.name")[0].text_content()
            menuItemPrice = menuItem.cssselect("span.price")[0].text_content()
            #print "- Menu Item: ", menuItemName , menuItemPrice

            listItem = menuItem.attrib['onclick']
            array = listItem.split(',')
            menuItemKey = array[1].split("\'")[1]
            #print  "--- key: ", menuItemKey

            menuItemKeyDict[sku] = menuItemKey
            descriptionElement = menuItem.cssselect("p")
            if (len(descriptionElement) > 0):
                menuItemDescription = descriptionElement[0].text_content()
                #print "--- Description: ", menuItemDescription
            else:
                menuItemDescription = ""

########################get modifiers:

            #menuItemKey = menuItemKeyDict.get(skuKey)
            modifierGroupList = []

            # Look up List of modifierGroupKeys from menuItemKey:
            modifierGroupKeyList = keyDict.get(menuItemKey)
        
            if modifierGroupKeyList is not None:
                #Go through modifierGroupKeys one by one:
                for modifierGroupName in modifierGroupKeyList:
                    #save modifierGroupName:
                    modifierGroupList.append(modifierGroupName)
        
            modifierGroupString = ""
            ##put into a comma-seperated string:
            for modifierGroupName in modifierGroupList:
                modifierGroupString = modifierGroupString + modifierGroupName + ","
        
            #remove last comma if it's there:
            modifierGroupString = modifierGroupString.rstrip(",")
        
######################

            ##Edit and trim values:
            menuGroupName = menuGroupName.strip()
            menuItemName = menuItemName.strip()

            """
            Save menu item names to dictionary mapped to SKUs.
            If this menu item already exists when used as an 
            additional side order/modifier in the Ingredients loop, 
            link it from the modifier group to this menu item with the SKU
            """
            menuItemsSKUDict[menuItemName] = sku

            data = {
                    'MenuGroupName' : menuGroupName,
                    'MenuGroupPosition' : menuGroupPosition,
                    'MenuGroupVisible' : 'TRUE',
                    'MenuItemName' : menuItemName,
                    'MenuItemPosition' : menuItemPosition,
                    'MenuItemDescription' : menuItemDescription,
                    'MenuItemVisible' : 'TRUE',
                    'MenuItemSize_1_SKU' : sku,
                    'MenuItemSize_1_Name' : "",
                    'MenuItemSize_1_Price' : menuItemPrice,
                    'MenuItemSize_1_NutritionalKJ' : "",
                    'MenuItemSize_1_Position' : 0,
                    'MenuItemSize_1_Modifiers' : modifierGroupString,
                    }
            menuItemPosition = menuItemPosition + 1
            sku = sku + 1
            if run is 1:
                scraperwiki.sqlite.save(unique_keys=['MenuItemSize_1_SKU'], data=data)




##Ingredients:
modifierGroupPosition = -1
ID = 1 
modifierGroupIngredientDict = {}
ingredientCategories = root.cssselect("div[class='lightboxcomponent fliesstextL']")
for ingredientCategory in ingredientCategories:
    modifierGroupPosition = modifierGroupPosition + 1
    headingQuestion = ingredientCategory.cssselect("h3")[0].text_content()
    #print "Heading question: " , headingQuestion

    ingredients = ingredientCategory.cssselect("div.ingredient")    
    modifierGroupKey = ingredients[0].cssselect("input")[0].attrib['name']
    #print "modifierGroupKey: ", modifierGroupKey

    ##create list of Ingredients
    ingredientsList = []
    modifierGroupIngredientDict[modifierGroupKey] = ingredientsList
    
    modifierPosition = 0
    for ingredient in ingredients:
        
        ingredientLabel = ingredient.cssselect("label") 
        ingredientName = ingredientLabel[0].text_content()

        ##strip off white space and dashes, if any:
        ingredientName = ingredientName.strip()
        ingredientName = ingredientName.rstrip("-")

        ingredientPriceSpan = ingredientLabel[0].cssselect("span")
        #assume if there is a price, that this ingredient/modifier is a size:
        ingredientPrice = ""


        #Check whether ingredient is mandatory radio or optional checkbox
        modifierMinSelect = "1"
        modifierMaxSelect = "1"
        
        selectionType = ingredient.cssselect("input")[0].attrib['type']
        selectionType = selectionType.strip()
        #print "selectionType: ", selectionType
        if selectionType == 'checkbox':
            modifierMinSelect = "0"
            modifierMaxSelect = ""
            #print ingredientName, " is a checkbox type"
        elif selectionType == 'radio':
            #print ingredientName, " is a radio type"
            pass
        else:
            #print ingredientName, " unrecognised type"
            pass


        overrideFlag = "FALSE"
        extraIngredientPrice = ""
        if len(ingredientPriceSpan) > 0:
            ingredientPriceString = ingredientPriceSpan[0].text_content()
            p = re.compile(r'\$.+')
            m = p.search(ingredientPriceString)
            if m is not None:
                price = m.group()
                ingredientPricePattern = re.compile(r"[\d]+\.[\d]+")
                extraIngredientPrice = ingredientPricePattern.findall(price)[0]
                #print "Ingredient price: ", ingredientPrice
#                overrideFlag = "TRUE"
                ingredientName = ingredientName.rstrip(price)
                ingredientName = ingredientName.strip()
                ingredientName = ingredientName.rstrip("+")
                ingredientName = ingredientName.strip()
#        print "Ingredient name: ", ingredientName


        #print "Ingredient name: ", ingredientName
        ###map names to their categories/keys:
        ingredientsList.append(ingredientName)
        
        #print "modifierGroupKey: ", modifierGroupKey
        #print "ingredientName: ", ingredientName
        #print "ID: ", ID

        #Check if current ingredient exists as a menuItem and link it with SKU if it does
        itemSizeSKU = menuItemsSKUDict.get(ingredientName)
        if itemSizeSKU is None:
           itemSizeSKU = ""
        else:
            print "Modifier: ", ingredientName ,", exists as menu item, ItemSizeSKU: ", itemSizeSKU
            ingredientName = ""
            pass


        data2 = {
                'ID' : ID,
                'ModifierGroup' : modifierGroupKey,
                'ModifierGroupPosition' : modifierGroupPosition,
                'ModifierMinSelect' : modifierMinSelect,
                'ModifierMaxSelect' : modifierMaxSelect,
                'ModifierPosition' : modifierPosition,
                'ItemSizeSKU' : itemSizeSKU,
                'ItemSizeName' : ingredientName,
                #'ItemSizePrice' : "",
                'AdditivePrice' : extraIngredientPrice,
                #'OverridePrice' : overrideFlag,
                }
        modifierPosition = modifierPosition+1
        ID = ID+1
        if run is 2: 
            scraperwiki.sqlite.save(unique_keys=['ID'], data=data2)


"""
-map SKU to menuItemKey
-map menuItemKey to List of modifierGroupKeys
-map modifierGroupKey to List of ingredientNames
Go through SKUs one by one:
    Look up menuItemKey from SKU
    Look up List of modifierGroupKeys from menuItemKey
    Go through modifierGroupKeys one by one:
        Look up List of ingredientNames from modifierGroupKey
        Go through List of ingredientNames one by one:
            add next ingredientName to comma-seperated list of modifierGroups entries
        


i = 0
for skuKey in menuItemKeyDict:
    
    i = i+1
    modifierGroupList = []
    #Look up menuItemKey from SKU:
    menuItemKey = menuItemKeyDict.get(skuKey)

    # Look up List of modifierGroupKeys from menuItemKey:
    modifierGroupKeyList = keyDict.get(menuItemKey)

    if modifierGroupKeyList is not None:
        #Go through modifierGroupKeys one by one:
        for modifierGroupName in modifierGroupKeyList:
            #save modifierGroupName:
            modifierGroupList.append(modifierGroupName)

    modifierGroupString = ""
    ##put into a comma-seperated string:
    for modifierGroupName in modifierGroupList:
        modifierGroupString = modifierGroupString + modifierGroupName + ","

    #remove last comma if it's there:
    modifierGroupString = modifierGroupString.rstrip(",")

    data3 = {
            'MenuItemSize_1_SKU' : skuKey,
            'MenuItemSize_1_Modifiers' : modifierGroupString,
            }

    #scraperwiki.sqlite.save(unique_keys=['MenuItemSize_1_SKU'], data=data3)







i = 0
for skuKey in menuItemKeyDict:
    
    i = i+1
    modifierGroupList = []
    #Look up menuItemKey from SKU:
    menuItemKey = menuItemKeyDict.get(skuKey)

    # Look up List of modifierGroupKeys from menuItemKey:
    modifierGroupKeyList = keyDict.get(menuItemKey)
    #print "menuItemKey: ", menuItemKey
    #print "modifierGroupKeyList: ", modifierGroupKeyList
    
    if modifierGroupKeyList is not None:
        #Go through modifierGroupKeys one by one:
        for modifierGroupKey in modifierGroupKeyList:
            #Look up List of ingredientNames from modifierGroupKey
            ingredientNamesList = modifierGroupIngredientDict.get(modifierGroupKey)
            #print "modifierGroupKey: ", modifierGroupKey
            #print "ingredientNamesList: ", ingredientNamesList
            for ingredientName in ingredientNamesList:
                modifierGroupList.append(ingredientName)
    
    modifierGroupString = ""
    ##put into a comma-seperated string:
    for modifierGroupName in modifierGroupList:
        modifierGroupString = modifierGroupString + modifierGroupName + ","

    #remove last comma if it's there:
    modifierGroupString = modifierGroupString.rstrip(",")

    data3 = {
            'MenuItemSize_1_SKU' : skuKey,
            'MenuItemSize_1_Modifiers' : modifierGroupString,
            }

    #scraperwiki.sqlite.save(unique_keys=['MenuItemSize_1_SKU'], data=data3)


"""



