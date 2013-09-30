# Collect data about specific properties (to monitor price over time)

from lxml import etree
from lxml.etree import tostring
from datetime import datetime
import time
import scraperwiki
import StringIO

DOMAIN = 'http://www.rightmove.co.uk' 

iProp = 0

try:
    scraperwiki.sqlite.execute("""
        create table magic
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."

def scrape_individual_house(house_url, propertyID):
    # download the unique property page
    HOUSE_URL = (DOMAIN + house_url).split('/svr/')[0]
    print 'Scraping %s' % HOUSE_URL
    house_html = scraperwiki.scrape(HOUSE_URL)
    house_parser = etree.HTMLParser()
    house_tree = etree.parse(StringIO.StringIO(house_html), house_parser)
    house_text = house_tree.xpath('string(//div[@class="propertyDetailDescription"])')
    # In this version, we don't care about views
    if True: #'views' in house_text.lower() or 'elevated position' in house_text.lower():
        house = {}
        stopped_phrase = None
        title = house_tree.xpath('string(//h1[@id="propertytype"])')
        
        # add date stamp
        timestamp = time.ctime()
        house['date'] = timestamp
        # add the property ID number
        house['propertyID'] = propertyID
        
        # unique key
        house['key'] = timestamp + propertyID
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
        item_text = house_text
        print # ends the line
        house['link'] = HOUSE_URL
        scraperwiki.sqlite.save(['link'], house, table_name='magic')
# scraperwiki.sqlite.save(unique_keys=[data={'payload':'fat beats'}, table_name='magic')

# list of properties to monitor
properties = [
    '38780849',
    '25614450',
    '38699822'
]

for property in properties:
    url = '/property-for-sale/property-' + property + '.html'
    scrape_individual_house(url, property)
# Collect data about specific properties (to monitor price over time)

from lxml import etree
from lxml.etree import tostring
from datetime import datetime
import time
import scraperwiki
import StringIO

DOMAIN = 'http://www.rightmove.co.uk' 

iProp = 0

try:
    scraperwiki.sqlite.execute("""
        create table magic
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."

def scrape_individual_house(house_url, propertyID):
    # download the unique property page
    HOUSE_URL = (DOMAIN + house_url).split('/svr/')[0]
    print 'Scraping %s' % HOUSE_URL
    house_html = scraperwiki.scrape(HOUSE_URL)
    house_parser = etree.HTMLParser()
    house_tree = etree.parse(StringIO.StringIO(house_html), house_parser)
    house_text = house_tree.xpath('string(//div[@class="propertyDetailDescription"])')
    # In this version, we don't care about views
    if True: #'views' in house_text.lower() or 'elevated position' in house_text.lower():
        house = {}
        stopped_phrase = None
        title = house_tree.xpath('string(//h1[@id="propertytype"])')
        
        # add date stamp
        timestamp = time.ctime()
        house['date'] = timestamp
        # add the property ID number
        house['propertyID'] = propertyID
        
        # unique key
        house['key'] = timestamp + propertyID
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
        item_text = house_text
        print # ends the line
        house['link'] = HOUSE_URL
        scraperwiki.sqlite.save(['link'], house, table_name='magic')
# scraperwiki.sqlite.save(unique_keys=[data={'payload':'fat beats'}, table_name='magic')

# list of properties to monitor
properties = [
    '38780849',
    '25614450',
    '38699822'
]

for property in properties:
    url = '/property-for-sale/property-' + property + '.html'
    scrape_individual_house(url, property)
