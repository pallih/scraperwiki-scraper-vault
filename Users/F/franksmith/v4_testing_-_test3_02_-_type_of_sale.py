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



def ScrapeAuction(inItemNumber):

### Auction Tags tested

    titleTag = 'h1'
    itemAuction1Tag = "//*/text() = 'Bid history:'"
    itemAuction2Tag = "//*/text() = 'Current bid:'"
    itemAuction3Tag = "//*/text() = 'Starting bid:'"
    itemAuction4Tag = "//*/text() = 'Winning bid:'"
    itemBuyNowTag = "//*/text() = 'Buy It Now'"
    itemMakeOfferTag = "//*/text() = 'Best Offer:'"
    itemSaleTag = "//span[contains(@class, 'vi-is1-prcsl')]"  #if this exists, the buy now item is on sale
    itemEnded1Tag = "//span[@id='v4-1-msg']"
    itemEnded2Tag = "//*/text() = 'Ended:'"
    itemBidGroupTag = "//span[@class='vi-is1-s6']//*"
    itemBidGroup2Tag = "//a[contains(@href, 'ViewBids')]"
    itemConditionTag = "//span[@class='vi-is1-condText']"
    itemDateGroupTag = "//span[@class='vi-is1-dt']//*"



### Current auction tags
    removedAuctionTag = '//div[@id="vi-container"]//div[@class="sm-imc sml-imc"]'
    categoryBreadCrumbGroupTag = '//div[@class="bbc-in bbc bbc-nav"]//ul/li/a'
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
#    itemConditionTag = "//span[@class='vi-is1-condText']"
    itemConditionTag2 = "//td[@class='vi-is1-clr'][1]"
    itemNumberOfBidsTag = "following-sibling::td//text()"  #Number of bids is the first text of td following the "Bid History" text
    itemBidHistoryTag = "//th[@class='vi-is1-lbl']"
#    itemDateGroupTag = "//span[@class='vi-is1-dt']//*"
    itemPriceTag = '//span[contains(@itemprop, "price")]'
    itemPriceTag2 = "//span[contains(@class, 'vi-is1-prcp')]"  #if there are two of these, it could be an "auction
                                                              #or Buy Now" or it could be a Buy Now that is on sale
    itemPriceTag3 = "//span[contains(@id, 'v4-')]" 

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
    try:
        html = urllib.urlopen(url).read()
    except:
        print "*********ERROR on reading URL*************"
        print url
        print html
        print "*********End of Error Report************"
    print html

    root = lxml.html.fromstring(html)


################################################

# check if auction:
    if root.xpath(itemAuction1Tag) | root.xpath(itemAuction2Tag) | root.xpath(itemAuction3Tag) | root.xpath(itemAuction4Tag) :
        ItemAuctionFlag = True
    else:
        ItemAuctionFlag = False
    print "ItemAuctionFlag: ", ItemAuctionFlag

# check if Buy It Now:
    if root.xpath(itemBuyNowTag):
        ItemBuyNowFlag = True
    else:
        ItemBuyNowFlag = False
    print "ItemBuyNowFlag: ", ItemBuyNowFlag

# check if On Sale:
    if root.xpath(itemSaleTag):
        ItemSaleFlag = True
    else:
        ItemSaleFlag = False
    print "ItemSaleFlag: ", ItemSaleFlag

# check if MakeOffer:
    if root.xpath(itemMakeOfferTag):
        ItemMakeOfferFlag = True
    else:
        ItemMakeOfferFlag = False
    print "ItemMakeOfferFlag: ", ItemMakeOfferFlag

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

# if it's an auction, find number of bids

    if ItemAuctionFlag:
        ItemBidGroup = root.xpath(itemBidGroup2Tag)
        print len(ItemBidGroup), ItemBidGroup
        if len(ItemBidGroup) == 0 :
            ItemNumberOfBids = "unknown"
        else:
            ItemNumberOfBids = ItemBidGroup[0].text_content()
        print "Number of Bids", ItemNumberOfBids


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



################################################




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





### Title, Description, and Seller selection Begin
    ItemTitle = root.cssselect(titleTag)[0].text_content()
### Title, Description, and Seller selection End


###  Reserve or not
    try:
        ItemReserveText = root.xpath(itemReserveTag)[0].text_content()
        itemReserveFlag = True
    except:
        ItemReserveText = None



    print ItemTitle
    print inItemNumber
    UpdateFlag = "No"
    return str(root.xpath(itemPriceTag + '/@id')[0]), UpdateFlag
    #return ItemActiveAuctionFlag, UpdateFlag




##Main start here

random.seed()


#Next, append to the active list, the items from the test6 "newTable"
activeList = AddNewItems([])
#activeList = activeList[60:]

for item in activeList :
    ActiveCode, UpdateFlag = ScrapeAuction(item)
    n = random.random() * 10 + 1
    print "Sleep for seconds: " + str(n)
    time.sleep(n)


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



def ScrapeAuction(inItemNumber):

### Auction Tags tested

    titleTag = 'h1'
    itemAuction1Tag = "//*/text() = 'Bid history:'"
    itemAuction2Tag = "//*/text() = 'Current bid:'"
    itemAuction3Tag = "//*/text() = 'Starting bid:'"
    itemAuction4Tag = "//*/text() = 'Winning bid:'"
    itemBuyNowTag = "//*/text() = 'Buy It Now'"
    itemMakeOfferTag = "//*/text() = 'Best Offer:'"
    itemSaleTag = "//span[contains(@class, 'vi-is1-prcsl')]"  #if this exists, the buy now item is on sale
    itemEnded1Tag = "//span[@id='v4-1-msg']"
    itemEnded2Tag = "//*/text() = 'Ended:'"
    itemBidGroupTag = "//span[@class='vi-is1-s6']//*"
    itemBidGroup2Tag = "//a[contains(@href, 'ViewBids')]"
    itemConditionTag = "//span[@class='vi-is1-condText']"
    itemDateGroupTag = "//span[@class='vi-is1-dt']//*"



### Current auction tags
    removedAuctionTag = '//div[@id="vi-container"]//div[@class="sm-imc sml-imc"]'
    categoryBreadCrumbGroupTag = '//div[@class="bbc-in bbc bbc-nav"]//ul/li/a'
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
#    itemConditionTag = "//span[@class='vi-is1-condText']"
    itemConditionTag2 = "//td[@class='vi-is1-clr'][1]"
    itemNumberOfBidsTag = "following-sibling::td//text()"  #Number of bids is the first text of td following the "Bid History" text
    itemBidHistoryTag = "//th[@class='vi-is1-lbl']"
#    itemDateGroupTag = "//span[@class='vi-is1-dt']//*"
    itemPriceTag = '//span[contains(@itemprop, "price")]'
    itemPriceTag2 = "//span[contains(@class, 'vi-is1-prcp')]"  #if there are two of these, it could be an "auction
                                                              #or Buy Now" or it could be a Buy Now that is on sale
    itemPriceTag3 = "//span[contains(@id, 'v4-')]" 

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
    try:
        html = urllib.urlopen(url).read()
    except:
        print "*********ERROR on reading URL*************"
        print url
        print html
        print "*********End of Error Report************"
    print html

    root = lxml.html.fromstring(html)


################################################

# check if auction:
    if root.xpath(itemAuction1Tag) | root.xpath(itemAuction2Tag) | root.xpath(itemAuction3Tag) | root.xpath(itemAuction4Tag) :
        ItemAuctionFlag = True
    else:
        ItemAuctionFlag = False
    print "ItemAuctionFlag: ", ItemAuctionFlag

# check if Buy It Now:
    if root.xpath(itemBuyNowTag):
        ItemBuyNowFlag = True
    else:
        ItemBuyNowFlag = False
    print "ItemBuyNowFlag: ", ItemBuyNowFlag

# check if On Sale:
    if root.xpath(itemSaleTag):
        ItemSaleFlag = True
    else:
        ItemSaleFlag = False
    print "ItemSaleFlag: ", ItemSaleFlag

# check if MakeOffer:
    if root.xpath(itemMakeOfferTag):
        ItemMakeOfferFlag = True
    else:
        ItemMakeOfferFlag = False
    print "ItemMakeOfferFlag: ", ItemMakeOfferFlag

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

# if it's an auction, find number of bids

    if ItemAuctionFlag:
        ItemBidGroup = root.xpath(itemBidGroup2Tag)
        print len(ItemBidGroup), ItemBidGroup
        if len(ItemBidGroup) == 0 :
            ItemNumberOfBids = "unknown"
        else:
            ItemNumberOfBids = ItemBidGroup[0].text_content()
        print "Number of Bids", ItemNumberOfBids


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



################################################




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





### Title, Description, and Seller selection Begin
    ItemTitle = root.cssselect(titleTag)[0].text_content()
### Title, Description, and Seller selection End


###  Reserve or not
    try:
        ItemReserveText = root.xpath(itemReserveTag)[0].text_content()
        itemReserveFlag = True
    except:
        ItemReserveText = None



    print ItemTitle
    print inItemNumber
    UpdateFlag = "No"
    return str(root.xpath(itemPriceTag + '/@id')[0]), UpdateFlag
    #return ItemActiveAuctionFlag, UpdateFlag




##Main start here

random.seed()


#Next, append to the active list, the items from the test6 "newTable"
activeList = AddNewItems([])
#activeList = activeList[60:]

for item in activeList :
    ActiveCode, UpdateFlag = ScrapeAuction(item)
    n = random.random() * 10 + 1
    print "Sleep for seconds: " + str(n)
    time.sleep(n)


# End Program
