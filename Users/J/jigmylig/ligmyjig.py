import scraperwiki
import lxml.html
import re

html =scraperwiki.scrape("http://www.deliveryhero.com.au/sydney/sushi-jung/")
root = lxml.html.fromstring(html)


run = 1 
# run is 1 or 2
#1 - Menu Items
#2 - Modifiers


##Keys linking food items to ingredients:
keyDict = {}
menuList = root.cssselect("div#menu_list_actual")
scripts = menuList[0].cssselect("script")
for script in scripts:
    content = script.text_content()
    
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
        
        ##get item keys linking to food items:
        pattern1 = re.compile(r"if \( ! ingSetsForItem[\'[\w-]+\'")
        roughItemKeys = pattern1.finditer(content)
        
        ingredientKeys = []
        for roughItemKey in roughItemKeys:
            itemKeyQ = keyPattern.search(roughItemKey.group())
            #get rid of quotation marks on both ends:
            menuItemKey = itemKeyQ.group().split("\'")[1]
           
            ##look up list of modifier keys from menu item key:
            modifierGroupKeys = keyDict.get(menuItemKey)
            if modifierGroupKeys is not None:
                #print "LIST ALREADY EXISTS"
                pass
            ##if it does not exist, create it and add to dictionary:
            if modifierGroupKeys is None:
                modifierGroupKeys = []
                keyDict[menuItemKey] = modifierGroupKeys
            ##Add modifierGroupKey to list 
            modifierGroupKeys.append(modifierKey)
            
            

##Food items:
dataList = []
sku = 0
menuItemKeyDict = {}
menuItemsSKUDict = {}
menuGroupPosition = -1
for sections in root.cssselect("div.menu_row"):

    for menuGroup in sections.cssselect("div[class='section']"):
        menuGroupPosition += 1
        menuGroupName = menuGroup.cssselect("h3")[0].text_content()
        #print "Menu Name: ", menuGroupName

        menuItemPosition = 0
        for menuItem in menuGroup.cssselect("ul li"):

            menuItemName = menuItem.cssselect("div.name")[0].text_content()
            menuItemPrice = menuItem.cssselect("span.price")[0].text_content()
            menuItemPrice = menuItemPrice.strip()
            menuItemPrice = menuItemPrice.lstrip('$')
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

            if run is 1:
                menuItemData = {
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
                        'MenuItemSize_1_Suggestion' : ""
                        }
                dataList.append(menuItemData)
                #scraperwiki.sqlite.save(unique_keys=['MenuItemSize_1_SKU'], data=data)

            menuItemPosition = menuItemPosition + 1
            sku = sku + 1


if run is 2:     
    ##Ingredients:
    modifierPositionColumnName = 'ModifierPosition'
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
        ingredientDataEntryList = []
        ingredientPriceFloatList =[]
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
            extraIngredientPrice = "0"
            if len(ingredientPriceSpan) > 0:
                ingredientPriceString = ingredientPriceSpan[0].text_content()
                p = re.compile(r'\$.+')
                m = p.search(ingredientPriceString)
                if m is not None:
                    price = m.group()
                    ingredientPricePattern = re.compile(r"[\d]+\.[\d]+")
                    extraIngredientPrice = ingredientPricePattern.findall(price)[0]
                    
    #                overrideFlag = "TRUE"
                    ingredientName = ingredientName.rstrip(price)
                    ingredientName = ingredientName.strip()
                    ingredientName = ingredientName.rstrip("+")
                    ingredientName = ingredientName.strip()
    
            ###map names to their categories/keys:
            ingredientsList.append(ingredientName)
            
            #Check if current ingredient exists as a menuItem and link it with SKU if it does
            itemSizeSKU = menuItemsSKUDict.get(ingredientName)
            if itemSizeSKU is None:
               itemSizeSKU = ""
            else:
                ingredientName = ""
                pass
            
            extraIngredientPriceFloat = float(extraIngredientPrice)
            ingredientPriceFloatList.append(extraIngredientPriceFloat)
    
            #modifierPosition = 0
    
            ingredientDataEntry = {
                    'ID' : ID,
                    'ModifierGroup' : modifierGroupKey,
                    'ModifierGroupPosition' : modifierGroupPosition,
                    'ModifierMinSelect' : modifierMinSelect,
                    'ModifierMaxSelect' : modifierMaxSelect,
                    'ItemSizeSKU' : itemSizeSKU,
                    'ItemSizeName' : ingredientName,
                    #'ItemSizePrice' : "",
                    'AdditivePrice' : extraIngredientPrice,
                    #'OverridePrice' : overrideFlag,
                    modifierPositionColumnName : modifierPosition,
                    }
            ingredientDataEntryList.append(ingredientDataEntry)
            dataList.append(ingredientDataEntryList)
            #scraperwiki.sqlite.save(unique_keys=['ID'], data=data2)
            modifierPosition = modifierPosition+1
            ID = ID+1
    
        listOfPriceCallOrderTuples = []
        callOrder = 0
        #map ingredient price to the order ingredients were called
        for nextIngredientPrice in ingredientPriceFloatList:
            priceCallOrderTuple = (nextIngredientPrice, callOrder)
            listOfPriceCallOrderTuples.append(priceCallOrderTuple)
            callOrder = callOrder + 1
    
        #sort tuples according to price (index 0 of tuples), then Call Order (index 1 of tuples):
        sortedListOfPriceCallOrderTuples = sorted(listOfPriceCallOrderTuples)
    
        #tuples now sorted by price:
        sortedModifierPosition = 0
        for nextSortedPriceCallOrderTuple in sortedListOfPriceCallOrderTuples:
            nextCallOrder = nextSortedPriceCallOrderTuple[1]
            ingredientDataEntryList[nextCallOrder][modifierPositionColumnName] = sortedModifierPosition
            sortedModifierPosition = sortedModifierPosition+1


uniqueKey = ''
if run is 1:
    uniqueKey = 'MenuItemSize_1_SKU'
elif run is 2:
    uniqueKey = 'ID'
else:
    print "ERROR: run must be set to 1 or 2"

for dataEntry in dataList:
        scraperwiki.sqlite.save(unique_keys=[uniqueKey], data=dataEntry)




