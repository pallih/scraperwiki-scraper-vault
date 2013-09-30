import mechanize
import lxml.html
import scraperwiki
import re

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
argosList = "http://www.argos.co.uk/webapp/wcs/stores/servlet/ArgosGSFindGiftListView?langId=-1&storeId=10001&GiftMode=Reset"

#286/6455
#467266

br = mechanize.Browser()
response = br.open(argosList)


allforms = list(br.forms())
print "There are %d forms" % len(allforms)

br.select_form(nr=1)
print "The controls of this form are", br.form

# put some values into the form
br["referenceNumber"] = "467266"

# submit and show what we have got
response = br.submit()



datasheet = response.read()
print datasheet

root = lxml.html.fromstring(datasheet)
print root

prodname = root.cssselect("td.product")
prodcatno = root.cssselect("td.catno")
prodqty = root.cssselect("td.qty")
prodprice = root.cssselect("td.price")

print "There are %d items on your shopping list" % len(prodname)

#print "Their corresponding attributes are:", [td.attrib  for td in prodname ]
#print lxml.html.tostring(prodname[0])

scraperwiki.sqlite.execute("drop table if exists swdata")

for index, item in enumerate(prodname):
    prodnameBig = lxml.html.tostring(prodname[index])
    prodnameBig = prodnameBig.replace('<td class="product">', '')
    prodnameBig = prodnameBig.replace('</td>', '')
    prodnameBig = " ".join(prodnameBig.split())
    prodnameSearch = prodnameBig.replace(' ', '%20')

    prodcatnoBig = lxml.html.tostring(prodcatno[index])
    prodcatnoBig = prodcatnoBig.replace('<td class="catno">', '')
    prodcatnoBig = prodcatnoBig.replace('</td>', '')
    prodcatnoBig = " ".join(prodcatnoBig.split())
    prodcatnoRep = prodcatnoBig.replace('/', '')
   
    
    prodqtyBig = lxml.html.tostring(prodqty [index])
    prodqtyBig = prodqtyBig.replace('<td class="qty">', '')
    prodqtyBig = prodqtyBig.replace('</td>', '')
    prodqtyBig = " ".join(prodqtyBig.split())

    prodpriceBig = lxml.html.tostring(prodprice [index])
    prodpriceBig = prodpriceBig.replace('<td class="price">', '')
    prodpriceBig = prodpriceBig.replace('</td>', '')
    prodpriceBig = prodpriceBig.replace('&#163;', '')
    prodpriceBig = " ".join(prodpriceBig.split())

    productURL = "http://www.argos.co.uk/webapp/wcs/stores/servlet/Search?storeId=10001&catalogId=1500002701&langId=-1&searchTerms=" + prodnameSearch
    print productURL
    productRoot = lxml.html.parse(productURL).getroot()
    productRootString = lxml.html.tostring(productRoot)
    print productRootString
    stringMatch = re.search(r'<h1',productRootString)
    noresults = re.search(r'<h1>Your search',productRootString)
    # title = Results for  WHITE EGYPTIAN COTTON FITTED SHEET - DOUBLE - Argos.co.uk
    # title = Buy White Egyptian Cotton Fitted Sheet - Double at Argos.co.uk - Your Online Shop for Sheets.
    if stringMatch:
        if noresults:
            prodImg = "http://www.danandcaroline.co.uk/wp-content/themes/fadelicious/style/images/giftlist-missingproduct.png"
            prodSku = "n/a"
        else:
            imgTag = productRoot.cssselect("img#mainimage")[0]
            imgSrc = imgTag.get("src")
            prodImg = "http://www.argos.co.uk" + imgSrc
            #prodImg = "http://www.danandcaroline.co.uk/wp-content/themes/fadelicious/style/images/giftlist-missingproduct.png"
    
            prodSku= productRoot.cssselect("span.partnumber")[0]
            #print prodSku
            prodSku= lxml.html.tostring(prodSku)
            prodSku= prodSku.replace('<span class="partnumber sku">', '')
            prodSku= prodSku.replace('</span>', '')
    else:
        imgTag = productRoot.cssselect("img.searchProductImgList")[0]
        imgSrc = imgTag.get("src")
        prodImg = "http://www.argos.co.uk" + imgSrc
        #prodImg = "http://www.danandcaroline.co.uk/wp-content/themes/fadelicious/style/images/giftlist-missingproduct.png"
    
        prodSku= productRoot.cssselect("span.partnum")[0]
        #print prodSku
        prodSku= lxml.html.tostring(prodSku)
        prodSku= prodSku.replace('<span class="partnum">', '')
        prodSku= prodSku.replace('</span>', '')
        prodSku= prodSku.replace('\n', '')
        prodSku= prodSku.replace('\t', '')
    #prodSku= "tbc"

    #imgSrc = imgSrc.replace('/wcsstore/argos/images/', '')
    #imgSrc = imgSrc.replace('.jpg', '')
    #imgSrc = imgTag.src
    #print imgSrc
    #print "The image URL is: ", imgSrc

    #print prodnameBig, prodcatnoBig, prodqtyBig, prodpriceBig, prodImg
    
    dataArray = { "productName":prodnameBig, "catNo":prodSku, "quantity":prodqtyBig, "price":prodpriceBig, "image":prodImg }
    print dataArray
    

    scraperwiki.sqlite.save(unique_keys=["catNo", "productName"], data=dataArray)
   
print scraperwiki.sqlite.select("* from swdata")


import mechanize
import lxml.html
import scraperwiki
import re

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
argosList = "http://www.argos.co.uk/webapp/wcs/stores/servlet/ArgosGSFindGiftListView?langId=-1&storeId=10001&GiftMode=Reset"

#286/6455
#467266

br = mechanize.Browser()
response = br.open(argosList)


allforms = list(br.forms())
print "There are %d forms" % len(allforms)

br.select_form(nr=1)
print "The controls of this form are", br.form

# put some values into the form
br["referenceNumber"] = "467266"

# submit and show what we have got
response = br.submit()



datasheet = response.read()
print datasheet

root = lxml.html.fromstring(datasheet)
print root

prodname = root.cssselect("td.product")
prodcatno = root.cssselect("td.catno")
prodqty = root.cssselect("td.qty")
prodprice = root.cssselect("td.price")

print "There are %d items on your shopping list" % len(prodname)

#print "Their corresponding attributes are:", [td.attrib  for td in prodname ]
#print lxml.html.tostring(prodname[0])

scraperwiki.sqlite.execute("drop table if exists swdata")

for index, item in enumerate(prodname):
    prodnameBig = lxml.html.tostring(prodname[index])
    prodnameBig = prodnameBig.replace('<td class="product">', '')
    prodnameBig = prodnameBig.replace('</td>', '')
    prodnameBig = " ".join(prodnameBig.split())
    prodnameSearch = prodnameBig.replace(' ', '%20')

    prodcatnoBig = lxml.html.tostring(prodcatno[index])
    prodcatnoBig = prodcatnoBig.replace('<td class="catno">', '')
    prodcatnoBig = prodcatnoBig.replace('</td>', '')
    prodcatnoBig = " ".join(prodcatnoBig.split())
    prodcatnoRep = prodcatnoBig.replace('/', '')
   
    
    prodqtyBig = lxml.html.tostring(prodqty [index])
    prodqtyBig = prodqtyBig.replace('<td class="qty">', '')
    prodqtyBig = prodqtyBig.replace('</td>', '')
    prodqtyBig = " ".join(prodqtyBig.split())

    prodpriceBig = lxml.html.tostring(prodprice [index])
    prodpriceBig = prodpriceBig.replace('<td class="price">', '')
    prodpriceBig = prodpriceBig.replace('</td>', '')
    prodpriceBig = prodpriceBig.replace('&#163;', '')
    prodpriceBig = " ".join(prodpriceBig.split())

    productURL = "http://www.argos.co.uk/webapp/wcs/stores/servlet/Search?storeId=10001&catalogId=1500002701&langId=-1&searchTerms=" + prodnameSearch
    print productURL
    productRoot = lxml.html.parse(productURL).getroot()
    productRootString = lxml.html.tostring(productRoot)
    print productRootString
    stringMatch = re.search(r'<h1',productRootString)
    noresults = re.search(r'<h1>Your search',productRootString)
    # title = Results for  WHITE EGYPTIAN COTTON FITTED SHEET - DOUBLE - Argos.co.uk
    # title = Buy White Egyptian Cotton Fitted Sheet - Double at Argos.co.uk - Your Online Shop for Sheets.
    if stringMatch:
        if noresults:
            prodImg = "http://www.danandcaroline.co.uk/wp-content/themes/fadelicious/style/images/giftlist-missingproduct.png"
            prodSku = "n/a"
        else:
            imgTag = productRoot.cssselect("img#mainimage")[0]
            imgSrc = imgTag.get("src")
            prodImg = "http://www.argos.co.uk" + imgSrc
            #prodImg = "http://www.danandcaroline.co.uk/wp-content/themes/fadelicious/style/images/giftlist-missingproduct.png"
    
            prodSku= productRoot.cssselect("span.partnumber")[0]
            #print prodSku
            prodSku= lxml.html.tostring(prodSku)
            prodSku= prodSku.replace('<span class="partnumber sku">', '')
            prodSku= prodSku.replace('</span>', '')
    else:
        imgTag = productRoot.cssselect("img.searchProductImgList")[0]
        imgSrc = imgTag.get("src")
        prodImg = "http://www.argos.co.uk" + imgSrc
        #prodImg = "http://www.danandcaroline.co.uk/wp-content/themes/fadelicious/style/images/giftlist-missingproduct.png"
    
        prodSku= productRoot.cssselect("span.partnum")[0]
        #print prodSku
        prodSku= lxml.html.tostring(prodSku)
        prodSku= prodSku.replace('<span class="partnum">', '')
        prodSku= prodSku.replace('</span>', '')
        prodSku= prodSku.replace('\n', '')
        prodSku= prodSku.replace('\t', '')
    #prodSku= "tbc"

    #imgSrc = imgSrc.replace('/wcsstore/argos/images/', '')
    #imgSrc = imgSrc.replace('.jpg', '')
    #imgSrc = imgTag.src
    #print imgSrc
    #print "The image URL is: ", imgSrc

    #print prodnameBig, prodcatnoBig, prodqtyBig, prodpriceBig, prodImg
    
    dataArray = { "productName":prodnameBig, "catNo":prodSku, "quantity":prodqtyBig, "price":prodpriceBig, "image":prodImg }
    print dataArray
    

    scraperwiki.sqlite.save(unique_keys=["catNo", "productName"], data=dataArray)
   
print scraperwiki.sqlite.select("* from swdata")


