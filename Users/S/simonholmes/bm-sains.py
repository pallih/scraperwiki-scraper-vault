###############################################################################
# Sainsbury's scraper
# http://www.sainsburys.co.uk/sol/storelocator/storelocator_detail_view.jsp?storeId=640&bmForm=store_details
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def getDetails(soup):
    thisname = soup.find("div", { "class" : "name" }).text
    print "Getting details for " + str(i) + " " + thisname
    record = {}
    vcard = soup.find("div", { "class" : "vcard" })
    imgsrc = soup.find("div", { "class" : "storeInfo" }).findNext('img')['src']
    latlng = imgsrc[imgsrc.find("center=")+7:imgsrc.find("&")]
    from datetime import datetime
    record['ThisID'] = i
    record['BusinessID'] = ""
    record['ReferrerID'] = 2
    record['RepID'] = ""
    record['BusinessChainID'] = 1
    record['CompanyName'] = "Sainsbury's " + thisname
    record['BuildingName'] = ""
    record['ThoroughFare'] = vcard.find("div", { "class" : "fn" }).text
    record['ThoroughFare2'] = vcard.findAll("div", { "class" : "street-address" })[0].text
    record['DependentLocality'] = vcard.findAll("div", { "class" : "street-address" })[1].text
    record['Locality'] = vcard.find("div", { "class" : "locality" }).text
    record['PostalCode'] = vcard.find("div", { "class" : "postal-code" }).text
    record['Country'] = "United Kingdom"
    record['Lat'] = latlng[:latlng.find(",")]
    record['Lng'] = latlng[latlng.find(",")+1:]
    record['Verified'] = ""
    record['BusinessTypeID'] = 1
    record['BusinessTypeOther'] = ""
    record['BusinessSubCats'] = ",13,"
    record['BusinessSubCatOther'] = ""
    record['ChangingID'] = 1
    record['NursingID'] = 3
    record['Website'] = 'http://www.sainsburys.co.uk/sol/storelocator/storelocator_detail_view.jsp?storeId=' + str(i) + '&bmForm=store_details'
    record['ContactName'] = vcard.findAll("div", { "class" : "adr" })[1].text
    record['ContactPosition'] = "Store Manager"
    record['Telephone'] = vcard.find("div", { "class" : "tel" }).text
    record['Email'] = ""
    record['Fax'] = ""
    record['LastModified'] = datetime.now()
    record['CreationDate'] = datetime.now()
    record['UsagePolicyID'] = 2
    record['AddressStatusID'] = 1
    record['latlngStatusID'] = 1
    scraperwiki.datastore.save(["ThisID"], record)


for i in range(0,5000):
    print i
    # retrieve a page
    starting_url = 'http://www.sainsburys.co.uk/sol/storelocator/storelocator_detail_view.jsp?storeId=4621'
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    divs = soup.find("div", { "class" : "storeFacilities containerBox" })
    if divs:
        # test to see if storefacilities div exists
        lis = divs.findAll('li')
        for li in lis:
            thistext = li.text
            if thistext == "National Lottery": # test to see if facilities include baby changing
                getDetails(soup)
                break
    else:
        print "no store here"

