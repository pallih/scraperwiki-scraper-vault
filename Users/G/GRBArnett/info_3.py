                                             



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
base_url = 'http://www.london-gazette.co.uk/issues/'

#And these are the numbers which we need to complete that URL to make each individual URL
#This array has been compiled using the =JOIN formula in Google Docs on a column of URL codes
codes=['60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60570/notices/1862967','60570/notices/1864757','60573/notices/1865355','60573/notices/1865355','60574/notices/1867811','60559/notices/1854783','60559/notices/1856466','60559/notices/1856720','60560/notices/1855858','60560/notices/1857101','60561/notices/1856805','60562/notices/1857504','60562/notices/1857647','60564/notices/1860225','60564/notices/1860227','60565/notices/1859185','60565/notices/1860793','60565/notices/1861033','60566/notices/1860248','60566/notices/1860263','60568/notices/1862090','60570/notices/1862961','60571/notices/1865828','60571/notices/1863751','60571/notices/1865829','60571/notices/1865830','60574/notices/1868314','60556/notices/1853945','60564/notices/1859729','60566/notices/1861372','60567/notices/1862271','60570/notices/1864575','60570/notices/1864591','60572/notices/1866017','60574/notices/1867687','60556/notices/1854636','60558/notices/1855383','60560/notices/1857613','60562/notices/1858823','60564/notices/1858561','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60570/notices/1862967','60573/notices/1865355','60573/notices/1865355','60574/notices/1867811','60574/notices/1868202','60558/notices/1854118','60559/notices/1854783','60559/notices/1856466','60559/notices/1854766','60559/notices/1856720','60560/notices/1855858','60560/notices/1857101','60561/notices/1856805','60562/notices/1857504','60562/notices/1857647','60564/notices/1859035','60564/notices/1860225','60565/notices/1859185','60565/notices/1859604','60565/notices/1860793','60565/notices/1861033','60566/notices/1860248','60566/notices/1860263','60568/notices/1862090','60570/notices/1862961','60571/notices/1863751','60571/notices/1865829','60571/notices/1865830','60571/notices/1865210','60574/notices/1868314','60559/notices/1854766']

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
base_url = 'http://www.london-gazette.co.uk/issues/'

#And these are the numbers which we need to complete that URL to make each individual URL
#This array has been compiled using the =JOIN formula in Google Docs on a column of URL codes
codes=['60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60570/notices/1862967','60570/notices/1864757','60573/notices/1865355','60573/notices/1865355','60574/notices/1867811','60559/notices/1854783','60559/notices/1856466','60559/notices/1856720','60560/notices/1855858','60560/notices/1857101','60561/notices/1856805','60562/notices/1857504','60562/notices/1857647','60564/notices/1860225','60564/notices/1860227','60565/notices/1859185','60565/notices/1860793','60565/notices/1861033','60566/notices/1860248','60566/notices/1860263','60568/notices/1862090','60570/notices/1862961','60571/notices/1865828','60571/notices/1863751','60571/notices/1865829','60571/notices/1865830','60574/notices/1868314','60556/notices/1853945','60564/notices/1859729','60566/notices/1861372','60567/notices/1862271','60570/notices/1864575','60570/notices/1864591','60572/notices/1866017','60574/notices/1867687','60556/notices/1854636','60558/notices/1855383','60560/notices/1857613','60562/notices/1858823','60564/notices/1858561','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60570/notices/1862967','60573/notices/1865355','60573/notices/1865355','60574/notices/1867811','60574/notices/1868202','60558/notices/1854118','60559/notices/1854783','60559/notices/1856466','60559/notices/1854766','60559/notices/1856720','60560/notices/1855858','60560/notices/1857101','60561/notices/1856805','60562/notices/1857504','60562/notices/1857647','60564/notices/1859035','60564/notices/1860225','60565/notices/1859185','60565/notices/1859604','60565/notices/1860793','60565/notices/1861033','60566/notices/1860248','60566/notices/1860263','60568/notices/1862090','60570/notices/1862961','60571/notices/1863751','60571/notices/1865829','60571/notices/1865830','60571/notices/1865210','60574/notices/1868314','60559/notices/1854766']

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
base_url = 'http://www.london-gazette.co.uk/issues/'

#And these are the numbers which we need to complete that URL to make each individual URL
#This array has been compiled using the =JOIN formula in Google Docs on a column of URL codes
codes=['60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60570/notices/1862967','60570/notices/1864757','60573/notices/1865355','60573/notices/1865355','60574/notices/1867811','60559/notices/1854783','60559/notices/1856466','60559/notices/1856720','60560/notices/1855858','60560/notices/1857101','60561/notices/1856805','60562/notices/1857504','60562/notices/1857647','60564/notices/1860225','60564/notices/1860227','60565/notices/1859185','60565/notices/1860793','60565/notices/1861033','60566/notices/1860248','60566/notices/1860263','60568/notices/1862090','60570/notices/1862961','60571/notices/1865828','60571/notices/1863751','60571/notices/1865829','60571/notices/1865830','60574/notices/1868314','60556/notices/1853945','60564/notices/1859729','60566/notices/1861372','60567/notices/1862271','60570/notices/1864575','60570/notices/1864591','60572/notices/1866017','60574/notices/1867687','60556/notices/1854636','60558/notices/1855383','60560/notices/1857613','60562/notices/1858823','60564/notices/1858561','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60570/notices/1862967','60573/notices/1865355','60573/notices/1865355','60574/notices/1867811','60574/notices/1868202','60558/notices/1854118','60559/notices/1854783','60559/notices/1856466','60559/notices/1854766','60559/notices/1856720','60560/notices/1855858','60560/notices/1857101','60561/notices/1856805','60562/notices/1857504','60562/notices/1857647','60564/notices/1859035','60564/notices/1860225','60565/notices/1859185','60565/notices/1859604','60565/notices/1860793','60565/notices/1861033','60566/notices/1860248','60566/notices/1860263','60568/notices/1862090','60570/notices/1862961','60571/notices/1863751','60571/notices/1865829','60571/notices/1865830','60571/notices/1865210','60574/notices/1868314','60559/notices/1854766']

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
base_url = 'http://www.london-gazette.co.uk/issues/'

#And these are the numbers which we need to complete that URL to make each individual URL
#This array has been compiled using the =JOIN formula in Google Docs on a column of URL codes
codes=['60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60570/notices/1862967','60570/notices/1864757','60573/notices/1865355','60573/notices/1865355','60574/notices/1867811','60559/notices/1854783','60559/notices/1856466','60559/notices/1856720','60560/notices/1855858','60560/notices/1857101','60561/notices/1856805','60562/notices/1857504','60562/notices/1857647','60564/notices/1860225','60564/notices/1860227','60565/notices/1859185','60565/notices/1860793','60565/notices/1861033','60566/notices/1860248','60566/notices/1860263','60568/notices/1862090','60570/notices/1862961','60571/notices/1865828','60571/notices/1863751','60571/notices/1865829','60571/notices/1865830','60574/notices/1868314','60556/notices/1853945','60564/notices/1859729','60566/notices/1861372','60567/notices/1862271','60570/notices/1864575','60570/notices/1864591','60572/notices/1866017','60574/notices/1867687','60556/notices/1854636','60558/notices/1855383','60560/notices/1857613','60562/notices/1858823','60564/notices/1858561','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60564/notices/1858560','60570/notices/1862967','60573/notices/1865355','60573/notices/1865355','60574/notices/1867811','60574/notices/1868202','60558/notices/1854118','60559/notices/1854783','60559/notices/1856466','60559/notices/1854766','60559/notices/1856720','60560/notices/1855858','60560/notices/1857101','60561/notices/1856805','60562/notices/1857504','60562/notices/1857647','60564/notices/1859035','60564/notices/1860225','60565/notices/1859185','60565/notices/1859604','60565/notices/1860793','60565/notices/1861033','60566/notices/1860248','60566/notices/1860263','60568/notices/1862090','60570/notices/1862961','60571/notices/1863751','60571/notices/1865829','60571/notices/1865830','60571/notices/1865210','60574/notices/1868314','60559/notices/1854766']

#go through the schoolIDs array above, and for each ID...
for item in codes:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)
