import scraperwiki
import lxml.html
import urllib
import urllib2
import json
import httplib
import re

geolink_regexp = re.compile("@(-?[0-9]+\\.[0-9]+),\\+? ?(-?[0-9]+\\.[0-9]+)")
postcode_regexp = re.compile("\\b[a-zA-Z]{1,2}[0-9]{1,2}[a-zA-Z]? ?[0-9a-zA-Z]{3}")
postcode_translations = { 'SL6 OER': 'SL6 0ER' } # Taplow Ct

regions = []
events = []
rnum = int(scraperwiki.sqlite.get_var("rnum" , 0))
enum = int(scraperwiki.sqlite.get_var("enum" , 0))
#rnum = 1
#enum = 0
batch_size = 10
ecount = 0
rcount = 0
# One of 'printable' or 'normal'
smode = 'normal'

def find_postcode(addr):
    m = postcode_regexp.search(addr)
    if m is not None:
        return m.group().upper()
    else:
        return None

def get_postcode(addr):
    pc = find_postcode(addr)
    if pc is not None:
        if pc in postcode_translations:
            return postcode_translations[pc]
        else:
            return pc.replace(" O", " 0")
    else:
        return None

def scrape_regions():
    regions_list = []
    html = scraperwiki.scrape("http://www.heritageopendays.org.uk/directory/")
    root = lxml.html.fromstring(html)
    map = root.cssselect("map[name='map']")[0]
    for area in map.cssselect("area"):
        regions_list.append({'name': area.get("alt").replace("Browse events in the ", "").replace(" region", ""), 'href': area.get("href")});
    return regions_list

def scrape_normal():
    pass

def scrape_printable():
    global ecount, rcount, enum
    for region in regions:
        ecount = 0
        if (region['name'] != "London and other UK Events"):
            print "Scraping %s (starting with record %s)" % (region['name'], enum)
            html = scraperwiki.scrape("http://www.heritageopendays.org.uk/directory/print/region/%s/" % (urllib.quote(region['name'])))
            root = lxml.html.fromstring(html)
            for div in root.cssselect("div.event"):
                if ecount >= enum:
                    add_event(scrape_printable_page(div, region))
                ecount = ecount + 1
    
            add_event(None, True)
            print "Finished %s" % (region['name'])
            ecount = 0
            enum = 0
    
        rcount = rcount + 1

def scrape_printable_page(div, region):
    h3 = div.find("h3")
    # Iterate through h4/p elements
    #h4s = div.findall("h4")
    items = div.cssselect("h4, p")
    item_name = ""
    item_value = ""

    # Event properties
    event_name = h3.text_content()
    address = ""
    description = ""
    directions = ""
    opening_times = ""
    prebooking_required = ""
    access_information = ""
    full_wheelchair_access = ""
    additional_information = ""
    organiser = ""
    latlng = (None, None)

    # Address is first h4
    if len(items) > 0 and items[0].tag == "h4":
        address = items[0].text_content().strip()

    # Then subsequent h4/p combinations contain other data
    for item in items[1:len(items)-1]:
        if item.tag == "h4":
            item_name = item.text_content().strip()
            item_value = ""
        else:
            item_value = item.text_content().strip()
            if item_name != "":
                if item_name == "Address":
                    address = item_value
                elif item_name == "Description":
                    description = item_value
                elif item_name == "Directions":
                    directions = item_value
                elif item_name == "Opening Times":
                    opening_times = item_value
                elif item_name == "Pre-Booking Required":
                    prebooking_required = item_value
                elif item_name == "Access Information":
                    access_information = item_value
                elif item_name == "Full Wheelchair Access?":
                    full_wheelchair_access = item_value
                elif item_name == "Additional Information":
                    additional_information = item_value
                elif item_name == "Organised By":
                    organiser = item_value
                else:
                    print "WARNING: Unknown item %s" % (item_name)
            item_name = ""

    if address != "":
        postcode = scraperwiki.geo.extract_gb_postcode(address)
        if postcode is not None and postcode != False:
            try:
                latlng = ukp_postcode_to_latlng(postcode)
            except urllib2.HTTPError as e:
                print "Warning: HTTP error resolving postcode for %s (%s) - %s" % (event_name, postcode, e)
            except urllib2.URLError as e:
                print "Warning: URL opening error resolving postcode for %s (%s) - %s" % (event_name, postcode, e)
            except httplib.BadStatusLine as e:
                print "Warning: BadStatusLine exception resolving postcode for %s (%s) - %s" % (event_name, postcode, e)
        else:
            print "Warning: Could not parse postcode for %s (%s)" % (event_name, address)

    #print h3.text_content()

    return {
        'region': region['name'],
        'name': event_name,
        'address' : address,
        'postcode' : postcode,
        'lat' : latlng[0],
        'lng' : latlng[1],
        'description': description,
        'directions': directions,
        'opening_times': opening_times,
        'prebooking_required': prebooking_required,
        'access_information': access_information,
        'full_wheelchair_access': full_wheelchair_access,
        'additional_information': additional_information,
        'organiser': organiser
    }

def scrape_normal():
    global ecount, rcount, enum
    for region in regions:
        ecount = 0
        scrape_listing(region)

def scrape_listing(region):
    global enum, ecount, rcount
    url = "http://www.heritageopendays.org.uk%s" % (region['href'].replace("/region/county/", "/regions/"))
    while url is not None:
        print "Scraping %s, (starting with record %s) from %s" % (region['name'], enum, url)
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        tables = root.cssselect('div#content > table')
        if len(tables) == 1:
            #print table.text_content()
            #tbody = tables[0].find("tbody")
            #if tbody is not None:
            for tr in tables[0].findall("tr"):
                #print "yes"
                cells = tr.findall("td")
                if len(cells) > 0:
                    link = cells[0].find("a")
                    if link is not None:
                        ename = link.text_content().strip()
                        eventurl = link.get("href")
                        if (eventurl is not None and eventurl != ""):
                            if ecount >= enum:
                                e = scrape_event({'name': ename, 'url': eventurl}, region)
                                add_event(e)
                            ecount = ecount + 1
    
        url = None
        # Try to get next page
        for a in root.cssselect('div#content p a'):
            if a.text_content() == ">":
                url = a.get("href")

    rcount = rcount + 1
    print "Finished %s" % (region['name'])
    ecount = 0
    enum = 0
    add_event(None, True)

def scrape_event(event, region):
    url = "http://www.heritageopendays.org.uk" + event['url']
    #print "Scraping event %s" % (event['name'])
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    divs = root.cssselect('div#content')

    if len(divs) != 1:
        return None

    event_code = None
    pos = event['url'].rstrip('/').rfind('/')
    if pos > -1:
        event_code = event['url'][pos:].strip('/')
    div = divs[0]
    h2 = div.find("h2")
    h3 = div.find("h3")
    # Iterate through h4/p elements
    #h4s = div.findall("h4")
    items = div.cssselect("h4, p")
    images = div.cssselect("p img")
    links = div.cssselect("p a")
    imglist = []
    item_name = ""
    item_value = ""

    # Event properties
    event_name = h2.text_content().strip()
    address = h3.text_content().strip()
    postcode = ""
    description = ""
    directions = ""
    opening_times = ""
    prebooking_required = "No"
    access_information = ""
    full_wheelchair_access = ""
    additional_information = ""
    organiser = ""
    website = ""
    latlng = (None, None)
    not_normally_open = 0
    not_normally_free = 0

    # Then subsequent h4/p combinations contain other data
    for item in items[1:len(items)-1]:
        if item.tag == "h4":
            item_name = item.text_content().strip()
            item_value = ""
        else:
            item_value = item.text_content().strip()
            if item_name != "" and item_value != "":
                if item_name == "Description":
                    description = item_value
                elif item_name == "Directions":
                    directions = item_value
                elif item_name == "Opening Times":
                    opening_times = item_value
                elif item_name == "Pre-Booking Required":
                    prebooking_required = item_value
                elif item_name == "Access":
                    access_information = item_value
                elif item_name == "Additional Information":
                    additional_information = item_value
                elif item_name == "Organised By":
                    organiser = item_value
                elif item_name == "Website":
                    website = item_value
                elif item_name == "Public Transport Details":
                    pass
                elif item_name == "Special Activities for Children/Families":
                    pass
                else:
                    print "WARNING: Unknown item %s" % (item_name)
            item_name = ""

    # Some information also in images
    for img in images:
        imglist.append(img.get("src"))
        #print img.get("src")
    
    if '/images/facility-keys/icon-ramp-access.gif' in imglist:
        full_wheelchair_access = 'Yes'
    if '/images/facility-keys/icon-not-normally-open.gif' in imglist:
        not_normally_open = 1
    if '/images/facility-keys/icon-not_normally-free.gif' in imglist:
        not_normally_free = 1
    if '/images/facility-keys/icon-partially-disabled.gif' in imglist:
        full_wheelchair_access = 'Partial'

    #http://maps.google.co.uk/maps?q=Please note that these maps are provided as a guide only, and may not be entirely accurate@51.530895,+ -0.692764&iwloc=A&hl=en
    # Get geocode from page
    for link in links:
        #print link.text_content().strip()
        if link.text_content().strip() == "View Map":
            href = link.get("href")
            m = geolink_regexp.search(href)
            if m is not None:
                latlng = (m.group(1), m.group(2))
                #print "Found geocode %s,%s in link " % latlng

    # Get the postcode
    if address != "":
        postcode = get_postcode(address)

    # Get lat/lon from postcode, if not available in web page
    if postcode is not None and postcode != "" and latlng[0] is None:
        try:
            latlng = ukp_postcode_to_latlng(postcode)
        except urllib2.HTTPError as e:
            print "Warning: HTTP error resolving postcode for %s (%s) - %s" % (event_name, postcode, e)
        except urllib2.URLError as e:
            print "Warning: URL opening error resolving postcode for %s (%s) - %s" % (event_name, postcode, e)
        except httplib.BadStatusLine as e:
            print "Warning: BadStatusLine exception resolving postcode for %s (%s) - %s" % (event_name, postcode, e)

    #print event_name
    #print event_code

    return {
        'region': region['name'],
        'name': event_name,
        'address' : address,
        'postcode' : postcode,
        'lat' : latlng[0],
        'lng' : latlng[1],
        'description': description,
        'directions': directions,
        'opening_times': opening_times,
        'prebooking_required': prebooking_required,
        'access_information': access_information,
        'full_wheelchair_access': full_wheelchair_access,
        'additional_information': additional_information,
        'organiser': organiser,
        'event_code': event_code,
        'not_normally_open': not_normally_open,
        'not_normally_free': not_normally_free
    }

# Lookup postcode from uk-postcodes.com
def ukp_postcode_to_latlng(postcode):
    #return scraperwiki.geo.gb_postcode_to_latlng(postcode)
    resp = urllib2.urlopen("http://www.uk-postcodes.com/postcode/%s.json" % (urllib.quote(postcode.replace(" ", ""))))
    respJson = json.loads(resp.read())
    resp.close()
    if 'geo' in respJson:
        return (respJson['geo']['lat'], respJson['geo']['lng'])
    else:
        return None

# Save the data in batches
def add_event(event=None, force=False):
    global events
    if event is not None:
        events.append(event)
    if len(events) >= batch_size or force == True:
        #for e in events
            #scraperwiki.sqlite.execute("UPDATE swdata SET event_code='%s', not_normally_open=%s, not_normally_free=%s WHERE name='%s' and region='%s'" % (e['event_code'], e['not_normally_open'], e['not_normally_free'], e['name'], e['region']))
        scraperwiki.sqlite.save(unique_keys=['region', 'name'], data=events)
        scraperwiki.sqlite.save_var("rnum", rcount)
        scraperwiki.sqlite.save_var("enum", ecount)
        events = []

# Get list of regions
regions = scrape_regions()

# Only process the regions we haven't saved yet
regions = regions[rnum:len(regions)-1]
rcount = rnum

# Temporary
#regions = [{'name': 'South West' }]
#regions = [regions[0]] # South East
enum = 0

# Scrape pages
if smode == 'printable':
    scrape_printable()
    #scraperwiki.sqlite.execute('ALTER TABLE swdata ADD COLUMN not_normally_open INTEGER DEFAULT 0')
elif smode == 'normal':
    scrape_normal()

import scraperwiki
import lxml.html
import urllib
import urllib2
import json
import httplib
import re

geolink_regexp = re.compile("@(-?[0-9]+\\.[0-9]+),\\+? ?(-?[0-9]+\\.[0-9]+)")
postcode_regexp = re.compile("\\b[a-zA-Z]{1,2}[0-9]{1,2}[a-zA-Z]? ?[0-9a-zA-Z]{3}")
postcode_translations = { 'SL6 OER': 'SL6 0ER' } # Taplow Ct

regions = []
events = []
rnum = int(scraperwiki.sqlite.get_var("rnum" , 0))
enum = int(scraperwiki.sqlite.get_var("enum" , 0))
#rnum = 1
#enum = 0
batch_size = 10
ecount = 0
rcount = 0
# One of 'printable' or 'normal'
smode = 'normal'

def find_postcode(addr):
    m = postcode_regexp.search(addr)
    if m is not None:
        return m.group().upper()
    else:
        return None

def get_postcode(addr):
    pc = find_postcode(addr)
    if pc is not None:
        if pc in postcode_translations:
            return postcode_translations[pc]
        else:
            return pc.replace(" O", " 0")
    else:
        return None

def scrape_regions():
    regions_list = []
    html = scraperwiki.scrape("http://www.heritageopendays.org.uk/directory/")
    root = lxml.html.fromstring(html)
    map = root.cssselect("map[name='map']")[0]
    for area in map.cssselect("area"):
        regions_list.append({'name': area.get("alt").replace("Browse events in the ", "").replace(" region", ""), 'href': area.get("href")});
    return regions_list

def scrape_normal():
    pass

def scrape_printable():
    global ecount, rcount, enum
    for region in regions:
        ecount = 0
        if (region['name'] != "London and other UK Events"):
            print "Scraping %s (starting with record %s)" % (region['name'], enum)
            html = scraperwiki.scrape("http://www.heritageopendays.org.uk/directory/print/region/%s/" % (urllib.quote(region['name'])))
            root = lxml.html.fromstring(html)
            for div in root.cssselect("div.event"):
                if ecount >= enum:
                    add_event(scrape_printable_page(div, region))
                ecount = ecount + 1
    
            add_event(None, True)
            print "Finished %s" % (region['name'])
            ecount = 0
            enum = 0
    
        rcount = rcount + 1

def scrape_printable_page(div, region):
    h3 = div.find("h3")
    # Iterate through h4/p elements
    #h4s = div.findall("h4")
    items = div.cssselect("h4, p")
    item_name = ""
    item_value = ""

    # Event properties
    event_name = h3.text_content()
    address = ""
    description = ""
    directions = ""
    opening_times = ""
    prebooking_required = ""
    access_information = ""
    full_wheelchair_access = ""
    additional_information = ""
    organiser = ""
    latlng = (None, None)

    # Address is first h4
    if len(items) > 0 and items[0].tag == "h4":
        address = items[0].text_content().strip()

    # Then subsequent h4/p combinations contain other data
    for item in items[1:len(items)-1]:
        if item.tag == "h4":
            item_name = item.text_content().strip()
            item_value = ""
        else:
            item_value = item.text_content().strip()
            if item_name != "":
                if item_name == "Address":
                    address = item_value
                elif item_name == "Description":
                    description = item_value
                elif item_name == "Directions":
                    directions = item_value
                elif item_name == "Opening Times":
                    opening_times = item_value
                elif item_name == "Pre-Booking Required":
                    prebooking_required = item_value
                elif item_name == "Access Information":
                    access_information = item_value
                elif item_name == "Full Wheelchair Access?":
                    full_wheelchair_access = item_value
                elif item_name == "Additional Information":
                    additional_information = item_value
                elif item_name == "Organised By":
                    organiser = item_value
                else:
                    print "WARNING: Unknown item %s" % (item_name)
            item_name = ""

    if address != "":
        postcode = scraperwiki.geo.extract_gb_postcode(address)
        if postcode is not None and postcode != False:
            try:
                latlng = ukp_postcode_to_latlng(postcode)
            except urllib2.HTTPError as e:
                print "Warning: HTTP error resolving postcode for %s (%s) - %s" % (event_name, postcode, e)
            except urllib2.URLError as e:
                print "Warning: URL opening error resolving postcode for %s (%s) - %s" % (event_name, postcode, e)
            except httplib.BadStatusLine as e:
                print "Warning: BadStatusLine exception resolving postcode for %s (%s) - %s" % (event_name, postcode, e)
        else:
            print "Warning: Could not parse postcode for %s (%s)" % (event_name, address)

    #print h3.text_content()

    return {
        'region': region['name'],
        'name': event_name,
        'address' : address,
        'postcode' : postcode,
        'lat' : latlng[0],
        'lng' : latlng[1],
        'description': description,
        'directions': directions,
        'opening_times': opening_times,
        'prebooking_required': prebooking_required,
        'access_information': access_information,
        'full_wheelchair_access': full_wheelchair_access,
        'additional_information': additional_information,
        'organiser': organiser
    }

def scrape_normal():
    global ecount, rcount, enum
    for region in regions:
        ecount = 0
        scrape_listing(region)

def scrape_listing(region):
    global enum, ecount, rcount
    url = "http://www.heritageopendays.org.uk%s" % (region['href'].replace("/region/county/", "/regions/"))
    while url is not None:
        print "Scraping %s, (starting with record %s) from %s" % (region['name'], enum, url)
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        tables = root.cssselect('div#content > table')
        if len(tables) == 1:
            #print table.text_content()
            #tbody = tables[0].find("tbody")
            #if tbody is not None:
            for tr in tables[0].findall("tr"):
                #print "yes"
                cells = tr.findall("td")
                if len(cells) > 0:
                    link = cells[0].find("a")
                    if link is not None:
                        ename = link.text_content().strip()
                        eventurl = link.get("href")
                        if (eventurl is not None and eventurl != ""):
                            if ecount >= enum:
                                e = scrape_event({'name': ename, 'url': eventurl}, region)
                                add_event(e)
                            ecount = ecount + 1
    
        url = None
        # Try to get next page
        for a in root.cssselect('div#content p a'):
            if a.text_content() == ">":
                url = a.get("href")

    rcount = rcount + 1
    print "Finished %s" % (region['name'])
    ecount = 0
    enum = 0
    add_event(None, True)

def scrape_event(event, region):
    url = "http://www.heritageopendays.org.uk" + event['url']
    #print "Scraping event %s" % (event['name'])
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    divs = root.cssselect('div#content')

    if len(divs) != 1:
        return None

    event_code = None
    pos = event['url'].rstrip('/').rfind('/')
    if pos > -1:
        event_code = event['url'][pos:].strip('/')
    div = divs[0]
    h2 = div.find("h2")
    h3 = div.find("h3")
    # Iterate through h4/p elements
    #h4s = div.findall("h4")
    items = div.cssselect("h4, p")
    images = div.cssselect("p img")
    links = div.cssselect("p a")
    imglist = []
    item_name = ""
    item_value = ""

    # Event properties
    event_name = h2.text_content().strip()
    address = h3.text_content().strip()
    postcode = ""
    description = ""
    directions = ""
    opening_times = ""
    prebooking_required = "No"
    access_information = ""
    full_wheelchair_access = ""
    additional_information = ""
    organiser = ""
    website = ""
    latlng = (None, None)
    not_normally_open = 0
    not_normally_free = 0

    # Then subsequent h4/p combinations contain other data
    for item in items[1:len(items)-1]:
        if item.tag == "h4":
            item_name = item.text_content().strip()
            item_value = ""
        else:
            item_value = item.text_content().strip()
            if item_name != "" and item_value != "":
                if item_name == "Description":
                    description = item_value
                elif item_name == "Directions":
                    directions = item_value
                elif item_name == "Opening Times":
                    opening_times = item_value
                elif item_name == "Pre-Booking Required":
                    prebooking_required = item_value
                elif item_name == "Access":
                    access_information = item_value
                elif item_name == "Additional Information":
                    additional_information = item_value
                elif item_name == "Organised By":
                    organiser = item_value
                elif item_name == "Website":
                    website = item_value
                elif item_name == "Public Transport Details":
                    pass
                elif item_name == "Special Activities for Children/Families":
                    pass
                else:
                    print "WARNING: Unknown item %s" % (item_name)
            item_name = ""

    # Some information also in images
    for img in images:
        imglist.append(img.get("src"))
        #print img.get("src")
    
    if '/images/facility-keys/icon-ramp-access.gif' in imglist:
        full_wheelchair_access = 'Yes'
    if '/images/facility-keys/icon-not-normally-open.gif' in imglist:
        not_normally_open = 1
    if '/images/facility-keys/icon-not_normally-free.gif' in imglist:
        not_normally_free = 1
    if '/images/facility-keys/icon-partially-disabled.gif' in imglist:
        full_wheelchair_access = 'Partial'

    #http://maps.google.co.uk/maps?q=Please note that these maps are provided as a guide only, and may not be entirely accurate@51.530895,+ -0.692764&iwloc=A&hl=en
    # Get geocode from page
    for link in links:
        #print link.text_content().strip()
        if link.text_content().strip() == "View Map":
            href = link.get("href")
            m = geolink_regexp.search(href)
            if m is not None:
                latlng = (m.group(1), m.group(2))
                #print "Found geocode %s,%s in link " % latlng

    # Get the postcode
    if address != "":
        postcode = get_postcode(address)

    # Get lat/lon from postcode, if not available in web page
    if postcode is not None and postcode != "" and latlng[0] is None:
        try:
            latlng = ukp_postcode_to_latlng(postcode)
        except urllib2.HTTPError as e:
            print "Warning: HTTP error resolving postcode for %s (%s) - %s" % (event_name, postcode, e)
        except urllib2.URLError as e:
            print "Warning: URL opening error resolving postcode for %s (%s) - %s" % (event_name, postcode, e)
        except httplib.BadStatusLine as e:
            print "Warning: BadStatusLine exception resolving postcode for %s (%s) - %s" % (event_name, postcode, e)

    #print event_name
    #print event_code

    return {
        'region': region['name'],
        'name': event_name,
        'address' : address,
        'postcode' : postcode,
        'lat' : latlng[0],
        'lng' : latlng[1],
        'description': description,
        'directions': directions,
        'opening_times': opening_times,
        'prebooking_required': prebooking_required,
        'access_information': access_information,
        'full_wheelchair_access': full_wheelchair_access,
        'additional_information': additional_information,
        'organiser': organiser,
        'event_code': event_code,
        'not_normally_open': not_normally_open,
        'not_normally_free': not_normally_free
    }

# Lookup postcode from uk-postcodes.com
def ukp_postcode_to_latlng(postcode):
    #return scraperwiki.geo.gb_postcode_to_latlng(postcode)
    resp = urllib2.urlopen("http://www.uk-postcodes.com/postcode/%s.json" % (urllib.quote(postcode.replace(" ", ""))))
    respJson = json.loads(resp.read())
    resp.close()
    if 'geo' in respJson:
        return (respJson['geo']['lat'], respJson['geo']['lng'])
    else:
        return None

# Save the data in batches
def add_event(event=None, force=False):
    global events
    if event is not None:
        events.append(event)
    if len(events) >= batch_size or force == True:
        #for e in events
            #scraperwiki.sqlite.execute("UPDATE swdata SET event_code='%s', not_normally_open=%s, not_normally_free=%s WHERE name='%s' and region='%s'" % (e['event_code'], e['not_normally_open'], e['not_normally_free'], e['name'], e['region']))
        scraperwiki.sqlite.save(unique_keys=['region', 'name'], data=events)
        scraperwiki.sqlite.save_var("rnum", rcount)
        scraperwiki.sqlite.save_var("enum", ecount)
        events = []

# Get list of regions
regions = scrape_regions()

# Only process the regions we haven't saved yet
regions = regions[rnum:len(regions)-1]
rcount = rnum

# Temporary
#regions = [{'name': 'South West' }]
#regions = [regions[0]] # South East
enum = 0

# Scrape pages
if smode == 'printable':
    scrape_printable()
    #scraperwiki.sqlite.execute('ALTER TABLE swdata ADD COLUMN not_normally_open INTEGER DEFAULT 0')
elif smode == 'normal':
    scrape_normal()

