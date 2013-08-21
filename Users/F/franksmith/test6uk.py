# Blank Python

print "Hello"

#import lxml.etree
import time
import lxml.html
import urllib
import scraperwiki
import time
import random
import mechanize
#import re
from lxml.html import fromstring
from lxml.html import tostring

def BuildURLList():

    urlDescriptionList = []
    urlList = []
#itemList.append('280712217861')  #current auction
#itemList.append('370527941606')  #current auction
#itemList.append('170659691608')  #finished auction
#itemList.append('360377819874')  #loufar4 current auction
#itemList.append('290589853392')  #finished auction with different picture URL
#    urlDescriptionList.append("beatle*+lennon+mccartney, NoB>0")
#    urlList.append("http://entertainment-memorabilia.shop.ebay.com/Entertainment-Memorabilia-/45100/i.html?LH_NOB=1..9%2C999&_nkw=%28beatle*%2C+lennon%2C+mccartney%29&rt=nc&_LH_NOB=1&_adv=1&_fsct=&_in_kw=2&_ipg=200&_oexkw=&_okw=beatle*+lennon+mccartney&_sc=1&_sop=16&_udhi=&_udlo=")


    urlDescriptionList.append("beatle*+lennon+mccartney, NoB>0")
    urlList.append("http://www.ebay.co.uk/sch/i.html?LH_Auction=1&_sadis=200&LH_SALE_CURRENCY=0&_sacat=0&_ftrt=901&_sabdhi=999&_ftrv=1&_sabdlo=1&_adv=1|1&_sop=3&_nkw=%28%28beatle*%2C%2C+lennon%2C%2C+%22george+harrison%22%2C%2C+ringo%2C%2C+mccartney%29%29&_dmd=1&_okw=beatle*+lennon+mccartney&_LH_NOB=1&LH_NOB=1&_ipg=200&rt=nc")

    for i in range(2,10):
        urlDescriptionList.append("beatle*+lennon+mccartney, NoB>0")
        urlList.append("http://www.ebay.co.uk/sch/i.html?LH_Auction=1&_sadis=200&LH_SALE_CURRENCY=0&_sacat=0&_ftrt=901&_sabdhi=999&_ftrv=1&_sabdlo=1&_adv=1|1&_sop=3&_nkw=%28%28beatle*%2C%2C+lennon%2C%2C+%22george+harrison%22%2C%2C+ringo%2C%2C+mccartney%29%29&_dmd=1&_okw=beatle*+lennon+mccartney&_LH_NOB=1&LH_NOB=1&_ipg=200&_skc=" + str((i-1)*200) + "&rt=nc&_pgn="+str(i))

#    urlDescriptionList.append("Sellers: loufar4, perrydcox, justrelax831, seltaeb65")
#    urlList.append("http://shop.ebay.com/i.html?_nkw=&_in_kw=1&_ex_kw=&_sacat=See-All-Categories&_okw=&_oexkw=&_adv=1&_udlo=&_udhi=&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=200&_fpos=Zip+code&_fsct=&LH_SALE_CURRENCY=0&_fss=1&_fsradio=%26LH_SpecificSeller%3D1&_saslop=1&_sasl=loufar4%2C+perrydcox%2C+justrelax831%2C+seltaeb65&_sop=10&_dmd=1&_ipg=200")


    urlDescriptionList.append("beatle*+lunch box+mastro+dimensional+record player+revell+notebook")
    urlList.append("http://shop.ebay.co.uk/i.html?_nkw=beatle*+%28%22lunch+box%22%2Cmastro%2Cdimensional%2C%22record+player%22%2Crevell%2Cnotebook%29&_in_kw=1&_ex_kw=&_sacat=See-All-Categories&_okw=beatle*+%28%22lunch+box%22%2Cmastro%2Cdimensional%2C%22record+player%22%2Crevell%2Cnotebook%29&_oexkw=&_adv=1&_udlo=&_udhi=&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=200&_fpos=Zip+code&_fsct=&LH_SALE_CURRENCY=0&_sop=10&_dmd=1&_ipg=200")


    urlDescriptionList.append("beatle*+remco+selcol+primrose+anglo+jaymar+lilo+mascot+brooch")
    urlList.append("http://shop.ebay.co.uk/i.html?_nkw=beatle*+%28remco%2Cselcol%2Cprimrose%2Canglo%2Cjaymar%2Clilo%2Cmascot%2Cbrooch%29&_sacat=0&_sop=10&_dmd=1&_odkw=beatle*+%28remco%2Cselcol%2Cprimrose%2Canglo%2Cjaymar%2Clilo%29&_osacat=0")


    urlDescriptionList.append("yellow sub*")
    urlList.append("http://www.ebay.co.uk/sch/i.html?_sop=1&_sacat=0&_nkw=yellow+sub*+%2868%2Cdimensional%2Cnotebook%2Cmodel%2Cgoebel%2Ccorgi%2Changer%2Cpromo*%2Cvintage%29+-%28invicta%2C+rolex%29&_dmd=1&_ipg=200&rt=nc")

    return urlList, urlDescriptionList


def auctionsearch(inUrl):

    listItemNumberGroupTag = "//div[@class='lview']//td[@class='dtl']/div/a"
    listItemNumberGroupTag = "//table[@class='li rsittlref']//td[@class='dtl']/div/a"  #replaced above tag on 3/13/12
    listItemNumberGroupTag = "//div[@class='lview']//td[@class='dtl']/div/a"           #replaced above tag on 4/18/12
    listItemNumberGroupTag = "//div[@id='Results']//td[@class='dtl']/div/a"           #replaced above tag on 4/24/12
    listItemNumberGroupTag = "//div[@class='lview']//td[@class='dtl']/div/a"           #start the uk version with this tag 5/4/12
    listItemNumberGroupTag = "//div[@id='Results']//td[@class='dtl']/div/a"           #replaced above tag on 6/16/12

    print "Reading auctionsearch URL"
    html = urllib.urlopen(inUrl).read()
    print html
    root = lxml.html.fromstring(html)
#    br = mechanize.Browser()
#    # Fake the user-agent - if the page knows we're Mechanize, it won't return all fields
#    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#    br.open(inUrl)
#    root = lxml.html.fromstring(br.response().read())
#    print br.response().read()
#    print root


    ListItemNumberGroup = root.xpath(listItemNumberGroupTag)
    ListItemNumber = []
    itemList = []
    print str(len(ListItemNumberGroup)) + " List Item Number Group Nodes"
    if len(ListItemNumberGroup) != 0:
        listIndex = 0
        for element in (ListItemNumberGroup):
            tempHref = element.get("href")
#            print tempHref
            tempSplitHrefArray = tempHref.split("/")
            tempListItemNumber = tempSplitHrefArray[5].split("?")[0]
#            print tempListItemNumber
            itemList.append(tempListItemNumber)
    return itemList


def BuildCurrentList(urlList, urlDescriptionList):
    currentList = []
    addedCounter = 0
    for listIndex, url in enumerate(urlList):
        itemList = []
        itemList = auctionsearch(url)
        for item in itemList:
            auctionData = {}
            auctionData['auctionNumber'] = item
            auctionData['timestamp'] = CurrentTimeStamp
            auctionData['sourceDescription'] = urlDescriptionList[listIndex]
            addedCounter += 1
            currentList.append(auctionData)
        print addedCounter, "items found in search: ", url

    return currentList





#scraperwiki.sqlite.attach("test3_4")

CurrentTimeStamp = time.strftime('%x %X %Z')
print "Timestamp: ", CurrentTimeStamp

tempTuple = BuildURLList()
urlList = tempTuple[0]
urlDescriptionList = tempTuple[1]
print urlList
print urlDescriptionList

currentList = BuildCurrentList(urlList, urlDescriptionList)
print currentList
print "Number of Records to Save: ", len(currentList)

scraperwiki.sqlite.execute("delete from newTable")
scraperwiki.sqlite.commit()

### Limit the list to only selected items
#currentList = []
#currentList.append({"auctionNumber":'190585013146'})
### 
#newData = {}
#for item in currentList :
#    newData["auctionNumber"] = item["auctionNumber"]
#    newData["currentTimeStamp"] = CurrentTimeStamp
#    scraperwiki.sqlite.save(["auctionNumber"], newData, table_name = "newTable", verbose = 0)

scraperwiki.sqlite.save(["auctionNumber"], currentList, table_name = "newTable", verbose = 0)

# End Program

