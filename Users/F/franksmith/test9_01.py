# Ended items only 

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
    auctionData = {}
    auctionData['itemNumber'] = "delete this row"
    scraperwiki.sqlite.save(["itemNumber"], auctionData, table_name="auction")

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
    #Build the active List from all the items we don't have in the auction table
    activeList = []
    activeDict = {}
    existingList = []
    existingDict = {}
#    scraperwiki.sqlite.attach("test6")
    scraperwiki.sqlite.attach("test8_01")
#    activeDict = scraperwiki.sqlite.select("auctionNumber from test6.newTable")  ## change this to test8_01 after we get it working
    activeDict = scraperwiki.sqlite.select("itemNumber from test8_01.auction")  ## change this to test8_01 after we get it working
    print activeDict
    for item in activeDict :
        activeList.append(item["itemNumber"])
    existingDict = scraperwiki.sqlite.select("itemNumber from auction")
    for item in existingDict :
        existingList.append(item["itemNumber"])
    for itemIndex in range(len(activeList)-1, -1, -1) :
        if activeList[itemIndex] in existingList :
            del activeList[itemIndex]
    random.shuffle(activeList)
    print activeList
    print "Length: ", len(activeList)

#$    print stophere

    return activeList

def ScrapeAuction(inItemNumber):

### Current auction tags
    titleTag = 'h1'
    itemPageNotRespondingTag = "//*/text() = 'Page Not Responding'"
    itemAuction1Tag = "//*/text() = 'Bid history:'"
    itemAuction2Tag = "//*/text() = 'Current bid:'"
    itemAuction3Tag = "//*/text() = 'Starting bid:'"
    itemAuction4Tag = "//*/text() = 'Winning bid:'"
    itemBuyNow1Tag = "//div[id='vi-container']//*/text() = 'Buy It Now'"
#    itemBuyNow1Tag = "//*/text() = 'Buy It Now'"
    itemBuyNow2Tag = "//*/text() = 'Sold For:'"
    itemBuyNow3Tag = "//*/text() = 'Price:'"  #use this for Buy Now that has ended without being sold
    itemMakeOfferTag = "//*/text() = 'Best Offer:'"
    itemSaleTag = "//span[contains(@class, 'vi-is1-prcsl')]"  #if this exists, the buy now item is on sale
    itemEnded1Tag = "//span[@id='v4-1-msg']"
    itemEnded2Tag = "//*/text() = 'Ended:'"
    itemBidGroupTag = "//a[contains(@href, 'ViewBids')]"
    itemConditionTag = "//span[@class='vi-is1-condText']"
    itemDateGroupTag = "//span[@class='vi-is1-dt']//*"


    removedAuctionTag = '//div[@id="vi-container"]//div[@class="sm-imc sml-imc"]'
    categoryBreadCrumbGroupTag = '//div[@class="bbc-in bbc bbc-nav"]//ul/li/a'
    itemTitle2Tag = '//h2[@class="vi-is1-titleH2"]'  
    descriptionTag = '//div[@class="item_description"]//*'
    sellerTag = "//table[contains(@class,'s-content')]//span[@class='mbg-nw']"
    sellerFeedbackTag = "//table[contains(@class,'s-content')]//a[@class='mbg-fb']//*"
    sellerFeedbackPercentageTag = "//table[contains(@class,'s-content')]//span[@class='s-gray z_a']"
    itemNumberTag = "//table[@class='sp1']/tr/td[2]"
    sellerLocationTag = "//table[@class='sp1']/tr[2]/td[2]"
    sellerSellsToLocationTag = "//table[@class='sp1']/tr[3]/td[2]"
    itemAttributeGroupTag = "//table[@class='vi-ia-attrGroup']//table/tr//*"
    itemConditionTag2 = "//td[@class='vi-is1-clr'][1]"
    itemNumberOfBidsTag = "following-sibling::td//text()"  #Number of bids is the first text of td following the "Bid History" text
    itemBidHistoryTag = "//th[@class='vi-is1-lbl']"
    itemActiveAuctionTag = "//span[@id='v4-1-msg']"
    itemPriceTag = "//span[contains(@class, 'vi-is1-prcp')]"  #if there are two of these, it could be an "auction
                                                              #or Buy Now" or it could be a Buy Now that is on sale

    itemReserveTag = "//a[@class='vi-is1-rsv']"   
#    itemBuyNowTag = "//a[@id='but_v4-4'] | //a[@id='but_v4-5']"         #Only for active buy now -- found but_v4-5 id on Buy Now on Sale with Make Offer
#    itemMakeOfferTag = "//a[@id='but_v4-2'] | //a[@id='but_v4-3']"      #Only for active make offer-- found but_v4-3 id on Buy Now on Sale with Make Offer
    itemPlaceBidTag = "//input[@id='but_v4-6']"   #Only for active auctions
    itemCompleteTag = "//table[@class='vi-ia-attrGroup']"
    itemPictureGroupTag = "//div[@class='vi-ipic1']//img[@src]"

### Completed auction tags
    sellerTag_c = "//span[@class='mbg-nw']"
    sellerFeedbackTag_c = "//a[@class='mbg-fb']//*"

    url = 'http://www.ebay.com/itm/' + inItemNumber
    print "Reading URL: ", url
    invalidread = 1
    while invalidread :
        try:
            html = urllib.urlopen(url).read()
            root = lxml.html.fromstring(html)
            invalidread = 0
        except:
            print "*********ERROR on reading URL*************"
            print url
            print "*********End of Error Report************"
            n = random.random() * 2 + 2    
            print "Sleep for seconds: " + str(n)
            time.sleep(n)
            invalidread = 1
    print html

    root = lxml.html.fromstring(html)

###  Completed/Ended section Begin

### Check if valid page
    if root.xpath(itemPageNotRespondingTag) :
        return "No"

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
        return "No"     #fix needed toupdate removed auctions?

#Check if it's ended.  We only want ended

# check if Item has ended (sale or auction):
    if len(root.xpath(itemEnded1Tag)) > 0 :
        ItemEnded1Flag = True
        print root.xpath(itemEnded1Tag)
        ItemEndedText = root.xpath(itemEnded1Tag)[0].text_content()
    else:
        ItemEnded1Flag = False
        ItemEndedText = None
    if root.xpath(itemEnded2Tag):
        ItemEndedFlag = True
    else:
        ItemEndedFlag = False
    print "ItemEndedFlag: ", ItemEndedFlag, ItemEnded1Flag, ItemEndedText

    if not ItemEndedFlag :
        return "No"

###  Completed/Ended section End

    ItemSoldFlag = True

# check if auction:
    if root.xpath(itemAuction1Tag) | root.xpath(itemAuction2Tag) | root.xpath(itemAuction3Tag) | root.xpath(itemAuction4Tag) :
        ItemAuctionFlag = True
    else:
        ItemAuctionFlag = False
    print "ItemAuctionFlag: ", ItemAuctionFlag

# check if Buy It Now:
    if root.xpath(itemBuyNow1Tag) | root.xpath(itemBuyNow2Tag):
        ItemBuyNowFlag = True
    elif root.xpath(itemBuyNow3Tag):
        ItemBuyNowFlag = True
        ItemSoldFlag = False
    else:
        ItemBuyNowFlag = False
    print "ItemBuyNowFlag: ", ItemBuyNowFlag

### Item Number and Title selection Begin
    ItemNumber = inItemNumber

    ItemTitle = root.cssselect(titleTag)[0].text_content()
### Item Number and Title selection End

###  Condition and Date selection Begin
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
    itemReserveFlag = False

# if it's an auction, find number of bids and price
    ItemNumberOfBids = None
    if ItemAuctionFlag:
        ItemBidGroup = root.xpath(itemBidGroupTag)
        print ItemBidGroup
        if len(ItemBidGroup) == 0 :
            ItemNumberOfBids = "unknown"
            ItemEndPrice = root.xpath(itemPriceTag)[0].text_content()
        else:
            ItemNumberOfBids = ItemBidGroup[0].text_content().split()[0]
            ItemEndPrice = root.xpath(itemPriceTag)[0].text_content()
            if ItemNumberOfBids == '0' :
                ItemSoldFlag = False
        print "Number of Bids", ItemNumberOfBids

###  Reserve or not
    try:
        ItemReserveText = root.xpath(itemReserveTag)[0].text_content()
        itemReserveFlag = True
        if "not met" in ItemReserveText :
            ItemSoldFlag = False
    except:
        ItemReserveText = None


###  Buy Now price
    ItemBuyNowPrice = None
    if ItemAuctionFlag and ItemBuyNowFlag :
        ItemBuyNowPrice = root.xpath(itemPriceTag)[1].text_content()
        ItemEndPrice = ItemBuyNowPrice
    elif ItemBuyNowFlag :
        ItemBuyNowPrice = root.xpath(itemPriceTag)[0].text_content()
        ItemEndPrice = ItemBuyNowPrice

    if not (ItemAuctionFlag or ItemBuyNowFlag):   # Seems to be rare case where a listing has ended and we can't determine what kind of listing it was
        ItemEndPrice = None
        print "Unable to determine listing type: ", url

###  Price selection End


    print ItemTitle
    print ItemNumber
    print ItemAuctionEndDate
    print ItemAuctionEndTime
    print ItemNumberOfBids
    print ItemEndPrice
    print ItemSoldFlag

    if 1 == 1 :
        print "Update the tables"
        UpdateFlag = "Yes"


## Save to Tables starts here

        auctionData = {}
        auctionData['itemNumber'] = ItemNumber
        auctionData['itemTitle'] = ItemTitle
        auctionData['itemAuctionEndDate'] = ItemAuctionEndDate
        auctionData['itemAuctionEndTime'] = ItemAuctionEndTime
        auctionData['itemNumberOfBids'] = ItemNumberOfBids
        auctionData['itemEndPrice'] = ItemEndPrice
        auctionData['itemBuyNowPrice'] = ItemBuyNowPrice
        auctionData['itemAuctionFlag'] = ItemAuctionFlag
        auctionData['itemBuyNowFlag'] = ItemBuyNowFlag
        auctionData['itemSoldFlag'] = ItemSoldFlag
        auctionData['itemReserveFlag'] = itemReserveFlag
        auctionData['itemEndedText'] = ItemEndedText
        auctionData['timestamp'] = CurrentTimeStamp
        auctionData['source'] = url
        scraperwiki.sqlite.save(["itemNumber"], auctionData, table_name="auction")

    else:
        print "Not updating tables"
        UpdateFlag = "No"


    return UpdateFlag




##Main start here

###First Time Only
CreateTables()
###End First Time Only


UpdateRunStats(0,0,"Begin Run")

random.seed()

#First, create a list of active items from the auction table
activeList = BuildActiveList()


#Then, scrape all of these items
#Maybe a TODO is if the auction ended with no bids, add it to a "check again" list to see if it's been relisted
UpdatedAuctionCount = 0
NotUpdatedAuctionCount = 0
for item in activeList :
    UpdateFlag = ScrapeAuction(item)
    if UpdateFlag == "Yes" :
        UpdatedAuctionCount += 1
    else:
        NotUpdatedAuctionCount += 1
    print "Updated Auctions: ", UpdatedAuctionCount, "Not Updated Auctions: ", NotUpdatedAuctionCount
    UpdateRunStats(UpdatedAuctionCount, NotUpdatedAuctionCount, "Run In Progress")
    n = random.random() * 2 + 2    
    print "Sleep for seconds: " + str(n)
    time.sleep(n)



UpdateRunStats(UpdatedAuctionCount, NotUpdatedAuctionCount, "Run Finished")



# End Program
