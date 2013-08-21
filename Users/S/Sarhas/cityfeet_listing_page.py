import scraperwiki
import urllib2
from lxml import etree
from bs4 import BeautifulSoup
from xml.dom.minidom import parseString

 
URL = "http://www.cityfeet.com/Commercial/ForLease/2310-Marconi-Court-San-Diego-CA-92154-16164771L16164771L3.aspx"

headers = { 'User-Agent' : 'Mozilla/5.0' }
req = urllib2.Request(URL, None, headers)
page = urllib2.urlopen(req)
html = BeautifulSoup(page.read())

# Address print Listings.h1.text, Listings.h2.text
Listings = html.find("div","listingProfileDetail")
StreetAddress = Listings.h1.text
CityStateZip = Listings.h2.text

# The Source Code in this Section is incomplete due to bot detection
PrimaryStats = html.find("div","primaryStats")
ForLease = PrimaryStats.h4.text
Zoning = PrimaryStats.ul.li.div.text

# Listing Company
ContactInfo = html.find("div","listingProfileContact")
Company = ContactInfo.find_all("div","contactModule clearfix")
ListingCompany = Company[0].span.next_sibling.next_sibling.text

# Listing Contact
ContactInfo = html.find("div", id="ctl00_CityfeetContentPlaceholder_ContactPrimary_divContactMain")
ContactInfo2 = ContactInfo.find("a", id="ctl00_CityfeetContentPlaceholder_ContactPrimary_aEmailAgent2")
ListingContact = ContactInfo2.text
ListingPhone = ContactInfo2.next_sibling




