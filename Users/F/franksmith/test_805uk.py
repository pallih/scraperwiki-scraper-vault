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
    sellerData['timestamp'] = CurrentTimeStamp
    sellerData['source'] = None
    scraperwiki.sqlite.save(["seller"], sellerData, table_name="seller")


    auctionData = {}
    auctionData['itemNumber'] = "delete this row"
    scraperwiki.sqlite.save(["itemNumber"], auctionData, table_name="auction")


#    auctionData = {}
#    auctionData['auctionNumber'] = "delete this row"
#    auctionData['auctionStatusCode'] = None
#    scraperwiki.sqlite.save(["auctionNumber"], auctionData, table_name="auctionStatus")


    return


def UpdateRunStats(inItemsUpdatedQty, inItemsNotUpdatedQty, inRunStatus):
    runStatsData = {}
    runStatsData["RunStatus"] = inRunStatus
    runStatsData["RunTime"] = CurrentTimeStamp
    runStatsData["ItemsUpdatedQty"] = inItemsUpdatedQty
    runStatsData["ItemsNotUpdatedQty"] = inItemsNotUpdatedQty
    scraperwiki.sqlite.save(["RunTime"], runStatsData, table_name = "RunStats")

    return

def BuildActiveList():
    #Build the active List from all the items in the auction table that haven't ended
    activeList = []
    activeDict = {}
    existingList = []
    existingDict = {}
    scraperwiki.sqlite.attach("test7uk")
    activeDict = scraperwiki.sqlite.select("auctionNumber from test7uk.newTable")
    print activeDict
    for item in activeDict :
        activeList.append(item["auctionNumber"])

    existingDict = scraperwiki.sqlite.select("itemNumber from auction")
    for item in existingDict :
        existingList.append(item["itemNumber"])
    for itemIndex in range(len(activeList)-1, -1, -1) :
        if activeList[itemIndex] in existingList :
            del activeList[itemIndex]
    #random.shuffle(activeList)
    print activeList
    print "Length: ", len(activeList)

    return activeList

def saveError(inItemNumber,inErrorMessage):
    data = {}
    data['itemNumber'] = inItemNumber
    data['errorMessage'] = inErrorMessage
    data['timestamp'] = CurrentTimeStamp
    scraperwiki.sqlite.save(["itemNumber"], data, table_name="errors")

    return


def WriteData():
    print "Writing %s records", addedCounter
    scraperwiki.sqlite.save(["seller"], sellerList, table_name="seller", verbose = 0)
    scraperwiki.sqlite.save(["itemNumber"], auctionList, table_name="auction", verbose = 0)
    scraperwiki.sqlite.save(["itemNumber", "attributeKey"], auctionAttributesList, table_name="auctionAttributes", verbose = 0)
    scraperwiki.sqlite.save(["itemNumber", "itemPictureKey"], auctionPicturesList, table_name="auctionPictures", verbose = 0)
    scraperwiki.sqlite.save(["itemNumber", "categoryNumber"], auctionCategoriesList, table_name="auctionCategories", verbose = 0)
    scraperwiki.sqlite.save(["categoryNumber"], CategoryList, table_name="Category", verbose = 0)
    print "All records written"

    return


def ScrapeAuction(inItemNumber, addedCounter):

    global sellerList
    global auctionList
    global auctionAttributesList
    global auctionPicturesList
    global auctionCategoriesList
    global CategoryList

    print inItemNumber, addedCounter




### Current auction tags
    titleTag = 'h1'
    itemPageNotRespondingTag = "//*/text() = 'Page Not Responding'"
    itemAuctionEndedTag = "//*/text() = 'Bidding has ended on this item.'"
    itemEbayMotorsTag = "//meta[contains(@content, 'ebaymotors')]"
    itemAuction1Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Bid history:'"
    itemAuction2Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Current bid:'"
    itemAuction3Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Starting bid:'"
    itemAuction4Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Winning bid:'"
    itemBuyNow1Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Buy It Now'"
    itemBuyNow2Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Sold For:'"
    itemBuyNow3Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Price:'"  #use this for Buy Now that has ended without being sold
    itemMakeOfferTag = "//div[contains(@class, 'u-flL lable')]/text() = 'Best Offer:'"
#    itemAuction1Tag = "//table[id='vi-tTbl']//*/text() = 'Bid history:'"
#    itemAuction2Tag = "//table[id='vi-tTbl']//*/text() = 'Current bid:'"
#    itemAuction3Tag = "//table[id='vi-tTbl']//*/text() = 'Starting bid:'"
#    itemAuction4Tag = "//table[id='vi-tTbl']//*/text() = 'Winning bid:'"
#    itemBuyNow1Tag = "//table[id='vi-tTbl']//*/text() = 'Buy It Now'"
#    itemBuyNow2Tag = "//table[id='vi-tTbl']//*/text() = 'Sold For:'"
#    itemBuyNow3Tag = "//table[id='vi-tTbl']//*/text() = 'Price:'"  #use this for Buy Now that has ended without being sold
#    itemMakeOfferTag = "//table[id='vi-tTbl']//*/text() = 'Best Offer:'"
#    itemSaleTag = "//span[contains(@class, 'vi-is1-prcsl')]"  #if this exists, the buy now item is on sale
    itemEnded1Tag = "//div[contains(@class, 'msgPad')]//*"
#    itemEnded1Tag = "//span[@id='v4-1-msg']"
    itemEnded2Tag = "//div[contains(@class, 'u-flL lable')]//*/text() = 'Ended:'"
#    itemEnded2Tag = "//table[id='vi-tTbl']//*/text() = 'Ended:'"
    itemBidGroupTag = "//a[contains(@href, 'ViewBids')]"
    itemConditionTag = "//div[contains(@class,'condText')]"
    itemConditionTag1 = "//span[@class='vi-is1-condText']"
    itemDateGroupTag = "//span[@class='vi-tm-left']//*"
#    itemDateGroupTag = "//span[@class='vi-is1-dt']//*"
    removedAuctionTag = '//div[@class="vimsg"]//div[@class="sm-imc sml-imc"]'
    descriptionTag = '//div[@id="desc_div"]//*'


    categoryBreadCrumbGroupTag = "//td[@id='vi-VR-brumb-lnkLst']//li/a"
#    categoryBreadCrumbGroupTag = '//div[@class="bbc-in bbc bbc-nav"]//ul/li/a'
    itemTitle2Tag = '//h2[@class="vi-is1-titleH2"]'  
    sellerTag = "//div[contains(@class,'si-content')]//span[@class='mbg-nw']"
    sellerFeedbackTag = "//div[contains(@class,'si-content')]//span[@class='mbg-l']//*"
    sellerFeedbackPercentageTag = "//div[contains(@id,'si-fb')]"
#    sellerFeedbackTag = "//table[contains(@class,'s-content')]//a[@class='mbg-fb']//*"
#    sellerFeedbackPercentageTag = "//table[contains(@class,'s-content')]//span[@class='s-gray z_a']"
    itemNumberTag = "//table[@class='sp1']/tr/td[2]"
    sellerLocationTag = "//div[@id='itemLocation']//text()"
    sellerSellsToLocationTag = "//div[@id='shipsTo']//text()"
#    sellerLocationTag = "//table[@class='sp1']/tr[2]/td[2]"
#    sellerSellsToLocationTag = "//table[@class='sp1']/tr[3]/td[2]"
    itemAttributeGroupTag = "//div[@class='itemAttr']//table/tr/child::*"
#    itemAttributeGroupTag = "//table[@class='vi-ia-attrGroup']//table/tr//*"
    itemConditionTag2 = "//td[@class='vi-is1-clr'][1]"
    itemNumberOfBidsTag = "following-sibling::td//text()"  #Number of bids is the first text of td following the "Bid History" text
    itemBidHistoryTag = "//th[@class='vi-is1-lbl']"
    itemActiveAuctionTag = "//span[@id='v4-1-msg']"
#    itemPriceTag = "//span[contains(@itemprop, 'price')]"  #if there are two of these, it could be an "auction
    itemPriceTag = "//div[contains(@class, 'vi-price')]//*"  #if there are two of these, it could be an "auction
    itemOrgPriceTag = "//span[contains(@id, 'saleOrgPrc')]"  
    itemDscPriceTag = "//span[contains(@id, 'saleDscPrc')]"  
#    itemPriceTag = "//span[contains(@class, 'vi-is1-prcp')]"  #if there are two of these, it could be an "auction
                                                              #or Buy Now" or it could be a Buy Now that is on sale

    itemReserveTag = "//a[@class='vi-is1-rsv']"   
#    itemBuyNowTag = "//a[@id='but_v4-4'] | //a[@id='but_v4-5']"         #Only for active buy now -- found but_v4-5 id on Buy Now on Sale with Make Offer
#    itemMakeOfferTag = "//a[@id='but_v4-2'] | //a[@id='but_v4-3']"      #Only for active make offer-- found but_v4-3 id on Buy Now on Sale with Make Offer
    itemPlaceBidTag = "//input[@id='but_v4-6']"   #Only for active auctions
    itemCompleteTag = "//table[@class='vi-ia-attrGroup']"
    itemPictureGroupTag = "//div[@id='imgC']//img[@src]"
#    itemPictureGroupTag = "//div[@class='vi-ipic1']//img[@src]"

    if addedCounter == 0 :
        sellerList = []
        auctionList = []
        auctionAttributesList = []
        auctionPicturesList = []
        auctionCategoriesList = []
        CategoryList = []

    url = 'http://www.ebay.com/itm/' + inItemNumber
    invalidread = 1
    invalidreadcount = 1
    while invalidread and invalidreadcount < 5 :
        print "Reading auctionsearch URL:", url, "  Attempt # ", invalidreadcount
        try:
            html = urllib.urlopen(url).read()
#            print html
            root = lxml.html.fromstring(html)
            invalidread = 0
        except:
            print "*********ERROR on reading URL*************"
            print url
            print "*********End of Error Report************"
            invalidread = 1
            invalidreadcount += 1

#    try:
#        html = urllib.urlopen(url).read()
#    except:
#        print "*********ERROR on reading URL*************"
#        print url
#        print "*********End of Error Report************"
    print html

#    root = lxml.html.fromstring(html)

###  Completed/Ended section Begin

### Check if valid page
    if root.xpath(itemPageNotRespondingTag) :
        return "No"

### Check if ebay motors
    if root.xpath(itemEbayMotorsTag) :
        return "No"

### Check first if it's removed, not available or ended
    try:
        removedAuctionText = root.xpath(removedAuctionTag)[0].text_content()
        if "has been removed" in removedAuctionText :
            return "No"
        notAvailableText = root.xpath(removedAuctionTag)[0].text_content()
        if "not available" in notAvailableText :
            return "No"
        if root.xpath(itemAuctionEndedTag) :
            return "No"
    except:
        removedAuctionText = None

###  Completed/Ended or Active Auction selection End

# check if auction:
    if root.xpath(itemAuction1Tag) | root.xpath(itemAuction2Tag) | root.xpath(itemAuction3Tag) | root.xpath(itemAuction4Tag) :
        ItemAuctionFlag = True
    else:
        ItemAuctionFlag = False
#    print "ItemAuctionFlag: ", ItemAuctionFlag

# check if Buy It Now:
    #print "test: ", itemBuyNow3Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Price:'" 
    #print "test: ", root.xpath(itemBuyNow3Tag)
    if root.xpath(itemBuyNow1Tag) | root.xpath(itemBuyNow2Tag):
        ItemBuyNowFlag = True
    elif root.xpath(itemBuyNow3Tag):
        ItemBuyNowFlag = True
    else:
        ItemBuyNowFlag = False
#    print "ItemBuyNowFlag: ", ItemBuyNowFlag

# check if On Sale:
    if len(root.xpath(itemDscPriceTag)) == 0 :
        ItemSaleFlag = True
    else:
        ItemSaleFlag = False
#    print "ItemSaleFlag: ", ItemSaleFlag

# check if MakeOffer:
    if root.xpath(itemMakeOfferTag):
        ItemMakeOfferFlag = True
    else:
        ItemMakeOfferFlag = False
#    print "ItemMakeOfferFlag: ", ItemMakeOfferFlag

# check if Item has ended (sale or auction):
    ItemEndedFlag = "False"
    ItemEnded1Flag = "False"
    ItemEndedText = None
    if len(root.xpath(itemEnded1Tag)) > 0 :
        if len(root.xpath(itemEnded1Tag)[0].text_content()) > 0 :
            ItemEnded1Flag = True
            ItemEndedText = root.xpath(itemEnded1Tag)[0].text_content()
        else:
            ItemEnded1Flag = False
            ItemEndedText = None
    if root.xpath(itemEnded2Tag):
        ItemEndedFlag = True
    else:
        ItemEndedFlag = False
#    print "ItemEndedFlag: ", ItemEndedFlag, ItemEnded1Flag, ItemEndedText
    if ItemEndedFlag or ItemEnded1Flag :
        return "No"
    else:
        InsertFlag = "Yes"

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
#            print "Category Title: ", tempTitle
            CategoryTitle.append(tempTitle)
            CategoryNumber.append(tempSplitHrefArray[5])
            CategoryParentNumber.append(tempCategoryParentNumber)
            tempCategoryParentNumber = tempSplitHrefArray[5]
###  Category selection End


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
#          print "picture: ", tempSrc
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
    ItemNumber = inItemNumber

    ItemTitle = root.cssselect(titleTag)[0].text_content()

    tempItemTitle2 = root.xpath(itemTitle2Tag)
    ItemTitle2 = ""
    if len(tempItemTitle2) != 0:
        ItemTitle2 = tempItemTitle2[0].text

    try:
        ItemDescriptionHTML = tostring(root.xpath(descriptionTag)[0]) 
        if len(ItemDescriptionHTML) > 32000 :
            ItemDescriptionHTML = ItemDescriptionHTML[:32000]

        ItemDescriptionText = root.xpath(descriptionTag)[0].text_content()
        if len(ItemDescriptionText) > 32000 :
            ItemDescriptionText = ItemDescriptionText[:32000]
    except:
        ItemDescriptionText = "unknown"

    try:
#        print "seller:", root.xpath(sellerTag)
        Seller = root.xpath(sellerTag)[0].text
    except:
        Seller = "unknown"

    try:
#        print "SellerFeedback :", root.xpath(sellerFeedbackTag)
        SellerFeedback = root.xpath(sellerFeedbackTag)[0].text
    except:
        SellerFeedback = "unknown"

    try:     # sometimes there is no percentage number
#        print "SellerFeedbackPercentage: ", root.xpath(sellerFeedbackPercentageTag)
        SellerFeedbackPercentage = root.xpath(sellerFeedbackPercentageTag)[0].text
        SellerFeedbackPercentage = SellerFeedbackPercentage.split()[0]    # Keeps only the percentage number
    except:
        SellerFeedbackPercentage = "unknown"

    try:
#        print "sellerLocation = ", root.xpath(sellerLocationTag)
        SellerLocation = root.xpath(sellerLocationTag)[5]
#        print "SellerSellsToLocation =", root.xpath(sellerSellsToLocationTag)
        SellerSellsToLocation = root.xpath(sellerSellsToLocationTag)[6]
    except:
        SellerLocation = "unknown"
        SellerSellsToLocation = "unknown"
### Title, Description, and Seller selection End


### Attribute Group selection Begin
    ItemAttributeGroup = root.xpath(itemAttributeGroupTag)
    key = []
    value = []
    i = -1
    firstFlag = True
#    print "Number of Attributes: ", len(ItemAttributeGroup)
    if len(ItemAttributeGroup) & 1 :    #if it's an odd number then there's an extra html tag we don't need
        del ItemAttributeGroup[-1]
#    print "Number of Attributes: ", len(ItemAttributeGroup)
    for element in ItemAttributeGroup:
        if firstFlag and len(element.text) > 0 :
            i += 1
            key.append(element.text)
            firstFlag = False
#            print "Attribute: ", element.text
        elif not(firstFlag) and len(element.text_content()) > 0 :
            value.append(element.text_content())
            firstFlag = True
#            print "Attribute Value: ", element.text_content()

#    firstTdAfterTh = False
#    for element in ItemAttributeGroup:
#        if element.tag == 'th':
#            i += 1
#            key.append(element.text)
#            firstTdAfterTh = True
#            print "Attribute: ", element.text
#        if element.tag == 'td' and firstTdAfterTh:
#            value.append(element.text_content())
#            firstTdAfterTh = False
#            print "Attribute Value: ", element.text_content()
### Attribute Group selection End


###  Condition and Date selection Begin
    try:
        ItemCondition = root.xpath(itemConditionTag)[0].text
    except:
        print "#########################################"
        print "itemConditionTag = ", itemConditionTag
        print root.xpath(itemConditionTag)
#        print stophere
        saveError(ItemNumber,"Fail on line 380, ItemCondition not found")
        return "No"

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

# if it's an auction, find number of bids and price
    ItemNumberOfBids = None
    if ItemAuctionFlag:
        ItemBidGroup = root.xpath(itemBidGroupTag)
#        print ItemBidGroup
        if len(ItemBidGroup) == 0 :
            ItemNumberOfBids = "unknown"
            ItemEndPrice = root.xpath(itemPriceTag)[0].text_content()
        else:
            ItemNumberOfBids = ItemBidGroup[0].text_content().split()[0]
            ItemEndPrice = root.xpath(itemPriceTag)[0].text_content()
#        print "Number of Bids", ItemNumberOfBids

###  Reserve or not
    itemReserveFlag = False

    try:
        ItemReserveText = root.xpath(itemReserveTag)[0].text_content()
        itemReserveFlag = True
    except:
        ItemReserveText = None

###  Buy Now or not
    ItemBuyNowPrice = None
    ItemOriginalBuyNowPrice = None
    if len(root.xpath(itemDscPriceTag)) == 0 :
        if ItemAuctionFlag and ItemBuyNowFlag :
            ItemBuyNowPrice = root.xpath(itemPriceTag)[1].text_content()
            ItemEndPrice = ItemBuyNowPrice
        elif ItemBuyNowFlag :
            ItemBuyNowPrice = root.xpath(itemPriceTag)[0].text_content()
            ItemEndPrice = ItemBuyNowPrice
    else :
        ItemBuyNowPrice = root.xpath(itemDscPriceTag)[0].text
        ItemOriginalBuyNowPrice = root.xpath(itemOrgPriceTag)[0].text
#        print "On Sale, Buy Now Price:", ItemBuyNowPrice
#        print "On Sale, Original Buy Now Price:", ItemOriginalBuyNowPrice
        ItemEndPrice = ItemBuyNowPrice

### See if we can determine what the Start Price is
# If we don't have the item number already in the database *AND* the number of bids is either 0 or 1,
#    then set the start price to the "end" price we already captured.
# If we do have the item number in the database *AND* there isn't a start price already stored *AND*
#    the number of bids is either 0 or 1, then set the start price to the "end" price we already captured.
# If we do have the item number in the database *AND* there already is a start price stored, then keep the
#    start price the same as what it is.
# If none of the above are true, set the start price to None.  (We could go to a lot of work to find out
#    what the actual start price is in these cases, but I don't want to do that work yet)

    msg = "Unable to determine"
    tempItemStartPrice = None
    if ItemAuctionFlag :
        try:
            # If already scraped this one before, then this captures the existing start price
            tempItemStartPrice = scraperwiki.sqlite.select("itemStartPrice from auction where itemNumber = ?", ItemNumber)[0]["itemStartPrice"][0]["itemStartPrice"]
            msg = "Already stored auction.  Start price depends whether we already have start price or on number of bids"
        except:
            #if the "try" fails, then this is the first time we've seen this one.  Set the start price to None and see if the number of bids < 2
            msg = "First time auction.  Start price depends on number of bids"
            tempItemStartPrice = None
#$        if tempItemStartPrice == None :
            if int(ItemNumberOfBids) < 2:            #Might need to change this to include Make Offer sales that have completed and were different from start
                msg = "Start Price determined from this scrape"
                tempItemStartPrice = ItemEndPrice
            else:
                msg = "Unable to determine start price -- too many bids already"
                tempItemStartPrice = None

    ItemStartPrice = tempItemStartPrice
#    print ItemStartPrice, msg

    if not (ItemAuctionFlag or ItemBuyNowFlag):   # Seems to be rare case where a listing has ended and we can't determine what kind of listing it was
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

## Save to Tables starts here

    if not ItemEndedFlag :
        addedCounter += 1

        sellerData = {}
        sellerData['seller'] = Seller
        sellerData['sellerLocation'] = SellerLocation
        sellerData['sellerSellsToLocation'] = SellerSellsToLocation
        sellerData['sellerFeedback'] = SellerFeedback
        sellerData['sellerFeedbackPercentage'] = SellerFeedbackPercentage
        sellerData['timestamp'] = CurrentTimeStamp
        sellerData['source'] = url
        sellerList.append(sellerData)

#        scraperwiki.sqlite.save(["seller"], sellerData, table_name="seller")


        auctionData = {}
        auctionData['itemNumber'] = ItemNumber
        auctionData['sellerFeedbackPercentage'] = SellerFeedbackPercentage
        auctionData['sellerFeedback'] = SellerFeedback
        auctionData['sellerSellsToLocation'] = SellerSellsToLocation
        auctionData['sellerLocation'] = SellerLocation
        auctionData['seller'] = Seller
        auctionData['itemTitle'] = ItemTitle
        auctionData['itemTitle2'] = ItemTitle2
        auctionData['itemDescriptionHTML'] = ItemDescriptionHTML
        auctionData['itemDescriptionText'] = ItemDescriptionText
        auctionData['itemCondition'] = ItemCondition
        auctionData['itemAuctionEndDate'] = ItemAuctionEndDate
        auctionData['itemAuctionEndTime'] = ItemAuctionEndTime
        auctionData['itemNumberOfBids'] = ItemNumberOfBids
        auctionData['itemStartPrice'] = ItemStartPrice
        auctionData['itemEndPrice'] = ItemEndPrice
        auctionData['itemBuyNowPrice'] = ItemBuyNowPrice
        auctionData['itemOriginalBuyNowPrice'] = ItemOriginalBuyNowPrice
        auctionData['itemAuctionFlag'] = ItemAuctionFlag
        auctionData['itemBuyNowFlag'] = ItemBuyNowFlag
        auctionData['itemMakeOfferFlag'] = ItemMakeOfferFlag
        auctionData['itemReserveFlag'] = itemReserveFlag
        auctionData['itemOnSaleFlag'] = ItemSaleFlag
        auctionData['timestamp'] = CurrentTimeStamp
        auctionData['source'] = url
        auctionList.append(auctionData)

#        scraperwiki.sqlite.save(["itemNumber"], auctionData, table_name="auction")

        auctionAttributesData = {}
        for listIndex, listItem in enumerate(key):
            auctionAttributesData['itemNumber'] = ItemNumber
            auctionAttributesData['attributeKey'] = key[listIndex]
            auctionAttributesData['attributeValue'] = value[listIndex]
            auctionAttributesData['timestamp'] = CurrentTimeStamp
            auctionAttributesData['source'] = url
            auctionAttributesList.append(auctionAttributesData.copy())

#            scraperwiki.sqlite.save(["itemNumber", "attributeKey"], auctionAttributesData, table_name="auctionAttributes")

        auctionPicturesData = {}
        for listIndex, listItem in enumerate(ItemPictureSmall):
            auctionPicturesData['itemNumber'] = ItemNumber
            auctionPicturesData['itemPictureKey'] = listIndex + 1
            auctionPicturesData['itemPictureSmall'] = ItemPictureSmall[listIndex]
            auctionPicturesData['itemPictureLarge'] = ItemPictureLarge[listIndex]
            auctionPicturesData['itemPicture_1'] = ItemPicture_1[listIndex]
            auctionPicturesData['itemPicture_12'] = ItemPicture_12[listIndex]
            auctionPicturesData['timestamp'] = CurrentTimeStamp
            auctionPicturesData['source'] = url
#            print listIndex, listItem, "Picture Data: ", auctionPicturesData
            auctionPicturesList.append(auctionPicturesData.copy())
#            print listIndex, listItem, "Picture List: ", auctionPicturesList

#            scraperwiki.sqlite.save(["itemNumber", "itemPictureKey"], auctionPicturesData, table_name="auctionPictures")

        auctionCategoriesData = {}
        for listIndex, listItem in enumerate(CategoryTitle):
            auctionCategoriesData['itemNumber'] = ItemNumber
            auctionCategoriesData['categoryNumber'] = CategoryNumber[listIndex]
            auctionCategoriesData['categoryTitle'] = CategoryTitle[listIndex]
            auctionCategoriesData['categoryParentNumber'] = CategoryParentNumber[listIndex]
            auctionCategoriesData['timestamp'] = CurrentTimeStamp
            auctionCategoriesData['source'] = url
            auctionCategoriesList.append(auctionCategoriesData.copy())

#            scraperwiki.sqlite.save(["itemNumber", "categoryNumber"], auctionCategoriesData, table_name="auctionCategories")

        CategoryData = {}
        for listIndex, listItem in enumerate(CategoryTitle):
            CategoryData['categoryNumber'] = CategoryNumber[listIndex]
            CategoryData['categoryTitle'] = CategoryTitle[listIndex]
            CategoryData['categoryParentNumber'] = CategoryParentNumber[listIndex]
            CategoryData['timestamp'] = CurrentTimeStamp
            CategoryData['source'] = url
#            print listIndex, listItem, "Category Data :", CategoryData
            CategoryList.append(CategoryData.copy())
#            print listIndex, listItem, "Category List :", CategoryList

#            scraperwiki.sqlite.save(["categoryNumber"], CategoryData, table_name="Category")

    else:
        print "Not inserting tables"
        InsertFlag = "No"


    return InsertFlag




##Main start here

###First Time Only
CreateTables()
###End First Time Only


UpdateRunStats(0,0,"Begin Run")

random.seed()

#First, create a list of active items from the auction table
activeList = BuildActiveList()

#Next, append to the active list, the items from the test6 "newTable"
#$activeList = AddNewItems(activeList)
#activeList = activeList[60:]

#activeList = ["200436498703"]
#activeList = activeList[:10]


#Then, scrape all of these items
#As we scrape, if the auction has not finished yet, add it to a new "stillActive" list
#Maybe a TODO is if the auction ended with no bids, add it to a "check again" list to see if it's been relisted
stillActiveList = []
completedItemList = []
InsertedAuctionCount = 0
NotInsertedAuctionCount = 0
addedCounter = 0
sellerList = []
auctionList = []
auctionAttributesList = []
auctionPicturesList = []
auctionCategoriesList = []
CategoryList = []

for item in activeList :
    InsertFlag = ScrapeAuction(item, addedCounter)
    if InsertFlag == "Yes" :
        InsertedAuctionCount += 1
        addedCounter += 1
    else:
        NotInsertedAuctionCount += 1
    print "Inserted Auctions: ", InsertedAuctionCount, "Not Inserted Auctions: ", NotInsertedAuctionCount
#    completedItemList.append(item)
    if addedCounter > 50 :
        WriteData()
        addedCounter = 0
        UpdateRunStats(InsertedAuctionCount, NotInsertedAuctionCount, "Run In Progress")
    n = random.random() * 2 + 2
    print "Sleep for seconds: " + str(n)
    time.sleep(n)

#Do final write to get anything left
WriteData()

#$print len(stillActiveList), "still active of ", len(activeList), "originally active"

#After scraping is finished, truncate the "activeTable"
#scraperwiki.sqlite.execute("delete from activeTable")
#scraperwiki.sqlite.commit()


#Then add the "stillActive" list to the "activeTable"
#$activeData = {}
#$print stillActiveList
#$for item in stillActiveList :
#$    activeData["auctionNumber"] = item
#$    activeData["currentTimeStamp"] = CurrentTimeStamp
#$    scraperwiki.sqlite.save(["auctionNumber"], activeData, table_name = "activeTable")


UpdateRunStats(InsertedAuctionCount, NotInsertedAuctionCount, "Run Finished")



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
    sellerData['timestamp'] = CurrentTimeStamp
    sellerData['source'] = None
    scraperwiki.sqlite.save(["seller"], sellerData, table_name="seller")


    auctionData = {}
    auctionData['itemNumber'] = "delete this row"
    scraperwiki.sqlite.save(["itemNumber"], auctionData, table_name="auction")


#    auctionData = {}
#    auctionData['auctionNumber'] = "delete this row"
#    auctionData['auctionStatusCode'] = None
#    scraperwiki.sqlite.save(["auctionNumber"], auctionData, table_name="auctionStatus")


    return


def UpdateRunStats(inItemsUpdatedQty, inItemsNotUpdatedQty, inRunStatus):
    runStatsData = {}
    runStatsData["RunStatus"] = inRunStatus
    runStatsData["RunTime"] = CurrentTimeStamp
    runStatsData["ItemsUpdatedQty"] = inItemsUpdatedQty
    runStatsData["ItemsNotUpdatedQty"] = inItemsNotUpdatedQty
    scraperwiki.sqlite.save(["RunTime"], runStatsData, table_name = "RunStats")

    return

def BuildActiveList():
    #Build the active List from all the items in the auction table that haven't ended
    activeList = []
    activeDict = {}
    existingList = []
    existingDict = {}
    scraperwiki.sqlite.attach("test7uk")
    activeDict = scraperwiki.sqlite.select("auctionNumber from test7uk.newTable")
    print activeDict
    for item in activeDict :
        activeList.append(item["auctionNumber"])

    existingDict = scraperwiki.sqlite.select("itemNumber from auction")
    for item in existingDict :
        existingList.append(item["itemNumber"])
    for itemIndex in range(len(activeList)-1, -1, -1) :
        if activeList[itemIndex] in existingList :
            del activeList[itemIndex]
    #random.shuffle(activeList)
    print activeList
    print "Length: ", len(activeList)

    return activeList

def saveError(inItemNumber,inErrorMessage):
    data = {}
    data['itemNumber'] = inItemNumber
    data['errorMessage'] = inErrorMessage
    data['timestamp'] = CurrentTimeStamp
    scraperwiki.sqlite.save(["itemNumber"], data, table_name="errors")

    return


def WriteData():
    print "Writing %s records", addedCounter
    scraperwiki.sqlite.save(["seller"], sellerList, table_name="seller", verbose = 0)
    scraperwiki.sqlite.save(["itemNumber"], auctionList, table_name="auction", verbose = 0)
    scraperwiki.sqlite.save(["itemNumber", "attributeKey"], auctionAttributesList, table_name="auctionAttributes", verbose = 0)
    scraperwiki.sqlite.save(["itemNumber", "itemPictureKey"], auctionPicturesList, table_name="auctionPictures", verbose = 0)
    scraperwiki.sqlite.save(["itemNumber", "categoryNumber"], auctionCategoriesList, table_name="auctionCategories", verbose = 0)
    scraperwiki.sqlite.save(["categoryNumber"], CategoryList, table_name="Category", verbose = 0)
    print "All records written"

    return


def ScrapeAuction(inItemNumber, addedCounter):

    global sellerList
    global auctionList
    global auctionAttributesList
    global auctionPicturesList
    global auctionCategoriesList
    global CategoryList

    print inItemNumber, addedCounter




### Current auction tags
    titleTag = 'h1'
    itemPageNotRespondingTag = "//*/text() = 'Page Not Responding'"
    itemAuctionEndedTag = "//*/text() = 'Bidding has ended on this item.'"
    itemEbayMotorsTag = "//meta[contains(@content, 'ebaymotors')]"
    itemAuction1Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Bid history:'"
    itemAuction2Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Current bid:'"
    itemAuction3Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Starting bid:'"
    itemAuction4Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Winning bid:'"
    itemBuyNow1Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Buy It Now'"
    itemBuyNow2Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Sold For:'"
    itemBuyNow3Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Price:'"  #use this for Buy Now that has ended without being sold
    itemMakeOfferTag = "//div[contains(@class, 'u-flL lable')]/text() = 'Best Offer:'"
#    itemAuction1Tag = "//table[id='vi-tTbl']//*/text() = 'Bid history:'"
#    itemAuction2Tag = "//table[id='vi-tTbl']//*/text() = 'Current bid:'"
#    itemAuction3Tag = "//table[id='vi-tTbl']//*/text() = 'Starting bid:'"
#    itemAuction4Tag = "//table[id='vi-tTbl']//*/text() = 'Winning bid:'"
#    itemBuyNow1Tag = "//table[id='vi-tTbl']//*/text() = 'Buy It Now'"
#    itemBuyNow2Tag = "//table[id='vi-tTbl']//*/text() = 'Sold For:'"
#    itemBuyNow3Tag = "//table[id='vi-tTbl']//*/text() = 'Price:'"  #use this for Buy Now that has ended without being sold
#    itemMakeOfferTag = "//table[id='vi-tTbl']//*/text() = 'Best Offer:'"
#    itemSaleTag = "//span[contains(@class, 'vi-is1-prcsl')]"  #if this exists, the buy now item is on sale
    itemEnded1Tag = "//div[contains(@class, 'msgPad')]//*"
#    itemEnded1Tag = "//span[@id='v4-1-msg']"
    itemEnded2Tag = "//div[contains(@class, 'u-flL lable')]//*/text() = 'Ended:'"
#    itemEnded2Tag = "//table[id='vi-tTbl']//*/text() = 'Ended:'"
    itemBidGroupTag = "//a[contains(@href, 'ViewBids')]"
    itemConditionTag = "//div[contains(@class,'condText')]"
    itemConditionTag1 = "//span[@class='vi-is1-condText']"
    itemDateGroupTag = "//span[@class='vi-tm-left']//*"
#    itemDateGroupTag = "//span[@class='vi-is1-dt']//*"
    removedAuctionTag = '//div[@class="vimsg"]//div[@class="sm-imc sml-imc"]'
    descriptionTag = '//div[@id="desc_div"]//*'


    categoryBreadCrumbGroupTag = "//td[@id='vi-VR-brumb-lnkLst']//li/a"
#    categoryBreadCrumbGroupTag = '//div[@class="bbc-in bbc bbc-nav"]//ul/li/a'
    itemTitle2Tag = '//h2[@class="vi-is1-titleH2"]'  
    sellerTag = "//div[contains(@class,'si-content')]//span[@class='mbg-nw']"
    sellerFeedbackTag = "//div[contains(@class,'si-content')]//span[@class='mbg-l']//*"
    sellerFeedbackPercentageTag = "//div[contains(@id,'si-fb')]"
#    sellerFeedbackTag = "//table[contains(@class,'s-content')]//a[@class='mbg-fb']//*"
#    sellerFeedbackPercentageTag = "//table[contains(@class,'s-content')]//span[@class='s-gray z_a']"
    itemNumberTag = "//table[@class='sp1']/tr/td[2]"
    sellerLocationTag = "//div[@id='itemLocation']//text()"
    sellerSellsToLocationTag = "//div[@id='shipsTo']//text()"
#    sellerLocationTag = "//table[@class='sp1']/tr[2]/td[2]"
#    sellerSellsToLocationTag = "//table[@class='sp1']/tr[3]/td[2]"
    itemAttributeGroupTag = "//div[@class='itemAttr']//table/tr/child::*"
#    itemAttributeGroupTag = "//table[@class='vi-ia-attrGroup']//table/tr//*"
    itemConditionTag2 = "//td[@class='vi-is1-clr'][1]"
    itemNumberOfBidsTag = "following-sibling::td//text()"  #Number of bids is the first text of td following the "Bid History" text
    itemBidHistoryTag = "//th[@class='vi-is1-lbl']"
    itemActiveAuctionTag = "//span[@id='v4-1-msg']"
#    itemPriceTag = "//span[contains(@itemprop, 'price')]"  #if there are two of these, it could be an "auction
    itemPriceTag = "//div[contains(@class, 'vi-price')]//*"  #if there are two of these, it could be an "auction
    itemOrgPriceTag = "//span[contains(@id, 'saleOrgPrc')]"  
    itemDscPriceTag = "//span[contains(@id, 'saleDscPrc')]"  
#    itemPriceTag = "//span[contains(@class, 'vi-is1-prcp')]"  #if there are two of these, it could be an "auction
                                                              #or Buy Now" or it could be a Buy Now that is on sale

    itemReserveTag = "//a[@class='vi-is1-rsv']"   
#    itemBuyNowTag = "//a[@id='but_v4-4'] | //a[@id='but_v4-5']"         #Only for active buy now -- found but_v4-5 id on Buy Now on Sale with Make Offer
#    itemMakeOfferTag = "//a[@id='but_v4-2'] | //a[@id='but_v4-3']"      #Only for active make offer-- found but_v4-3 id on Buy Now on Sale with Make Offer
    itemPlaceBidTag = "//input[@id='but_v4-6']"   #Only for active auctions
    itemCompleteTag = "//table[@class='vi-ia-attrGroup']"
    itemPictureGroupTag = "//div[@id='imgC']//img[@src]"
#    itemPictureGroupTag = "//div[@class='vi-ipic1']//img[@src]"

    if addedCounter == 0 :
        sellerList = []
        auctionList = []
        auctionAttributesList = []
        auctionPicturesList = []
        auctionCategoriesList = []
        CategoryList = []

    url = 'http://www.ebay.com/itm/' + inItemNumber
    invalidread = 1
    invalidreadcount = 1
    while invalidread and invalidreadcount < 5 :
        print "Reading auctionsearch URL:", url, "  Attempt # ", invalidreadcount
        try:
            html = urllib.urlopen(url).read()
#            print html
            root = lxml.html.fromstring(html)
            invalidread = 0
        except:
            print "*********ERROR on reading URL*************"
            print url
            print "*********End of Error Report************"
            invalidread = 1
            invalidreadcount += 1

#    try:
#        html = urllib.urlopen(url).read()
#    except:
#        print "*********ERROR on reading URL*************"
#        print url
#        print "*********End of Error Report************"
    print html

#    root = lxml.html.fromstring(html)

###  Completed/Ended section Begin

### Check if valid page
    if root.xpath(itemPageNotRespondingTag) :
        return "No"

### Check if ebay motors
    if root.xpath(itemEbayMotorsTag) :
        return "No"

### Check first if it's removed, not available or ended
    try:
        removedAuctionText = root.xpath(removedAuctionTag)[0].text_content()
        if "has been removed" in removedAuctionText :
            return "No"
        notAvailableText = root.xpath(removedAuctionTag)[0].text_content()
        if "not available" in notAvailableText :
            return "No"
        if root.xpath(itemAuctionEndedTag) :
            return "No"
    except:
        removedAuctionText = None

###  Completed/Ended or Active Auction selection End

# check if auction:
    if root.xpath(itemAuction1Tag) | root.xpath(itemAuction2Tag) | root.xpath(itemAuction3Tag) | root.xpath(itemAuction4Tag) :
        ItemAuctionFlag = True
    else:
        ItemAuctionFlag = False
#    print "ItemAuctionFlag: ", ItemAuctionFlag

# check if Buy It Now:
    #print "test: ", itemBuyNow3Tag = "//div[contains(@class, 'u-flL lable')]/text() = 'Price:'" 
    #print "test: ", root.xpath(itemBuyNow3Tag)
    if root.xpath(itemBuyNow1Tag) | root.xpath(itemBuyNow2Tag):
        ItemBuyNowFlag = True
    elif root.xpath(itemBuyNow3Tag):
        ItemBuyNowFlag = True
    else:
        ItemBuyNowFlag = False
#    print "ItemBuyNowFlag: ", ItemBuyNowFlag

# check if On Sale:
    if len(root.xpath(itemDscPriceTag)) == 0 :
        ItemSaleFlag = True
    else:
        ItemSaleFlag = False
#    print "ItemSaleFlag: ", ItemSaleFlag

# check if MakeOffer:
    if root.xpath(itemMakeOfferTag):
        ItemMakeOfferFlag = True
    else:
        ItemMakeOfferFlag = False
#    print "ItemMakeOfferFlag: ", ItemMakeOfferFlag

# check if Item has ended (sale or auction):
    ItemEndedFlag = "False"
    ItemEnded1Flag = "False"
    ItemEndedText = None
    if len(root.xpath(itemEnded1Tag)) > 0 :
        if len(root.xpath(itemEnded1Tag)[0].text_content()) > 0 :
            ItemEnded1Flag = True
            ItemEndedText = root.xpath(itemEnded1Tag)[0].text_content()
        else:
            ItemEnded1Flag = False
            ItemEndedText = None
    if root.xpath(itemEnded2Tag):
        ItemEndedFlag = True
    else:
        ItemEndedFlag = False
#    print "ItemEndedFlag: ", ItemEndedFlag, ItemEnded1Flag, ItemEndedText
    if ItemEndedFlag or ItemEnded1Flag :
        return "No"
    else:
        InsertFlag = "Yes"

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
#            print "Category Title: ", tempTitle
            CategoryTitle.append(tempTitle)
            CategoryNumber.append(tempSplitHrefArray[5])
            CategoryParentNumber.append(tempCategoryParentNumber)
            tempCategoryParentNumber = tempSplitHrefArray[5]
###  Category selection End


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
#          print "picture: ", tempSrc
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
    ItemNumber = inItemNumber

    ItemTitle = root.cssselect(titleTag)[0].text_content()

    tempItemTitle2 = root.xpath(itemTitle2Tag)
    ItemTitle2 = ""
    if len(tempItemTitle2) != 0:
        ItemTitle2 = tempItemTitle2[0].text

    try:
        ItemDescriptionHTML = tostring(root.xpath(descriptionTag)[0]) 
        if len(ItemDescriptionHTML) > 32000 :
            ItemDescriptionHTML = ItemDescriptionHTML[:32000]

        ItemDescriptionText = root.xpath(descriptionTag)[0].text_content()
        if len(ItemDescriptionText) > 32000 :
            ItemDescriptionText = ItemDescriptionText[:32000]
    except:
        ItemDescriptionText = "unknown"

    try:
#        print "seller:", root.xpath(sellerTag)
        Seller = root.xpath(sellerTag)[0].text
    except:
        Seller = "unknown"

    try:
#        print "SellerFeedback :", root.xpath(sellerFeedbackTag)
        SellerFeedback = root.xpath(sellerFeedbackTag)[0].text
    except:
        SellerFeedback = "unknown"

    try:     # sometimes there is no percentage number
#        print "SellerFeedbackPercentage: ", root.xpath(sellerFeedbackPercentageTag)
        SellerFeedbackPercentage = root.xpath(sellerFeedbackPercentageTag)[0].text
        SellerFeedbackPercentage = SellerFeedbackPercentage.split()[0]    # Keeps only the percentage number
    except:
        SellerFeedbackPercentage = "unknown"

    try:
#        print "sellerLocation = ", root.xpath(sellerLocationTag)
        SellerLocation = root.xpath(sellerLocationTag)[5]
#        print "SellerSellsToLocation =", root.xpath(sellerSellsToLocationTag)
        SellerSellsToLocation = root.xpath(sellerSellsToLocationTag)[6]
    except:
        SellerLocation = "unknown"
        SellerSellsToLocation = "unknown"
### Title, Description, and Seller selection End


### Attribute Group selection Begin
    ItemAttributeGroup = root.xpath(itemAttributeGroupTag)
    key = []
    value = []
    i = -1
    firstFlag = True
#    print "Number of Attributes: ", len(ItemAttributeGroup)
    if len(ItemAttributeGroup) & 1 :    #if it's an odd number then there's an extra html tag we don't need
        del ItemAttributeGroup[-1]
#    print "Number of Attributes: ", len(ItemAttributeGroup)
    for element in ItemAttributeGroup:
        if firstFlag and len(element.text) > 0 :
            i += 1
            key.append(element.text)
            firstFlag = False
#            print "Attribute: ", element.text
        elif not(firstFlag) and len(element.text_content()) > 0 :
            value.append(element.text_content())
            firstFlag = True
#            print "Attribute Value: ", element.text_content()

#    firstTdAfterTh = False
#    for element in ItemAttributeGroup:
#        if element.tag == 'th':
#            i += 1
#            key.append(element.text)
#            firstTdAfterTh = True
#            print "Attribute: ", element.text
#        if element.tag == 'td' and firstTdAfterTh:
#            value.append(element.text_content())
#            firstTdAfterTh = False
#            print "Attribute Value: ", element.text_content()
### Attribute Group selection End


###  Condition and Date selection Begin
    try:
        ItemCondition = root.xpath(itemConditionTag)[0].text
    except:
        print "#########################################"
        print "itemConditionTag = ", itemConditionTag
        print root.xpath(itemConditionTag)
#        print stophere
        saveError(ItemNumber,"Fail on line 380, ItemCondition not found")
        return "No"

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

# if it's an auction, find number of bids and price
    ItemNumberOfBids = None
    if ItemAuctionFlag:
        ItemBidGroup = root.xpath(itemBidGroupTag)
#        print ItemBidGroup
        if len(ItemBidGroup) == 0 :
            ItemNumberOfBids = "unknown"
            ItemEndPrice = root.xpath(itemPriceTag)[0].text_content()
        else:
            ItemNumberOfBids = ItemBidGroup[0].text_content().split()[0]
            ItemEndPrice = root.xpath(itemPriceTag)[0].text_content()
#        print "Number of Bids", ItemNumberOfBids

###  Reserve or not
    itemReserveFlag = False

    try:
        ItemReserveText = root.xpath(itemReserveTag)[0].text_content()
        itemReserveFlag = True
    except:
        ItemReserveText = None

###  Buy Now or not
    ItemBuyNowPrice = None
    ItemOriginalBuyNowPrice = None
    if len(root.xpath(itemDscPriceTag)) == 0 :
        if ItemAuctionFlag and ItemBuyNowFlag :
            ItemBuyNowPrice = root.xpath(itemPriceTag)[1].text_content()
            ItemEndPrice = ItemBuyNowPrice
        elif ItemBuyNowFlag :
            ItemBuyNowPrice = root.xpath(itemPriceTag)[0].text_content()
            ItemEndPrice = ItemBuyNowPrice
    else :
        ItemBuyNowPrice = root.xpath(itemDscPriceTag)[0].text
        ItemOriginalBuyNowPrice = root.xpath(itemOrgPriceTag)[0].text
#        print "On Sale, Buy Now Price:", ItemBuyNowPrice
#        print "On Sale, Original Buy Now Price:", ItemOriginalBuyNowPrice
        ItemEndPrice = ItemBuyNowPrice

### See if we can determine what the Start Price is
# If we don't have the item number already in the database *AND* the number of bids is either 0 or 1,
#    then set the start price to the "end" price we already captured.
# If we do have the item number in the database *AND* there isn't a start price already stored *AND*
#    the number of bids is either 0 or 1, then set the start price to the "end" price we already captured.
# If we do have the item number in the database *AND* there already is a start price stored, then keep the
#    start price the same as what it is.
# If none of the above are true, set the start price to None.  (We could go to a lot of work to find out
#    what the actual start price is in these cases, but I don't want to do that work yet)

    msg = "Unable to determine"
    tempItemStartPrice = None
    if ItemAuctionFlag :
        try:
            # If already scraped this one before, then this captures the existing start price
            tempItemStartPrice = scraperwiki.sqlite.select("itemStartPrice from auction where itemNumber = ?", ItemNumber)[0]["itemStartPrice"][0]["itemStartPrice"]
            msg = "Already stored auction.  Start price depends whether we already have start price or on number of bids"
        except:
            #if the "try" fails, then this is the first time we've seen this one.  Set the start price to None and see if the number of bids < 2
            msg = "First time auction.  Start price depends on number of bids"
            tempItemStartPrice = None
#$        if tempItemStartPrice == None :
            if int(ItemNumberOfBids) < 2:            #Might need to change this to include Make Offer sales that have completed and were different from start
                msg = "Start Price determined from this scrape"
                tempItemStartPrice = ItemEndPrice
            else:
                msg = "Unable to determine start price -- too many bids already"
                tempItemStartPrice = None

    ItemStartPrice = tempItemStartPrice
#    print ItemStartPrice, msg

    if not (ItemAuctionFlag or ItemBuyNowFlag):   # Seems to be rare case where a listing has ended and we can't determine what kind of listing it was
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

## Save to Tables starts here

    if not ItemEndedFlag :
        addedCounter += 1

        sellerData = {}
        sellerData['seller'] = Seller
        sellerData['sellerLocation'] = SellerLocation
        sellerData['sellerSellsToLocation'] = SellerSellsToLocation
        sellerData['sellerFeedback'] = SellerFeedback
        sellerData['sellerFeedbackPercentage'] = SellerFeedbackPercentage
        sellerData['timestamp'] = CurrentTimeStamp
        sellerData['source'] = url
        sellerList.append(sellerData)

#        scraperwiki.sqlite.save(["seller"], sellerData, table_name="seller")


        auctionData = {}
        auctionData['itemNumber'] = ItemNumber
        auctionData['sellerFeedbackPercentage'] = SellerFeedbackPercentage
        auctionData['sellerFeedback'] = SellerFeedback
        auctionData['sellerSellsToLocation'] = SellerSellsToLocation
        auctionData['sellerLocation'] = SellerLocation
        auctionData['seller'] = Seller
        auctionData['itemTitle'] = ItemTitle
        auctionData['itemTitle2'] = ItemTitle2
        auctionData['itemDescriptionHTML'] = ItemDescriptionHTML
        auctionData['itemDescriptionText'] = ItemDescriptionText
        auctionData['itemCondition'] = ItemCondition
        auctionData['itemAuctionEndDate'] = ItemAuctionEndDate
        auctionData['itemAuctionEndTime'] = ItemAuctionEndTime
        auctionData['itemNumberOfBids'] = ItemNumberOfBids
        auctionData['itemStartPrice'] = ItemStartPrice
        auctionData['itemEndPrice'] = ItemEndPrice
        auctionData['itemBuyNowPrice'] = ItemBuyNowPrice
        auctionData['itemOriginalBuyNowPrice'] = ItemOriginalBuyNowPrice
        auctionData['itemAuctionFlag'] = ItemAuctionFlag
        auctionData['itemBuyNowFlag'] = ItemBuyNowFlag
        auctionData['itemMakeOfferFlag'] = ItemMakeOfferFlag
        auctionData['itemReserveFlag'] = itemReserveFlag
        auctionData['itemOnSaleFlag'] = ItemSaleFlag
        auctionData['timestamp'] = CurrentTimeStamp
        auctionData['source'] = url
        auctionList.append(auctionData)

#        scraperwiki.sqlite.save(["itemNumber"], auctionData, table_name="auction")

        auctionAttributesData = {}
        for listIndex, listItem in enumerate(key):
            auctionAttributesData['itemNumber'] = ItemNumber
            auctionAttributesData['attributeKey'] = key[listIndex]
            auctionAttributesData['attributeValue'] = value[listIndex]
            auctionAttributesData['timestamp'] = CurrentTimeStamp
            auctionAttributesData['source'] = url
            auctionAttributesList.append(auctionAttributesData.copy())

#            scraperwiki.sqlite.save(["itemNumber", "attributeKey"], auctionAttributesData, table_name="auctionAttributes")

        auctionPicturesData = {}
        for listIndex, listItem in enumerate(ItemPictureSmall):
            auctionPicturesData['itemNumber'] = ItemNumber
            auctionPicturesData['itemPictureKey'] = listIndex + 1
            auctionPicturesData['itemPictureSmall'] = ItemPictureSmall[listIndex]
            auctionPicturesData['itemPictureLarge'] = ItemPictureLarge[listIndex]
            auctionPicturesData['itemPicture_1'] = ItemPicture_1[listIndex]
            auctionPicturesData['itemPicture_12'] = ItemPicture_12[listIndex]
            auctionPicturesData['timestamp'] = CurrentTimeStamp
            auctionPicturesData['source'] = url
#            print listIndex, listItem, "Picture Data: ", auctionPicturesData
            auctionPicturesList.append(auctionPicturesData.copy())
#            print listIndex, listItem, "Picture List: ", auctionPicturesList

#            scraperwiki.sqlite.save(["itemNumber", "itemPictureKey"], auctionPicturesData, table_name="auctionPictures")

        auctionCategoriesData = {}
        for listIndex, listItem in enumerate(CategoryTitle):
            auctionCategoriesData['itemNumber'] = ItemNumber
            auctionCategoriesData['categoryNumber'] = CategoryNumber[listIndex]
            auctionCategoriesData['categoryTitle'] = CategoryTitle[listIndex]
            auctionCategoriesData['categoryParentNumber'] = CategoryParentNumber[listIndex]
            auctionCategoriesData['timestamp'] = CurrentTimeStamp
            auctionCategoriesData['source'] = url
            auctionCategoriesList.append(auctionCategoriesData.copy())

#            scraperwiki.sqlite.save(["itemNumber", "categoryNumber"], auctionCategoriesData, table_name="auctionCategories")

        CategoryData = {}
        for listIndex, listItem in enumerate(CategoryTitle):
            CategoryData['categoryNumber'] = CategoryNumber[listIndex]
            CategoryData['categoryTitle'] = CategoryTitle[listIndex]
            CategoryData['categoryParentNumber'] = CategoryParentNumber[listIndex]
            CategoryData['timestamp'] = CurrentTimeStamp
            CategoryData['source'] = url
#            print listIndex, listItem, "Category Data :", CategoryData
            CategoryList.append(CategoryData.copy())
#            print listIndex, listItem, "Category List :", CategoryList

#            scraperwiki.sqlite.save(["categoryNumber"], CategoryData, table_name="Category")

    else:
        print "Not inserting tables"
        InsertFlag = "No"


    return InsertFlag




##Main start here

###First Time Only
CreateTables()
###End First Time Only


UpdateRunStats(0,0,"Begin Run")

random.seed()

#First, create a list of active items from the auction table
activeList = BuildActiveList()

#Next, append to the active list, the items from the test6 "newTable"
#$activeList = AddNewItems(activeList)
#activeList = activeList[60:]

#activeList = ["200436498703"]
#activeList = activeList[:10]


#Then, scrape all of these items
#As we scrape, if the auction has not finished yet, add it to a new "stillActive" list
#Maybe a TODO is if the auction ended with no bids, add it to a "check again" list to see if it's been relisted
stillActiveList = []
completedItemList = []
InsertedAuctionCount = 0
NotInsertedAuctionCount = 0
addedCounter = 0
sellerList = []
auctionList = []
auctionAttributesList = []
auctionPicturesList = []
auctionCategoriesList = []
CategoryList = []

for item in activeList :
    InsertFlag = ScrapeAuction(item, addedCounter)
    if InsertFlag == "Yes" :
        InsertedAuctionCount += 1
        addedCounter += 1
    else:
        NotInsertedAuctionCount += 1
    print "Inserted Auctions: ", InsertedAuctionCount, "Not Inserted Auctions: ", NotInsertedAuctionCount
#    completedItemList.append(item)
    if addedCounter > 50 :
        WriteData()
        addedCounter = 0
        UpdateRunStats(InsertedAuctionCount, NotInsertedAuctionCount, "Run In Progress")
    n = random.random() * 2 + 2
    print "Sleep for seconds: " + str(n)
    time.sleep(n)

#Do final write to get anything left
WriteData()

#$print len(stillActiveList), "still active of ", len(activeList), "originally active"

#After scraping is finished, truncate the "activeTable"
#scraperwiki.sqlite.execute("delete from activeTable")
#scraperwiki.sqlite.commit()


#Then add the "stillActive" list to the "activeTable"
#$activeData = {}
#$print stillActiveList
#$for item in stillActiveList :
#$    activeData["auctionNumber"] = item
#$    activeData["currentTimeStamp"] = CurrentTimeStamp
#$    scraperwiki.sqlite.save(["auctionNumber"], activeData, table_name = "activeTable")


UpdateRunStats(InsertedAuctionCount, NotInsertedAuctionCount, "Run Finished")



# End Program
