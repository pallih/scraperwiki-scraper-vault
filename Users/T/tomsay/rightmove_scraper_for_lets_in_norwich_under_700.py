# Collect data from one estate agent only - all sales and lettings including sold/let agreed

# Kept separate from 'rightmove' deliberately
# Version without views criterion
# but does require detached houses
from lxml import etree
from lxml.etree import tostring
from datetime import datetime
import scraperwiki
import StringIO

stop_phrases = ["bungalow", "bunaglow" ]
DOMAIN = 'http://www.rightmove.co.uk' 

iProp = 0

def scrape_individual_house(house_url, saleType):
    # download the unique property page
    HOUSE_URL = (DOMAIN + house_url).split('/svr/')[0]
    #print 'Scraping %s' % HOUSE_URL
    house_html = scraperwiki.scrape(HOUSE_URL)
    house_parser = etree.HTMLParser()
    house_tree = etree.parse(StringIO.StringIO(house_html), house_parser)
    house_text = house_tree.xpath('string(//div[@class="propertyDetailDescription"])')
    # In this version, we don't care about views
    if True: #'views' in house_text.lower() or 'elevated position' in house_text.lower():
        house = {}
        stopped_phrase = None
        title = house_tree.xpath('string(//h1[@id="propertytype"])')
        # Check for stop phrases
        for sp in stop_phrases:
            if (sp in house_text.lower()):
                #print 'Ignoring %s because of stop phrase: %s' % (HOUSE_URL, sp)
                stopped_phrase = sp
            if (sp in title.lower()):
                stopped_phrase = sp
        #if not any(d.get('link') == HOUSE_URL for d in house_items):

        house['saleType'] = saleType

        # the correct syntax is string(//img/@src)
        #image_url = tostring(house_tree.xpath('//img[@id="mainphoto"]')[0])
        house['image_url'] = ''
        image_url = ''
        try:
            image_url = house_tree.xpath('//img[@id="mainphoto"]')[0]
            image_url = image_url.xpath('//img[@id="mainphoto"]/@src')[0]
            house['image_url'] = image_url
        except:
            pass 
           
        # Get price into nice numerical-only format
        house['price'] = 0
        price = 0
        try:
            price = house_tree.xpath('string(//div[@id="amount"])') 
            price = price[1:] # remove unicode £ at start
            price = price.replace(",", "") # remove commas
            price = price.strip() # remove whitespace
            price = int(price) # check it is converted to an integer
            if price < 200:
                price = price * 4 # cost per week must be multiplied by 4 (~4.34) to get the month cost
            print str(price) + " : ", # print price to console
            house['price'] = price # store the price after updating
        except:
            pass

        address = house_tree.xpath('string(//div[@id="addresscontainer"])')
        # strip out \t, \r, \n
        address = address.replace("\n", "")
        address = address.replace("\t", "")
        address = address.replace("\r", "")
        # add spaces back in
        address = address.replace(",", ", ")
        house['address'] = address
        print address + " : ",

        map_img = house_tree.xpath('//a[@id="minimapwrapper"]/img')
        if map_img:
            map_img = tostring(house_tree.xpath('//a[@id="minimapwrapper"]/img')[0])
        else:
            map_img = ''
        
        house['title'] = title
        #print 'HOUSE FOUND! %s, %s ' % (house['title'], HOUSE_URL)
        item_text = '<a href="' + HOUSE_URL + '">' + image_url + '</a>'
        #item_text += '<div style="position:relative;">'
        item_text += '<a href="' + HOUSE_URL + '">' + map_img + '</a>'
        #item_text += '<img id="googlemapicon" src="http://www.rightmove.co.uk/ps/images11074/maps/icons/rmpin.png"'
        #item_text += ' style="position:absolute;top:100px;left:100px;alt="Property location" /></div>'
        item_text += house_text
        item_text = item_text.replace("views","<span style='font-weight:bold;color:red;'>views</span>")
        #house['description'] = item_text.replace("fireplace","<span style='font-weight:bold;color:red;'>fireplace</span>")
        if stopped_phrase:
            a = 1
            #house['stop'] = stopped_phrase
        #else:
        #    #house['stop'] = ''
        #    print HOUSE_URL
        print # ends the line
        house['link'] = HOUSE_URL
        scraperwiki.sqlite.save(['link'], house)

# Gather list of results for an individual location. 
def scrape_results_page(results_url, saleType, initial=False):
    global iProp
    results_url = DOMAIN + results_url
    html = scraperwiki.scrape(results_url)
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


            

# 1. Delete all existing records

try:
    print "Deleting existing table... ",
    scraperwiki.sqlite.execute("drop table if exists swdata")
    print "OK"
except scraperwiki.sqlite.SqliteError, e:
    print str(e)

#clean_old_links()

# 3. Lettings
#url2 = '/property-to-rent/find/JB-Property-Services/Waltham-Abbey.html/svr/3112?locationIdentifier=BRANCH^7557&sortByPriceDescending=false&includeLetAgreed=true&_includeLetAgreed=on'
#url2 = '/property-to-rent/find.html?#searchType=RENT&locationIdentifier=REGION%5E1018&insId=2&radius=0.0&displayPropertyType=&minBedrooms=2&maxBedrooms=&minPrice=&maxPrice=700&maxDaysSinceAdded=&retirement=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare=false'
#INITIAL_URL = url2
#scrape_results_page(INITIAL_URL, "Lettings", initial=True)

exchanges = {
    'Birmingham':   ('B1','REGION%5E162'),
    'Leeds':  ('LS1','REGION%5E787'),

}

for exc, pcode in exchanges.iteritems():
    url = '/property-to-rent/find.html?locationIdentifier=' + pcode[1] + '&radius=1.0&houseFlatShare=true'
    scrape_results_page(url, exc, initial=True)
# Collect data from one estate agent only - all sales and lettings including sold/let agreed

# Kept separate from 'rightmove' deliberately
# Version without views criterion
# but does require detached houses
from lxml import etree
from lxml.etree import tostring
from datetime import datetime
import scraperwiki
import StringIO

stop_phrases = ["bungalow", "bunaglow" ]
DOMAIN = 'http://www.rightmove.co.uk' 

iProp = 0

def scrape_individual_house(house_url, saleType):
    # download the unique property page
    HOUSE_URL = (DOMAIN + house_url).split('/svr/')[0]
    #print 'Scraping %s' % HOUSE_URL
    house_html = scraperwiki.scrape(HOUSE_URL)
    house_parser = etree.HTMLParser()
    house_tree = etree.parse(StringIO.StringIO(house_html), house_parser)
    house_text = house_tree.xpath('string(//div[@class="propertyDetailDescription"])')
    # In this version, we don't care about views
    if True: #'views' in house_text.lower() or 'elevated position' in house_text.lower():
        house = {}
        stopped_phrase = None
        title = house_tree.xpath('string(//h1[@id="propertytype"])')
        # Check for stop phrases
        for sp in stop_phrases:
            if (sp in house_text.lower()):
                #print 'Ignoring %s because of stop phrase: %s' % (HOUSE_URL, sp)
                stopped_phrase = sp
            if (sp in title.lower()):
                stopped_phrase = sp
        #if not any(d.get('link') == HOUSE_URL for d in house_items):

        house['saleType'] = saleType

        # the correct syntax is string(//img/@src)
        #image_url = tostring(house_tree.xpath('//img[@id="mainphoto"]')[0])
        house['image_url'] = ''
        image_url = ''
        try:
            image_url = house_tree.xpath('//img[@id="mainphoto"]')[0]
            image_url = image_url.xpath('//img[@id="mainphoto"]/@src')[0]
            house['image_url'] = image_url
        except:
            pass 
           
        # Get price into nice numerical-only format
        house['price'] = 0
        price = 0
        try:
            price = house_tree.xpath('string(//div[@id="amount"])') 
            price = price[1:] # remove unicode £ at start
            price = price.replace(",", "") # remove commas
            price = price.strip() # remove whitespace
            price = int(price) # check it is converted to an integer
            if price < 200:
                price = price * 4 # cost per week must be multiplied by 4 (~4.34) to get the month cost
            print str(price) + " : ", # print price to console
            house['price'] = price # store the price after updating
        except:
            pass

        address = house_tree.xpath('string(//div[@id="addresscontainer"])')
        # strip out \t, \r, \n
        address = address.replace("\n", "")
        address = address.replace("\t", "")
        address = address.replace("\r", "")
        # add spaces back in
        address = address.replace(",", ", ")
        house['address'] = address
        print address + " : ",

        map_img = house_tree.xpath('//a[@id="minimapwrapper"]/img')
        if map_img:
            map_img = tostring(house_tree.xpath('//a[@id="minimapwrapper"]/img')[0])
        else:
            map_img = ''
        
        house['title'] = title
        #print 'HOUSE FOUND! %s, %s ' % (house['title'], HOUSE_URL)
        item_text = '<a href="' + HOUSE_URL + '">' + image_url + '</a>'
        #item_text += '<div style="position:relative;">'
        item_text += '<a href="' + HOUSE_URL + '">' + map_img + '</a>'
        #item_text += '<img id="googlemapicon" src="http://www.rightmove.co.uk/ps/images11074/maps/icons/rmpin.png"'
        #item_text += ' style="position:absolute;top:100px;left:100px;alt="Property location" /></div>'
        item_text += house_text
        item_text = item_text.replace("views","<span style='font-weight:bold;color:red;'>views</span>")
        #house['description'] = item_text.replace("fireplace","<span style='font-weight:bold;color:red;'>fireplace</span>")
        if stopped_phrase:
            a = 1
            #house['stop'] = stopped_phrase
        #else:
        #    #house['stop'] = ''
        #    print HOUSE_URL
        print # ends the line
        house['link'] = HOUSE_URL
        scraperwiki.sqlite.save(['link'], house)

# Gather list of results for an individual location. 
def scrape_results_page(results_url, saleType, initial=False):
    global iProp
    results_url = DOMAIN + results_url
    html = scraperwiki.scrape(results_url)
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


            

# 1. Delete all existing records

try:
    print "Deleting existing table... ",
    scraperwiki.sqlite.execute("drop table if exists swdata")
    print "OK"
except scraperwiki.sqlite.SqliteError, e:
    print str(e)

#clean_old_links()

# 3. Lettings
#url2 = '/property-to-rent/find/JB-Property-Services/Waltham-Abbey.html/svr/3112?locationIdentifier=BRANCH^7557&sortByPriceDescending=false&includeLetAgreed=true&_includeLetAgreed=on'
#url2 = '/property-to-rent/find.html?#searchType=RENT&locationIdentifier=REGION%5E1018&insId=2&radius=0.0&displayPropertyType=&minBedrooms=2&maxBedrooms=&minPrice=&maxPrice=700&maxDaysSinceAdded=&retirement=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare=false'
#INITIAL_URL = url2
#scrape_results_page(INITIAL_URL, "Lettings", initial=True)

exchanges = {
    'Birmingham':   ('B1','REGION%5E162'),
    'Leeds':  ('LS1','REGION%5E787'),

}

for exc, pcode in exchanges.iteritems():
    url = '/property-to-rent/find.html?locationIdentifier=' + pcode[1] + '&radius=1.0&houseFlatShare=true'
    scrape_results_page(url, exc, initial=True)
