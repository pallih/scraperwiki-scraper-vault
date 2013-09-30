###############################################################################
# Harvester scraper
# http://www.harvester.co.uk/find-a-harvester/harvester-directory.html
# http://www.harvester.co.uk/find-a-harvester/alwalton.html
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def getDetails(soup):
    print "Getting details for " + thisname
    record = {}
    objaddress = soup.find("address")
    #print objaddress
    address = objaddress.findAll(text=True)
    adrlast = len(address)
    #print address
    #print adrlast
    add1a = address[0].strip()
    add3 = address[adrlast-1].strip() # postcode
    add2b = address[adrlast-2].strip() # locality
    if adrlast < 4:
        add1b = ""
    else:
        add1b = address[1].strip()
    if adrlast > 4:
        add2a = address[2].strip() # dependent locality
    else:
        add2a = ""
    #imgs = soup.find("div",{"id":"right_content"}).findAll("img")
    from datetime import datetime
    #imgsrc = imgs[0]['src']
    #latlng = imgsrc[imgsrc.find("center=")+7:imgsrc.find("&")]
    #contacts = content[1].findAll(text=True)
    thistel = soup.find("p",{"class":"telephone"}).find("span").text
    if thistel.find(" ") > -1:
        tel = thistel
    else:
        tel = thistel[:4] + " " + thistel[4:]
    from datetime import datetime
    record['ThisID'] = starting_url
    record['BusinessID'] = ""
    record['ReferrerID'] = 2
    record['RepID'] = ""
    record['BusinessChainID'] = 16
    record['CompanyName'] = thisname + " Harvester"
    record['BuildingName'] = ""
    record['ThoroughFare'] = add1a
    record['ThoroughFare2'] = add1b
    record['DependentLocality'] = add2a
    record['Locality'] = add2b
    record['PostalCode'] = add3.upper()
    record['Country'] = "United Kingdom"
    record['Lat'] = ""
    record['Lng'] = ""
    record['Verified'] = ""
    record['BusinessTypeID'] = 2
    record['BusinessTypeOther'] = ""
    record['BusinessSubCats'] = ",7,,8,"
    record['BusinessSubCatOther'] = ""
    record['ChangingID'] = 1
    record['NursingID'] = 3
    record['Website'] = starting_url
    record['ContactName'] = ""
    record['ContactPosition'] = ""
    record['Telephone'] = tel
    record['Email'] = ""
    record['Fax'] = ""
    record['LastModified'] = datetime.now()
    record['CreationDate'] = datetime.now()
    record['UsagePolicyID'] = 1
    record['AddressStatusID'] = 1
    record['latlngStatusID'] = 2
    scraperwiki.datastore.save(["ThisID"], record)


listurl = 'http://www.harvester.co.uk/find-a-harvester/harvester-directory.html'
listhtml = scraperwiki.scrape(listurl)
listsoup = BeautifulSoup(listhtml)
links = listsoup.findAll("a",{"class" : "search_result_title"})
#for i in range(1):
for a in links:
    print a['href']
    if a['href'].find("france") == -1:
        starting_url = a['href']
        html = scraperwiki.scrape(starting_url)
        soup = BeautifulSoup(html)
        objaddress = soup.find("address")
        if objaddress:
            # test to see if storefacilities div exists
            thisname = a.text
            getDetails(soup)
        else:
            print "no info here"


###############################################################################
# Harvester scraper
# http://www.harvester.co.uk/find-a-harvester/harvester-directory.html
# http://www.harvester.co.uk/find-a-harvester/alwalton.html
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def getDetails(soup):
    print "Getting details for " + thisname
    record = {}
    objaddress = soup.find("address")
    #print objaddress
    address = objaddress.findAll(text=True)
    adrlast = len(address)
    #print address
    #print adrlast
    add1a = address[0].strip()
    add3 = address[adrlast-1].strip() # postcode
    add2b = address[adrlast-2].strip() # locality
    if adrlast < 4:
        add1b = ""
    else:
        add1b = address[1].strip()
    if adrlast > 4:
        add2a = address[2].strip() # dependent locality
    else:
        add2a = ""
    #imgs = soup.find("div",{"id":"right_content"}).findAll("img")
    from datetime import datetime
    #imgsrc = imgs[0]['src']
    #latlng = imgsrc[imgsrc.find("center=")+7:imgsrc.find("&")]
    #contacts = content[1].findAll(text=True)
    thistel = soup.find("p",{"class":"telephone"}).find("span").text
    if thistel.find(" ") > -1:
        tel = thistel
    else:
        tel = thistel[:4] + " " + thistel[4:]
    from datetime import datetime
    record['ThisID'] = starting_url
    record['BusinessID'] = ""
    record['ReferrerID'] = 2
    record['RepID'] = ""
    record['BusinessChainID'] = 16
    record['CompanyName'] = thisname + " Harvester"
    record['BuildingName'] = ""
    record['ThoroughFare'] = add1a
    record['ThoroughFare2'] = add1b
    record['DependentLocality'] = add2a
    record['Locality'] = add2b
    record['PostalCode'] = add3.upper()
    record['Country'] = "United Kingdom"
    record['Lat'] = ""
    record['Lng'] = ""
    record['Verified'] = ""
    record['BusinessTypeID'] = 2
    record['BusinessTypeOther'] = ""
    record['BusinessSubCats'] = ",7,,8,"
    record['BusinessSubCatOther'] = ""
    record['ChangingID'] = 1
    record['NursingID'] = 3
    record['Website'] = starting_url
    record['ContactName'] = ""
    record['ContactPosition'] = ""
    record['Telephone'] = tel
    record['Email'] = ""
    record['Fax'] = ""
    record['LastModified'] = datetime.now()
    record['CreationDate'] = datetime.now()
    record['UsagePolicyID'] = 1
    record['AddressStatusID'] = 1
    record['latlngStatusID'] = 2
    scraperwiki.datastore.save(["ThisID"], record)


listurl = 'http://www.harvester.co.uk/find-a-harvester/harvester-directory.html'
listhtml = scraperwiki.scrape(listurl)
listsoup = BeautifulSoup(listhtml)
links = listsoup.findAll("a",{"class" : "search_result_title"})
#for i in range(1):
for a in links:
    print a['href']
    if a['href'].find("france") == -1:
        starting_url = a['href']
        html = scraperwiki.scrape(starting_url)
        soup = BeautifulSoup(html)
        objaddress = soup.find("address")
        if objaddress:
            # test to see if storefacilities div exists
            thisname = a.text
            getDetails(soup)
        else:
            print "no info here"


