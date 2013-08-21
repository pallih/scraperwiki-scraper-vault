# Blank Python

print "Hello"

#import lxml.etree
import time
import lxml.html
import urllib
import scraperwiki
import random
import mechanize
#import re
from lxml.html import fromstring
from lxml.html import tostring

def UpdateRunStats(inCategoriesReadQty, inProductsReadQty, inRunStatus):
    runStatsData = {}
    runStatsData["RunStatus"] = inRunStatus
    runStatsData["RunTime"] = CurrentTimeStamp
    runStatsData["CategoriesReadQty"] = inCategoriesReadQty
    runStatsData["ProductsWrittenQty"] = inProductsReadQty
    scraperwiki.sqlite.save(["RunTime"], runStatsData, table_name = "RunStats")

    return

def BuildURLList():

    urlDescriptionList = []
    urlList = []
    urlDescriptionList.append("The Fest")
    urlList.append("http://www.thefest.com/")

#http://www.google.com/#q=beatles&hl=en&tbs=cat:2618&tbm=shop&fp=1&cad=b&bav=on.2,or.r_gc.r_pw.
#http://www.google.com/#q=beatles&hl=en&tbs=cat:2618&tbm=shop&fp=1&bav=on.2,or.r_gc.r_pw.&cad=b
#http://www.google.com/search?q=beatles&tbm=shop&hl=en&aq=f#q=beatles&hl=en&tbm=shop&source=lnt&tbs=cat:2618&sa=X&ei=GX5ITpHtLuOrsAKA543-BQ&ved=0CCgQpwU&bav=on.2,or.r_gc.r_pw.&fp=e812f2706985ae2e&biw=1024&bih=505



    return urlList, urlDescriptionList


def readUrl(inUrl):

    tryCount = 0
    while tryCount < 5 :
#        print "Create CookieJar"
        cookies = mechanize.CookieJar()
#        print "Build Opener"
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
#        print "Add Headers"
        opener.addheaders = [("User-agent", "Mozilla/5.0 (compatible; MyProgram/0.1)"),("From", "responsible.person@example.com")]
#        print "Install Opener"
        mechanize.install_opener(opener)
        try:
#            print "Open URL"
            response = mechanize.urlopen(inUrl)
            tryCount = 99
        except:
            tryCount += 1
            print "******** Error on urlopen ***********"
            print "URL: ", inUrl
            print "Trying Again....", tryCount

#    print response.read()
#    html = urllib.urlopen(inUrl).read()
#    print "Reading Response"
    html = response.read()
#    print "Response Read:", html[0:100]
    root = lxml.html.fromstring(html)
#    print "Root created: ", root

    return root


def productscrape(inUrl, categoryLinkCount, productLinkCount):

    def SaveTables():
        productData = {}
        productData['productOfferingID'] = None
        productData['productOfferingName'] = productName
        productData['productOfferingDescription'] = productDescription
        productData['productOfferingNormalPrice'] = productNormalPrice
        productData['productOfferingDiscountPrice'] = productDiscountPrice
        productData['productOfferingCatalogueNumber'] = productCatalogueNumber
        productData['productOfferingCategory'] = productCategory[-1].text
        productData['productOfferingPicture'] = productPicture
        productData['timestamp'] = CurrentTimeStamp
        productData['source'] = inUrl
        scraperwiki.sqlite.save(["productOfferingName", "productOfferingCatalogueNumber"], productData, table_name="Product Offering")

        UpdateRunStats(categoryLinkCount, productLinkCount, "Run In Progress")

        return

    productNameTag = "//h1[@id='productName']"
    productDescriptionTag = "//div[@id='productDescription']"
    productPriceTag = "//h2[@id='productPrices']"
    productNormalPriceTag = "//span[@class='normalprice']"
    productDiscountPriceTag = "//span[@class='productSpecialPrice']"
    productCatalogueTag = "//div[@id='productDetailsList']"
    productPictureTag = "//link[contains(@href,'http://www.thefest.com/store/images/products')]"
    listProductLinksTag = "//div[contains(@class,'CenterBoxContentsProducts')]"
    listCategoryTag = "//div[@id='navBreadCrumb']//a"

#<H1 id=productName class=productGeneral>COLLECTIBLE 1962 PEN</H1>
#<H2 id=productPrices class=productGeneral>$98.00</H2>
#<DIV id=productDescription class="productGeneral biggerText">BRAND NEW- LIMITED EDITION- The manufacturer apologizes but due to the unprecedented scope of this project delivery will be delayed until August. Over the next 2 years, this new licensee will be offering a series of 9 pens one for each year commemorating 1962 thru 1970 , In order to ensure you will have a chance to complete the collection, we will first offer the next in the series to the earliest purchasers of the former edition pen.</DIV>
#<DIV id=productDetailsList class="floatingBox back">Catalogue Number: 3501 </DIV>
#<link href="http://www.thefest.com/store/images/products/3501.JPG" rel="image_src"/>
#<DIV id=navBreadCrumb><A href="http://www.thefest.com/store/">Store</A>&nbsp;::&nbsp; <A href="http://www.thefest.com/store/beatles-collectible-pens-c-418?zenid=ehf9re9gqklv9ctrp7l6faron7">Beatles Collectible Pens</A>&nbsp;::&nbsp; COLLECTIBLE 1962 PEN </DIV>

#    print "Reading URL", inUrl
    root = readUrl(inUrl)
    productName = root.xpath(productNameTag)[0].text
    productDescription = root.xpath(productDescriptionTag)
    if len(productDescription) == 0:
        productDescription = None
    else:
        productDescription = " ".join(productDescription[0].text_content().split())
    productPrice = root.xpath(productPriceTag)[0].text
#    print productPrice
#    print "Length of price: ", len(productPrice)
    if len(productPrice) < 3 :
        productNormalPrice = root.xpath(productNormalPriceTag)[0].text.split()[-1]
        print "Normal Price: ", productNormalPrice
        productDiscountPrice = root.xpath(productDiscountPriceTag)[0].text.split()[-1]
        print "Discount Price: ", productDiscountPrice
    else:
        productNormalPrice = productPrice.split()[-1]
        productDiscountPrice = None
#    productPrice = root.xpath(productPriceTag)[0].text.split()[-1]
    productCatalogueNumber = root.xpath(productCatalogueTag)[0].text.split()[-1]
    productPicture = root.xpath(productPictureTag)
    if len(productPicture) == 0:
        productPicture = None
    else:
        productPicture = productPicture[0].get("href")
    productCategory = root.xpath(listCategoryTag)

#    print "Product Name: ", productName
    SaveTables()
#    print "Product Description: ", productDescription
#    print "Product Price: ", productPrice
#    print "Product Catalogue Number: ", productCatalogueNumber
#    print "Product Picture: ", productPicture
#    print "ProductCategory list", productCategory
#    for category in productCategory :
#        print "Category: ", category.text

#    productData = {}
#    productData['productOfferingID'] = None
#    productData['productOfferingName'] = productName
#    productData['productOfferingDescription'] = productDescription
#    productData['productOfferingPrice'] = productPrice
#    productData['productOfferingCatalogNumber'] = productCatalogueNumber
#    productData['productOfferingPicture'] = productPicture
#    productData['productOfferingCategory'] = productCategory[-1].text
#    productData['timestamp'] = CurrentTimeStamp
#    productData['source'] = None
#    scraperwiki.sqlite.save(["productOfferingName"], productData, table_name="Product Offering")

#    categoryList = []
#    ListProductLinks = root.xpath(listProductLinksTag)
#    productList = []
#    print str(len(ListCategoryLinks)) + " Category Links"
#    print str(len(ListProductLinks)) + " Product Links"
#    if len(ListCategoryLinks) != 0:
#        listIndex = 0
#        for element in (ListCategoryLinks):
#            tempHref = element.get("href")
#            print tempHref
#            page1 = readUrl(tempHref)
#            print page1

    return 


def categorysearch(inUrl):

    firstPageCategoryLinksTag = "//div[@class='category_table']//a"
    categoryPageCategoryLinksTag = "//div[contains(@class,'categoryListBoxContents')]//a"
    listProductLinksTag = "//div[contains(@class,'centerBoxContentsProducts')]//h3/a"
    categoryNextPageTag = "//a[contains(@title,'Next Page')]"
    categoryPageCount = 0
    productPageCount = 0

 #   print "Reading URL"
    root = readUrl(inUrl)
    categoryPageCount += 1
    print "Category Page Read Count: ", categoryPageCount
    categoryList = root.xpath(firstPageCategoryLinksTag)
    productList = root.xpath(listProductLinksTag)
    newCategoryList = []
    categoryLinkCount = 0
    productLinkCount = 0
    loopCounter = 1
    while len(categoryList) != 0:

        print "Loop Counter = ", loopCounter, "length = ", len(categoryList)
        loopCounter += 1
        print str(len(categoryList)) + " Category Links"
        print str(len(productList)) + " Product Links"
        for1Counter = 1
        for listIndex, element in enumerate(categoryList):
            tempHref = element.get("href")
            print "Category For Counter = ", for1Counter, "length = ", len(categoryList), "   URL = ...", tempHref[-30:]
            for1Counter += 1
            page1 = readUrl(tempHref)
            categoryPageCount += 1
   #         print "Category Page Read Count: ", categoryPageCount
            categoryLinkCount += 1
   #         print "Total Categories: ", categoryLinkCount
            newCategoryList.extend(page1.xpath(categoryPageCategoryLinksTag))
            nextPageLink = page1.xpath(categoryNextPageTag)
            if len(nextPageLink) > 0 :
                newCategoryList.append(nextPageLink[0])
#                print "Next Page: ", nextPageLink[0]
            productList.extend(page1.xpath(listProductLinksTag))
            for2Counter = 1
            for productIndex, productLink in enumerate(productList):
                tempHref = productLink.get("href")
                print "Product For Counter = ", for2Counter, "length = ", len(productList), "   URL = ", tempHref[-30:]
                for2Counter += 1
#                print tempHref
                productscrape(tempHref, categoryLinkCount, productLinkCount)
                productPageCount += 1
   #             print "Product Page Read Count: ", productPageCount
                productLinkCount += 1
   #             print "Total Products: ", productLinkCount
            productList = []
        categoryList = newCategoryList
        newCategoryList = []


    print "Grand Total Categories: ", categoryLinkCount
    print "Grand Total Products: ", productLinkCount

    return categoryLinkCount, productLinkCount


def BuildCurrentList(urlList, urlDescriptionList):
    currentList = []
    addedCounter = 0
    for listIndex, url in enumerate(urlList):
        categoryList = []
        productList = []
        categoryLinkCount, productLinkCount = categorysearch(url)
#        for item in categoryList:
#            auctionData = {}
#            auctionData['auctionNumber'] = item
#            auctionData['timestamp'] = CurrentTimeStamp
#            auctionData['sourceDescription'] = urlDescriptionList[listIndex]
#            addedCounter += 1
#            currentList.append(auctionData)
#        print len(productList), "items found in search: ", url
#        print productList

    return categoryLinkCount, productLinkCount


CurrentTimeStamp = time.strftime('%x %X %Z')
print "Timestamp: ", CurrentTimeStamp

UpdateRunStats(0,0,"Begin Run")

tempTuple = BuildURLList()
urlList = tempTuple[0]
urlDescriptionList = tempTuple[1]
print urlList
print urlDescriptionList

categoryLinkCount, productLinkCount = BuildCurrentList(urlList, urlDescriptionList)
print "Grand Total Categories: ", categoryLinkCount
print "Grand Total Products: ", productLinkCount

UpdateRunStats(categoryLinkCount, productLinkCount, "Run Finished")


# End Program


