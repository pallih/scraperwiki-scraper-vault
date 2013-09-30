# Blank Python  

print "Hello"

import time
import lxml.html
import urllib
import scraperwiki
import time
import random
from lxml.html import fromstring
from lxml.html import tostring

CurrentTimeStamp = time.strftime('%x %X %Z')
print "Timestamp: ", CurrentTimeStamp


def CreateTables():
    sellerData = {}
    sellerData['seller'] = "delete this row"
    sellerData['sellerLocation'] = None
    sellerData['sellerSellsToLocation'] = None
    sellerData['sellerFeedback'] = None
    sellerData['sellerFeedbackPercentage'] = None
    sellerData['timestamp'] = CurrentTimeStamp
    sellerData['source'] = None
    scraperwiki.sqlite.save(["seller"], sellerData, table_name="seller")


    auctionData = {}
    auctionData['itemNumber'] = "delete this row"
    auctionData['itemNumberOfBids'] = 0
    auctionData['itemEndPrice'] = 0
    auctionData['itemActiveAuctionFlag'] = "No"
    auctionData['itemActiveAuctionText'] = "None"
    scraperwiki.sqlite.save(["itemNumber"], auctionData, table_name="auction")


    auctionData = {}
    auctionData['auctionNumber'] = "delete this row"
    auctionData['auctionStatusCode'] = None
    scraperwiki.sqlite.save(["auctionNumber"], auctionData, table_name="auctionStatus")


    return


def UpdateRunStats(inCompletedItemsList, inItemsUpdatedQty, inItemsNotUpdatedQty, inRunStatus):
    runStatsData = {}
    runStatsData["RunStatus"] = inRunStatus
    runStatsData["RunTime"] = CurrentTimeStamp
    runStatsData["CompletedItemsList"] = inCompletedItemsList
    runStatsData["ItemsUpdatedQty"] = inItemsUpdatedQty
    runStatsData["ItemsNotUpdatedQty"] = inItemsNotUpdatedQty
    scraperwiki.sqlite.save(["RunTime"], runStatsData, table_name = "RunStats")

    return

def BuildActiveList():
    #Build the active List from all the items in the auction table that haven't ended
    activeList = []
    activeDict = {}
#    activeDict = scraperwiki.sqlite.select("itemNumber from auction where itemActiveAuctionFlag = 'Yes'")
    item = {}
    for item in activeDict :
        activeList.append(item["itemNumber"])

    print activeList
    return activeList


def AddNewItems(activeList):
    scraperwiki.sqlite.attach("test6")
    scrapeList = scraperwiki.sqlite.select("auctionNumber from test6.newTable")
    for item in scrapeList:
        if item["auctionNumber"] not in activeList:
            activeList.append(item["auctionNumber"])

    random.shuffle(activeList)
    print activeList
    print "Length: ", len(activeList)
    return activeList



def normalize_whitespace(str):            # taken from icodesnip.com
    import re
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str

def ScrapeAuction(inItemNumber):

#### Flow of section
#  If new to us auction
#    If auction still current
#      scrape for all attributes using current auction tags
#    Else
#      scrape for all attributes using completed auction tags
#  Else
#    If auction still current
#      scrape for update attributes using current auction tags
#    Else
#      scrape for update attributes using completed auction tags
####

### Current auction tags
    removedAuctionTag = '//div[@id="vi-container"]//div[@class="sm-imc sml-imc"]'
    categoryBreadCrumbGroupTag = '//div[@class="bbc-in bbc bbc-nav"]//ul/li/a'
    titleTag = 'h1'
    itemTitle2Tag = '//h2[@class="vi-is1-titleH2"]'  
    descriptionTag = '//div[@class="item_description"]//*'
    sellerTag = "//table[contains(@class,'s-content')]//span[@class='mbg-nw']"
    sellerFeedbackTag = "//table[contains(@class,'s-content')]//a[@class='mbg-fb']//*"
    sellerFeedbackPercentageTag = "//table[contains(@class,'s-content')]//span[@class='s-gray z_a']"
#    sellerTag = "//span[@class='mbg-nw']"
#    sellerFeedbackTag = "//a[@class='mbg-fb']//*"
#    sellerFeedbackPercentageTag = "//span[@class='s-gray z_a']"

    itemNumberTag = "//table[@class='sp1']/tr/td[2]"
    sellerLocationTag = "//table[@class='sp1']/tr[2]/td[2]"
    sellerSellsToLocationTag = "//table[@class='sp1']/tr[3]/td[2]"
    itemAttributeGroupTag = "//table[@class='vi-ia-attrGroup']//table/tr//*"
    itemConditionTag = "//span[@class='vi-is1-condText']"
    itemConditionTag2 = "//td[@class='vi-is1-clr'][1]"
    itemNumberOfBidsTag = "following-sibling::td//text()"  #Number of bids is the first text of td following the "Bid History" text
    itemBidHistoryTag = "//th[@class='vi-is1-lbl']"
    itemActiveAuctionTag = "//span[@id='v4-1-msg']"
    itemDateGroupTag = "//span[@class='vi-is1-dt']//*"
    itemPriceTag = '//span[contains(@itemprop, "price")]'
    itemPriceTag2 = "//span[contains(@class, 'vi-is1-prcp')]"  #if there are two of these, it could be an "auction
                                                              #or Buy Now" or it could be a Buy Now that is on sale
    itemPriceTag3 = "//span[contains(@id, 'v4-')]" 
    itemSaleTag = "//span[contains(@class, 'vi-is1-prcsl')]"  #if this exists, the buy now item is on sale

    itemReserveTag = "//a[@class='vi-is1-rsv']"   
    itemBuyNowTag = "//a[@id='but_v4-4'] | //a[@id='but_v4-5']"         #Only for active buy now -- found but_v4-5 id on Buy Now on Sale with Make Offer
    itemMakeOfferTag = "//a[@id='but_v4-2'] | //a[@id='but_v4-3']"      #Only for active make offer-- found but_v4-3 id on Buy Now on Sale with Make Offer
    itemPlaceBidTag = "//input[@id='but_v4-6']"   #Only for active auctions
    itemCompleteTag = "//table[@class='vi-ia-attrGroup']"
    itemPictureGroupTag = "//div[@class='vi-ipic1']//img[@src]"

### Completed auction tags
    sellerTag_c = "//span[@class='mbg-nw']"
    sellerFeedbackTag_c = "//a[@class='mbg-fb']//*"


    url = 'http://www.ebay.com/itm/' + inItemNumber
    print "Reading URL: ", url
    try:
        html = urllib.urlopen(url).read()
    except:
        print "*********ERROR on reading URL*************"
        print url
        print html
        print "*********End of Error Report************"
    print html

    root = lxml.html.fromstring(html)

###  Completed/Ended or Active Auction selection Begin
### Check first if it's removed or not
    ItemRemovedFlag = False
    try:
        removedAuctionText = root.xpath(removedAuctionTag)[0].text_content()
        if "has been removed" in removedAuctionText :
            ItemActiveAuctionFlag = removedAuctionText
            ItemRemovedFlag = True
    except:
        try:
            ItemActiveAuctionFlag = root.xpath(itemActiveAuctionTag)[0].text_content()
        except:
            ItemActiveAuctionFlag = "Active"

    if ItemRemovedFlag :
        return ItemActiveAuctionFlag, "No"     #fix needed toupdate removed auctions
###  Completed/Ended or Active Auction selection End



###  Category selection Begin
    CategoryBreadCrumbGroup = root.xpath(categoryBreadCrumbGroupTag)
    CategoryTitle = []
    CategoryNumber = []
    CategoryParentNumber = []
    tempCategoryParentNumber = None
    if len(CategoryBreadCrumbGroup) != 0:
        listIndex = 0
        for element in (CategoryBreadCrumbGroup):
            tempHref = element.get("href")
            tempSplitHrefArray = tempHref.split("/")
            tempTitle = tempSplitHrefArray[4]
            if tempTitle[-1:] == "-":           #  if the last character of the title is a "-", then strip it off
                tempTitle = tempTitle[:-1]
            CategoryTitle.append(tempTitle)
            CategoryNumber.append(tempSplitHrefArray[5])
            CategoryParentNumber.append(tempCategoryParentNumber)
            tempCategoryParentNumber = tempSplitHrefArray[5]
###  Category selection End


###  Completed/Ended or Active Auction selection Begin
    try:
        ItemActiveAuctionFlag = root.xpath(itemActiveAuctionTag)[0].text_content()
    except:
        ItemActiveAuctionFlag = "Active"

###  Completed/Ended or Active Auction selection End


###  Picture selection Begin
    ItemPictureGroup = root.xpath(itemPictureGroupTag)
    ItemPictureSmall = []
    ItemPictureLarge = []
    ItemPicture_12 = []
    ItemPicture_1 = []
    ListSrcSplit = []
    if len(ItemPictureGroup) != 0:
      for elementIndex, element in enumerate(ItemPictureGroup):
          tempSrc = element.get("src")
          if tempSrc.find("ebaystatic") == -1:  #skip the ebaystatic pics
              tempSplitPoint = tempSrc.find("_")  #extract just the first part of the src name (up to the underscore)
              tempSrcSplit = tempSrc[0:tempSplitPoint]
              if tempSrcSplit not in ListSrcSplit:  #if already captured the first part of the name, don't need it again
                  ListSrcSplit.append(tempSrcSplit)
                  ItemPictureSmall.append(tempSrc)
                  # Looks like the large pictures end in "_3.jpg" rather than the captured ones that end in "_3x.jpg"
                  # So, strip out the x (where x is some other number)and keep the large picture URL.  
                  # The x is always in the same position in the string
                  # Picture URLs are not consistent.  Get different possible options, just in case
                  tempPictureLarge = tempSrc[:-5] + tempSrc[-4:]
                  ItemPictureLarge.append(tempPictureLarge)
                  tempPicture_12 = tempSrcSplit + "_12.jpg"
                  ItemPicture_12.append(tempPicture_12)
                  tempPicture_1 = tempSrcSplit + "_1.jpg"
                  ItemPicture_1.append(tempPicture_1)
#          listIndex += 1
  
###  Picture selection End


### Title, Description, and Seller selection Begin
    ItemTitle = root.cssselect(titleTag)[0].text_content()
    tempItemTitle2 = root.xpath(itemTitle2Tag)
    ItemTitle2 = ""
    if len(tempItemTitle2) != 0:
        ItemTitle2 = tempItemTitle2[0].text
    ItemDescriptionHTML = tostring(root.xpath(descriptionTag)[0]) 
    if len(ItemDescriptionHTML) > 32000 :
        ItemDescriptionHTML = ItemDescriptionHTML[:32000]
#    ItemDescriptionText = normalize_whitespace(root.xpath(descriptionTag)[0].text_content())
    ItemDescriptionText = root.xpath(descriptionTag)[0].text_content()
    if len(ItemDescriptionText) > 32000 :
        ItemDescriptionText = ItemDescriptionText[:32000]

    try:
        Seller = root.xpath(sellerTag)[0].text
    except:
        try:
            Seller = root.xpath(sellerTag_c)[0].text
        except:
            Seller = None


    try:
        SellerFeedback = root.xpath(sellerFeedbackTag)[0].tail
    except:
        try:
            SellerFeedback = root.xpath(sellerFeedbackTag_c)[0].tail
        except:
            SellerFeedback = None

    try:     # sometimes there is no percentage number
        SellerFeedbackPercentage = root.xpath(sellerFeedbackPercentageTag)[0].text
        SellerFeedbackPercentage = SellerFeedbackPercentage.split()[0]    # Keeps only the percentage number
    except:
        SellerFeedbackPercentage = None
    ItemNumber = root.xpath(itemNumberTag)[0].text
    SellerLocation = root.xpath(sellerLocationTag)[0].text
    SellerSellsToLocation = root.xpath(sellerSellsToLocationTag)[0].text
### Title, Description, and Seller selection End


### Attribute Group selection Begin
    ItemAttributeGroup = root.xpath(itemAttributeGroupTag)
    key = []
    value = []
    i = -1
    firstTdAfterTh = False
    for element in ItemAttributeGroup:
        if element.tag == 'th':
            i += 1
            key.append(element.text)
            firstTdAfterTh = True
        if element.tag == 'td' and firstTdAfterTh:
            value.append(element.text_content())
            firstTdAfterTh = False
### Attribute Group selection End


###  Condition and Date selection Begin
    ItemCondition = root.xpath(itemConditionTag)[0].text_content()
    ItemDateGroup = root.xpath(itemDateGroupTag)
    if len(ItemDateGroup) == 0 or ItemDateGroup[-2].text == None :
        ItemAuctionEndDate = "unknown"
        ItemAuctionEndTime = "unknown"
    else:
        ItemAuctionEndDate = ItemDateGroup[-2].text
        if ItemAuctionEndDate.find("(") != -1 :
            ItemAuctionEndDate = ItemAuctionEndDate[1:]  #strip off the starting '(' from the date
        ItemAuctionEndTime = ItemDateGroup[-1].text
        if ItemAuctionEndTime.find(")") != -1 :
            ItemAuctionEndTime = ItemAuctionEndTime[:-1]  #strip off the trailing ')' from the time
###  Condition and Date selection End


### Price and Number of Bids selection Begin
###  Bids allowed or not


    itemAuctionFlag = False
    itemBuyNowFlag = False
    itemMakeOfferFlag = False
    itemReserveFlag = False
    itemOnSaleFlag = False
    ItemNumberOfBids = 0

    for item in root.xpath(itemBidHistoryTag):
#        print item
#        print item.text
#        print item.xpath("following-sibling::td//text()")[0]
        if item.text == "Bid history:" :
            itemAuctionFlag = True
            ItemNumberOfBids = int(item.xpath(itemNumberOfBidsTag)[0])
            ItemEndPrice = root.xpath(itemPriceTag)[0].text_content()





###  Reserve or not
    try:
        ItemReserveText = root.xpath(itemReserveTag)[0].text_content()
        itemReserveFlag = True
    except:
        ItemReserveText = None


###  Buy Now or not
    try:
        ItemBuyNowText = root.xpath(itemBuyNowTag)[0].text_content()
        itemBuyNowFlag = True
        print "here1"
        if itemAuctionFlag:    #if it's an "auction or Buy Now", then the Buy Now price is the second price
            ItemBuyNowPrice = root.xpath(itemPriceTag)[1].text_content()
            print "here2.1"
            ItemOriginalBuyNowPrice = None      # assume if "auction or Buy Now" then it cannot be on sale -- need to verify
        else:                  #if it's only a Buy Now, see if it's on sale or not
            print "here2"
            try:
                print "here3"
                ItemSaleText = root.xpath(itemSaleTag)[0].text_content()   #if this path exists, then it's on sale
                print "here4"
                itemOnSaleFlag = True
                ItemBuyNowPrice = root.xpath(itemPriceTag + "//text()")[3]   #the text() is an lxml only extension to xpath.  It splits the text into a list of "text" and "tail" items.  This allows us to get the price without the associated "Original Price" hidden html text
                print "here5"
                ItemOriginalBuyNowPrice = root.xpath(itemPriceTag + "//text()")[1]   #the text() is an lxml only extension to xpath.  It splits the text into a list of "text" and "tail" items.  This allows us to get the price without the associated "Original Price" hidden html text
                print "here6"
            except:
                print "here7"
                ItemBuyNowPrice = root.xpath(itemPriceTag)[0].text_content()
                print "here8"
                ItemOriginalBuyNowPrice = None
        ItemEndPrice = ItemBuyNowPrice
        print ItemBuyNowPrice
        print ItemOriginalBuyNowPrice
        print ItemEndPrice
    except:
        ItemBuyNowText = None
        print "excpt: ", ItemBuyNowText
#        print "excpt: ", ItemOriginalBuyNowPrice
#        print "excpt: ", ItemEndPrice



###  Make Offer or not
    try:
        ItemMakeOfferText = root.xpath(itemMakeOfferTag)[0].text_content()
        itemMakeOfferFlag = True
    except:
        ItemMakeOfferText = None

    DataRecord = {}
    PriceClass = []
    PriceText = []
    DataRecord['AttribCount'] = len(root.xpath(itemPriceTag))
    for node in root.xpath(itemPriceTag):
        PriceClass.append(node.xpath("@id"))
        PriceText.append(node.text_content())
    DataRecord['PriceClass'] = PriceClass
    DataRecord['PriceText'] = PriceText
    if ItemActiveAuctionFlag == "Active":
        DataRecord['itemActiveAuctionFlag'] = "Yes"
        DataRecord['itemActiveAuctionText'] = ""
    else:
        DataRecord['itemActiveAuctionFlag'] = "No"
        DataRecord['itemActiveAuctionText'] = ItemActiveAuctionFlag
    DataRecord['itemAuctionFlag'] = itemAuctionFlag
    DataRecord['itemBuyNowFlag'] = itemBuyNowFlag
    DataRecord['itemMakeOfferFlag'] = itemMakeOfferFlag
    DataRecord['itemReserveFlag'] = itemReserveFlag
    DataRecord['itemOnSaleFlag'] = itemOnSaleFlag
    print DataRecord
    DataRecord['auctionNumber'] = ItemNumber
    DataRecord['PriceTagPath'] = '1'
    scraperwiki.sqlite.save(["auctionNumber", "PriceTagPath"], DataRecord, table_name="DataRecord")

    DataRecord = {}
    PriceClass = []
    PriceText = []
    DataRecord['AttribCount'] = len(root.xpath(itemPriceTag2))
    for node in root.xpath(itemPriceTag2):
        PriceClass.append(node.xpath("@id"))
        PriceText.append(node.text_content())
    DataRecord['PriceClass'] = PriceClass
    DataRecord['PriceText'] = PriceText
    if ItemActiveAuctionFlag == "Active":
        DataRecord['itemActiveAuctionFlag'] = "Yes"
        DataRecord['itemActiveAuctionText'] = ""
    else:
        DataRecord['itemActiveAuctionFlag'] = "No"
        DataRecord['itemActiveAuctionText'] = ItemActiveAuctionFlag
    DataRecord['itemAuctionFlag'] = itemAuctionFlag
    DataRecord['itemBuyNowFlag'] = itemBuyNowFlag
    DataRecord['itemMakeOfferFlag'] = itemMakeOfferFlag
    DataRecord['itemReserveFlag'] = itemReserveFlag
    DataRecord['itemOnSaleFlag'] = itemOnSaleFlag
    print DataRecord
    DataRecord['auctionNumber'] = ItemNumber
    DataRecord['PriceTagPath'] = '2'
    scraperwiki.sqlite.save(["auctionNumber", "PriceTagPath"], DataRecord, table_name="DataRecord")

    DataRecord = {}
    PriceClass = []
    PriceText = []
    DataRecord['AttribCount'] = len(root.xpath(itemPriceTag3))
    for node in root.xpath(itemPriceTag3):
        PriceClass.append(node.xpath("@id"))
        PriceText.append(node.text_content())
    DataRecord['PriceClass'] = PriceClass
    DataRecord['PriceText'] = PriceText
    if ItemActiveAuctionFlag == "Active":
        DataRecord['itemActiveAuctionFlag'] = "Yes"
        DataRecord['itemActiveAuctionText'] = ""
    else:
        DataRecord['itemActiveAuctionFlag'] = "No"
        DataRecord['itemActiveAuctionText'] = ItemActiveAuctionFlag
    DataRecord['itemAuctionFlag'] = itemAuctionFlag
    DataRecord['itemBuyNowFlag'] = itemBuyNowFlag
    DataRecord['itemMakeOfferFlag'] = itemMakeOfferFlag
    DataRecord['itemReserveFlag'] = itemReserveFlag
    DataRecord['itemOnSaleFlag'] = itemOnSaleFlag
    print DataRecord
    DataRecord['auctionNumber'] = ItemNumber
    DataRecord['PriceTagPath'] = '3'
    scraperwiki.sqlite.save(["auctionNumber", "PriceTagPath"], DataRecord, table_name="DataRecord")


    if not (itemAuctionFlag or itemBuyNowFlag):   # Seems to be rare case where a listing has ended and we can't determine what kind of listing it was
        ItemEndPrice = None
        print "Unable to determine listing type: ", url

###  Price selection End


#    print ItemTitle
#    print ItemTitle2
#    print ItemDescriptionHTML
#    print ItemDescriptionText
#    print Seller
#    print SellerFeedback
#    print SellerFeedbackPercentage
#    print ItemNumber
#    print SellerLocation
#    print SellerSellsToLocation
#    print ItemCondition
#    print ItemAuctionEndDate
#    print ItemAuctionEndTime
#    print ItemNumberOfBids
#    print ItemEndPrice

    updatedInfo = {}
    updatedInfo['itemNumber'] = ItemNumber
    updatedInfo['itemNumberOfBids'] = ItemNumberOfBids
    updatedInfo['itemEndPrice'] = ItemEndPrice
    if ItemActiveAuctionFlag == "Active":
        updatedInfo['itemActiveAuctionFlag'] = "Yes"
        updatedInfo['itemActiveAuctionText'] = ""
    else:
        updatedInfo['itemActiveAuctionFlag'] = "No"
        updatedInfo['itemActiveAuctionText'] = ItemActiveAuctionFlag
    updatedNumberOfPictures = len(ItemPictureSmall)
    updatedNumberOfAttributes = len(key)
    print updatedInfo
#    print currentAuctionInfo
#    print updatedInfo == currentAuctionInfo
#    print updatedNumberOfPictures, currentNumberOfPictures, updatedNumberOfPictures == currentNumberOfPictures
#    print updatedNumberOfAttributes, currentNumberOfAttributes, updatedNumberOfAttributes == currentNumberOfAttributes


##### Change if test to second one if want to update every row ####
#    if updatedInfo != currentAuctionInfo or updatedNumberOfPictures != currentNumberOfPictures or updatedNumberOfAttributes != currentNumberOfAttributes :
    if 1 == 1 :
        print "Update the tables"
        UpdateFlag = "Yes"


## Save to Tables starts here



    return str(root.xpath(itemPriceTag + '/@id')[0]), UpdateFlag
    #return ItemActiveAuctionFlag, UpdateFlag




##Main start here

###First Time Only
#CreateTables()
###End First Time Only


UpdateRunStats([],0,0,"Begin Run")

random.seed()

#First, create a list of active items from the auction table
activeList = BuildActiveList()

#Next, append to the active list, the items from the test6 "newTable"
activeList = AddNewItems(activeList)
#activeList = activeList[60:]

#Then, scrape all of these items
#As we scrape, if the auction has not finished yet, add it to a new "stillActive" list
#Maybe a TODO is if the auction ended with no bids, add it to a "check again" list to see if it's been relisted
stillActiveList = []
completedItemList = []
UpdatedAuctionCount = 0
NotUpdatedAuctionCount = 0
PriceIDList = []
for item in activeList :
    ActiveCode, UpdateFlag = ScrapeAuction(item)
    print "AC: ", ActiveCode
    PriceIDList.append(ActiveCode)
    if UpdateFlag == "Yes" :
        UpdatedAuctionCount += 1
    else:
        NotUpdatedAuctionCount += 1
    if ActiveCode == "Active":
        stillActiveList.append(item)
    print "Updated Auctions: ", UpdatedAuctionCount, "Not Updated Auctions: ", NotUpdatedAuctionCount, PriceIDList
    completedItemList.append(item)
    UpdateRunStats(completedItemList, UpdatedAuctionCount, NotUpdatedAuctionCount, "Run In Progress")
    n = random.random() * 10 + 3
    print "Sleep for seconds: " + str(n)
    time.sleep(n)


print len(stillActiveList), "still active of ", len(activeList), "originally active"

#After scraping is finished, truncate the "activeTable"
#scraperwiki.sqlite.execute("delete from activeTable")
#scraperwiki.sqlite.commit()


#Then add the "stillActive" list to the "activeTable"
activeData = {}
print stillActiveList
for item in stillActiveList :
    activeData["auctionNumber"] = item
    activeData["currentTimeStamp"] = CurrentTimeStamp
    scraperwiki.sqlite.save(["auctionNumber"], activeData, table_name = "activeTable")


UpdateRunStats(completedItemList, UpdatedAuctionCount, NotUpdatedAuctionCount, "Run Finished")



# End Program
# Blank Python  

print "Hello"

import time
import lxml.html
import urllib
import scraperwiki
import time
import random
from lxml.html import fromstring
from lxml.html import tostring

CurrentTimeStamp = time.strftime('%x %X %Z')
print "Timestamp: ", CurrentTimeStamp


def CreateTables():
    sellerData = {}
    sellerData['seller'] = "delete this row"
    sellerData['sellerLocation'] = None
    sellerData['sellerSellsToLocation'] = None
    sellerData['sellerFeedback'] = None
    sellerData['sellerFeedbackPercentage'] = None
    sellerData['timestamp'] = CurrentTimeStamp
    sellerData['source'] = None
    scraperwiki.sqlite.save(["seller"], sellerData, table_name="seller")


    auctionData = {}
    auctionData['itemNumber'] = "delete this row"
    auctionData['itemNumberOfBids'] = 0
    auctionData['itemEndPrice'] = 0
    auctionData['itemActiveAuctionFlag'] = "No"
    auctionData['itemActiveAuctionText'] = "None"
    scraperwiki.sqlite.save(["itemNumber"], auctionData, table_name="auction")


    auctionData = {}
    auctionData['auctionNumber'] = "delete this row"
    auctionData['auctionStatusCode'] = None
    scraperwiki.sqlite.save(["auctionNumber"], auctionData, table_name="auctionStatus")


    return


def UpdateRunStats(inCompletedItemsList, inItemsUpdatedQty, inItemsNotUpdatedQty, inRunStatus):
    runStatsData = {}
    runStatsData["RunStatus"] = inRunStatus
    runStatsData["RunTime"] = CurrentTimeStamp
    runStatsData["CompletedItemsList"] = inCompletedItemsList
    runStatsData["ItemsUpdatedQty"] = inItemsUpdatedQty
    runStatsData["ItemsNotUpdatedQty"] = inItemsNotUpdatedQty
    scraperwiki.sqlite.save(["RunTime"], runStatsData, table_name = "RunStats")

    return

def BuildActiveList():
    #Build the active List from all the items in the auction table that haven't ended
    activeList = []
    activeDict = {}
#    activeDict = scraperwiki.sqlite.select("itemNumber from auction where itemActiveAuctionFlag = 'Yes'")
    item = {}
    for item in activeDict :
        activeList.append(item["itemNumber"])

    print activeList
    return activeList


def AddNewItems(activeList):
    scraperwiki.sqlite.attach("test6")
    scrapeList = scraperwiki.sqlite.select("auctionNumber from test6.newTable")
    for item in scrapeList:
        if item["auctionNumber"] not in activeList:
            activeList.append(item["auctionNumber"])

    random.shuffle(activeList)
    print activeList
    print "Length: ", len(activeList)
    return activeList



def normalize_whitespace(str):            # taken from icodesnip.com
    import re
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str

def ScrapeAuction(inItemNumber):

#### Flow of section
#  If new to us auction
#    If auction still current
#      scrape for all attributes using current auction tags
#    Else
#      scrape for all attributes using completed auction tags
#  Else
#    If auction still current
#      scrape for update attributes using current auction tags
#    Else
#      scrape for update attributes using completed auction tags
####

### Current auction tags
    removedAuctionTag = '//div[@id="vi-container"]//div[@class="sm-imc sml-imc"]'
    categoryBreadCrumbGroupTag = '//div[@class="bbc-in bbc bbc-nav"]//ul/li/a'
    titleTag = 'h1'
    itemTitle2Tag = '//h2[@class="vi-is1-titleH2"]'  
    descriptionTag = '//div[@class="item_description"]//*'
    sellerTag = "//table[contains(@class,'s-content')]//span[@class='mbg-nw']"
    sellerFeedbackTag = "//table[contains(@class,'s-content')]//a[@class='mbg-fb']//*"
    sellerFeedbackPercentageTag = "//table[contains(@class,'s-content')]//span[@class='s-gray z_a']"
#    sellerTag = "//span[@class='mbg-nw']"
#    sellerFeedbackTag = "//a[@class='mbg-fb']//*"
#    sellerFeedbackPercentageTag = "//span[@class='s-gray z_a']"

    itemNumberTag = "//table[@class='sp1']/tr/td[2]"
    sellerLocationTag = "//table[@class='sp1']/tr[2]/td[2]"
    sellerSellsToLocationTag = "//table[@class='sp1']/tr[3]/td[2]"
    itemAttributeGroupTag = "//table[@class='vi-ia-attrGroup']//table/tr//*"
    itemConditionTag = "//span[@class='vi-is1-condText']"
    itemConditionTag2 = "//td[@class='vi-is1-clr'][1]"
    itemNumberOfBidsTag = "following-sibling::td//text()"  #Number of bids is the first text of td following the "Bid History" text
    itemBidHistoryTag = "//th[@class='vi-is1-lbl']"
    itemActiveAuctionTag = "//span[@id='v4-1-msg']"
    itemDateGroupTag = "//span[@class='vi-is1-dt']//*"
    itemPriceTag = '//span[contains(@itemprop, "price")]'
    itemPriceTag2 = "//span[contains(@class, 'vi-is1-prcp')]"  #if there are two of these, it could be an "auction
                                                              #or Buy Now" or it could be a Buy Now that is on sale
    itemPriceTag3 = "//span[contains(@id, 'v4-')]" 
    itemSaleTag = "//span[contains(@class, 'vi-is1-prcsl')]"  #if this exists, the buy now item is on sale

    itemReserveTag = "//a[@class='vi-is1-rsv']"   
    itemBuyNowTag = "//a[@id='but_v4-4'] | //a[@id='but_v4-5']"         #Only for active buy now -- found but_v4-5 id on Buy Now on Sale with Make Offer
    itemMakeOfferTag = "//a[@id='but_v4-2'] | //a[@id='but_v4-3']"      #Only for active make offer-- found but_v4-3 id on Buy Now on Sale with Make Offer
    itemPlaceBidTag = "//input[@id='but_v4-6']"   #Only for active auctions
    itemCompleteTag = "//table[@class='vi-ia-attrGroup']"
    itemPictureGroupTag = "//div[@class='vi-ipic1']//img[@src]"

### Completed auction tags
    sellerTag_c = "//span[@class='mbg-nw']"
    sellerFeedbackTag_c = "//a[@class='mbg-fb']//*"


    url = 'http://www.ebay.com/itm/' + inItemNumber
    print "Reading URL: ", url
    try:
        html = urllib.urlopen(url).read()
    except:
        print "*********ERROR on reading URL*************"
        print url
        print html
        print "*********End of Error Report************"
    print html

    root = lxml.html.fromstring(html)

###  Completed/Ended or Active Auction selection Begin
### Check first if it's removed or not
    ItemRemovedFlag = False
    try:
        removedAuctionText = root.xpath(removedAuctionTag)[0].text_content()
        if "has been removed" in removedAuctionText :
            ItemActiveAuctionFlag = removedAuctionText
            ItemRemovedFlag = True
    except:
        try:
            ItemActiveAuctionFlag = root.xpath(itemActiveAuctionTag)[0].text_content()
        except:
            ItemActiveAuctionFlag = "Active"

    if ItemRemovedFlag :
        return ItemActiveAuctionFlag, "No"     #fix needed toupdate removed auctions
###  Completed/Ended or Active Auction selection End



###  Category selection Begin
    CategoryBreadCrumbGroup = root.xpath(categoryBreadCrumbGroupTag)
    CategoryTitle = []
    CategoryNumber = []
    CategoryParentNumber = []
    tempCategoryParentNumber = None
    if len(CategoryBreadCrumbGroup) != 0:
        listIndex = 0
        for element in (CategoryBreadCrumbGroup):
            tempHref = element.get("href")
            tempSplitHrefArray = tempHref.split("/")
            tempTitle = tempSplitHrefArray[4]
            if tempTitle[-1:] == "-":           #  if the last character of the title is a "-", then strip it off
                tempTitle = tempTitle[:-1]
            CategoryTitle.append(tempTitle)
            CategoryNumber.append(tempSplitHrefArray[5])
            CategoryParentNumber.append(tempCategoryParentNumber)
            tempCategoryParentNumber = tempSplitHrefArray[5]
###  Category selection End


###  Completed/Ended or Active Auction selection Begin
    try:
        ItemActiveAuctionFlag = root.xpath(itemActiveAuctionTag)[0].text_content()
    except:
        ItemActiveAuctionFlag = "Active"

###  Completed/Ended or Active Auction selection End


###  Picture selection Begin
    ItemPictureGroup = root.xpath(itemPictureGroupTag)
    ItemPictureSmall = []
    ItemPictureLarge = []
    ItemPicture_12 = []
    ItemPicture_1 = []
    ListSrcSplit = []
    if len(ItemPictureGroup) != 0:
      for elementIndex, element in enumerate(ItemPictureGroup):
          tempSrc = element.get("src")
          if tempSrc.find("ebaystatic") == -1:  #skip the ebaystatic pics
              tempSplitPoint = tempSrc.find("_")  #extract just the first part of the src name (up to the underscore)
              tempSrcSplit = tempSrc[0:tempSplitPoint]
              if tempSrcSplit not in ListSrcSplit:  #if already captured the first part of the name, don't need it again
                  ListSrcSplit.append(tempSrcSplit)
                  ItemPictureSmall.append(tempSrc)
                  # Looks like the large pictures end in "_3.jpg" rather than the captured ones that end in "_3x.jpg"
                  # So, strip out the x (where x is some other number)and keep the large picture URL.  
                  # The x is always in the same position in the string
                  # Picture URLs are not consistent.  Get different possible options, just in case
                  tempPictureLarge = tempSrc[:-5] + tempSrc[-4:]
                  ItemPictureLarge.append(tempPictureLarge)
                  tempPicture_12 = tempSrcSplit + "_12.jpg"
                  ItemPicture_12.append(tempPicture_12)
                  tempPicture_1 = tempSrcSplit + "_1.jpg"
                  ItemPicture_1.append(tempPicture_1)
#          listIndex += 1
  
###  Picture selection End


### Title, Description, and Seller selection Begin
    ItemTitle = root.cssselect(titleTag)[0].text_content()
    tempItemTitle2 = root.xpath(itemTitle2Tag)
    ItemTitle2 = ""
    if len(tempItemTitle2) != 0:
        ItemTitle2 = tempItemTitle2[0].text
    ItemDescriptionHTML = tostring(root.xpath(descriptionTag)[0]) 
    if len(ItemDescriptionHTML) > 32000 :
        ItemDescriptionHTML = ItemDescriptionHTML[:32000]
#    ItemDescriptionText = normalize_whitespace(root.xpath(descriptionTag)[0].text_content())
    ItemDescriptionText = root.xpath(descriptionTag)[0].text_content()
    if len(ItemDescriptionText) > 32000 :
        ItemDescriptionText = ItemDescriptionText[:32000]

    try:
        Seller = root.xpath(sellerTag)[0].text
    except:
        try:
            Seller = root.xpath(sellerTag_c)[0].text
        except:
            Seller = None


    try:
        SellerFeedback = root.xpath(sellerFeedbackTag)[0].tail
    except:
        try:
            SellerFeedback = root.xpath(sellerFeedbackTag_c)[0].tail
        except:
            SellerFeedback = None

    try:     # sometimes there is no percentage number
        SellerFeedbackPercentage = root.xpath(sellerFeedbackPercentageTag)[0].text
        SellerFeedbackPercentage = SellerFeedbackPercentage.split()[0]    # Keeps only the percentage number
    except:
        SellerFeedbackPercentage = None
    ItemNumber = root.xpath(itemNumberTag)[0].text
    SellerLocation = root.xpath(sellerLocationTag)[0].text
    SellerSellsToLocation = root.xpath(sellerSellsToLocationTag)[0].text
### Title, Description, and Seller selection End


### Attribute Group selection Begin
    ItemAttributeGroup = root.xpath(itemAttributeGroupTag)
    key = []
    value = []
    i = -1
    firstTdAfterTh = False
    for element in ItemAttributeGroup:
        if element.tag == 'th':
            i += 1
            key.append(element.text)
            firstTdAfterTh = True
        if element.tag == 'td' and firstTdAfterTh:
            value.append(element.text_content())
            firstTdAfterTh = False
### Attribute Group selection End


###  Condition and Date selection Begin
    ItemCondition = root.xpath(itemConditionTag)[0].text_content()
    ItemDateGroup = root.xpath(itemDateGroupTag)
    if len(ItemDateGroup) == 0 or ItemDateGroup[-2].text == None :
        ItemAuctionEndDate = "unknown"
        ItemAuctionEndTime = "unknown"
    else:
        ItemAuctionEndDate = ItemDateGroup[-2].text
        if ItemAuctionEndDate.find("(") != -1 :
            ItemAuctionEndDate = ItemAuctionEndDate[1:]  #strip off the starting '(' from the date
        ItemAuctionEndTime = ItemDateGroup[-1].text
        if ItemAuctionEndTime.find(")") != -1 :
            ItemAuctionEndTime = ItemAuctionEndTime[:-1]  #strip off the trailing ')' from the time
###  Condition and Date selection End


### Price and Number of Bids selection Begin
###  Bids allowed or not


    itemAuctionFlag = False
    itemBuyNowFlag = False
    itemMakeOfferFlag = False
    itemReserveFlag = False
    itemOnSaleFlag = False
    ItemNumberOfBids = 0

    for item in root.xpath(itemBidHistoryTag):
#        print item
#        print item.text
#        print item.xpath("following-sibling::td//text()")[0]
        if item.text == "Bid history:" :
            itemAuctionFlag = True
            ItemNumberOfBids = int(item.xpath(itemNumberOfBidsTag)[0])
            ItemEndPrice = root.xpath(itemPriceTag)[0].text_content()





###  Reserve or not
    try:
        ItemReserveText = root.xpath(itemReserveTag)[0].text_content()
        itemReserveFlag = True
    except:
        ItemReserveText = None


###  Buy Now or not
    try:
        ItemBuyNowText = root.xpath(itemBuyNowTag)[0].text_content()
        itemBuyNowFlag = True
        print "here1"
        if itemAuctionFlag:    #if it's an "auction or Buy Now", then the Buy Now price is the second price
            ItemBuyNowPrice = root.xpath(itemPriceTag)[1].text_content()
            print "here2.1"
            ItemOriginalBuyNowPrice = None      # assume if "auction or Buy Now" then it cannot be on sale -- need to verify
        else:                  #if it's only a Buy Now, see if it's on sale or not
            print "here2"
            try:
                print "here3"
                ItemSaleText = root.xpath(itemSaleTag)[0].text_content()   #if this path exists, then it's on sale
                print "here4"
                itemOnSaleFlag = True
                ItemBuyNowPrice = root.xpath(itemPriceTag + "//text()")[3]   #the text() is an lxml only extension to xpath.  It splits the text into a list of "text" and "tail" items.  This allows us to get the price without the associated "Original Price" hidden html text
                print "here5"
                ItemOriginalBuyNowPrice = root.xpath(itemPriceTag + "//text()")[1]   #the text() is an lxml only extension to xpath.  It splits the text into a list of "text" and "tail" items.  This allows us to get the price without the associated "Original Price" hidden html text
                print "here6"
            except:
                print "here7"
                ItemBuyNowPrice = root.xpath(itemPriceTag)[0].text_content()
                print "here8"
                ItemOriginalBuyNowPrice = None
        ItemEndPrice = ItemBuyNowPrice
        print ItemBuyNowPrice
        print ItemOriginalBuyNowPrice
        print ItemEndPrice
    except:
        ItemBuyNowText = None
        print "excpt: ", ItemBuyNowText
#        print "excpt: ", ItemOriginalBuyNowPrice
#        print "excpt: ", ItemEndPrice



###  Make Offer or not
    try:
        ItemMakeOfferText = root.xpath(itemMakeOfferTag)[0].text_content()
        itemMakeOfferFlag = True
    except:
        ItemMakeOfferText = None

    DataRecord = {}
    PriceClass = []
    PriceText = []
    DataRecord['AttribCount'] = len(root.xpath(itemPriceTag))
    for node in root.xpath(itemPriceTag):
        PriceClass.append(node.xpath("@id"))
        PriceText.append(node.text_content())
    DataRecord['PriceClass'] = PriceClass
    DataRecord['PriceText'] = PriceText
    if ItemActiveAuctionFlag == "Active":
        DataRecord['itemActiveAuctionFlag'] = "Yes"
        DataRecord['itemActiveAuctionText'] = ""
    else:
        DataRecord['itemActiveAuctionFlag'] = "No"
        DataRecord['itemActiveAuctionText'] = ItemActiveAuctionFlag
    DataRecord['itemAuctionFlag'] = itemAuctionFlag
    DataRecord['itemBuyNowFlag'] = itemBuyNowFlag
    DataRecord['itemMakeOfferFlag'] = itemMakeOfferFlag
    DataRecord['itemReserveFlag'] = itemReserveFlag
    DataRecord['itemOnSaleFlag'] = itemOnSaleFlag
    print DataRecord
    DataRecord['auctionNumber'] = ItemNumber
    DataRecord['PriceTagPath'] = '1'
    scraperwiki.sqlite.save(["auctionNumber", "PriceTagPath"], DataRecord, table_name="DataRecord")

    DataRecord = {}
    PriceClass = []
    PriceText = []
    DataRecord['AttribCount'] = len(root.xpath(itemPriceTag2))
    for node in root.xpath(itemPriceTag2):
        PriceClass.append(node.xpath("@id"))
        PriceText.append(node.text_content())
    DataRecord['PriceClass'] = PriceClass
    DataRecord['PriceText'] = PriceText
    if ItemActiveAuctionFlag == "Active":
        DataRecord['itemActiveAuctionFlag'] = "Yes"
        DataRecord['itemActiveAuctionText'] = ""
    else:
        DataRecord['itemActiveAuctionFlag'] = "No"
        DataRecord['itemActiveAuctionText'] = ItemActiveAuctionFlag
    DataRecord['itemAuctionFlag'] = itemAuctionFlag
    DataRecord['itemBuyNowFlag'] = itemBuyNowFlag
    DataRecord['itemMakeOfferFlag'] = itemMakeOfferFlag
    DataRecord['itemReserveFlag'] = itemReserveFlag
    DataRecord['itemOnSaleFlag'] = itemOnSaleFlag
    print DataRecord
    DataRecord['auctionNumber'] = ItemNumber
    DataRecord['PriceTagPath'] = '2'
    scraperwiki.sqlite.save(["auctionNumber", "PriceTagPath"], DataRecord, table_name="DataRecord")

    DataRecord = {}
    PriceClass = []
    PriceText = []
    DataRecord['AttribCount'] = len(root.xpath(itemPriceTag3))
    for node in root.xpath(itemPriceTag3):
        PriceClass.append(node.xpath("@id"))
        PriceText.append(node.text_content())
    DataRecord['PriceClass'] = PriceClass
    DataRecord['PriceText'] = PriceText
    if ItemActiveAuctionFlag == "Active":
        DataRecord['itemActiveAuctionFlag'] = "Yes"
        DataRecord['itemActiveAuctionText'] = ""
    else:
        DataRecord['itemActiveAuctionFlag'] = "No"
        DataRecord['itemActiveAuctionText'] = ItemActiveAuctionFlag
    DataRecord['itemAuctionFlag'] = itemAuctionFlag
    DataRecord['itemBuyNowFlag'] = itemBuyNowFlag
    DataRecord['itemMakeOfferFlag'] = itemMakeOfferFlag
    DataRecord['itemReserveFlag'] = itemReserveFlag
    DataRecord['itemOnSaleFlag'] = itemOnSaleFlag
    print DataRecord
    DataRecord['auctionNumber'] = ItemNumber
    DataRecord['PriceTagPath'] = '3'
    scraperwiki.sqlite.save(["auctionNumber", "PriceTagPath"], DataRecord, table_name="DataRecord")


    if not (itemAuctionFlag or itemBuyNowFlag):   # Seems to be rare case where a listing has ended and we can't determine what kind of listing it was
        ItemEndPrice = None
        print "Unable to determine listing type: ", url

###  Price selection End


#    print ItemTitle
#    print ItemTitle2
#    print ItemDescriptionHTML
#    print ItemDescriptionText
#    print Seller
#    print SellerFeedback
#    print SellerFeedbackPercentage
#    print ItemNumber
#    print SellerLocation
#    print SellerSellsToLocation
#    print ItemCondition
#    print ItemAuctionEndDate
#    print ItemAuctionEndTime
#    print ItemNumberOfBids
#    print ItemEndPrice

    updatedInfo = {}
    updatedInfo['itemNumber'] = ItemNumber
    updatedInfo['itemNumberOfBids'] = ItemNumberOfBids
    updatedInfo['itemEndPrice'] = ItemEndPrice
    if ItemActiveAuctionFlag == "Active":
        updatedInfo['itemActiveAuctionFlag'] = "Yes"
        updatedInfo['itemActiveAuctionText'] = ""
    else:
        updatedInfo['itemActiveAuctionFlag'] = "No"
        updatedInfo['itemActiveAuctionText'] = ItemActiveAuctionFlag
    updatedNumberOfPictures = len(ItemPictureSmall)
    updatedNumberOfAttributes = len(key)
    print updatedInfo
#    print currentAuctionInfo
#    print updatedInfo == currentAuctionInfo
#    print updatedNumberOfPictures, currentNumberOfPictures, updatedNumberOfPictures == currentNumberOfPictures
#    print updatedNumberOfAttributes, currentNumberOfAttributes, updatedNumberOfAttributes == currentNumberOfAttributes


##### Change if test to second one if want to update every row ####
#    if updatedInfo != currentAuctionInfo or updatedNumberOfPictures != currentNumberOfPictures or updatedNumberOfAttributes != currentNumberOfAttributes :
    if 1 == 1 :
        print "Update the tables"
        UpdateFlag = "Yes"


## Save to Tables starts here



    return str(root.xpath(itemPriceTag + '/@id')[0]), UpdateFlag
    #return ItemActiveAuctionFlag, UpdateFlag




##Main start here

###First Time Only
#CreateTables()
###End First Time Only


UpdateRunStats([],0,0,"Begin Run")

random.seed()

#First, create a list of active items from the auction table
activeList = BuildActiveList()

#Next, append to the active list, the items from the test6 "newTable"
activeList = AddNewItems(activeList)
#activeList = activeList[60:]

#Then, scrape all of these items
#As we scrape, if the auction has not finished yet, add it to a new "stillActive" list
#Maybe a TODO is if the auction ended with no bids, add it to a "check again" list to see if it's been relisted
stillActiveList = []
completedItemList = []
UpdatedAuctionCount = 0
NotUpdatedAuctionCount = 0
PriceIDList = []
for item in activeList :
    ActiveCode, UpdateFlag = ScrapeAuction(item)
    print "AC: ", ActiveCode
    PriceIDList.append(ActiveCode)
    if UpdateFlag == "Yes" :
        UpdatedAuctionCount += 1
    else:
        NotUpdatedAuctionCount += 1
    if ActiveCode == "Active":
        stillActiveList.append(item)
    print "Updated Auctions: ", UpdatedAuctionCount, "Not Updated Auctions: ", NotUpdatedAuctionCount, PriceIDList
    completedItemList.append(item)
    UpdateRunStats(completedItemList, UpdatedAuctionCount, NotUpdatedAuctionCount, "Run In Progress")
    n = random.random() * 10 + 3
    print "Sleep for seconds: " + str(n)
    time.sleep(n)


print len(stillActiveList), "still active of ", len(activeList), "originally active"

#After scraping is finished, truncate the "activeTable"
#scraperwiki.sqlite.execute("delete from activeTable")
#scraperwiki.sqlite.commit()


#Then add the "stillActive" list to the "activeTable"
activeData = {}
print stillActiveList
for item in stillActiveList :
    activeData["auctionNumber"] = item
    activeData["currentTimeStamp"] = CurrentTimeStamp
    scraperwiki.sqlite.save(["auctionNumber"], activeData, table_name = "activeTable")


UpdateRunStats(completedItemList, UpdatedAuctionCount, NotUpdatedAuctionCount, "Run Finished")



# End Program
