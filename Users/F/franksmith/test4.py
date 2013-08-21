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

scraperwiki.sqlite.attach("test3_3")

CurrentTimeStamp = time.strftime('%x %X %Z')
print "Timestamp: ", CurrentTimeStamp

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
#      print tempHref
      tempSplitHrefArray = tempHref.split("/")
      tempListItemNumber = tempSplitHrefArray[4].split("?")[0]
#      print tempListItemNumber
      itemList.append(tempListItemNumber)


  return itemList


urlDescriptionList = []
urlList = []
#itemList.append('280712217861')  #current auction
#itemList.append('370527941606')  #current auction
#itemList.append('170659691608')  #finished auction
#itemList.append('360377819874')  #loufar4 current auction
#itemList.append('290589853392')  #finished auction with different picture URL
urlDescriptionList.append("beatle*+lennon+mccartney, NoB>0")
urlList.append("http://entertainment-memorabilia.shop.ebay.com/Entertainment-Memorabilia-/45100/i.html?LH_NOB=1..9%2C999&_nkw=%28beatle*%2C+lennon%2C+mccartney%29&rt=nc&_LH_NOB=1&_adv=1&_fsct=&_in_kw=2&_ipg=200&_oexkw=&_okw=beatle*+lennon+mccartney&_sc=1&_sop=16&_udhi=&_udlo=")

currentList = scraperwiki.sqlite.select("* from test3_3.auctionStatus")
print currentList

# First, delete anything in currentList that has ended
#   If it hasn't ended, add it to the list of still active auctions

auctionStatusItemNumber = []
auctionStatusData = []
deletedCounter = 0
for auctionStatusData in currentList:
  if "ended" in auctionStatusData["auctionStatusCode"]:
    print "Auction ended: ", auctionStatusData["auctionNumber"], auctionStatusData["auctionStatusCode"]
    sql = 'delete from auction where auctionNumber = "%s"' % auctionStatusData["auctionNumber"]
    print sql
    try:
      scraperwiki.sqlite.execute(sql)
#    scraperwiki.sqlite.execute("select * from table_that_doesnot_exist")
    except scraperwiki.sqlite.SqliteError, e:
      print str(e)
      print stophere
    scraperwiki.sqlite.commit()
    print "Auction deleted: ", auctionStatusData["auctionNumber"]
    deletedCounter += 1
  else:
    print "Auction kept: ", auctionStatusData["auctionNumber"]
    auctionStatusItemNumber.append(auctionStatusData["auctionNumber"])

print deletedCounter, "auctions deleted"

print auctionStatusItemNumber
  
addedCounter = 0
for listIndex, url in enumerate(urlList):
  itemList = []
  itemList = auctionsearch(url)
  for item in itemList:
    #print item, auctionStatusItemNumber
    if item not in auctionStatusItemNumber :
      auctionData = {}
      auctionData['auctionNumber'] = item
      auctionData['auctionStatusCode'] = "New"
      auctionData['timestamp'] = CurrentTimeStamp
      auctionData['sourceDescription'] = urlDescriptionList[listIndex]
      addedCounter += 1
      scraperwiki.sqlite.save(["auctionNumber"], auctionData, table_name="auction")

print addedCounter, "auctions added"
# End Program

