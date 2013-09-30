import scraperwiki
import urlparse
import lxml.html
import lxml.etree
import mechanize
import re
import simplejson, urllib
from datetime import datetime

GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false'

# Geocodes an address string and returns a lat/long pair
def geocode(address,sensor=False, **geo_args):
    geo_args.update({
        'address': address,
        'region': 'uk'
    })

    url = GEOCODE_BASE_URL + '&' + urllib.urlencode(geo_args)
    result = simplejson.load(urllib.urlopen(url))
    if len(result['results'])>0:
        lat = result['results'][0]['geometry']['location']['lat']
        lng = result['results'][0]['geometry']['location']['lng']
    else:
        lat = 0
        lng = 0
    return lat, lng

def scrape_detail(id):

    # Set up the detail page url
    url = 'http://planning.fife.gov.uk/online/applicationDetails.do?activeTab=details&keyVal='+id
    
    # Set up the browser
    br = mechanize.Browser()
    br.set_handle_robots(False)
    
    # Open the detail page URL and get it ready to scrape
    response = br.open(url)
    root = lxml.html.fromstring(response.read())
    
    # Print the url for debugging in case the scraper fails
    print "detail link: " + br.response().geturl()
    
    # Set up a record to place the data
    record = {}
    
    # Place records that always appear in the response
    record['applicant name'] = root.xpath('.//table//th[contains(text(), "Applicant Name")]')[0].getnext().xpath('.//text()')[0]

    record['ward'] = root.xpath('.//table//th[contains(text(), "Ward")]')[0].getnext().xpath('.//text()')[0]
    record['case officer'] = root.xpath('.//table//th[contains(text(), "Case Office")]')[0].getnext().xpath('.//text()')[0]
    record['date_scraped'] = datetime.now()
    
    # Place records that do not always appear in the response, enters 'N/A' if not
    if root.xpath('.//table//th[contains(text(), "Agent Name")]'):
        record['agent name'] = root.xpath('.//table//th[contains(text(), "Agent Name")]')[0].getnext().xpath('.//text()')[0]
    else:
        record['agent name'] = 'N/A'

    if root.xpath('.//table//th[contains(text(), "Agent Address")]'):
        record['agent address'] = root.xpath('.//table//th[contains(text(), "Agent Address")]')[0].getnext().xpath('.//text()')[0]
    else:
        record['agent address'] = 'N/A'


    return record
    
# scrape_table function: gets passed an individual page to scrape
def scrape_list_page(root):
    rows = root.cssselect("div.col-a li")  # selects all <li> blocks within <div class = "col-a">
    counter = 0
    
    # Only scrape if the response has a list of items, i.e. there is more than one planning 
    # application in the week searched. Otherwise the response redirects to the detail page 
    # for the one application and is ignored by the scraper.
    
    if rows:
      for row in rows:
        counter += 1
        print "looking at page item: " + str(counter)
        
        # Set up our data record - we'll need it later
        record = {}
        
        # Get the detail link
        detail_link = row.xpath('.//a/@href')[0]
        
        # Place items into the data record
        record['ref'] = ' '.join(row.xpath('.//p[@class="metaInfo"]/text()')[0].split())
        record['date received'] = ' '.join(row.xpath('.//p[@class="metaInfo"]/text()')[1].split())
        record['address'] = ' '.join(row.xpath('.//p[@class="address"]/text()')[0].split())
        record['proposal'] = ' '.join(row.xpath('.//a/text()')[0].split())
        record['status'] = ' '.join(row.xpath('.//p[@class="metaInfo"]/text()')[3].split())
        record['detail'] = re.search(r'\w+$', detail_link).group()
        record['lat'], record['lng'] = geocode(record['address'])
        
        # Scrape the associated applicaiton page for details
        detail = scrape_detail(record['detail'])
        
        # Scrapes the detail page and updates the data record with its items
        record.update(detail)
        
        # Store the data
        scraperwiki.sqlite.save(["ref"], record)
    else:
        return

# Set up the start URL         
search_url = 'http://planning.fife.gov.uk/online/search.do?action=weeklyList'

# Set up the browser
br = mechanize.Browser()
br.set_handle_robots(False)

# Open the start URL
response = br.open(search_url)

# Select the search form and submit
br.select_form(name="searchCriteriaForm")
br.submit()

# Set up the response page to be scraped and send it to the scrape function
response_lxml = lxml.html.fromstring(br.response().read())
scrape_list_page(response_lxml)
 
 import scraperwiki
import urlparse
import lxml.html
import lxml.etree
import mechanize
import re
import simplejson, urllib
from datetime import datetime

GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false'

# Geocodes an address string and returns a lat/long pair
def geocode(address,sensor=False, **geo_args):
    geo_args.update({
        'address': address,
        'region': 'uk'
    })

    url = GEOCODE_BASE_URL + '&' + urllib.urlencode(geo_args)
    result = simplejson.load(urllib.urlopen(url))
    if len(result['results'])>0:
        lat = result['results'][0]['geometry']['location']['lat']
        lng = result['results'][0]['geometry']['location']['lng']
    else:
        lat = 0
        lng = 0
    return lat, lng

def scrape_detail(id):

    # Set up the detail page url
    url = 'http://planning.fife.gov.uk/online/applicationDetails.do?activeTab=details&keyVal='+id
    
    # Set up the browser
    br = mechanize.Browser()
    br.set_handle_robots(False)
    
    # Open the detail page URL and get it ready to scrape
    response = br.open(url)
    root = lxml.html.fromstring(response.read())
    
    # Print the url for debugging in case the scraper fails
    print "detail link: " + br.response().geturl()
    
    # Set up a record to place the data
    record = {}
    
    # Place records that always appear in the response
    record['applicant name'] = root.xpath('.//table//th[contains(text(), "Applicant Name")]')[0].getnext().xpath('.//text()')[0]

    record['ward'] = root.xpath('.//table//th[contains(text(), "Ward")]')[0].getnext().xpath('.//text()')[0]
    record['case officer'] = root.xpath('.//table//th[contains(text(), "Case Office")]')[0].getnext().xpath('.//text()')[0]
    record['date_scraped'] = datetime.now()
    
    # Place records that do not always appear in the response, enters 'N/A' if not
    if root.xpath('.//table//th[contains(text(), "Agent Name")]'):
        record['agent name'] = root.xpath('.//table//th[contains(text(), "Agent Name")]')[0].getnext().xpath('.//text()')[0]
    else:
        record['agent name'] = 'N/A'

    if root.xpath('.//table//th[contains(text(), "Agent Address")]'):
        record['agent address'] = root.xpath('.//table//th[contains(text(), "Agent Address")]')[0].getnext().xpath('.//text()')[0]
    else:
        record['agent address'] = 'N/A'


    return record
    
# scrape_table function: gets passed an individual page to scrape
def scrape_list_page(root):
    rows = root.cssselect("div.col-a li")  # selects all <li> blocks within <div class = "col-a">
    counter = 0
    
    # Only scrape if the response has a list of items, i.e. there is more than one planning 
    # application in the week searched. Otherwise the response redirects to the detail page 
    # for the one application and is ignored by the scraper.
    
    if rows:
      for row in rows:
        counter += 1
        print "looking at page item: " + str(counter)
        
        # Set up our data record - we'll need it later
        record = {}
        
        # Get the detail link
        detail_link = row.xpath('.//a/@href')[0]
        
        # Place items into the data record
        record['ref'] = ' '.join(row.xpath('.//p[@class="metaInfo"]/text()')[0].split())
        record['date received'] = ' '.join(row.xpath('.//p[@class="metaInfo"]/text()')[1].split())
        record['address'] = ' '.join(row.xpath('.//p[@class="address"]/text()')[0].split())
        record['proposal'] = ' '.join(row.xpath('.//a/text()')[0].split())
        record['status'] = ' '.join(row.xpath('.//p[@class="metaInfo"]/text()')[3].split())
        record['detail'] = re.search(r'\w+$', detail_link).group()
        record['lat'], record['lng'] = geocode(record['address'])
        
        # Scrape the associated applicaiton page for details
        detail = scrape_detail(record['detail'])
        
        # Scrapes the detail page and updates the data record with its items
        record.update(detail)
        
        # Store the data
        scraperwiki.sqlite.save(["ref"], record)
    else:
        return

# Set up the start URL         
search_url = 'http://planning.fife.gov.uk/online/search.do?action=weeklyList'

# Set up the browser
br = mechanize.Browser()
br.set_handle_robots(False)

# Open the start URL
response = br.open(search_url)

# Select the search form and submit
br.select_form(name="searchCriteriaForm")
br.submit()

# Set up the response page to be scraped and send it to the scrape function
response_lxml = lxml.html.fromstring(br.response().read())
scrape_list_page(response_lxml)
 
 