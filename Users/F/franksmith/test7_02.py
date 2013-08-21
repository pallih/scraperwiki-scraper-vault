# Blank Python

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
from dateutil.parser import *
from datetime import date

def BuildURLList():

    urlDescriptionList = []
    urlList = []
#itemList.append('280712217861')  #current auction
#itemList.append('370527941606')  #current auction
#itemList.append('170659691608')  #finished auction
#itemList.append('360377819874')  #loufar4 current auction
#itemList.append('290589853392')  #finished auction with different picture URL

    for i in range(1,10):
        urlDescriptionList.append("beatles music memorabilia category - Completed")
        urlList.append("http://www.ebay.com/csc/Beatles-/29924/i.html?LH_Complete=1&rt=nc&_adv=1&_dmd=7&_fsct=&_in_kw=1&_ipg=200&_oexkw=&_okw=&_sop=13&_udhi=&_udlo=&_pgn="+str(i))

    return urlList, urlDescriptionList


def fetchelement(inElement, inTag):
    element = inElement.xpath(inTag)
    return element

def checklength(inList,inLength):
    if len(inList) != inLength:
        print "******Length not correct"
        print "Length of list is: ", len(inList), " but should be: ", inLength
    return

def formatDate(inText):
    thisYear = date.today().year
    thisMonth = date.today().month
    tempMonth = parse(inText).month
    if tempMonth > thisMonth:
        tempDateTime = str(parse(str(thisYear - 1) + "-" + inText))
    else:
        tempDateTime = str(parse(inText))
    return tempDateTime

def saveRecord(inKey, inData, inTable):
    scraperwiki.sqlite.save(inKey,inData,inTable)
    return

def checkRecord(inItemNumber, inTable):
    recordDict = scraperwiki.sqlite.select("itemNumber from " + inTable +" where itemNumber = " + inItemNumber)
    if len(recordDict) > 0 :
        return "Yes"
    else:
        return "No"

def auctionsearch(inUrl):

    addedCounter = 0
#    listItemNumberGroupTag = "//div[@class='lview']//td[@class='dtl']/div/a"
    listItemNumberGroupTag = "//div[contains(@class,'rs rsw')]//td[@class='dtl']/div[@class='ittl']"
#    listItemBeginTag = "//div[@class='lview']//table"
    listItemBeginTag = "//div[contains(@class,'rs rsw')]//table"
    itemPriceTag = "//span[contains(@class, 'vi-is1-prcp')]"
#    listItemNumberTag = "descendant::td[@class='dtl']/div/a"
#    listItemNumberTag = "//td[@class='dtl']/div/a"
    listItemTitleTag = "//td[@class='dtl']/div[@class='ittl']/a"
    listItemPictureTag = "//td[contains(@class,'pic')]"
    itemPictureTag = "descendant::img"
    listItemTypeTag = "//td[@class='bids']|//td[@class='bids bin1']"
    listItemPriceTag = "//td[contains(@class,'prc')]"  #^\$?-?0*(?:\d+(?!,)(?:\.\d{1,2})?|(?:\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?))$
    listItemDateTag = "//td[contains(@class,'tme')]//span"
    itemSoldTag = "descendant::span[@class='sold']"
    invalidread = 1
    invalidreadcount = 1
    while invalidread and invalidreadcount < 5 :
        print "Reading auctionsearch URL.  Attempt # ", invalidreadcount, inUrl
        html = urllib.urlopen(inUrl).read()
#        print html
        root = lxml.html.fromstring(html)
        try:
            currentElement = root.xpath(listItemBeginTag)[0]
            invalidread = 0
        except:
            invalidread = 1
            invalidreadcount += 1
#    print currentElement
    listItemNumberGroup = root.xpath(listItemNumberGroupTag)
    listItemNumber = []
    itemList = []
    itemQty = len(listItemNumberGroup)
#    print itemQty
    x1 = fetchelement(currentElement, listItemTitleTag)
    checklength(x1, itemQty)
    x2 = fetchelement(currentElement, listItemPictureTag)
    checklength(x2, itemQty)
    x3 = fetchelement(currentElement, listItemPriceTag)
    checklength(x3, itemQty)
    x4 = fetchelement(currentElement, listItemTypeTag)
    checklength(x4, itemQty)
    x5 = fetchelement(currentElement, listItemDateTag)
    checklength(x5, itemQty)
#    tempHref = x1[0].get("href")
#    tempSplitHrefArray = tempHref.split("/")
#    tempItemNumber = tempSplitHrefArray[5].split("?")[0]
#    if checkRecord(tempItemNumber, "auction") == "Yes" :     #if we already have the last itemNumber on page in table, then skip this page of results
#        print "Skipping page: ", inUrl[-5:]
#        time.sleep(5)
#        return 0      
#    else:
#        print "Reading page: ", inUrl[-5:]
    print "Reading page: ", inUrl[-5:]
    for i in range(itemQty):
#    for i in range(50):
#        print i
        tempHref = x1[i].get("href")
        tempTitle = x1[i].get("title")
#        print tempTitle
        tempSplitHrefArray = tempHref.split("/")
        tempItemNumber = tempSplitHrefArray[5].split("?")[0]
        try:
            tempPictureFileName = x2[i].xpath(itemPictureTag)[0].get("src")
        except:
            tempPictureFileName = None
        print "Line: ", i, tempItemNumber, tempTitle, tempPictureFileName
        tempPriceGroup = x3[i].xpath("descendant::div")
        print tempPriceGroup, len(tempPriceGroup)
        if len(tempPriceGroup) == 0 :
            tempPrice1 = x3[i].text
            tempPrice2 = None
        else:
            tempPrice1 = tempPriceGroup[0].text
#            tempPrice2 = tempPriceGroup[1].text
        tempTypeGroup = x4[i].xpath("descendant::div|descendant::b")
#        tempTypeGroup = x4[i].xpath("descendant::div")
        if len(tempTypeGroup) == 0 :
            tempType1 = x4[i].text.strip()
            tempType2 = None
        elif len(tempTypeGroup) == 1 :
#            print tempTypeGroup[0].text
            tempType1 = tempTypeGroup[0].text
            tempType2 = tempTypeGroup[0].text
        else:
            tempType1 = tempTypeGroup[0].text
            tempType2 = tempTypeGroup[1].text
        tempSoldGroup = x4[i].xpath(itemSoldTag)
        tempSoldFlag = 1
        if len(tempSoldGroup) == 0 :
            tempSoldFlag = 0
        tempDateTime = formatDate(x5[i].text)
#        tempDateTime = str(parse(x5[i].text).month)   #.split()
        tempDate = tempDateTime
        print tempDateTime
        newData = {}
        newData['itemBestOfferFlag'] = 0   #default to 0, but may be overridden later
        newData['itemAuctionFlag'] = 0
        newData['itemBuyNowFlag'] = 0
        newData['itemNumber'] = tempItemNumber
        newData['itemTitle'] = tempTitle
        newData['itemEndPrice'] = tempPrice1

        if tempType1 == "Buy It Now":
            newData['itemBuyNowFlag'] = 1

        if tempType1 == "Best Offer":
            newData['itemBestOfferFlag'] = 1

        if tempType1.split()[-1] == "Bids" or tempType1.split()[-1] == "Bid":
            newData['itemAuctionFlag'] = 1
            newData['itemNumberBids'] = tempType1.split()[0]

        newData['itemSoldFlag'] = tempSoldFlag
        newData['itemDateTime'] = tempDateTime
        newData['itemPictureFileName'] = tempPictureFileName

#        print newData

        saveRecord(['itemNumber', 'itemDateTime'], newData, 'Auction')
        addedCounter += 1

#    print stophere

    return addedCounter


def BuildCurrentList(urlList, urlDescriptionList):
    currentList = []
    addedCounter = 0
    totalcount = 0
    pagesSkippedCounter = 0
    for listIndex, url in enumerate(urlList):
        itemList = []
        addedCounter = auctionsearch(url)
        totalcount += addedCounter
        if addedCounter == 0 :
            pagesSkippedCounter += 1
            if pagesSkippedCounter > 2 :
                break

    return totalcount

CurrentTimeStamp = time.strftime('%x %X %Z')
print "Timestamp: ", CurrentTimeStamp

tempTuple = BuildURLList()
urlList = tempTuple[0]
urlDescriptionList = tempTuple[1]
print urlList
print urlDescriptionList

totalcount = BuildCurrentList(urlList, urlDescriptionList)

print "Run finished", totalcount
# End Program

