###############################################################################
# PH scraper
# http://www.pizzahut.co.uk/restaurants/find-a-hut/map-info.aspx?storeid=993&d=140
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def getDetails(divs):
    content = divs.find("div",{"class":"left"}).findAll("p")
    #print content[0]
    thisname = content[0].find("strong").text
    print "Getting details for " + str(i) + ": " + thisname
    address = content[0].findAll(text=True)
    adrlast = len(address)
    add3 = address[adrlast-1].strip() # postcode
    add2b = address[adrlast-2].strip() # locality
    add2a = address[adrlast-3].strip() # dependent locality
    add1a = address[2].strip()
    if adrlast > 6:
        add1b = address[3].strip()
    else:
        add1b = ""
    from datetime import datetime
    record = {}
    record['ThisID'] = i
    record['BusinessID'] = ""
    record['ReferrerID'] = 2
    record['RepID'] = ""
    record['BusinessChainID'] = 13
    record['CompanyName'] = thisname
    record['BuildingName'] = ""
    record['ThoroughFare'] = add1a
    record['ThoroughFare2'] = add1b
    record['DependentLocality'] = add2a
    record['Locality'] = add2b
    record['PostalCode'] = add3
    record['Country'] = "United Kingdom"
    record['Lat'] = ""
    record['Lng'] = ""
    record['Verified'] = ""
    record['BusinessTypeID'] = 1
    record['BusinessTypeOther'] = ""
    record['BusinessSubCats'] = ",2,"
    record['BusinessSubCatOther'] = ""
    record['ChangingID'] = 1
    record['NursingID'] = 3
    record['Website'] = 'http://www.pizzahut.co.uk/restaurants/find-a-hut/map-info.aspx?storeid=' + str(i) + '&d=140'
    record['ContactName'] = ""
    record['ContactPosition'] = ""
    record['Telephone'] = content[1].find("strong").text
    record['Email'] = ""
    record['Fax'] = ""
    record['LastModified'] = datetime.now()
    record['CreationDate'] = datetime.now()
    record['UsagePolicyID'] = 1
    record['AddressStatusID'] = 1
    record['latlngStatusID'] = 2
    scraperwiki.datastore.save(["ThisID"], record)


for i in range(30,1000):
    print i
    # retrieve a page
    starting_url = 'http://www.pizzahut.co.uk/restaurants/find-a-hut/map-info.aspx?storeid=' + str(i) + '&d=140'
    #print "opening page " + starting_url 
    html = scraperwiki.scrape(starting_url)
    #print "making soup"
    soup = BeautifulSoup(html)
    divs = soup.find("div", { "class" : "inner" })
    if divs:
        # print "Found content"
        services = divs.find("ul", {"class" : "services"})
        if services:
            lis = services.findAll("li")
            for li in lis:
                if li.text == "Baby changing":
                    getDetails(divs)
                    break
        else:
            print "no services"
    else:
        print "no store here"


###############################################################################
# PH scraper
# http://www.pizzahut.co.uk/restaurants/find-a-hut/map-info.aspx?storeid=993&d=140
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def getDetails(divs):
    content = divs.find("div",{"class":"left"}).findAll("p")
    #print content[0]
    thisname = content[0].find("strong").text
    print "Getting details for " + str(i) + ": " + thisname
    address = content[0].findAll(text=True)
    adrlast = len(address)
    add3 = address[adrlast-1].strip() # postcode
    add2b = address[adrlast-2].strip() # locality
    add2a = address[adrlast-3].strip() # dependent locality
    add1a = address[2].strip()
    if adrlast > 6:
        add1b = address[3].strip()
    else:
        add1b = ""
    from datetime import datetime
    record = {}
    record['ThisID'] = i
    record['BusinessID'] = ""
    record['ReferrerID'] = 2
    record['RepID'] = ""
    record['BusinessChainID'] = 13
    record['CompanyName'] = thisname
    record['BuildingName'] = ""
    record['ThoroughFare'] = add1a
    record['ThoroughFare2'] = add1b
    record['DependentLocality'] = add2a
    record['Locality'] = add2b
    record['PostalCode'] = add3
    record['Country'] = "United Kingdom"
    record['Lat'] = ""
    record['Lng'] = ""
    record['Verified'] = ""
    record['BusinessTypeID'] = 1
    record['BusinessTypeOther'] = ""
    record['BusinessSubCats'] = ",2,"
    record['BusinessSubCatOther'] = ""
    record['ChangingID'] = 1
    record['NursingID'] = 3
    record['Website'] = 'http://www.pizzahut.co.uk/restaurants/find-a-hut/map-info.aspx?storeid=' + str(i) + '&d=140'
    record['ContactName'] = ""
    record['ContactPosition'] = ""
    record['Telephone'] = content[1].find("strong").text
    record['Email'] = ""
    record['Fax'] = ""
    record['LastModified'] = datetime.now()
    record['CreationDate'] = datetime.now()
    record['UsagePolicyID'] = 1
    record['AddressStatusID'] = 1
    record['latlngStatusID'] = 2
    scraperwiki.datastore.save(["ThisID"], record)


for i in range(30,1000):
    print i
    # retrieve a page
    starting_url = 'http://www.pizzahut.co.uk/restaurants/find-a-hut/map-info.aspx?storeid=' + str(i) + '&d=140'
    #print "opening page " + starting_url 
    html = scraperwiki.scrape(starting_url)
    #print "making soup"
    soup = BeautifulSoup(html)
    divs = soup.find("div", { "class" : "inner" })
    if divs:
        # print "Found content"
        services = divs.find("ul", {"class" : "services"})
        if services:
            lis = services.findAll("li")
            for li in lis:
                if li.text == "Baby changing":
                    getDetails(divs)
                    break
        else:
            print "no services"
    else:
        print "no store here"


