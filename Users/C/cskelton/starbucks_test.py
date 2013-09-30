###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html
import urllib

storenumber = 0

while storenumber < 20:
    storenumber = storenumber + 1
    storenumberstring = str(storenumber)
    print storenumberstring
    storeURL = 'http://www.starbucks.ca/store/' + storenumberstring
    print storeURL
    html = urllib.urlopen(storeURL).read()
    print html
    root = lxml.html.fromstring(html)
    storename = root.cssselect("h2")[2]
    street = root.cssselect("span.street-address")
    extended = root.cssselect("span.extended-address")
    locality = root.cssselect("span.locality")
    region = root.cssselect("span.region")
    postalcode = root.cssselect("span.postal-code")
    country = root.cssselect("span.country-name")
    telephone = root.cssselect("span.tel")   
    print storename.text_content() 
    try:
        record = {}
        record['ID'] = storenumberstring
        record['Storename'] = storename.text_content()
        record['Street'] = street[0].text_content()
        record['Extended'] = extended[0].text_content()
        record['Locality'] = locality[0].text_content()
        record['Region'] = region[0].text_content()
        record['Postal'] = postalcode[0].text_content()
        record['Country'] = country[0].text_content()
        record['Telephone'] = telephone[0].text_content()
        print record, '------------'
        # Finally, save the record to the datastore - 'Artist' is our unique key
    scraperwiki.sqlite.save(["Storename"], record)

###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html
import urllib

storenumber = 0

while storenumber < 20:
    storenumber = storenumber + 1
    storenumberstring = str(storenumber)
    print storenumberstring
    storeURL = 'http://www.starbucks.ca/store/' + storenumberstring
    print storeURL
    html = urllib.urlopen(storeURL).read()
    print html
    root = lxml.html.fromstring(html)
    storename = root.cssselect("h2")[2]
    street = root.cssselect("span.street-address")
    extended = root.cssselect("span.extended-address")
    locality = root.cssselect("span.locality")
    region = root.cssselect("span.region")
    postalcode = root.cssselect("span.postal-code")
    country = root.cssselect("span.country-name")
    telephone = root.cssselect("span.tel")   
    print storename.text_content() 
    try:
        record = {}
        record['ID'] = storenumberstring
        record['Storename'] = storename.text_content()
        record['Street'] = street[0].text_content()
        record['Extended'] = extended[0].text_content()
        record['Locality'] = locality[0].text_content()
        record['Region'] = region[0].text_content()
        record['Postal'] = postalcode[0].text_content()
        record['Country'] = country[0].text_content()
        record['Telephone'] = telephone[0].text_content()
        print record, '------------'
        # Finally, save the record to the datastore - 'Artist' is our unique key
    scraperwiki.sqlite.save(["Storename"], record)

