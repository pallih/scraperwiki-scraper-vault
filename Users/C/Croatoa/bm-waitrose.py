###############################################################################
# Waitrose scraper
# http://www.waitrose.com/branches/branchdetails.aspx?uid=456
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def getDetails(soup):
    thisname = soup.title.text[:soup.title.text.find(" - ")]
    print "Getting details for " + str(i) + " " + thisname
    record = {}
    vcard = soup.find("div", { "class" : "lc" })
    address = vcard.find("p")
    add1 = address.findAll(text=True)[0].strip()
    if add1.find(",") > -1:
        add1a = add1[:add1.find(",")]
        add1b = add1[add1.find(",")+1:]
    else:
        add1a = add1
        add1b = ""
    add2 = address.findAll(text=True)[1].strip().split(",")
    if len(add2) > 2:
        if add2[2].strip() == '':
            add2a = add2[0].strip()
            add2b = add2[1].strip()
        else:
            add1b = add2[0].strip()
            add2a = add2[1].strip()
            add2b = add2[2].strip()            
    else:
        add2a = ""
        add2b = add2[0].strip()
    add3 = address.findAll(text=True)[2].strip()
    from datetime import datetime
    record['ThisID'] = i
    record['BusinessID'] = ""
    record['ReferrerID'] = 2
    record['RepID'] = ""
    record['BusinessChainID'] = 12
    record['CompanyName'] = thisname
    record['BuildingName'] = ""
    record['ThoroughFare'] = add1a
    record['ThoroughFare2'] = add1b
    record['DependentLocality'] = add2a
    record['Locality'] = add2b
    record['PostalCode'] = add3
    record['Country'] = "United Kingdom"
    record['Lat'] = soup.find("input", {"id":"_latHidden"})['value']
    record['Lng'] = soup.find("input", {"id":"_lonHidden"})['value']
    record['Verified'] = ""
    record['BusinessTypeID'] = 1
    record['BusinessTypeOther'] = ""
    record['BusinessSubCats'] = ",13,"
    record['BusinessSubCatOther'] = ""
    record['ChangingID'] = 1
    record['NursingID'] = 3
    record['Website'] = 'http://www.waitrose.com/branches/branchdetails.aspx?uid=' + str(i)
    record['ContactName'] = ""
    record['ContactPosition'] = ""
    record['Telephone'] = vcard.findAll("p")[1].text
    record['Email'] = ""
    record['Fax'] = ""
    record['LastModified'] = datetime.now()
    record['CreationDate'] = datetime.now()
    record['UsagePolicyID'] = 2
    record['AddressStatusID'] = 1
    record['latlngStatusID'] = 1
    scraperwiki.datastore.save(["ThisID"], record)


for i in range(106,999):
    print i
    # retrieve a page
    starting_url = 'http://www.waitrose.com/content/waitrose/en/bf_home/bf/' + str(i)
    try:
        html = scraperwiki.scrape(starting_url)
    except:
        print "Page not found"
    else:
        soup = BeautifulSoup(html)
        divs = soup.findAll("div", { "class" : "list" })
        if divs:
            for div in divs:
                if div.find(text="Baby Change Facility"): # test to see if facilities include baby changing
                    getDetails(soup)
                    break
        else:
            print "no store here"

