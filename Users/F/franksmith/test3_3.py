# Blank Python

#TODO Add sold flag info if item sold
#     Item is defined as sold when it meets the reserve, or
#       There was at least one bid, or
#       Buy It Now was used
#TODO Capture shipping costs
#TODO Add item complete info when auction is over
#TODO Add capture into database
#TODO Add ability to capture multiple items
#TODO Verify URL item number is same as scraped item number (if not, somthing is wrong with xpath tag)
#TODO Capture URLs of any pictures (and download them?)
#     Sometimes the ebay pictures ending in "_3.jpg" don't work.  But the ones ending in "_12.jpg" do (but they are smaller)

#TODO Capture number of watchers (how to get this info?)
#TODO Capture winning bidder and time of winning bid (maybe all bid info?)
#TODO Add random delay time between calls to scrape function
#TODO Add auction length in days
#TODO Capture Questions and Answers



print "Hello"

#import lxml.etree
import time
import lxml.html
import urllib
import scraperwiki
import time
import random
#import re
from lxml.html import fromstring
from lxml.html import tostring

CurrentTimeStamp = time.strftime('%x %X %Z')
print "Timestamp: ", CurrentTimeStamp



def BuildActiveList():
    #Build the active List from all the items in the auction table that haven't ended
    activeList = []
    activeDict = scraperwiki.sqlite.select("itemNumber from auction where itemActiveAuctionFlag = 'Yes'")
    print activeDict
    item = {}
    for item in activeDict :
        activeList.append(item["itemNumber"])
    print activeList


    return activeList


def AddNewItems(activeList):
    scraperwiki.sqlite.attach("test6")
    scrapeList = scraperwiki.sqlite.select("auctionNumber from test6.newTable")
    print scrapeList
    for item in scrapeList:
#        print item["auctionNumber"]
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
  itemTitle2Tag = '//h2[@class="vi-is1-titleH2"]'  # Sub title (title2) may not be there for each scrape
  #descriptionTag = 'div[class="item_description"]'  ## FOR cssselect
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
  #itemAuctionEndDateTag = "//span[@class='vi-is1-dt']//span[not(@*)][last()]"  # Get span node that does not have any attributes to allow for current auctions
  #itemAuctionEndTimeTag = "//span[@class='vi-is1-t']"
#/root/Datasets/Dataset[contains(@Pattern, 'xyz')]
  itemPriceTag = "//span[contains(@class, 'vi-is1-prcp')]"  #if there are two of these, it could be an "auction 
                                                            #or Buy Now" or it could be a Buy Now that is on sale
  itemSaleTag = "//span[contains(@class, 'vi-is1-prcsl')]"  #if this exists, the buy now item is on sale
  itemReserveTag = "//a[@class='vi-is1-rsv']"   
  itemBuyNowTag = "//a[@id='but_v4-4']"         #Only for active buy now
  itemMakeOfferTag = "//a[@id='but_v4-2']"      #Only for active make offer
  itemPlaceBidTag = "//input[@id='but_v4-6']"   #Only for active auctions
#  itemSoldTag = "//table[@class='vi-ia-attrGroup']//table/tr"
  itemCompleteTag = "//table[@class='vi-ia-attrGroup']"
  itemPictureGroupTag = "//div[@class='vi-ipic1']//img[@src]"

###Save all the info as it now exists (if it exists)
  try:
    currentInfo = scraperwiki.sqlite.select("* from auction where itemNumber = ?", inItemNumber)
  except:
    currentInfo = None

  # url below is a completed auction
  #url = 'http://cgi.ebay.com/170659691608'
  # url below is a current auction
  #url = 'http://cgi.ebay.com/370527941606'
  url = 'http://cgi.ebay.com/' + inItemNumber
  print "Reading URL: ", url
  html = urllib.urlopen(url).read()
  print html
  #print (content.tag)

  #doc = fromstring(content)
  #doc.make_links_absolute(url)
  #print doc

  root = lxml.html.fromstring(html)

###  Completed/Ended or Active Auction selection Begin
### Check first if it's removed or not
  ItemRemovedFlag = False
  try:
    removedAuctionText = root.xpath(removedAuctionTag)[0].text_content()
    print removedAuctionText
    if "has been removed" in removedAuctionText :
      ItemActiveAuctionFlag = removedAuctionText
      ItemRemovedFlag = True
      print "IAAF: ", ItemActiveAuctionFlag
  except:
    try:
      print "try2"
      ItemActiveAuctionFlag = root.xpath(itemActiveAuctionTag)[0].text_content()
    except:
      print "except2"
      ItemActiveAuctionFlag = "Active"

  print "Auction Removed?: ", ItemActiveAuctionFlag
  print ItemRemovedFlag
  if ItemRemovedFlag :
    return ItemActiveAuctionFlag
###  Completed/Ended or Active Auction selection End





###  Category selection Begin
  CategoryBreadCrumbGroup = root.xpath(categoryBreadCrumbGroupTag)
  CategoryTitle = []
  CategoryNumber = []
  CategoryParentNumber = []
  tempCategoryParentNumber = None
  print str(len(CategoryBreadCrumbGroup)) + " Category Group Nodes"
  if len(CategoryBreadCrumbGroup) != 0:
    listIndex = 0
    for element in (CategoryBreadCrumbGroup):
      tempHref = element.get("href")
#      print tempHref
      tempSplitHrefArray = tempHref.split("/")
      tempTitle = tempSplitHrefArray[3]
      if tempTitle[-1:] == "-":           #  if the last character of the title is a "-", then strip it off
         tempTitle = tempTitle[:-1]
      CategoryTitle.append(tempTitle)
      CategoryNumber.append(tempSplitHrefArray[4])
      CategoryParentNumber.append(tempCategoryParentNumber)
      tempCategoryParentNumber = tempSplitHrefArray[4]
      print "Title: ", CategoryTitle[len(CategoryTitle)-1], "  Number: ", CategoryNumber[len(CategoryTitle)-1], "  Parent: ", CategoryParentNumber[len(CategoryTitle)-1]
###  Category selection End


###  Completed/Ended or Active Auction selection Begin
  try:
    ItemActiveAuctionFlag = root.xpath(itemActiveAuctionTag)[0].text_content()
  except:
    ItemActiveAuctionFlag = "Active"

  print ItemActiveAuctionFlag
###  Completed/Ended or Active Auction selection End


###  Picture selection Begin
  ItemPictureGroup = root.xpath(itemPictureGroupTag)
  ItemPictureSmall = []
  ItemPictureLarge = []
  ItemPicture_12 = []
  ItemPicture_1 = []
  ListSrcSplit = []
  print str(len(ItemPictureGroup)) + " Picture Group Nodes"
  if len(ItemPictureGroup) != 0:
#   listIndex = 0
    for elementIndex, element in enumerate(ItemPictureGroup):
      tempSrc = element.get("src")
#      print tempSrc
      if tempSrc.find("ebaystatic") == -1:  #skip the ebaystatic pics
        tempSplitPoint = tempSrc.find("_")  #extract just the first part of the src name (up to the underscore)
        tempSrcSplit = tempSrc[0:tempSplitPoint]
        #print "First Part: ", tempSrcSplit
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
  
  print "Total number of pictures: ", len(ItemPictureSmall), "small,  ", len(ItemPictureLarge), "LARGE"
###  Picture selection End


### Title, Description, and Seller selection Begin
  ItemTitle = root.cssselect(titleTag)[0].text_content()
  tempItemTitle2 = root.xpath(itemTitle2Tag)
  ItemTitle2 = ""
  if len(tempItemTitle2) != 0:
    ItemTitle2 = tempItemTitle2[0].text
  ItemDescriptionHTML = tostring(root.xpath(descriptionTag)[0]) 
  if len(ItemDescriptionHTML) > 32000 :
    print "HTML length: ", len(ItemDescriptionHTML)
    ItemDescriptionHTML = ItemDescriptionHTML[:32000]
#  ItemDescriptionText = normalize_whitespace(root.xpath(descriptionTag)[0].text_content())
  ItemDescriptionText = root.xpath(descriptionTag)[0].text_content()
  if len(ItemDescriptionText) > 32000 :
    print "Text length: ", len(ItemDescriptionText)
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
  print str(len(ItemAttributeGroup)) + " Attribute Group Nodes"
  #print tostring(ItemAttributeGroup[0])
  key = []
  value = []
  i = -1
  firstTdAfterTh = False
  for element in ItemAttributeGroup:
    #print ("%s - %s - %s" % (element.tag, element.text, element.text_content()))
    if element.tag == 'th':
        i += 1
        key.append(element.text)
        firstTdAfterTh = True
    if element.tag == 'td' and firstTdAfterTh:
        value.append(element.text_content())
        firstTdAfterTh = False
#        print i, key[i], value[i]
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
      print root.xpath(itemBidHistoryTag)
      ItemNumberOfBids = int(root.xpath(itemNumberOfBidsTag)[1].text)
    else:
      ItemNumberOfBids = 0
  except:
    ItemAuctionFlag = False
    ItemNumberOfBids = 0

  print "Auction type: ", ItemAuctionFlag
  print ItemNumberOfBids

###  Reserve or not
  try:
    ItemReserveText = root.xpath(itemReserveTag)[0].text_content()
  except:
    ItemReserveText = None

  print "Reserve?: ", ItemReserveText

###  Buy Now or not
  try:
    ItemBuyNowText = root.xpath(itemBuyNowTag)[0].text_content()
    if ItemAuctionFlag:    #if it's an "auction or Buy Now", then the Buy Now price is the second price
      ItemBuyNowPrice = root.xpath(itemPriceTag)[1].text_content()
      ItemOriginalBuyNowPrice = None      # assume if "auction or Buy Now" then it cannot be on sale -- need to verify
    else:                  #if it's only a Buy Now, see if it's on sale or not
      try:
          ItemSaleText = root.xpath(itemSaleTag)[0].text_content()   #if this path exists, then it's on sale
          ItemBuyNowPrice = root.xpath(itemPriceTag + "//text()")[3]   #the text() is an lxml only extension to xpath.  It splits the text into a list of "text" and "tail" items.  This allows us to get the price without the associated "Original Price" hidden html text
          ItemOriginalBuyNowPrice = root.xpath(itemPriceTag + "//text()")[1]   #the text() is an lxml only extension to xpath.  It splits the text into a list of "text" and "tail" items.  This allows us to get the price without the associated "Original Price" hidden html text
      except:
          ItemBuyNowPrice = root.xpath(itemPriceTag)[0].text_content()
          ItemOriginalBuyNowPrice = None
    print "Buy Now price: ", ItemBuyNowPrice
    print "Original Buy Now price: ", ItemOriginalBuyNowPrice
  except:
    ItemBuyNowText = None

  print "Buy Now?: ", ItemBuyNowText

###  Make Offer or not
  try:
    ItemMakeOfferText = root.xpath(itemMakeOfferTag)[0].text_content()
  except:
    ItemMakeOfferText = None

  print "Make Offer?: ", ItemMakeOfferText

  test1 = root.xpath(itemPriceTag)
  print test1
  print "length: ", len(test1)
  for listIndex, element in enumerate(test1):
    print listIndex,  root.xpath(itemPriceTag)[listIndex].text_content()

  print stophere

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
      print msg
      print "try2: ", tempItemStartPrice
    except:
      #if the "try" fails, then this is the first time we've seen this one.  Set the start price to None and see if the number of bids < 2
      msg = "First time auction.  Start price depends on number of bids"
      print msg
      tempItemStartPrice = None
    print "try1: ", tempItemStartPrice
    if tempItemStartPrice == None :
#      tempItemNumber = scraperwiki.sqlite.select("itemNumberOfBids from auction where itemNumber = ?", ItemNumber)
#      print tempItemNumber[0]["itemNumberOfBids"]
      if ItemNumberOfBids < 2:            #Might need to change this to include Make Offer sales that have completed and were different from start
        msg = "Start Price determined from this scrape"
        print msg
        tempItemStartPrice = ItemEndPrice
      else:
        msg = "Unable to determine start price -- too many bids already"
        tempItemStartPrice = None
    else:
      msg = "Start Price already captured"
      print msg
      tempItemStartPrice = tempItemStartPrice

#Do we even need this anymore?
  except:
    print "except1: ", tempItemStartPrice
#    if ItemNumberOfBids < 2:            #Might need to change this to include Make Offer sales that have completed and were different from start
#      tempItemStartPrice = "No auction stored, Start Price determined from this scrpae: " + ItemEndPrice

  print msg, "duplicate msg?"
  ItemStartPrice = tempItemStartPrice
  print "Start Price: ", ItemStartPrice
  print "Current or End Price: ", ItemEndPrice

###  Price selection End


  print ItemTitle
  print ItemTitle2
  print ItemDescriptionHTML
  print ItemDescriptionText
  print Seller
  print SellerFeedback
  print SellerFeedbackPercentage
  print ItemNumber
  print SellerLocation
  print SellerSellsToLocation
  print ItemCondition
  print ItemAuctionEndDate
  print ItemAuctionEndTime
  print ItemNumberOfBids
  print ItemEndPrice

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
#    print listIndex
    auctionAttributesData['itemNumber'] = ItemNumber
    auctionAttributesData['attributeKey'] = key[listIndex]
    auctionAttributesData['attributeValue'] = value[listIndex]
    auctionAttributesData['timestamp'] = CurrentTimeStamp
    auctionAttributesData['source'] = url
    scraperwiki.sqlite.save(["itemNumber", "attributeKey"], auctionAttributesData, table_name="auctionAttributes")

  auctionPicturesData = {}
  for listIndex, listItem in enumerate(ItemPictureSmall):
#    print listIndex
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
#    print listIndex
    auctionCategoriesData['itemNumber'] = ItemNumber
    auctionCategoriesData['categoryNumber'] = CategoryNumber[listIndex]
    auctionCategoriesData['categoryTitle'] = CategoryTitle[listIndex]
    auctionCategoriesData['categoryParentNumber'] = CategoryParentNumber[listIndex]
    auctionCategoriesData['timestamp'] = CurrentTimeStamp
    auctionCategoriesData['source'] = url
    scraperwiki.sqlite.save(["itemNumber", "categoryNumber"], auctionCategoriesData, table_name="auctionCategories")

  CategoryData = {}
  for listIndex, listItem in enumerate(CategoryTitle):
#    print listIndex
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

  return ItemActiveAuctionFlag



def auctionsearch(inUrl):

  listItemNumberGroupTag = "//div[@class='lview']//td[@class='dtl']/div/a"
  
  print "Reading auctionsearch URL"
  html = urllib.urlopen(inUrl).read()
  print html
  root = lxml.html.fromstring(html)

  ListItemNumberGroup = root.xpath(listItemNumberGroupTag)
  ListItemNumber = []
  itemList = []
  print str(len(ListItemNumberGroup)) + " List Item Number Group Nodes"
  if len(ListItemNumberGroup) != 0:
    listIndex = 0
    for element in (ListItemNumberGroup):
      tempHref = element.get("href")
      print tempHref
      tempSplitHrefArray = tempHref.split("/")
      tempListItemNumber = tempSplitHrefArray[4].split("?")[0]
      print tempListItemNumber
      itemList.append(tempListItemNumber)


  return itemList


##Main start here

itemList = []

itemList.append('370534126956')  #removed auction

itemList = ScrapeAuction(itemList[0])

#Creating exchange of informatino with test6 within this block

#First, create a list of active items from the auction table
activeList = BuildActiveList()

#Next, append to the active list, the items from the test6 "newTable"
activeList = AddNewItems(activeList)
activeList = activeList

#Then, scrape all of these items
#As we scrape, if the auction has not finished yet, add it to a new "stillActive" list
#Maybe a TODO is if the auction ended with no bids, add it to a "check again" list to see if it's been relisted
stillActiveList = []
for item in activeList :
    ActiveCode = ScrapeAuction(item)
    if ActiveCode == "Active":
        stillActiveList.append(item)
print len(stillActiveList), "still active of ", len(activeList), "originally active"

#After scraping is finished, truncate the "activeTable"
scraperwiki.sqlite.execute("delete from activeTable")
scraperwiki.sqlite.commit()


#Then add the "stillActive" list to the "activeTable"
activeData = {}
print stillActiveList
for item in stillActiveList :
    activeData["auctionNumber"] = item
    activeData["currentTimeStamp"] = CurrentTimeStamp
    scraperwiki.sqlite.save(["auctionNumber"], activeData, table_name = "activeTable")

print stophere
#End of creating information exchange with test6


random.seed()

#for i in xrange(10):
#    n = random.random()
#    print str(i) + ": sleep for seconds: " + str(n)
#    time.sleep(n)

#url = "http://entertainment-memorabilia.shop.ebay.com/Entertainment-Memorabilia-/45100/i.html?LH_NOB=1..9%2C999&_nkw=%28beatle*%2C+lennon%2C+mccartney%29&_trkparms=65%253A16%257C66%253A4%257C39%253A1&rt=nc&_LH_NOB=1&_adv=1&_dmd=1&_fsct=&_in_kw=2&_ipg=25&_oexkw=&_okw=beatle*+lennon+mccartney&_sop=16&_trksid=p3286.c0.m14.l1514&_udhi=&_udlo="
#url = "http://entertainment-memorabilia.shop.ebay.com/Entertainment-Memorabilia-/45100/i.html?LH_NOB=1..9%2C999&_nkw=%28beatle*%2C+lennon%2C+mccartney%29&_trkparms=65%253A16%257C66%253A2%257C39%253A1&rt=nc&_LH_NOB=1&_adv=1&_fsct=&_in_kw=2&_ipg=25&_oexkw=&_okw=beatle*+lennon+mccartney&_sc=1&_sop=16&_trksid=p3286.c0.m14.l1514&_udhi=&_udlo="
#url = "http://shop.ebay.com/i.html?&_nkw=beatles&_sacat=See-All-Categories"
#url = "http://entertainment-memorabilia.shop.ebay.com/Entertainment-Memorabilia-/45100/i.html?LH_NOB=1..9%2C999&_nkw=%28beatle*%2C+lennon%2C+mccartney%29&_trkparms=65%253A16%257C66%253A2%257C39%253A1&rt=nc&_LH_NOB=1&_adv=1&_fsct=&_in_kw=2&_ipg=25&_oexkw=&_okw=beatle*+lennon+mccartney&_sc=1&_sop=16&_udhi=&_udlo="
url = "http://entertainment-memorabilia.shop.ebay.com/Entertainment-Memorabilia-/45100/i.html?LH_NOB=1..9%2C999&_nkw=%28beatle*%2C+lennon%2C+mccartney%29&rt=nc&_LH_NOB=1&_adv=1&_fsct=&_in_kw=2&_ipg=25&_oexkw=&_okw=beatle*+lennon+mccartney&_sc=1&_sop=16&_udhi=&_udlo="

itemList = []

#itemList = auctionsearch(url)

scraperwiki.sqlite.attach("test4")
scrapeList = scraperwiki.sqlite.select("auctionNumber from test4.auction")
print scrapeList
dictItem = {}
#for dictItem in scrapeList:
#  itemList.append(dictItem["auctionNumber"])

print itemList



itemList.append('370534126956')  #removed auction
#itemList.append('110718554648')  #finished auction
#itemList.append('170659691608')  #finished auction
#itemList.append('360377819874')  #loufar4 current auction
#itemList.append('290589853392')  #finished auction with different picture URL
for item in itemList:
  n = random.random() * 10
  print "Sleep for seconds: " + str(n)
  time.sleep(n)
  scrapeauction(item)

# End Program

#test = "Testing:"
#for table in root.cssselect('table[class="s-content"].span[class="mbg-nw"]'):
#    test += table.text_content()
#print test

#desc = "ITEM DESCRIPTION: "
# The following are good, but not needed
#descAxis = root.xpath('descendant-or-self::div[@class="item_description"]//*')
#print len(descAxis)
#for div in root.xpath('//div[@class="item_description"]//*'):
#for div in descAxis:
#    print div
#    desc += div.text_content()


#desc += tostring(root.xpath('//div[@class="item_description"]//*')[0])  #text_content()
#desc += lxml.etree.tostring(root)

#print desc

#for tr in root.cssselect("table[align='left'] tr.tcont"):
#    tds = tr.cssselect("td")
#    data = {
#        'variable' : tds[0].text_content(),
#        'valeur' : int(tds[4].text_content())
#    }
#    scraperwiki.sqlite.save(unique_keys=['country'], data=data)
