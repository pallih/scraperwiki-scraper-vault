                                             



import scraperwiki

# Blank Python

# typical URL is http://www.london-gazette.co.uk/id/issues/60112/notices/1568529
# list of URLs collected by scraper at https://scraperwiki.com/scrapers/bankruptcies/
# Downloaded as CSV and codes extracted in Google Docs by using =RIGHT(A2, 7)
# Cycle through a list of those codes, created by using the =JOIN formula in Google Docs

#If you want to understand this scraper - start at the bottom where it says 'base_url'

import scraperwiki
#import urlparse
import lxml.html
from lxml import etree

#TM - set debug on or off
debug = False

# search for a span property by XPath
def search_by_span_attribute(root, attribute, value):
    foundVal = root.xpath("//span[@" + attribute + "='" + value + "']")
    if foundVal:
        if debug:
            print attribute + " " + value + " found with text: " + foundVal[0].text
        return foundVal[0].text
    else:
        if debug:
            print attribute + " not found."
        return ""

# custom search
def search_xpath(root, xpath):
    foundVal = root.xpath(xpath)
    if foundVal:
        if debug:
            print xpath + " returned text: " + foundVal[0].text
        return foundVal[0].text
    else:
        if debug:
            print xpath + " returned no results found."
        return ""

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Create a new empty record
    record = {}

    record['pubdate'] = search_by_span_attribute(root, "property", "g:hasPublicationDate")
    record['noticecode'] = search_by_span_attribute(root, "property", "g:hasNoticeCode")
    #TM - you'll need to look for an example of this from page source when you come across one that should have it... unless it is the same as court:courtName below?
    #record['registry'] = search_by_span_attribute(root, "property",
    record['company number'] = search_by_span_attribute(root, "property", "organisation:companyNumber")
    record['company name'] = search_by_span_attribute(root, "property", "organisation:name")
    record['nature of business'] = search_by_span_attribute(root, "property", "organisation:natureOfBusiness")
    #record['trade classification'] = search_by_span_attribute(root, "property",
    record['date of appointment'] = search_by_span_attribute(root, "property", "corp-insolvency:dateOfAppointment")
    #TM - this one is a bit special as there are two that match it if you search for just the "vCard:label" property. To guarantee the right one, we have to customize the XPath a bit...
    record['registered office of company'] = search_xpath(root, "//span[@rel='organisation:hasRegisteredOffice']//span[@property='vCard:label']")
    record['registered office address of company'] = search_by_span_attribute(root, "property", "organisation:hasOffice")
    #record['sector'] = search_by_span_attribute(root, "property",
    record['date of appointment'] = search_by_span_attribute(root, "property", "corp-insolvency:dateOfAppointment")
    record['court'] = search_by_span_attribute(root, "property", "court:courtName")
    #record['date'] = search_by_span_attribute(root, "property", #same as date?
    #record['urlcode'] = search_by_span_attribute(root, "property",
    record['ID'] = item

    scraperwiki.sqlite.save(["ID"], record)
       

#this creates a new function and (re)names whatever parameter is passed to it - i.e. 'next_link' below - as 'url'
def scrape_page(url):
    #now 'url' is scraped with the scraperwiki library imported above, and the contents put into a new object, 'html'
    html = scraperwiki.scrape(url)
    #TM - commented out the below print
    #print html
    #now we use the lxml.html function imported above to convert 'html' into a new object, 'root'
    #TM - except we are now using etree!
    #root = lxml.html.fromstring(html)
    root = etree.HTML(html)
    #now we call another function on root, which we write - above
    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
base_url = 'http://www.belfast-gazette.co.uk/issues/'

#And these are the numbers which we need to complete that URL to make each individual URL
#This array has been compiled using the =JOIN formula in Google Docs on a column of URL codes
codes=['7508/notices/15','7508/notices/16','7510/notices/49','7506/notices/35','7508/notices/27','7508/notices/28','7508/notices/29','7508/notices/30','7508/notices/31','7508/notices/32','7508/notices/33','7508/notices/34','7508/notices/35','7508/notices/36','7508/notices/37','7508/notices/38','7508/notices/39','7508/notices/40','7508/notices/41','7508/notices/42','7508/notices/43','7510/notices/60','7510/notices/61','7510/notices/62','7510/notices/63','7510/notices/64','7510/notices/65','7510/notices/66','7512/notices/43','7512/notices/44','7512/notices/45','7514/notices/28','7514/notices/29','7514/notices/30','7514/notices/31','7514/notices/32','7508/notices/44','7512/notices/46','7506/notices/26','7506/notices/27','7508/notices/17','7510/notices/50','7512/notices/19','7512/notices/20','7512/notices/21','7512/notices/22','7512/notices/23','7514/notices/14','7514/notices/15','7506/notices/36','7506/notices/37','7506/notices/38','7508/notices/45','7508/notices/46','7508/notices/47','7508/notices/48','7508/notices/49','7508/notices/50','7510/notices/67','7510/notices/68','7510/notices/69','7510/notices/70','7510/notices/71','7514/notices/33','7514/notices/34','7514/notices/35','7514/notices/36','7514/notices/37','7514/notices/38','7514/notices/39','7514/notices/40','7514/notices/41','7514/notices/42','7514/notices/43','7514/notices/44','7512/notices/47','7514/notices/45','7506/notices/22','7506/notices/23','7506/notices/32','7506/notices/33','7508/notices/22','7510/notices/54','7512/notices/28','7512/notices/29','7512/notices/30','7512/notices/31','7512/notices/32','7514/notices/16','7514/notices/17','7514/notices/18']

#go through the schoolIDs array above, and for each ID...
for item in codes:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)
                                             



import scraperwiki

# Blank Python

# typical URL is http://www.london-gazette.co.uk/id/issues/60112/notices/1568529
# list of URLs collected by scraper at https://scraperwiki.com/scrapers/bankruptcies/
# Downloaded as CSV and codes extracted in Google Docs by using =RIGHT(A2, 7)
# Cycle through a list of those codes, created by using the =JOIN formula in Google Docs

#If you want to understand this scraper - start at the bottom where it says 'base_url'

import scraperwiki
#import urlparse
import lxml.html
from lxml import etree

#TM - set debug on or off
debug = False

# search for a span property by XPath
def search_by_span_attribute(root, attribute, value):
    foundVal = root.xpath("//span[@" + attribute + "='" + value + "']")
    if foundVal:
        if debug:
            print attribute + " " + value + " found with text: " + foundVal[0].text
        return foundVal[0].text
    else:
        if debug:
            print attribute + " not found."
        return ""

# custom search
def search_xpath(root, xpath):
    foundVal = root.xpath(xpath)
    if foundVal:
        if debug:
            print xpath + " returned text: " + foundVal[0].text
        return foundVal[0].text
    else:
        if debug:
            print xpath + " returned no results found."
        return ""

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Create a new empty record
    record = {}

    record['pubdate'] = search_by_span_attribute(root, "property", "g:hasPublicationDate")
    record['noticecode'] = search_by_span_attribute(root, "property", "g:hasNoticeCode")
    #TM - you'll need to look for an example of this from page source when you come across one that should have it... unless it is the same as court:courtName below?
    #record['registry'] = search_by_span_attribute(root, "property",
    record['company number'] = search_by_span_attribute(root, "property", "organisation:companyNumber")
    record['company name'] = search_by_span_attribute(root, "property", "organisation:name")
    record['nature of business'] = search_by_span_attribute(root, "property", "organisation:natureOfBusiness")
    #record['trade classification'] = search_by_span_attribute(root, "property",
    record['date of appointment'] = search_by_span_attribute(root, "property", "corp-insolvency:dateOfAppointment")
    #TM - this one is a bit special as there are two that match it if you search for just the "vCard:label" property. To guarantee the right one, we have to customize the XPath a bit...
    record['registered office of company'] = search_xpath(root, "//span[@rel='organisation:hasRegisteredOffice']//span[@property='vCard:label']")
    record['registered office address of company'] = search_by_span_attribute(root, "property", "organisation:hasOffice")
    #record['sector'] = search_by_span_attribute(root, "property",
    record['date of appointment'] = search_by_span_attribute(root, "property", "corp-insolvency:dateOfAppointment")
    record['court'] = search_by_span_attribute(root, "property", "court:courtName")
    #record['date'] = search_by_span_attribute(root, "property", #same as date?
    #record['urlcode'] = search_by_span_attribute(root, "property",
    record['ID'] = item

    scraperwiki.sqlite.save(["ID"], record)
       

#this creates a new function and (re)names whatever parameter is passed to it - i.e. 'next_link' below - as 'url'
def scrape_page(url):
    #now 'url' is scraped with the scraperwiki library imported above, and the contents put into a new object, 'html'
    html = scraperwiki.scrape(url)
    #TM - commented out the below print
    #print html
    #now we use the lxml.html function imported above to convert 'html' into a new object, 'root'
    #TM - except we are now using etree!
    #root = lxml.html.fromstring(html)
    root = etree.HTML(html)
    #now we call another function on root, which we write - above
    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
base_url = 'http://www.belfast-gazette.co.uk/issues/'

#And these are the numbers which we need to complete that URL to make each individual URL
#This array has been compiled using the =JOIN formula in Google Docs on a column of URL codes
codes=['7508/notices/15','7508/notices/16','7510/notices/49','7506/notices/35','7508/notices/27','7508/notices/28','7508/notices/29','7508/notices/30','7508/notices/31','7508/notices/32','7508/notices/33','7508/notices/34','7508/notices/35','7508/notices/36','7508/notices/37','7508/notices/38','7508/notices/39','7508/notices/40','7508/notices/41','7508/notices/42','7508/notices/43','7510/notices/60','7510/notices/61','7510/notices/62','7510/notices/63','7510/notices/64','7510/notices/65','7510/notices/66','7512/notices/43','7512/notices/44','7512/notices/45','7514/notices/28','7514/notices/29','7514/notices/30','7514/notices/31','7514/notices/32','7508/notices/44','7512/notices/46','7506/notices/26','7506/notices/27','7508/notices/17','7510/notices/50','7512/notices/19','7512/notices/20','7512/notices/21','7512/notices/22','7512/notices/23','7514/notices/14','7514/notices/15','7506/notices/36','7506/notices/37','7506/notices/38','7508/notices/45','7508/notices/46','7508/notices/47','7508/notices/48','7508/notices/49','7508/notices/50','7510/notices/67','7510/notices/68','7510/notices/69','7510/notices/70','7510/notices/71','7514/notices/33','7514/notices/34','7514/notices/35','7514/notices/36','7514/notices/37','7514/notices/38','7514/notices/39','7514/notices/40','7514/notices/41','7514/notices/42','7514/notices/43','7514/notices/44','7512/notices/47','7514/notices/45','7506/notices/22','7506/notices/23','7506/notices/32','7506/notices/33','7508/notices/22','7510/notices/54','7512/notices/28','7512/notices/29','7512/notices/30','7512/notices/31','7512/notices/32','7514/notices/16','7514/notices/17','7514/notices/18']

#go through the schoolIDs array above, and for each ID...
for item in codes:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)
                                             



import scraperwiki

# Blank Python

# typical URL is http://www.london-gazette.co.uk/id/issues/60112/notices/1568529
# list of URLs collected by scraper at https://scraperwiki.com/scrapers/bankruptcies/
# Downloaded as CSV and codes extracted in Google Docs by using =RIGHT(A2, 7)
# Cycle through a list of those codes, created by using the =JOIN formula in Google Docs

#If you want to understand this scraper - start at the bottom where it says 'base_url'

import scraperwiki
#import urlparse
import lxml.html
from lxml import etree

#TM - set debug on or off
debug = False

# search for a span property by XPath
def search_by_span_attribute(root, attribute, value):
    foundVal = root.xpath("//span[@" + attribute + "='" + value + "']")
    if foundVal:
        if debug:
            print attribute + " " + value + " found with text: " + foundVal[0].text
        return foundVal[0].text
    else:
        if debug:
            print attribute + " not found."
        return ""

# custom search
def search_xpath(root, xpath):
    foundVal = root.xpath(xpath)
    if foundVal:
        if debug:
            print xpath + " returned text: " + foundVal[0].text
        return foundVal[0].text
    else:
        if debug:
            print xpath + " returned no results found."
        return ""

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Create a new empty record
    record = {}

    record['pubdate'] = search_by_span_attribute(root, "property", "g:hasPublicationDate")
    record['noticecode'] = search_by_span_attribute(root, "property", "g:hasNoticeCode")
    #TM - you'll need to look for an example of this from page source when you come across one that should have it... unless it is the same as court:courtName below?
    #record['registry'] = search_by_span_attribute(root, "property",
    record['company number'] = search_by_span_attribute(root, "property", "organisation:companyNumber")
    record['company name'] = search_by_span_attribute(root, "property", "organisation:name")
    record['nature of business'] = search_by_span_attribute(root, "property", "organisation:natureOfBusiness")
    #record['trade classification'] = search_by_span_attribute(root, "property",
    record['date of appointment'] = search_by_span_attribute(root, "property", "corp-insolvency:dateOfAppointment")
    #TM - this one is a bit special as there are two that match it if you search for just the "vCard:label" property. To guarantee the right one, we have to customize the XPath a bit...
    record['registered office of company'] = search_xpath(root, "//span[@rel='organisation:hasRegisteredOffice']//span[@property='vCard:label']")
    record['registered office address of company'] = search_by_span_attribute(root, "property", "organisation:hasOffice")
    #record['sector'] = search_by_span_attribute(root, "property",
    record['date of appointment'] = search_by_span_attribute(root, "property", "corp-insolvency:dateOfAppointment")
    record['court'] = search_by_span_attribute(root, "property", "court:courtName")
    #record['date'] = search_by_span_attribute(root, "property", #same as date?
    #record['urlcode'] = search_by_span_attribute(root, "property",
    record['ID'] = item

    scraperwiki.sqlite.save(["ID"], record)
       

#this creates a new function and (re)names whatever parameter is passed to it - i.e. 'next_link' below - as 'url'
def scrape_page(url):
    #now 'url' is scraped with the scraperwiki library imported above, and the contents put into a new object, 'html'
    html = scraperwiki.scrape(url)
    #TM - commented out the below print
    #print html
    #now we use the lxml.html function imported above to convert 'html' into a new object, 'root'
    #TM - except we are now using etree!
    #root = lxml.html.fromstring(html)
    root = etree.HTML(html)
    #now we call another function on root, which we write - above
    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
base_url = 'http://www.belfast-gazette.co.uk/issues/'

#And these are the numbers which we need to complete that URL to make each individual URL
#This array has been compiled using the =JOIN formula in Google Docs on a column of URL codes
codes=['7508/notices/15','7508/notices/16','7510/notices/49','7506/notices/35','7508/notices/27','7508/notices/28','7508/notices/29','7508/notices/30','7508/notices/31','7508/notices/32','7508/notices/33','7508/notices/34','7508/notices/35','7508/notices/36','7508/notices/37','7508/notices/38','7508/notices/39','7508/notices/40','7508/notices/41','7508/notices/42','7508/notices/43','7510/notices/60','7510/notices/61','7510/notices/62','7510/notices/63','7510/notices/64','7510/notices/65','7510/notices/66','7512/notices/43','7512/notices/44','7512/notices/45','7514/notices/28','7514/notices/29','7514/notices/30','7514/notices/31','7514/notices/32','7508/notices/44','7512/notices/46','7506/notices/26','7506/notices/27','7508/notices/17','7510/notices/50','7512/notices/19','7512/notices/20','7512/notices/21','7512/notices/22','7512/notices/23','7514/notices/14','7514/notices/15','7506/notices/36','7506/notices/37','7506/notices/38','7508/notices/45','7508/notices/46','7508/notices/47','7508/notices/48','7508/notices/49','7508/notices/50','7510/notices/67','7510/notices/68','7510/notices/69','7510/notices/70','7510/notices/71','7514/notices/33','7514/notices/34','7514/notices/35','7514/notices/36','7514/notices/37','7514/notices/38','7514/notices/39','7514/notices/40','7514/notices/41','7514/notices/42','7514/notices/43','7514/notices/44','7512/notices/47','7514/notices/45','7506/notices/22','7506/notices/23','7506/notices/32','7506/notices/33','7508/notices/22','7510/notices/54','7512/notices/28','7512/notices/29','7512/notices/30','7512/notices/31','7512/notices/32','7514/notices/16','7514/notices/17','7514/notices/18']

#go through the schoolIDs array above, and for each ID...
for item in codes:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)
