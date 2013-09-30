import scraperwiki
# Code taken from http://www.travisglines.com/web-coding/python-xml-parser-tutorial
#import library to do http requests:
import urllib2
from lxml import etree
from bs4 import BeautifulSoup
from xml.dom.minidom import parseString
import time

ListingsInfo = []
##############################################
##############################################
##############################################
##############################################
# Gets Information from Individual Pages
def get_listing_info(URL):
    # URL = "http://www.cityfeet.com/Commercial/ForLease/2310-Marconi-Court-San-Diego-CA-92154-16164771L16164771L3.aspx"

    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(URL, None, headers)
    page2 = urllib2.urlopen(req)
    html2 = BeautifulSoup(page2.read())

    # Address print Listings.h1.text, Listings.h2.text
    Listings = html2.find("div","listingProfileDetail")
    StreetAddress = Listings.h1.text
    CityStateZip = Listings.h2.text

    # The Source Code in this Section is incomplete due to bot detection
    PrimaryStats = html2.find("div","primaryStats")
    ForLease = PrimaryStats.h4.text
    Zoning = PrimaryStats.ul.li.div.text
    
    # Listing Company
    ContactInfo = html2.find("div","listingProfileContact")
    Company = ContactInfo.find_all("div","contactModule clearfix")
    ListingCompany = Company[0].span.next_sibling.next_sibling.text

    # Listing Contact
    ContactInfo = html2.find("div", id="ctl00_CityfeetContentPlaceholder_ContactPrimary_divContactMain")
    ContactInfo2 = ContactInfo.find("a", id="ctl00_CityfeetContentPlaceholder_ContactPrimary_aEmailAgent2")
    ListingContact = ContactInfo2.text
    ListingPhone = ContactInfo2.next_sibling
    ListingsInfo.append((StreetAddress,CityStateZip,ForLease,Zoning,ListingCompany,ListingContact,ListingPhone))
    print StreetAddress,CityStateZip,ForLease,Zoning,ListingCompany,ListingContact,ListingPhone

####################################################
####################################################
####################################################
####################################################

# Get all Listing URLs

baseURL = "http://www.cityfeet.com/cont/ca/san-diego-county-industrial-space?pgNum="
endURL = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
ListingBaseURL = "http://www.cityfeet.com/"
ListingURLs = []

for pageNum in endURL:
    SearchURL = baseURL + str(pageNum)
    print SearchURL
    # Open Page and Create DOM object
    page = urllib2.urlopen(SearchURL)
    html = BeautifulSoup(page.read())
    print pageNum

    # Get Listing URL
    Listings = html.find_all("div","property featured clearfix")
    for Listing in Listings:
        ListingRelURL = Listing.div.div.h3.a['href']
        ListingURL = ListingBaseURL + ListingRelURL
        print ListingURL
        ListingURLs.append(ListingURL)

print len(ListingURLs)
####################################################
####################################################
####################################################
####################################################


a = 235
while a < 242 :
    pageflip = ListingURLs[a]
    get_listing_info(pageflip)
    print "Turn Page", str(a)
    # time.sleep(2)
    a += 1

for info in ListingsInfo:
    data = {
        'StreetAddress' : info[0],
        'CityStateZip' : info[1],
        'ForLease' : info[2],
        'Zoning' : info[3],
        'ListingCompany' : info[4],
        'ListingContact' : info[5],
        'ListingPhone' : info[6],
    }
    scraperwiki.sqlite.save(unique_keys=['StreetAddress'], data=data)







import scraperwiki
# Code taken from http://www.travisglines.com/web-coding/python-xml-parser-tutorial
#import library to do http requests:
import urllib2
from lxml import etree
from bs4 import BeautifulSoup
from xml.dom.minidom import parseString
import time

ListingsInfo = []
##############################################
##############################################
##############################################
##############################################
# Gets Information from Individual Pages
def get_listing_info(URL):
    # URL = "http://www.cityfeet.com/Commercial/ForLease/2310-Marconi-Court-San-Diego-CA-92154-16164771L16164771L3.aspx"

    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(URL, None, headers)
    page2 = urllib2.urlopen(req)
    html2 = BeautifulSoup(page2.read())

    # Address print Listings.h1.text, Listings.h2.text
    Listings = html2.find("div","listingProfileDetail")
    StreetAddress = Listings.h1.text
    CityStateZip = Listings.h2.text

    # The Source Code in this Section is incomplete due to bot detection
    PrimaryStats = html2.find("div","primaryStats")
    ForLease = PrimaryStats.h4.text
    Zoning = PrimaryStats.ul.li.div.text
    
    # Listing Company
    ContactInfo = html2.find("div","listingProfileContact")
    Company = ContactInfo.find_all("div","contactModule clearfix")
    ListingCompany = Company[0].span.next_sibling.next_sibling.text

    # Listing Contact
    ContactInfo = html2.find("div", id="ctl00_CityfeetContentPlaceholder_ContactPrimary_divContactMain")
    ContactInfo2 = ContactInfo.find("a", id="ctl00_CityfeetContentPlaceholder_ContactPrimary_aEmailAgent2")
    ListingContact = ContactInfo2.text
    ListingPhone = ContactInfo2.next_sibling
    ListingsInfo.append((StreetAddress,CityStateZip,ForLease,Zoning,ListingCompany,ListingContact,ListingPhone))
    print StreetAddress,CityStateZip,ForLease,Zoning,ListingCompany,ListingContact,ListingPhone

####################################################
####################################################
####################################################
####################################################

# Get all Listing URLs

baseURL = "http://www.cityfeet.com/cont/ca/san-diego-county-industrial-space?pgNum="
endURL = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
ListingBaseURL = "http://www.cityfeet.com/"
ListingURLs = []

for pageNum in endURL:
    SearchURL = baseURL + str(pageNum)
    print SearchURL
    # Open Page and Create DOM object
    page = urllib2.urlopen(SearchURL)
    html = BeautifulSoup(page.read())
    print pageNum

    # Get Listing URL
    Listings = html.find_all("div","property featured clearfix")
    for Listing in Listings:
        ListingRelURL = Listing.div.div.h3.a['href']
        ListingURL = ListingBaseURL + ListingRelURL
        print ListingURL
        ListingURLs.append(ListingURL)

print len(ListingURLs)
####################################################
####################################################
####################################################
####################################################


a = 235
while a < 242 :
    pageflip = ListingURLs[a]
    get_listing_info(pageflip)
    print "Turn Page", str(a)
    # time.sleep(2)
    a += 1

for info in ListingsInfo:
    data = {
        'StreetAddress' : info[0],
        'CityStateZip' : info[1],
        'ForLease' : info[2],
        'Zoning' : info[3],
        'ListingCompany' : info[4],
        'ListingContact' : info[5],
        'ListingPhone' : info[6],
    }
    scraperwiki.sqlite.save(unique_keys=['StreetAddress'], data=data)







