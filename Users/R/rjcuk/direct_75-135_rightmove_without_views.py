# Collect data from one estate agent only - all sales and lettings including sold/let agreed

from lxml import etree
from lxml.etree import tostring
from datetime import datetime
import scraperwiki
import StringIO
import sys
from urllib2 import *

DOMAIN = 'http://www.rightmove.co.uk' 

iProp = 0

def scrape_individual_house(house_url, saleType):
    # download the unique property page
    HOUSE_URL = (DOMAIN + house_url).split('/svr/')[0]
    #print 'Scraping %s' % HOUSE_URL
    house_html = scraperwiki.scrape(HOUSE_URL)
    house_parser = etree.HTMLParser()
    house_tree = etree.parse(StringIO.StringIO(house_html), house_parser)
    house = {}
    
    # Record name
    house['title'] = house_tree.xpath('string(//h1[@id="propertytype"])')

    # Record as Sales/Lettings
    house['saleType'] = saleType

    # Image
    image_url = house_tree.xpath('//img[@id="mainphoto"]')[0]
    image_url = image_url.xpath('//img[@id="mainphoto"]/@src')[0]
    house['image_url'] = image_url
    
    # Get price into nice numerical-only format
    price = house_tree.xpath('string(//div[@id="amount"])') 
    price = price[1:] # remove unicode £ at start
    price = price.replace(",", "") # remove commas
    price = price.strip() # remove whitespace
    price = int(price) # check it is converted to an integer
    if price < 200: # *** ASSUMPTION: If cost is less than 200, assume it means PCW (week), so multiply by 4 to get PCM (month)
        price = price * 4 # cost per week must be multiplied by 4 (~4.34) to get the month cost
    print str(price) + " : ", # print price to console
    house['price'] = price # store the price after updating

    # Address
    address = house_tree.xpath('string(//div[@id="addresscontainer"])')
    # strip out \t, \r, \n
    address = address.replace("\n", "")
    address = address.replace("\t", "")
    address = address.replace("\r", "")
    # add spaces back in
    address = address.replace(",", ", ")
    house['address'] = address
    print address + " : ",

    house['link'] = HOUSE_URL
    house['sold'] = 0 # the property is 'on the market' because it appears in the search results

    # save to database or update it (cannot replace by 'save')
    # delete if already exists and replace (add) with new copy (ordering is regardless)
    # REMEMBER you cannot delete from swdata if the database is cleaned down
    # This will result in 1 permittable error if the database has been cleared down
    try:
        scraperwiki.sqlite.execute("delete from swdata where link = '" + house['link'] + "'") # this operation is silent
        scraperwiki.sqlite.commit()
    except scraperwiki.sqlite.SqliteError, e:
        print "Error: " + str(e)
    
    print "Adding... ",
    scraperwiki.sqlite.save(['link'], house) # save to database
    print "OK"

# Gather list of results for an individual location. 
def scrape_results_page(results_url, saleType, initial=False):
    global iProp
    results_url = DOMAIN + results_url
    try:
        html = scraperwiki.scrape(results_url)
    except:
        print "Error: ",sys.exc_info()
        req = Request(results_url)
        try:
            response = urlopen(req)
        except httplib.HTTPException, e:
            print "Error in HTTP: ",e
            sys.exit(-1)
        except URLError, e:
            if hasattr(e, 'reason'):
                print 'Error: We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'Error: The server couldnt fulfill the request.'
                print 'Error code: ', e.code
            sys.exit(-1)
        except:
            print "Error: unknown error: ",sys.exc_info()
            sys.exit(-1)
        else:
            html = response.read()
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO.StringIO(html), parser)
    house_links = tree.xpath('//ol[@id="summaries"]//a[starts-with(text(), "More details")]/@href')
    for house_link in house_links:
        print str(iProp) + " : ",
        scrape_individual_house(house_link, saleType)
        iProp += 1
    if initial:
        results_links = tree.xpath('//ul[@class="items"]//a/@href')
        for r in results_links:
            scrape_results_page(r, saleType)

# Clean up old properties
def clean_old_links():
    print "Now checking all properties for status... "
    allProperties = scraperwiki.sqlite.select("* from swdata") # returns a dict
    for aProperty in allProperties:
        # Try to scrape the page of the property
        # If certain information cannot be read from it, then that property has been deleted
        house_html = ''
        try:
            house_html = scraperwiki.scrape(aProperty['link'])
        except:
            print "Error: ",sys.exc_info()
            req = Request(aProperty['link'])
            try:
                response = urlopen(req)
            except httplib.HTTPException, e:
                print "Error in HTTP: ",e
                sys.exit(-1)
            except URLError, e:
                if hasattr(e, 'reason'):
                    print 'Error: We failed to reach a server.'
                    print 'Reason: ', e.reason
                elif hasattr(e, 'code'):
                    print 'Error: The server couldnt fulfill the request.'
                    print 'Error code: ', e.code
                sys.exit(-1)
            except:
                print "Error: unknown error: ",sys.exc_info()
                sys.exit(-1)
            else:
                house_html = response.read()
        house_parser = etree.HTMLParser()
        house_tree = etree.parse(StringIO.StringIO(house_html), house_parser)
        try:
            house_text = house_tree.xpath('string(//div[@class="errorbox"])')
            if 'removed this property' in house_text:
                # mark the property as sold as it is showing the 'removed' page on Rightmove
                try:
                    scraperwiki.sqlite.execute("update swdata set sold = 1 where link = '" + aProperty['link'] + "'")
                    scraperwiki.sqlite.commit()
                    print aProperty['link'] + " : Updated (sold/let by)"
                except scraperwiki.sqlite.SqliteError, e:
                    print "Error: " + str(e)
            else:
                # if this passes then keep the property and update it just incase it was previously removed
                try:
                    scraperwiki.sqlite.execute("update swdata set sold = 0 where link = '" + aProperty['link'] + "'")
                    scraperwiki.sqlite.commit()
                    print aProperty['link'] + " : Updated (available)"
                except scraperwiki.sqlite.SqliteError, e:
                    print "Error: " + str(e)
        except etree.XPathError, e:
            print "Error: " + str(e)

def empty_database():
    try:
        print "Deleting existing table... ",
        scraperwiki.sqlite.execute("drop table if exists swdata")
        scraperwiki.sqlite.commit()
        print "OK"
    except scraperwiki.sqlite.SqliteError, e:
        print str(e)

# Alternative: just drop the table and forget all the old ones
#empty_database()

# 2. Sales
url1 = '/property-for-sale/find/JB-Property-Services/Waltham-Abbey.html/svr/3112?locationIdentifier=BRANCH^7557&sortByPriceDescending=false&includeSSTC=true&_includeSSTC=on'
INITIAL_URL = url1
# download the search page
#scrape_results_page(INITIAL_URL, "Sales", initial=True)

# 3. Lettings
url2 = '/property-to-rent/find/JB-Property-Services/Waltham-Abbey.html/svr/3112?locationIdentifier=BRANCH^7557&sortByPriceDescending=false&includeLetAgreed=true&_includeLetAgreed=on'
INITIAL_URL = url2
# download the search page
scrape_results_page(INITIAL_URL, "Lettings", initial=True)

# 1. Check all existing properties and flag as remove if they no longer exist

clean_old_links()
# Collect data from one estate agent only - all sales and lettings including sold/let agreed

from lxml import etree
from lxml.etree import tostring
from datetime import datetime
import scraperwiki
import StringIO
import sys
from urllib2 import *

DOMAIN = 'http://www.rightmove.co.uk' 

iProp = 0

def scrape_individual_house(house_url, saleType):
    # download the unique property page
    HOUSE_URL = (DOMAIN + house_url).split('/svr/')[0]
    #print 'Scraping %s' % HOUSE_URL
    house_html = scraperwiki.scrape(HOUSE_URL)
    house_parser = etree.HTMLParser()
    house_tree = etree.parse(StringIO.StringIO(house_html), house_parser)
    house = {}
    
    # Record name
    house['title'] = house_tree.xpath('string(//h1[@id="propertytype"])')

    # Record as Sales/Lettings
    house['saleType'] = saleType

    # Image
    image_url = house_tree.xpath('//img[@id="mainphoto"]')[0]
    image_url = image_url.xpath('//img[@id="mainphoto"]/@src')[0]
    house['image_url'] = image_url
    
    # Get price into nice numerical-only format
    price = house_tree.xpath('string(//div[@id="amount"])') 
    price = price[1:] # remove unicode £ at start
    price = price.replace(",", "") # remove commas
    price = price.strip() # remove whitespace
    price = int(price) # check it is converted to an integer
    if price < 200: # *** ASSUMPTION: If cost is less than 200, assume it means PCW (week), so multiply by 4 to get PCM (month)
        price = price * 4 # cost per week must be multiplied by 4 (~4.34) to get the month cost
    print str(price) + " : ", # print price to console
    house['price'] = price # store the price after updating

    # Address
    address = house_tree.xpath('string(//div[@id="addresscontainer"])')
    # strip out \t, \r, \n
    address = address.replace("\n", "")
    address = address.replace("\t", "")
    address = address.replace("\r", "")
    # add spaces back in
    address = address.replace(",", ", ")
    house['address'] = address
    print address + " : ",

    house['link'] = HOUSE_URL
    house['sold'] = 0 # the property is 'on the market' because it appears in the search results

    # save to database or update it (cannot replace by 'save')
    # delete if already exists and replace (add) with new copy (ordering is regardless)
    # REMEMBER you cannot delete from swdata if the database is cleaned down
    # This will result in 1 permittable error if the database has been cleared down
    try:
        scraperwiki.sqlite.execute("delete from swdata where link = '" + house['link'] + "'") # this operation is silent
        scraperwiki.sqlite.commit()
    except scraperwiki.sqlite.SqliteError, e:
        print "Error: " + str(e)
    
    print "Adding... ",
    scraperwiki.sqlite.save(['link'], house) # save to database
    print "OK"

# Gather list of results for an individual location. 
def scrape_results_page(results_url, saleType, initial=False):
    global iProp
    results_url = DOMAIN + results_url
    try:
        html = scraperwiki.scrape(results_url)
    except:
        print "Error: ",sys.exc_info()
        req = Request(results_url)
        try:
            response = urlopen(req)
        except httplib.HTTPException, e:
            print "Error in HTTP: ",e
            sys.exit(-1)
        except URLError, e:
            if hasattr(e, 'reason'):
                print 'Error: We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'Error: The server couldnt fulfill the request.'
                print 'Error code: ', e.code
            sys.exit(-1)
        except:
            print "Error: unknown error: ",sys.exc_info()
            sys.exit(-1)
        else:
            html = response.read()
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO.StringIO(html), parser)
    house_links = tree.xpath('//ol[@id="summaries"]//a[starts-with(text(), "More details")]/@href')
    for house_link in house_links:
        print str(iProp) + " : ",
        scrape_individual_house(house_link, saleType)
        iProp += 1
    if initial:
        results_links = tree.xpath('//ul[@class="items"]//a/@href')
        for r in results_links:
            scrape_results_page(r, saleType)

# Clean up old properties
def clean_old_links():
    print "Now checking all properties for status... "
    allProperties = scraperwiki.sqlite.select("* from swdata") # returns a dict
    for aProperty in allProperties:
        # Try to scrape the page of the property
        # If certain information cannot be read from it, then that property has been deleted
        house_html = ''
        try:
            house_html = scraperwiki.scrape(aProperty['link'])
        except:
            print "Error: ",sys.exc_info()
            req = Request(aProperty['link'])
            try:
                response = urlopen(req)
            except httplib.HTTPException, e:
                print "Error in HTTP: ",e
                sys.exit(-1)
            except URLError, e:
                if hasattr(e, 'reason'):
                    print 'Error: We failed to reach a server.'
                    print 'Reason: ', e.reason
                elif hasattr(e, 'code'):
                    print 'Error: The server couldnt fulfill the request.'
                    print 'Error code: ', e.code
                sys.exit(-1)
            except:
                print "Error: unknown error: ",sys.exc_info()
                sys.exit(-1)
            else:
                house_html = response.read()
        house_parser = etree.HTMLParser()
        house_tree = etree.parse(StringIO.StringIO(house_html), house_parser)
        try:
            house_text = house_tree.xpath('string(//div[@class="errorbox"])')
            if 'removed this property' in house_text:
                # mark the property as sold as it is showing the 'removed' page on Rightmove
                try:
                    scraperwiki.sqlite.execute("update swdata set sold = 1 where link = '" + aProperty['link'] + "'")
                    scraperwiki.sqlite.commit()
                    print aProperty['link'] + " : Updated (sold/let by)"
                except scraperwiki.sqlite.SqliteError, e:
                    print "Error: " + str(e)
            else:
                # if this passes then keep the property and update it just incase it was previously removed
                try:
                    scraperwiki.sqlite.execute("update swdata set sold = 0 where link = '" + aProperty['link'] + "'")
                    scraperwiki.sqlite.commit()
                    print aProperty['link'] + " : Updated (available)"
                except scraperwiki.sqlite.SqliteError, e:
                    print "Error: " + str(e)
        except etree.XPathError, e:
            print "Error: " + str(e)

def empty_database():
    try:
        print "Deleting existing table... ",
        scraperwiki.sqlite.execute("drop table if exists swdata")
        scraperwiki.sqlite.commit()
        print "OK"
    except scraperwiki.sqlite.SqliteError, e:
        print str(e)

# Alternative: just drop the table and forget all the old ones
#empty_database()

# 2. Sales
url1 = '/property-for-sale/find/JB-Property-Services/Waltham-Abbey.html/svr/3112?locationIdentifier=BRANCH^7557&sortByPriceDescending=false&includeSSTC=true&_includeSSTC=on'
INITIAL_URL = url1
# download the search page
#scrape_results_page(INITIAL_URL, "Sales", initial=True)

# 3. Lettings
url2 = '/property-to-rent/find/JB-Property-Services/Waltham-Abbey.html/svr/3112?locationIdentifier=BRANCH^7557&sortByPriceDescending=false&includeLetAgreed=true&_includeLetAgreed=on'
INITIAL_URL = url2
# download the search page
scrape_results_page(INITIAL_URL, "Lettings", initial=True)

# 1. Check all existing properties and flag as remove if they no longer exist

clean_old_links()
