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

def BuildURLList():

    urlDescriptionList = []
    urlList = []
#itemList.append('280712217861')  #current auction
#itemList.append('370527941606')  #current auction
#itemList.append('170659691608')  #finished auction
#itemList.append('360377819874')  #loufar4 current auction
#itemList.append('290589853392')  #finished auction with different picture URL

    for i in range(1,30):
        urlDescriptionList.append("beatles music memorabilia category")
        urlList.append("http://www.ebay.com/sch/Beatles-/29924/i.html?&rt=nc&_catref=1&_ipg=200&_sc=1&_sop=10&_trksid=p3286.c0.m2000018.l2552&_pgn="+str(i))

    for i in range(1,30):
        urlDescriptionList.append("beatles search")
        urlList.append("http://www.ebay.com/sch/i.html?_nkw=beatles&_in_kw=1&_ex_kw=&_sacat=See-All-Categories&_okw=beatles&_oexkw=&_adv=1&_udlo=&_udhi=&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=200&_fpos=Zip+code&_fsct=&LH_SALE_CURRENCY=0&_sop=10&_dmd=7&_ipg=200&_pgn="+str(i))
    
    return urlList, urlDescriptionList


def fetchelement(inElement, inTag):
    element = inElement.xpath(inTag)
    return element

def checklength(inList,inLength):
    if len(inList) != inLength:
        print "******Length not correct"
        print "Length of list is: ", len(inList), " but should be: ", inLength
    return

def saveRecord(inKey, inData, inTable):
    scraperwiki.sqlite.save(inKey,inData,inTable)
    return

def auctionsearch(inUrl):

    addedCounter = 0
    listItemNumberGroupTag = "//div[@class='lview']//td[@class='dtl']/div/a"
    listItemBeginTag = "//div[@class='lview']//table"
    itemPriceTag = "//span[contains(@class, 'vi-is1-prcp')]"
#    listItemNumberTag = "descendant::td[@class='dtl']/div/a"
    listItemNumberTag = "//td[@class='dtl']/div/a"
    listItemPictureTag = "//td[contains(@class,'pic')]"
    itemPictureTag = "descendant::img"
    listItemTypeTag = "//td[contains(@class,'bids')]"
    listItemPriceTag = "//td[contains(@class,'prc')]"
    listItemDateTag = "//td[contains(@class,'tme')]//span"
    invalidread = 1
    while invalidread :
        print "Reading auctionsearch URL"
        html = urllib.urlopen(inUrl).read()
        print html
        root = lxml.html.fromstring(html)
        try:
            currentElement = root.xpath(listItemBeginTag)[0]
            invalidread = 0
        except:
            invalidread = 1
    print currentElement
    listItemNumberGroup = root.xpath(listItemNumberGroupTag)
    listItemNumber = []
    itemList = []
    itemQty = len(listItemNumberGroup)
    print itemQty
    x1 = fetchelement(currentElement, listItemNumberTag)
    checklength(x1, 200)
    x2 = fetchelement(currentElement, listItemPictureTag)
    checklength(x2, 200)
    x3 = fetchelement(currentElement, listItemPriceTag)
    checklength(x3, 200)
    x4 = fetchelement(currentElement, listItemTypeTag)
    checklength(x4, 200)
    x5 = fetchelement(currentElement, listItemDateTag)
    checklength(x5, 200)
    for i in range(itemQty):
#        print i
        tempHref = x1[i].get("href")
        tempTitle = x1[i].get("title")
#        print tempTitle
        tempSplitHrefArray = tempHref.split("/")
        tempItemNumber = tempSplitHrefArray[5].split("?")[0]
        print tempItemNumber, tempTitle
        try:
            tempPictureFileName = x2[i].xpath(itemPictureTag)[0].get("src")
        except:
            tempPictureFileName = None
#        print tempPictureFileName
        tempPriceGroup = x3[i].xpath("descendant::div")
        if len(tempPriceGroup) == 0 :
            tempPrice1 = x3[i].text
            tempPrice2 = None
        else:
            tempPrice1 = tempPriceGroup[0].text
            tempPrice2 = tempPriceGroup[1].text
#        print tempPrice1
#        print tempPrice2
        tempTypeGroup = x4[i].xpath("descendant::div|descendant::b")
#        print tempTypeGroup
        if len(tempTypeGroup) == 0 :
            tempType1 = x4[i].text.strip()
            tempType2 = None
        elif len(tempTypeGroup) == 1 :
            tempType1 = x4[i].text.strip()
            tempType2 = tempTypeGroup[0].text
        else:
            tempType1 = tempTypeGroup[0].text
            tempType2 = tempTypeGroup[1].text
#        print tempType1, tempType1 == "Buy It Now", "***"+tempType1+"***"
#        print tempType2
        tempDateTime = str(parse(x5[i].text))   #.split()
        tempDate = tempDateTime
#        print tempDateTime
        newData = {}
        newData['itemBestOfferFlag'] = 0   #default to 0, but may be overridden later
        newData['itemNumber'] = tempItemNumber
        newData['itemTitle'] = tempTitle
        newData['itemCurrentPrice'] = tempPrice1

        if tempType1 == "Buy It Now":
            newData['itemBuyNowPrice'] = tempPrice1
        elif tempType2 == "Buy It Now":
            newData['itemBuyNowPrice'] = tempPrice2
        else:
            newData['itemBuyNowPrice'] = None

        if tempType1 == "Buy It Now":
            newData['itemBuyNowFlag'] = 1
            if tempType2 != None and tempType2.split()[-1] == "Offer" :
                newData['itemBestOfferFlag'] = 1
        elif tempType2 == "Buy It Now":
            newData['itemBuyNowFlag'] = 1
        else:
            newData['itemBuyNowFlag'] = 0

        if tempType1.split()[-1] == "Bids" or tempType1.split()[-1] == "Bid":
            newData['itemAuctionFlag'] = 1
            newData['itemNumberBids'] = tempType1.split()[0]
        else:
            newData['itemAuctionFlag'] = 0

        newData['itemDateTime'] = tempDateTime

#        print newData

        saveRecord(['itemNumber'], newData, 'Auction')
        addedCounter += 1

#    print stophere

    return addedCounter


def BuildCurrentList(urlList, urlDescriptionList):
    currentList = []
    addedCounter = 0
    totalcount = 0
    for listIndex, url in enumerate(urlList):
        itemList = []
        addedCounter = auctionsearch(url)
        totalcount += addedCounter

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

