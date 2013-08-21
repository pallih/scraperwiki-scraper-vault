###############################################################################
# Cafe rouge scraper
# http://www.caferouge.co.uk/locations/listall
# 
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def getDetails(objaddress):
    print "Getting details for " + thisname
    record = {}
    #print objaddress
    address = objaddress.findAll(text=True)
    adrlast = len(address)
    #print address
    #print adrlast
    add1a = address[0].strip()
    add1b = address[1].strip()
    add3 = address[adrlast-4].strip() # postcode
    add2b = address[adrlast-5].strip() # locality
    if adrlast > 7:
        add2a = address[adrlast-6].strip() # dependent locality
    else:
        add2a = ""
    #imgs = soup.find("div",{"id":"right_content"}).findAll("img")
    from datetime import datetime
    #imgsrc = imgs[0]['src']
    #latlng = imgsrc[imgsrc.find("center=")+7:imgsrc.find("&")]
    #contacts = content[1].findAll(text=True)
    thistel = objaddress.find("strong").text
    if thistel.find(" ") > -1:
        tel = thistel
    else:
        tel = thistel[:4] + " " + thistel[4:]
    from datetime import datetime
    record['ThisID'] = thisname
    record['BusinessID'] = ""
    record['ReferrerID'] = 2
    record['RepID'] = ""
    record['BusinessChainID'] = 15
    record['CompanyName'] = "Cafe Rouge " + thisname
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
    record['BusinessSubCats'] = ",6,,7,"
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


listurl = 'http://www.caferouge.co.uk/locations/listall'
listhtml = scraperwiki.scrape(listurl)
listsoup = BeautifulSoup(listhtml)
cols = listsoup.findAll("div",{"class" : "paper_content"})
#for i in range(1):
for div in cols:
    links = div.findAll("a")
    for a in links:
        print a['href']
        if a['href'].find("milton-keynes-") == -1:
            starting_url = a['href']
            html = scraperwiki.scrape(starting_url)
            soup = BeautifulSoup(html)
            objaddress = soup.find("address")
            if objaddress:
                # test to see if storefacilities div exists
                thisname = a.text
                getDetails(objaddress)
            else:
                print "no info here"


