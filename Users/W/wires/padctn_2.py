# Queries padctn to get current tax appraisal on properties

# table schema:
# Properties
# street, parcelID, 2012app, scraped

# Appraisal2013
# owner, street, zip, dist, parcelID, lastsaleprice, lastsaledate, totalval, landval, impval, acres, sqft, year, foundation, siding, rooms, bedrooms, fullbaths, halfbaths, fixtures

import scraperwiki
import lxml.html
import lxml.etree
import re
import resource
import xlrd
import cookielib, urllib2

from sys import exit
import geopy.geocoders
import geopy.distance

def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
        lambda mo: mo.group(0)[0].upper() +
            mo.group(0)[1:].lower(),
        s)

def getAppraisal(propID,parcelID):
    try:
    #    print "propID = " + propID + "."
        pageURL = "http://www.padctnwebpro.com/WebproNashville/searchResults.asp?cboSearchType=Parcel&SearchVal1=" + propID
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        html = lxml.html.parse(opener.open(pageURL)).getroot()
    #    print html.text_content()
        links = html.cssselect('a')
        newURL = "http://www.padctnwebpro.com/WebproNashville/" + links[0].get('href')

#summary-bottom.asp?A1=2337573&A2=1
        record = lxml.html.parse(opener.open(newURL.replace("Summary","summary-bottom"))).getroot()
        fields = record.cssselect('td')
        neighborhood = fields[49].text_content().strip()
        apprData = {'parcelID': parcelID,
            'neighborhood': neighborhood}
        scraperwiki.sqlite.save(unique_keys=["parcelID"], data=apprData, table_name="Districts")
    except:
        print "Could not get appraisal info for parcelID " + parcelID + " at " + address
            
    # owner, street, parcelID, lastsaleprice, lastsaledate, totalval, landval, impval, acres, sqft, year, foundation, siding, rooms, bedrooms, fullbaths, halfbaths, fixtures


def getExcel():
    xlbin = scraperwiki.scrape("http://home.mcgehee.com/appraisaldistrict.xls") 
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    for rownumber in range(0, sheet.nrows):
        propData = {
            'parcelID': sheet.cell_value(rownumber,0).strip(),
            'scraped': 0}
        scraperwiki.sqlite.save(unique_keys=["parcelID"], data=propData, table_name="Properties")

def cleanparcel():
    props = scraperwiki.sqlite.select("* FROM Properties")
    for i in props:
        parcelID = i['parcelID'].strip()
        scraperwiki.sqlite.execute("UPDATE Properties SET parcelID = " + parcelID + " WHERE street = '" + i['street'] + "'")
        street = i['street'].strip()
        scraperwiki.sqlite.execute("UPDATE Properties SET street = '" + street + "' WHERE parcelID = " + parcelID)
        scraperwiki.sqlite.commit()
        
def cleanResults():
    scraperwiki.sqlite.execute("DROP TABLE Appraisal2013")
    scraperwiki.sqlite.commit()

def cleanUtil():
    props = scraperwiki.sqlite.select("* FROM Properties WHERE parcelID = '130-04-0-045.00'")
    for i in props:
        scraperwiki.sqlite.execute("UPDATE Properties SET parcelID = '130-04-0-112.00' WHERE street = '" + i['street'] + "'")
        scraperwiki.sqlite.commit

# Main program

getExcel()
props = {}
#cleanparcel()
#cleanResults()
#cleanUtil()
#scraperwiki.sqlite.execute("UPDATE Properties SET scraped = 0")
#scraperwiki.sqlite.commit()
props = scraperwiki.sqlite.select("* FROM Properties WHERE scraped = 0 ORDER BY parcelID ASC")


for i in props:
    parcelID = i['parcelID'].strip()
    newID = ''.join(parcelID.split("-"))
    newID = ''.join(newID.split(".")).strip()
    print "Getting 2013 assessment neighborhood for parcel " + parcelID + "."
    newApp = getAppraisal(newID, parcelID)
    scraperwiki.sqlite.execute("UPDATE Properties SET scraped = 1 WHERE parcelID = '" + parcelID + "'")
    scraperwiki.sqlite.commit()



