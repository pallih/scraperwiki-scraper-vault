import scraperwiki
import lxml.html
import decimal
import random
import unicodedata

# ------- This is the object class that will hold the scraped article information
class ArticleClass:
    description = ''
    priceCAStr = ''
    priceCADec = decimal.Decimal('0.00')
    priceUSStr = ''
    priceUSDec = decimal.Decimal('0.00')
    itemStr = ''
    imageLink = ''
    decimal.getcontext().prec = 2
    # This class function converts the class data into a string format
    # We need to strip out "weird" IKEA characters to make the database happy
    def toStr(self):
        self.description = unicodedata.normalize('NFKD', unicode(self.description)).encode('ascii', 'ignore')
        return '{0}|{1}|{2}|{3}|{4}'.format(self.description, self.priceCAStr, self.priceUSStr, self.itemStr, self.imageLink)

    # This class function loads the class attributes using a string created by toStr()
    def loadStr(self, str):
        itemList = str.split('|')
        self.description = itemList[0]
        self.priceCAStr = itemList[1].encode('ascii', 'ignore')
        self.priceCADec = decimal.Decimal(self.priceCAStr.translate(None, '$'))
        self.priceUSStr = itemList[2].encode('ascii', 'ignore')
        self.priceUSDec = decimal.Decimal(self.priceUSStr.translate(None, '$'))
        self.itemStr = itemList[3]
        self.imageLink = itemList[4]
        return

# ------ This function is the "scraper" that extracts information from the CA and US IKEA pages
# It returns an ArticleClass object containing the information extracted
def scrapeArticle( articleNum ):
    # Scrape the search page on Canadian and US IKEA sites; the product page should return
    itemPageHTMLCA = scraperwiki.scrape("http://www.ikea.com/ca/en/search/?query=" + articleNum)
    itemPageHTMLUS = scraperwiki.scrape("http://www.ikea.com/us/en/search/?query=" + articleNum)

    # Parse it for XML
    itemPageRootCA = lxml.html.fromstring(itemPageHTMLCA)
    itemPageRootUS = lxml.html.fromstring(itemPageHTMLUS)

    artC = ArticleClass()

    metaList = itemPageRootCA.cssselect("head meta")
    for el in metaList:
        if 'name' in el.attrib:
            if el.attrib['name'] == 'title':
                artC.description = el.attrib['content']
            if el.attrib['name'] == 'price':
                artC.priceCAStr = el.attrib['content']
            if el.attrib['name'] == 'partnumber':
                artC.itemStr = el.attrib['content']

    # Scrape US price information
    metaList = itemPageRootUS.cssselect("head meta")
    for el in metaList:
        if 'name' in el.attrib:
            if el.attrib['name'] == 'price':
                artC.priceUSStr = el.attrib['content']

    # Scrape item image link
    linkList = itemPageRootCA.cssselect("head link")
    for el in linkList:
        if 'rel' in el.attrib:
            if el.attrib['rel'] == 'image_src':
                artC.imageLink = el.attrib['href']

    artC.priceCADec = decimal.Decimal(artC.priceCAStr.translate(None, '$'))
    artC.priceUSDec = decimal.Decimal(artC.priceUSStr.translate(None, '$'))
    return artC;

# ------ This function loads ArticleClass objects from the datastore into a Dictionary
def loadArticles(sID):
    sList = { 'definer': 1 }

    textList = scraperwiki.sqlite.select("* from `{0}` where sessionID = {0}".format(sID))[0]
    for clef in textList.keys():
        if (clef != 'sessionID') and (clef != 'length'):
            sList[clef] = ArticleClass()
            sList[clef].loadStr(textList[clef])
    del sList['definer']
    scraperwiki.sqlite.execute('drop table if exists `{0}`'.format(sID))
    #    scraperwiki.sqlite.execute("delete from swdata where sessionID = {0}".format(sID))
    scraperwiki.sqlite.commit()
    return sList

# ------ This function saves a Dictionary of ArticleClass objects to the datastore
def saveArticles(sID, sList):
    strList = { 'sessionID': sID }

    for el in sList.keys():
        strList[el] = sList[el].toStr()
    strList['length'] = len(sList)
    scraperwiki.sqlite.execute('create table `{0}` (length int)'.format(sID))
    scraperwiki.sqlite.save(['length'], strList, table_name='{0}'.format(sID), verbose=2)
    scraperwiki.sqlite.commit()
    return

# ------ Here begins the "main" function

# -----------------------------------------------
# These are the arguments that we'll receive from the web form POST
articleNos = [ '501.822.05', '502.084.51', '401.341.06' ]
sessionID = 2130024694
requestedAction = 'Add'
actionItem = '0'
# -----------------------------------------------


# Seed the random number generator
random.seed()

# If this is the initial order form, the sessionID argument will be 0 and shoppingList is empty
# If there is a sessionID, load the shoppingList from the database
if sessionID == 0:
    sessionID = random.getrandbits(32)
    shoppingList = {}
else:
    # Load the shoppingList from the database
    shoppingList = loadArticles(sessionID)

if requestedAction == 'Add':
    # Add new articles to the shoppingList (whether there was an existing list or not)
    for artNo in articleNos:
        art1 = scrapeArticle(artNo)
        itemkey = '{0}'.format(random.getrandbits(32))
        while itemkey in shoppingList:
            itemkey = '{0}'.format(random.getrandbits(32))
        shoppingList[itemkey] = art1
elif requestedAction == 'Delete':
    # Delete the actionItem from the shoppingList (if it's there)
    if actionItem in shoppingList:
        del shoppingList[actionItem]
    else:
        print("Odd: we couldn't find the actionItem in the shoppingList")
else:
    print('Not quite certain what requestedAction you were looking for')

# Iterate through the shoppingList and print article information
for clef in shoppingList.keys():
    print("<b> {0} </b>: ".format(clef) + shoppingList[clef].description + " (" + shoppingList[clef].itemStr + ")")

# Commit the shoppingList to the database
saveArticles(sessionID, shoppingList)
print sessionID
import scraperwiki
import lxml.html
import decimal
import random
import unicodedata

# ------- This is the object class that will hold the scraped article information
class ArticleClass:
    description = ''
    priceCAStr = ''
    priceCADec = decimal.Decimal('0.00')
    priceUSStr = ''
    priceUSDec = decimal.Decimal('0.00')
    itemStr = ''
    imageLink = ''
    decimal.getcontext().prec = 2
    # This class function converts the class data into a string format
    # We need to strip out "weird" IKEA characters to make the database happy
    def toStr(self):
        self.description = unicodedata.normalize('NFKD', unicode(self.description)).encode('ascii', 'ignore')
        return '{0}|{1}|{2}|{3}|{4}'.format(self.description, self.priceCAStr, self.priceUSStr, self.itemStr, self.imageLink)

    # This class function loads the class attributes using a string created by toStr()
    def loadStr(self, str):
        itemList = str.split('|')
        self.description = itemList[0]
        self.priceCAStr = itemList[1].encode('ascii', 'ignore')
        self.priceCADec = decimal.Decimal(self.priceCAStr.translate(None, '$'))
        self.priceUSStr = itemList[2].encode('ascii', 'ignore')
        self.priceUSDec = decimal.Decimal(self.priceUSStr.translate(None, '$'))
        self.itemStr = itemList[3]
        self.imageLink = itemList[4]
        return

# ------ This function is the "scraper" that extracts information from the CA and US IKEA pages
# It returns an ArticleClass object containing the information extracted
def scrapeArticle( articleNum ):
    # Scrape the search page on Canadian and US IKEA sites; the product page should return
    itemPageHTMLCA = scraperwiki.scrape("http://www.ikea.com/ca/en/search/?query=" + articleNum)
    itemPageHTMLUS = scraperwiki.scrape("http://www.ikea.com/us/en/search/?query=" + articleNum)

    # Parse it for XML
    itemPageRootCA = lxml.html.fromstring(itemPageHTMLCA)
    itemPageRootUS = lxml.html.fromstring(itemPageHTMLUS)

    artC = ArticleClass()

    metaList = itemPageRootCA.cssselect("head meta")
    for el in metaList:
        if 'name' in el.attrib:
            if el.attrib['name'] == 'title':
                artC.description = el.attrib['content']
            if el.attrib['name'] == 'price':
                artC.priceCAStr = el.attrib['content']
            if el.attrib['name'] == 'partnumber':
                artC.itemStr = el.attrib['content']

    # Scrape US price information
    metaList = itemPageRootUS.cssselect("head meta")
    for el in metaList:
        if 'name' in el.attrib:
            if el.attrib['name'] == 'price':
                artC.priceUSStr = el.attrib['content']

    # Scrape item image link
    linkList = itemPageRootCA.cssselect("head link")
    for el in linkList:
        if 'rel' in el.attrib:
            if el.attrib['rel'] == 'image_src':
                artC.imageLink = el.attrib['href']

    artC.priceCADec = decimal.Decimal(artC.priceCAStr.translate(None, '$'))
    artC.priceUSDec = decimal.Decimal(artC.priceUSStr.translate(None, '$'))
    return artC;

# ------ This function loads ArticleClass objects from the datastore into a Dictionary
def loadArticles(sID):
    sList = { 'definer': 1 }

    textList = scraperwiki.sqlite.select("* from `{0}` where sessionID = {0}".format(sID))[0]
    for clef in textList.keys():
        if (clef != 'sessionID') and (clef != 'length'):
            sList[clef] = ArticleClass()
            sList[clef].loadStr(textList[clef])
    del sList['definer']
    scraperwiki.sqlite.execute('drop table if exists `{0}`'.format(sID))
    #    scraperwiki.sqlite.execute("delete from swdata where sessionID = {0}".format(sID))
    scraperwiki.sqlite.commit()
    return sList

# ------ This function saves a Dictionary of ArticleClass objects to the datastore
def saveArticles(sID, sList):
    strList = { 'sessionID': sID }

    for el in sList.keys():
        strList[el] = sList[el].toStr()
    strList['length'] = len(sList)
    scraperwiki.sqlite.execute('create table `{0}` (length int)'.format(sID))
    scraperwiki.sqlite.save(['length'], strList, table_name='{0}'.format(sID), verbose=2)
    scraperwiki.sqlite.commit()
    return

# ------ Here begins the "main" function

# -----------------------------------------------
# These are the arguments that we'll receive from the web form POST
articleNos = [ '501.822.05', '502.084.51', '401.341.06' ]
sessionID = 2130024694
requestedAction = 'Add'
actionItem = '0'
# -----------------------------------------------


# Seed the random number generator
random.seed()

# If this is the initial order form, the sessionID argument will be 0 and shoppingList is empty
# If there is a sessionID, load the shoppingList from the database
if sessionID == 0:
    sessionID = random.getrandbits(32)
    shoppingList = {}
else:
    # Load the shoppingList from the database
    shoppingList = loadArticles(sessionID)

if requestedAction == 'Add':
    # Add new articles to the shoppingList (whether there was an existing list or not)
    for artNo in articleNos:
        art1 = scrapeArticle(artNo)
        itemkey = '{0}'.format(random.getrandbits(32))
        while itemkey in shoppingList:
            itemkey = '{0}'.format(random.getrandbits(32))
        shoppingList[itemkey] = art1
elif requestedAction == 'Delete':
    # Delete the actionItem from the shoppingList (if it's there)
    if actionItem in shoppingList:
        del shoppingList[actionItem]
    else:
        print("Odd: we couldn't find the actionItem in the shoppingList")
else:
    print('Not quite certain what requestedAction you were looking for')

# Iterate through the shoppingList and print article information
for clef in shoppingList.keys():
    print("<b> {0} </b>: ".format(clef) + shoppingList[clef].description + " (" + shoppingList[clef].itemStr + ")")

# Commit the shoppingList to the database
saveArticles(sessionID, shoppingList)
print sessionID
