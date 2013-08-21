import scraperwiki
import urlparse
import lxml.html
import re
import urllib2
from lxml.html import tostring

monitors = ['u3011','herpderp']

for monitor in monitors:
    print 'SEARCHING FOR "' + monitor + '"...'

    # initialize record
    record = {}

    # search for product page
    search_result = 'http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&Order=BESTMATCH&Description=' + monitor
    
    # turn search page HTML into lxml object
    root = lxml.html.fromstring(scraperwiki.scrape(search_result))

    # Calm down guyblow, you need to make sure you actually returned results
    # Otherwise you will just select whatever random item NewEgg decides to feature
    if root.cssselect('h3.alert'):
        print 'No item could be found - you may want to return some sort of error code or alert structure instead'
        continue
    else:
        result_element = root.cssselect('div.itemCell')[0]
        title_element = result_element.cssselect('div.itemText')[0]
        # Get the title description only if the line description (more detail) does not exist
        # Store the record as the list of values first and then assign the value from one of the elements
        # This is just a little hack to avoid creating excess elements and is usually considered a half-kludge... I've been drinking
        record['name'] = title_element.cssselect('span.itemDescription')
        if len(record['name']) >= 2:
            record['name'] = record['name'][1].text
        else:
            record['name'] = record['name'][0].text
        # Get the url of the product details page - surely there is a function to select elements by tag or is it just cssselect?
        record['url'] = result_element.cssselect('a')[0].attrib['href']
        # Get the price element and value using a similar trick as in the name
        record['price'] = result_element.cssselect('li.priceFinal')[0]
        record['price'] = record['price'].cssselect('strong')[0].text + record['price'].cssselect('sup')[0].text
        # Go to the product details page
        # root = lxml.html.fromstring(scraperwiki.scrape(record['url']))
        # Print results
        print record['name']
        print record['url']
        print record['price']