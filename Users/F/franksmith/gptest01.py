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



def BuildActiveList():
    #Build the active List from all the items in the auction table that haven't ended
    activeList = []
    activeDict = {}
#    activeDict = scraperwiki.sqlite.select("itemNumber from auction where itemActiveAuctionFlag = 'Yes'")
    item = {}
    for item in activeDict :
        activeList.append(item["itemNumber"])


    return activeList


def AddNewItems(activeList):
    scraperwiki.sqlite.attach("test6")
    scrapeList = scraperwiki.sqlite.select("auctionNumber from test6.newTable")
    for item in scrapeList:
        if item["auctionNumber"] not in activeList:
            activeList.append(item["auctionNumber"])

    return activeList



def normalize_whitespace(str):            # taken from icodesnip.com
    import re
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str

def ScrapeAuction(inItemNumber):

  removedAuctionTag = '//div[@id="vi-container"]//div[@class="sm-imc sml-imc"]'
  categoryBreadCrumbGroupTag = '//div[@class="bbc-in bbc bbc-nav"]//ul/li/a'
  titleTag = 'h1'
  itemTitle2Tag = '//h2[@class="vi-is1-titleH2"]'  
  descriptionTag = '//div[@class="item_description"]//*'
  sellerTag = "//table[contains(@class,'s-content')]//span[@class='mbg-nw']"
  sellerFeedbackTag = "//table[contains(@class,'s-content')]//a[@class='mbg-fb']//*"
  sellerFeedbackPercentageTag = "//table[contains(@class,'s-content')]//span[@class='s-gray z_a']"
  itemNumberTag = "//table[@class='sp1']/tr/td[2]"
  sellerLocationTag = "//table[@class='sp1']/tr[2]/td[2]"
  sellerSellsToLocationTag = "//table[@class='sp1']/tr[3]/td[2]"
  itemAttributeGroupTag = "//table[@class='vi-ia-attrGroup']//table/tr//*"
  itemConditionTag = "//span[@class='vi-is1-condText']"
  itemConditionTag2 = "//td[@class='vi-is1-clr'][1]"
  itemNumberOfBidsTag = "//span[@class='vi-is1-s6']//span[1]"  #change this to vi-is1-lbl search for "Bid History:"
  itemBidHistoryTag = "//th[@class='vi-is1-lbl']//text()"
  itemActiveAuctionTag = "//span[@id='v4-1-msg']"
  itemDateGroupTag = "//span[@class='vi-is1-dt']//*"
  itemPriceTag = "//span[@class='vi-is1-prcp']"  #if there are two of these, the second is the buy now price
                                                 #when there is only one price, it's the current price, unless it's
                                                 #only a Buy Now sale, then it's the Buy Now price
  itemReserveTag = "//a[@class='vi-is1-rsv']"   
  itemBuyNowTag = "//a[@id='but_v4-4']"         #Only for active buy now
  itemMakeOfferTag = "//a[@id='but_v4-2']"      #Only for active make offer
  itemPlaceBidTag = "//input[@id='but_v4-6']"   #Only for active auctions
  itemCompleteTag = "//table[@class='vi-ia-attrGroup']"
  itemPictureGroupTag = "//div[@class='vi-ipic1']//img[@src]"

###Save all the info as it now exists (if it exists)
  try:
    currentInfo = scraperwiki.sqlite.select("itemNumber, itemNumberOfBids, itemEndPrice, itemActiveAuctionFlag, itemActiveAuctionText from auction where itemNumber = ?", inItemNumber)[0]
    currentNumberOfPictures = scraperwiki.sqlite.select("count(itemPictureSmall) from auctionPictures where itemNumber = ?", inItemNumber)[0]["count(itemPictureSmall)"]
    currentNumberOfAttributes = scraperwiki.sqlite.select("count(attributeKey) from auctionAttributes where itemNumber = ?", inItemNumber)[0]["count(attributeKey)"]
  except scraperwiki.sqlite.SqliteError, e:
    print str(e)
  except:
    currentInfo = None
    currentNumberOfPictures = None
    currentNumberOfAttributes = None


  print currentInfo

  url = 'http://cgi.ebay.com/' + inItemNumber
  print "Reading URL: ", url
  html = urllib.urlopen(url).read()
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
    return ItemActiveAuctionFlag
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
      tempTitle = tempSplitHrefArray[3]
      if tempTitle[-1:] == "-":           #  if the last character of the title is a "-", then strip it off
         tempTitle = tempTitle[:-1]
      CategoryTitle.append(tempTitle)
      CategoryNumber.append(tempSplitHrefArray[4])
      CategoryParentNumber.append(tempCategoryParentNumber)
      tempCategoryParentNumber = tempSplitHrefArray[4]
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
#  ItemDescriptionText = normalize_whitespace(root.xpath(descriptionTag)[0].text_content())
  ItemDescriptionText = root.xpath(descriptionTag)[0].text_content()
  if len(ItemDescriptionText) > 32000 :
    ItemDescriptionText = ItemDescriptionText[:32000]
  Seller = root.xpath(sellerTag)[0].text
  SellerFeedback = root.xpath(sellerFeedbackTag)[0].tail
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
  if len(ItemDateGroup) == 0 :
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
  try:
    ItemAuctionFlag = "Bid history:" in root.xpath(itemBidHistoryTag)
    if ItemAuctionFlag :
      ItemNumberOfBids = int(root.xpath(itemNumberOfBidsTag)[1].text)
    else:
      ItemNumberOfBids = 0
  except:
    ItemAuctionFlag = False
    ItemNumberOfBids = 0


###  Reserve or not
  try:
    ItemReserveText = root.xpath(itemReserveTag)[0].text_content()
  except:
    ItemReserveText = None


###  Buy Now or not
  try:
    ItemBuyNowText = root.xpath(itemBuyNowTag)[0].text_content()
    if ItemAuctionFlag:    #if it's an auction or Buy Now, then the Buy Now price is the second price
      ItemBuyNowPrice = root.xpath(itemPriceTag)[1].text_content()
    else:                  #if it's only a Buy Now sale
      ItemBuyNowPrice = root.xpath(itemPriceTag)[0].text_content()
  except:
    ItemBuyNowText = None


###  Make Offer or not
  try:
    ItemMakeOfferText = root.xpath(itemMakeOfferTag)[0].text_content()
  except:
    ItemMakeOfferText = None



  ItemEndPrice = root.xpath(itemPriceTag)[0].text

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
  try:
    try:
      # If already scraped this one before, then this captures the existing start price
      tempItemStartPrice = scraperwiki.sqlite.select("itemStartPrice from auction where itemNumber = ?", ItemNumber)[0]["itemStartPrice"][0]["itemStartPrice"]
      msg = "Already stored auction.  Start price depends whether we already have start price or on number of bids"
    except:
      #if the "try" fails, then this is the first time we've seen this one.  Set the start price to None and see if the number of bids < 2
      msg = "First time auction.  Start price depends on number of bids"
      tempItemStartPrice = None
    if tempItemStartPrice == None :
      if ItemNumberOfBids < 2:            #Might need to change this to include Make Offer sales that have completed and were different from start
        msg = "Start Price determined from this scrape"
        tempItemStartPrice = ItemEndPrice
      else:
        msg = "Unable to determine start price -- too many bids already"
        tempItemStartPrice = None
    else:
      msg = "Start Price already captured"
      tempItemStartPrice = tempItemStartPrice

#Do we even need this anymore?
  except:
    print "except1: ", tempItemStartPrice

  ItemStartPrice = tempItemStartPrice

###  Price selection End


#  print ItemTitle
#  print ItemTitle2
#  print ItemDescriptionHTML
#  print ItemDescriptionText
#  print Seller
#  print SellerFeedback
#  print SellerFeedbackPercentage
#  print ItemNumber
#  print SellerLocation
#  print SellerSellsToLocation
#  print ItemCondition
#  print ItemAuctionEndDate
#  print ItemAuctionEndTime
#  print ItemNumberOfBids
#  print ItemEndPrice

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
  print currentInfo
  print updatedInfo == currentInfo
  print updatedNumberOfPictures, currentNumberOfPictures, updatedNumberOfPictures == currentNumberOfPictures
  print updatedNumberOfAttributes, currentNumberOfAttributes, updatedNumberOfAttributes == currentNumberOfAttributes


  if updatedInfo != currentInfo or updatedNumberOfPictures != currentNumberOfPictures or updatedNumberOfAttributes != currentNumberOfAttributes :
    print "Update the tables"
    UpdateFlag = "Yes"


## Save to Tables starts here

    sellerData = {}
    sellerData['seller'] = Seller
    sellerData['sellerLocation'] = SellerLocation
    sellerData['sellerSellsToLocation'] = SellerSellsToLocation
    sellerData['sellerFeedback'] = SellerFeedback
    sellerData['sellerFeedbackPercentage'] = SellerFeedbackPercentage
    sellerData['timestamp'] = CurrentTimeStamp
    sellerData['source'] = url
    scraperwiki.sqlite.save(["seller"], sellerData, table_name="seller")


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
    if ItemActiveAuctionFlag == "Active":
      auctionData['itemActiveAuctionFlag'] = "Yes"
      auctionData['itemActiveAuctionText'] = ""
    else:
      auctionData['itemActiveAuctionFlag'] = "No"
      auctionData['itemActiveAuctionText'] = ItemActiveAuctionFlag
    auctionData['timestamp'] = CurrentTimeStamp
    auctionData['source'] = url
    scraperwiki.sqlite.save(["itemNumber"], auctionData, table_name="auction")


    auctionData = {}
    auctionData['auctionNumber'] = ItemNumber
    auctionData['auctionStatusCode'] = ItemActiveAuctionFlag
#  auctionData = scraperwiki.sqlite.select("* from test4.auction where auctionNumber = ?", ItemNumber)
#  print auctionData
    scraperwiki.sqlite.save(["auctionNumber"], auctionData, table_name="auctionStatus")


    auctionAttributesData = {}
    for listIndex, listItem in enumerate(key):
        auctionAttributesData['itemNumber'] = ItemNumber
        auctionAttributesData['attributeKey'] = key[listIndex]
        auctionAttributesData['attributeValue'] = value[listIndex]
        auctionAttributesData['timestamp'] = CurrentTimeStamp
        auctionAttributesData['source'] = url
        scraperwiki.sqlite.save(["itemNumber", "attributeKey"], auctionAttributesData, table_name="auctionAttributes")

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
        scraperwiki.sqlite.save(["itemNumber", "itemPictureKey"], auctionPicturesData, table_name="auctionPictures")

    auctionCategoriesData = {}
    for listIndex, listItem in enumerate(CategoryTitle):
        auctionCategoriesData['itemNumber'] = ItemNumber
        auctionCategoriesData['categoryNumber'] = CategoryNumber[listIndex]
        auctionCategoriesData['categoryTitle'] = CategoryTitle[listIndex]
        auctionCategoriesData['categoryParentNumber'] = CategoryParentNumber[listIndex]
        auctionCategoriesData['timestamp'] = CurrentTimeStamp
        auctionCategoriesData['source'] = url
        scraperwiki.sqlite.save(["itemNumber", "categoryNumber"], auctionCategoriesData, table_name="auctionCategories")

    CategoryData = {}
    for listIndex, listItem in enumerate(CategoryTitle):
        CategoryData['categoryNumber'] = CategoryNumber[listIndex]
        CategoryData['categoryTitle'] = CategoryTitle[listIndex]
        CategoryData['categoryParentNumber'] = CategoryParentNumber[listIndex]
        CategoryData['timestamp'] = CurrentTimeStamp
        CategoryData['source'] = url
        scraperwiki.sqlite.save(["categoryNumber"], CategoryData, table_name="Category")

#History tables start here

    sellerHistoryData = {}
    sellerHistoryData['surrogateKey'] = 1
    sellerHistoryData['seller'] = Seller
    sellerHistoryData['sellerLocation'] = SellerLocation
    sellerHistoryData['sellerSellsToLocation'] = SellerSellsToLocation
    sellerHistoryData['sellerFeedback'] = SellerFeedback
    sellerHistoryData['sellerFeedbackPercentage'] = SellerFeedbackPercentage
    sellerHistoryData['timestamp'] = CurrentTimeStamp
    sellerHistoryData['source'] = url
    scraperwiki.sqlite.save(["surrogateKey"], sellerHistoryData, table_name="sellerHistory")

  else:
    print "Not updating tables"
    UpdateFlag = "No"


  return ItemActiveAuctionFlag, UpdateFlag




##Main start here

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
UpdatedAuctionCount = 0
NotUpdatedAuctionCount = 0
for item in activeList :
    ActiveCode, UpdateFlag = ScrapeAuction(item)
    if UpdateFlag == "Yes" :
        UpdatedAuctionCount += 1
    else:
        NotUpdatedAuctionCount += 1
    if ActiveCode == "Active":
        stillActiveList.append(item)
    print "Updated Auctions: ", UpdatedAuctionCount, "Not Updated Auctions: ", NotUpdatedAuctionCount
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



def BuildActiveList():
    #Build the active List from all the items in the auction table that haven't ended
    activeList = []
    activeDict = {}
#    activeDict = scraperwiki.sqlite.select("itemNumber from auction where itemActiveAuctionFlag = 'Yes'")
    item = {}
    for item in activeDict :
        activeList.append(item["itemNumber"])


    return activeList


def AddNewItems(activeList):
    scraperwiki.sqlite.attach("test6")
    scrapeList = scraperwiki.sqlite.select("auctionNumber from test6.newTable")
    for item in scrapeList:
        if item["auctionNumber"] not in activeList:
            activeList.append(item["auctionNumber"])

    return activeList



def normalize_whitespace(str):            # taken from icodesnip.com
    import re
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str

def ScrapeAuction(inItemNumber):

  removedAuctionTag = '//div[@id="vi-container"]//div[@class="sm-imc sml-imc"]'
  categoryBreadCrumbGroupTag = '//div[@class="bbc-in bbc bbc-nav"]//ul/li/a'
  titleTag = 'h1'
  itemTitle2Tag = '//h2[@class="vi-is1-titleH2"]'  
  descriptionTag = '//div[@class="item_description"]//*'
  sellerTag = "//table[contains(@class,'s-content')]//span[@class='mbg-nw']"
  sellerFeedbackTag = "//table[contains(@class,'s-content')]//a[@class='mbg-fb']//*"
  sellerFeedbackPercentageTag = "//table[contains(@class,'s-content')]//span[@class='s-gray z_a']"
  itemNumberTag = "//table[@class='sp1']/tr/td[2]"
  sellerLocationTag = "//table[@class='sp1']/tr[2]/td[2]"
  sellerSellsToLocationTag = "//table[@class='sp1']/tr[3]/td[2]"
  itemAttributeGroupTag = "//table[@class='vi-ia-attrGroup']//table/tr//*"
  itemConditionTag = "//span[@class='vi-is1-condText']"
  itemConditionTag2 = "//td[@class='vi-is1-clr'][1]"
  itemNumberOfBidsTag = "//span[@class='vi-is1-s6']//span[1]"  #change this to vi-is1-lbl search for "Bid History:"
  itemBidHistoryTag = "//th[@class='vi-is1-lbl']//text()"
  itemActiveAuctionTag = "//span[@id='v4-1-msg']"
  itemDateGroupTag = "//span[@class='vi-is1-dt']//*"
  itemPriceTag = "//span[@class='vi-is1-prcp']"  #if there are two of these, the second is the buy now price
                                                 #when there is only one price, it's the current price, unless it's
                                                 #only a Buy Now sale, then it's the Buy Now price
  itemReserveTag = "//a[@class='vi-is1-rsv']"   
  itemBuyNowTag = "//a[@id='but_v4-4']"         #Only for active buy now
  itemMakeOfferTag = "//a[@id='but_v4-2']"      #Only for active make offer
  itemPlaceBidTag = "//input[@id='but_v4-6']"   #Only for active auctions
  itemCompleteTag = "//table[@class='vi-ia-attrGroup']"
  itemPictureGroupTag = "//div[@class='vi-ipic1']//img[@src]"

###Save all the info as it now exists (if it exists)
  try:
    currentInfo = scraperwiki.sqlite.select("itemNumber, itemNumberOfBids, itemEndPrice, itemActiveAuctionFlag, itemActiveAuctionText from auction where itemNumber = ?", inItemNumber)[0]
    currentNumberOfPictures = scraperwiki.sqlite.select("count(itemPictureSmall) from auctionPictures where itemNumber = ?", inItemNumber)[0]["count(itemPictureSmall)"]
    currentNumberOfAttributes = scraperwiki.sqlite.select("count(attributeKey) from auctionAttributes where itemNumber = ?", inItemNumber)[0]["count(attributeKey)"]
  except scraperwiki.sqlite.SqliteError, e:
    print str(e)
  except:
    currentInfo = None
    currentNumberOfPictures = None
    currentNumberOfAttributes = None


  print currentInfo

  url = 'http://cgi.ebay.com/' + inItemNumber
  print "Reading URL: ", url
  html = urllib.urlopen(url).read()
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
    return ItemActiveAuctionFlag
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
      tempTitle = tempSplitHrefArray[3]
      if tempTitle[-1:] == "-":           #  if the last character of the title is a "-", then strip it off
         tempTitle = tempTitle[:-1]
      CategoryTitle.append(tempTitle)
      CategoryNumber.append(tempSplitHrefArray[4])
      CategoryParentNumber.append(tempCategoryParentNumber)
      tempCategoryParentNumber = tempSplitHrefArray[4]
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
#  ItemDescriptionText = normalize_whitespace(root.xpath(descriptionTag)[0].text_content())
  ItemDescriptionText = root.xpath(descriptionTag)[0].text_content()
  if len(ItemDescriptionText) > 32000 :
    ItemDescriptionText = ItemDescriptionText[:32000]
  Seller = root.xpath(sellerTag)[0].text
  SellerFeedback = root.xpath(sellerFeedbackTag)[0].tail
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
  if len(ItemDateGroup) == 0 :
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
  try:
    ItemAuctionFlag = "Bid history:" in root.xpath(itemBidHistoryTag)
    if ItemAuctionFlag :
      ItemNumberOfBids = int(root.xpath(itemNumberOfBidsTag)[1].text)
    else:
      ItemNumberOfBids = 0
  except:
    ItemAuctionFlag = False
    ItemNumberOfBids = 0


###  Reserve or not
  try:
    ItemReserveText = root.xpath(itemReserveTag)[0].text_content()
  except:
    ItemReserveText = None


###  Buy Now or not
  try:
    ItemBuyNowText = root.xpath(itemBuyNowTag)[0].text_content()
    if ItemAuctionFlag:    #if it's an auction or Buy Now, then the Buy Now price is the second price
      ItemBuyNowPrice = root.xpath(itemPriceTag)[1].text_content()
    else:                  #if it's only a Buy Now sale
      ItemBuyNowPrice = root.xpath(itemPriceTag)[0].text_content()
  except:
    ItemBuyNowText = None


###  Make Offer or not
  try:
    ItemMakeOfferText = root.xpath(itemMakeOfferTag)[0].text_content()
  except:
    ItemMakeOfferText = None



  ItemEndPrice = root.xpath(itemPriceTag)[0].text

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
  try:
    try:
      # If already scraped this one before, then this captures the existing start price
      tempItemStartPrice = scraperwiki.sqlite.select("itemStartPrice from auction where itemNumber = ?", ItemNumber)[0]["itemStartPrice"][0]["itemStartPrice"]
      msg = "Already stored auction.  Start price depends whether we already have start price or on number of bids"
    except:
      #if the "try" fails, then this is the first time we've seen this one.  Set the start price to None and see if the number of bids < 2
      msg = "First time auction.  Start price depends on number of bids"
      tempItemStartPrice = None
    if tempItemStartPrice == None :
      if ItemNumberOfBids < 2:            #Might need to change this to include Make Offer sales that have completed and were different from start
        msg = "Start Price determined from this scrape"
        tempItemStartPrice = ItemEndPrice
      else:
        msg = "Unable to determine start price -- too many bids already"
        tempItemStartPrice = None
    else:
      msg = "Start Price already captured"
      tempItemStartPrice = tempItemStartPrice

#Do we even need this anymore?
  except:
    print "except1: ", tempItemStartPrice

  ItemStartPrice = tempItemStartPrice

###  Price selection End


#  print ItemTitle
#  print ItemTitle2
#  print ItemDescriptionHTML
#  print ItemDescriptionText
#  print Seller
#  print SellerFeedback
#  print SellerFeedbackPercentage
#  print ItemNumber
#  print SellerLocation
#  print SellerSellsToLocation
#  print ItemCondition
#  print ItemAuctionEndDate
#  print ItemAuctionEndTime
#  print ItemNumberOfBids
#  print ItemEndPrice

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
  print currentInfo
  print updatedInfo == currentInfo
  print updatedNumberOfPictures, currentNumberOfPictures, updatedNumberOfPictures == currentNumberOfPictures
  print updatedNumberOfAttributes, currentNumberOfAttributes, updatedNumberOfAttributes == currentNumberOfAttributes


  if updatedInfo != currentInfo or updatedNumberOfPictures != currentNumberOfPictures or updatedNumberOfAttributes != currentNumberOfAttributes :
    print "Update the tables"
    UpdateFlag = "Yes"


## Save to Tables starts here

    sellerData = {}
    sellerData['seller'] = Seller
    sellerData['sellerLocation'] = SellerLocation
    sellerData['sellerSellsToLocation'] = SellerSellsToLocation
    sellerData['sellerFeedback'] = SellerFeedback
    sellerData['sellerFeedbackPercentage'] = SellerFeedbackPercentage
    sellerData['timestamp'] = CurrentTimeStamp
    sellerData['source'] = url
    scraperwiki.sqlite.save(["seller"], sellerData, table_name="seller")


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
    if ItemActiveAuctionFlag == "Active":
      auctionData['itemActiveAuctionFlag'] = "Yes"
      auctionData['itemActiveAuctionText'] = ""
    else:
      auctionData['itemActiveAuctionFlag'] = "No"
      auctionData['itemActiveAuctionText'] = ItemActiveAuctionFlag
    auctionData['timestamp'] = CurrentTimeStamp
    auctionData['source'] = url
    scraperwiki.sqlite.save(["itemNumber"], auctionData, table_name="auction")


    auctionData = {}
    auctionData['auctionNumber'] = ItemNumber
    auctionData['auctionStatusCode'] = ItemActiveAuctionFlag
#  auctionData = scraperwiki.sqlite.select("* from test4.auction where auctionNumber = ?", ItemNumber)
#  print auctionData
    scraperwiki.sqlite.save(["auctionNumber"], auctionData, table_name="auctionStatus")


    auctionAttributesData = {}
    for listIndex, listItem in enumerate(key):
        auctionAttributesData['itemNumber'] = ItemNumber
        auctionAttributesData['attributeKey'] = key[listIndex]
        auctionAttributesData['attributeValue'] = value[listIndex]
        auctionAttributesData['timestamp'] = CurrentTimeStamp
        auctionAttributesData['source'] = url
        scraperwiki.sqlite.save(["itemNumber", "attributeKey"], auctionAttributesData, table_name="auctionAttributes")

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
        scraperwiki.sqlite.save(["itemNumber", "itemPictureKey"], auctionPicturesData, table_name="auctionPictures")

    auctionCategoriesData = {}
    for listIndex, listItem in enumerate(CategoryTitle):
        auctionCategoriesData['itemNumber'] = ItemNumber
        auctionCategoriesData['categoryNumber'] = CategoryNumber[listIndex]
        auctionCategoriesData['categoryTitle'] = CategoryTitle[listIndex]
        auctionCategoriesData['categoryParentNumber'] = CategoryParentNumber[listIndex]
        auctionCategoriesData['timestamp'] = CurrentTimeStamp
        auctionCategoriesData['source'] = url
        scraperwiki.sqlite.save(["itemNumber", "categoryNumber"], auctionCategoriesData, table_name="auctionCategories")

    CategoryData = {}
    for listIndex, listItem in enumerate(CategoryTitle):
        CategoryData['categoryNumber'] = CategoryNumber[listIndex]
        CategoryData['categoryTitle'] = CategoryTitle[listIndex]
        CategoryData['categoryParentNumber'] = CategoryParentNumber[listIndex]
        CategoryData['timestamp'] = CurrentTimeStamp
        CategoryData['source'] = url
        scraperwiki.sqlite.save(["categoryNumber"], CategoryData, table_name="Category")

#History tables start here

    sellerHistoryData = {}
    sellerHistoryData['surrogateKey'] = 1
    sellerHistoryData['seller'] = Seller
    sellerHistoryData['sellerLocation'] = SellerLocation
    sellerHistoryData['sellerSellsToLocation'] = SellerSellsToLocation
    sellerHistoryData['sellerFeedback'] = SellerFeedback
    sellerHistoryData['sellerFeedbackPercentage'] = SellerFeedbackPercentage
    sellerHistoryData['timestamp'] = CurrentTimeStamp
    sellerHistoryData['source'] = url
    scraperwiki.sqlite.save(["surrogateKey"], sellerHistoryData, table_name="sellerHistory")

  else:
    print "Not updating tables"
    UpdateFlag = "No"


  return ItemActiveAuctionFlag, UpdateFlag




##Main start here

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
UpdatedAuctionCount = 0
NotUpdatedAuctionCount = 0
for item in activeList :
    ActiveCode, UpdateFlag = ScrapeAuction(item)
    if UpdateFlag == "Yes" :
        UpdatedAuctionCount += 1
    else:
        NotUpdatedAuctionCount += 1
    if ActiveCode == "Active":
        stillActiveList.append(item)
    print "Updated Auctions: ", UpdatedAuctionCount, "Not Updated Auctions: ", NotUpdatedAuctionCount
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





# End Program
