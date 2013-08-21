###############################################################################
# Debenhams scraper
# for all http://mystore.debenhams.com
#
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def getDetails(soup):
    print "Getting details for " + thisname
    record = {}
    content = soup.find("div", { "class" : "right-block right-address" }).findAll("div")
    address = content[0].findAll(text=True)
    adrlast = len(address)
    #print adrlast
    add1a = address[0].strip()
    add1b = address[1].strip()
    add3 = address[adrlast-1].strip() # postcode
    add2b = address[adrlast-2].strip() # locality
    if adrlast > 4:
        add2a = address[adrlast-3].strip() # dependent locality of
    else:
        add2a = ""
    imgs = soup.find("div",{"id":"right_content"}).findAll("img")
    from datetime import datetime
    imgsrc = imgs[0]['src']
    latlng = imgsrc[imgsrc.find("center=")+7:imgsrc.find("&")]
    contacts = content[1].findAll(text=True)
    from datetime import datetime
    record['ThisID'] = thisname
    record['BusinessID'] = ""
    record['ReferrerID'] = 2
    record['RepID'] = ""
    record['BusinessChainID'] = 14
    record['CompanyName'] = "Debenhams " + thisname
    record['BuildingName'] = ""
    record['ThoroughFare'] = add1a[:add1a.find(",")]
    record['ThoroughFare2'] = add1b[:add1b.find(",")]
    record['DependentLocality'] = add2a[:add2a.find(",")]
    record['Locality'] = add2b[:add2b.find(",")]
    record['PostalCode'] = add3
    record['Country'] = "United Kingdom"
    record['Lat'] = latlng[:latlng.find(",")]
    record['Lng'] = latlng[latlng.find(",")+1:]
    record['Verified'] = ""
    record['BusinessTypeID'] = 1
    record['BusinessTypeOther'] = ""
    record['BusinessSubCats'] = ",2,,4,,5,"
    record['BusinessSubCatOther'] = ""
    record['ChangingID'] = 1
    record['NursingID'] = 1
    record['Website'] = starting_url
    record['ContactName'] = contacts[1].strip()
    record['ContactPosition'] = "Store Manager"
    record['Telephone'] = "08445 616 161"
    record['Email'] = ""
    record['Fax'] = ""
    record['LastModified'] = datetime.now()
    record['CreationDate'] = datetime.now()
    record['UsagePolicyID'] = 1
    record['AddressStatusID'] = 1
    record['latlngStatusID'] = 1
    scraperwiki.datastore.save(["ThisID"], record)


listurl = 'http://mystore.debenhams.com'
listhtml = scraperwiki.scrape(listurl)
listsoup = BeautifulSoup(listhtml)
cols = listsoup.findAll("div",{"class" : "column"})
#for i in range(1):
for div in cols:
    links = cols[3].findAll("a")
    for a in links:
        print a['href']
        if a['href'].find("Vietnam") == -1:
            starting_url = 'http://mystore.debenhams.com' + a['href'] + '/services'
            html = scraperwiki.scrape(starting_url)
            soup = BeautifulSoup(html)
            divs = soup.find("div", { "id" : "central_content" })
            if divs:
                # test to see if storefacilities div exists
                h3s = divs.findAll('h3')
                for h3 in h3s:
                    thistext = h3.text
                    if thistext == "Parent and Baby room": # test to see if facilities include baby changing
                        h2 = divs.find("h2").text[26:]
                        if h2.find(" - Desire") > -1:
                            thisname = h2[:h2.find(" - Desire")]
                        else:
                            thisname = h2
                        getDetails(soup)
                        break
            else:
                print "no info here"

