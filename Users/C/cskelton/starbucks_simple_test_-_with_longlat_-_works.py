###############################################################################
# working fine, just looks like a problem opening scraperwiki csvs in Excel
# need to upload to Google Docs first, then download as Excel; then missing fields populate

import scraperwiki
import urlparse
import lxml.html
import urllib
import time

storenumber = 7544

while storenumber < 20000:
    time.sleep(5) # longer sleep to avoid getting locked out by servers
    storenumber = storenumber + 1 # putting this at top instead of bottom seemed to make a difference for redirect loops
    url = 'http://www.starbucks.ca/store/' + str(storenumber)
    html = urllib.urlopen(url).read()
    print html
    root = lxml.html.fromstring(html)
    addressblock = root.cssselect("div.adr")
    if addressblock:
        storename = root.cssselect("h2")[2]
        street = root.cssselect("span.street-address")
        extended = root.cssselect("span.extended-address")
        locality = root.cssselect("span.locality")
        region = root.cssselect("span.region")
        postcode = root.cssselect("span.postal-code")        
        country = root.cssselect("span.country-name")
        tel = root.cssselect("div.tel")
        longlat = root.cssselect("div#map")
        record = {}
        record['StoreID'] = str(storenumber)
        try:
            record['Storename'] = storename.text_content()
        except:
            record['Storename'] = ""
        try:
            record['Street'] = street[0].text_content()
        except:
            record['Street'] = ""
        try:
            record['Extended'] = extended[0].text_content()
        except:
            record['Extended'] = ""
        try:
            record['Locality'] = locality[0].text_content()
        except:
            record['Locality'] = ""
        try:
            record['Region'] = region[0].text_content()
        except:
            record['Region'] = ""
        try:
            record['Postcode'] = postcode[0].text_content()
        except:
            record['Postcode'] = ""
        try:
            record['Country'] = country[0].text_content()
        except:
            record['Country'] = ""
        try:
            record['Tel'] = tel[0].text_content()
        except:
            record['Tel'] = ""
        try:
            record['Lat'] = longlat[0].attrib['data-store-lat']
        except:
            record['Lat'] = ""
        try:
            record['Long'] = longlat[0].attrib['data-store-lon']
        except:
            record['Long'] = ""
        print record
        scraperwiki.sqlite.save(["StoreID"], record)


