                                             



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
codes=['58342/notices/265935','58342/notices/265936','58342/notices/265937','58342/notices/263665','58342/notices/265938','58342/notices/263666','58342/notices/265939','58344/notices/266520','58344/notices/266521','58346/notices/268418','58346/notices/268419','58346/notices/268420','58346/notices/268421','58348/notices/270125','58348/notices/270126','58348/notices/270127','58348/notices/270500','58348/notices/270501','58348/notices/270502','58349/notices/269352','58349/notices/271870','58349/notices/271871','58349/notices/271872','58349/notices/271873','58349/notices/271874','58349/notices/271877','58349/notices/271878','58349/notices/269348','58349/notices/271879','58349/notices/271880','58349/notices/269349','58349/notices/269353','58349/notices/271881','58350/notices/272536','58350/notices/272537','58350/notices/272538','58350/notices/272539','58350/notices/272540','58350/notices/272541','58350/notices/272542','58352/notices/272106','58352/notices/273754','58352/notices/273755','58352/notices/272103','58352/notices/273756','58352/notices/273757','58352/notices/273906','58352/notices/272107','58352/notices/273907','58352/notices/273908','58352/notices/273909','58353/notices/274400','58353/notices/274401','58353/notices/272921','58353/notices/274402','58353/notices/274403','58353/notices/274404','58353/notices/274405','58354/notices/276625','58354/notices/276626','58354/notices/276627','58354/notices/276628','58354/notices/276629','58354/notices/276630','58368/notices/278092','58368/notices/278093','58368/notices/278094','58368/notices/278095','58368/notices/278096','58368/notices/278400','58368/notices/278401','58368/notices/278402','58368/notices/278403','58368/notices/278404','58368/notices/278419','58368/notices/278420','58368/notices/278421','58368/notices/278422','58368/notices/278423','58368/notices/276367','58370/notices/279276','58370/notices/279277','58370/notices/279278','58370/notices/279279','58370/notices/279237','58370/notices/279238','58370/notices/279239','58371/notices/280274','58371/notices/280275','58371/notices/280276','58371/notices/280277','58371/notices/278361','58371/notices/280278','58371/notices/280279','58372/notices/282193','58372/notices/282194','58372/notices/282195','58372/notices/282196','58372/notices/282199','58372/notices/282200','58372/notices/282201','58372/notices/282202','58373/notices/283371','58373/notices/280841','58373/notices/283372','58373/notices/283373','58373/notices/280842','58373/notices/283374','58373/notices/282925','58373/notices/282926','58373/notices/282927','58373/notices/282928','58374/notices/283490','58374/notices/281810','58374/notices/281811','58374/notices/283491','58374/notices/283492','58374/notices/281812','58374/notices/283493','58376/notices/285019','58376/notices/285020','58376/notices/285021','58376/notices/285022','58376/notices/285023','58376/notices/284927','58376/notices/284928','58376/notices/284929','58376/notices/284930','58376/notices/284931','58376/notices/285033','58376/notices/285034','58376/notices/285035','58376/notices/285036','58377/notices/284285','58377/notices/284286','58377/notices/286318','58377/notices/286319','58377/notices/286653','58377/notices/286320','58377/notices/286654','58377/notices/284287','58377/notices/286655','58379/notices/288889','58379/notices/286607','58379/notices/288890','58379/notices/288891','58379/notices/288892','58379/notices/289001','58379/notices/289002','58379/notices/289003','58379/notices/286608','58379/notices/289004']

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
codes=['58342/notices/265935','58342/notices/265936','58342/notices/265937','58342/notices/263665','58342/notices/265938','58342/notices/263666','58342/notices/265939','58344/notices/266520','58344/notices/266521','58346/notices/268418','58346/notices/268419','58346/notices/268420','58346/notices/268421','58348/notices/270125','58348/notices/270126','58348/notices/270127','58348/notices/270500','58348/notices/270501','58348/notices/270502','58349/notices/269352','58349/notices/271870','58349/notices/271871','58349/notices/271872','58349/notices/271873','58349/notices/271874','58349/notices/271877','58349/notices/271878','58349/notices/269348','58349/notices/271879','58349/notices/271880','58349/notices/269349','58349/notices/269353','58349/notices/271881','58350/notices/272536','58350/notices/272537','58350/notices/272538','58350/notices/272539','58350/notices/272540','58350/notices/272541','58350/notices/272542','58352/notices/272106','58352/notices/273754','58352/notices/273755','58352/notices/272103','58352/notices/273756','58352/notices/273757','58352/notices/273906','58352/notices/272107','58352/notices/273907','58352/notices/273908','58352/notices/273909','58353/notices/274400','58353/notices/274401','58353/notices/272921','58353/notices/274402','58353/notices/274403','58353/notices/274404','58353/notices/274405','58354/notices/276625','58354/notices/276626','58354/notices/276627','58354/notices/276628','58354/notices/276629','58354/notices/276630','58368/notices/278092','58368/notices/278093','58368/notices/278094','58368/notices/278095','58368/notices/278096','58368/notices/278400','58368/notices/278401','58368/notices/278402','58368/notices/278403','58368/notices/278404','58368/notices/278419','58368/notices/278420','58368/notices/278421','58368/notices/278422','58368/notices/278423','58368/notices/276367','58370/notices/279276','58370/notices/279277','58370/notices/279278','58370/notices/279279','58370/notices/279237','58370/notices/279238','58370/notices/279239','58371/notices/280274','58371/notices/280275','58371/notices/280276','58371/notices/280277','58371/notices/278361','58371/notices/280278','58371/notices/280279','58372/notices/282193','58372/notices/282194','58372/notices/282195','58372/notices/282196','58372/notices/282199','58372/notices/282200','58372/notices/282201','58372/notices/282202','58373/notices/283371','58373/notices/280841','58373/notices/283372','58373/notices/283373','58373/notices/280842','58373/notices/283374','58373/notices/282925','58373/notices/282926','58373/notices/282927','58373/notices/282928','58374/notices/283490','58374/notices/281810','58374/notices/281811','58374/notices/283491','58374/notices/283492','58374/notices/281812','58374/notices/283493','58376/notices/285019','58376/notices/285020','58376/notices/285021','58376/notices/285022','58376/notices/285023','58376/notices/284927','58376/notices/284928','58376/notices/284929','58376/notices/284930','58376/notices/284931','58376/notices/285033','58376/notices/285034','58376/notices/285035','58376/notices/285036','58377/notices/284285','58377/notices/284286','58377/notices/286318','58377/notices/286319','58377/notices/286653','58377/notices/286320','58377/notices/286654','58377/notices/284287','58377/notices/286655','58379/notices/288889','58379/notices/286607','58379/notices/288890','58379/notices/288891','58379/notices/288892','58379/notices/289001','58379/notices/289002','58379/notices/289003','58379/notices/286608','58379/notices/289004']

#go through the schoolIDs array above, and for each ID...
for item in codes:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)
