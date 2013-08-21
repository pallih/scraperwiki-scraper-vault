import scraperwiki
import lxml.html
import lxml.etree
import urlparse
import datetime
import re

# Register of modification orders, mostly to enable off-road traffic

url = "http://www.derbyshire.gov.uk/leisure/countryside/Access_recreation/rights_of_way/register_of_application/register.asp"


# Other registers that need scraping:
#  http://www.derbyshire.gov.uk/leisure/countryside/Access_recreation/rights_of_way/path_closure_register/search_the_register/register_all.asp
#  http://www.derbyshire.gov.uk/leisure/countryside/Access_recreation/rights_of_way/declaration_register/default.asp
#  http://www.planning-inspectorate.gov.uk/pins/row_order_advertising/councils/2010/Derbyshire_County_Council.htm

# Also, every path and byway appears to have a unique ID.  These need to be obtained somehow.


def Main():
    doc = lxml.html.parse(url)
    root = doc.getroot()
    rows = root.cssselect("table#AutoNumber1 tr")

    headings = [ td.text  for td in rows[0].cssselect("td strong") ]
    print headings
    assert headings == ['Application Number', 'Date of Receipt', 'Description', 'Stage', 'Parish'], lxml.etree.tostring(rows[0])
    for i in range(1, len(rows)):
        row = rows[i]
        #print lxml.etree.tostring(row)
        data = dict(zip(headings, row.cssselect("td")))

        alink = data["Application Number"].cssselect("a")[0]
        data["Application Number"] = alink.text.strip()
        data["link"] = urlparse.urljoin(url, alink.get("href"))

        print i, data["link"]
        ldate = data["Date of Receipt"].text.strip()
        if ldate:
            data["Date of Receipt"] = datetime.date(int(ldate[6:10]), int(ldate[3:5]), int(ldate[0:2]))
        else:
            print "Missing date", lxml.etree.tostring(row)
            del data["Date of Receipt"]
            
        data["Description"] = data["Description"].text.strip()
        data["Stage"] = data["Stage"].text.strip()
        data["Parish"] = data["Parish"].text.strip()
        
        FurtherData(data)
        

def FurtherData(data):
    doc = lxml.html.parse(data["link"])
    root = doc.getroot()
    rows = root.cssselect("table#AutoNumber4 tr")
    headings = [ td.text  for td in rows[0].cssselect("td strong") ]
    assert 3 <= len(rows) <= 10
    assert headings == ['Effect', 'District', 'Parish', 'Path', 'Start', 'End'], lxml.etree.tostring(rows[0])

    result = [ ]
    for row in rows[1:-1]:
        tds = row.cssselect("td")
        rowtexts = [ td.text.strip()  for td in tds ]
        fdata = dict(zip(headings, rowtexts))
        ldata = data.copy()
    
        #assert fdata["Parish"] == ldata["Parish"], (fdata, ldata)
        ldata["Parish"] = fdata["Parish"] # we can get multiple parishes in the same application
        ldata["Effect"] = fdata["Effect"]
        ldata["District"] = fdata["District"]
        ldata["Path"] = fdata["Path"]
        ldata["Start"] = fdata["Start"]
        ldata["End"] = fdata["End"]

        colour = "ffffff"
        if re.search("(?i)footpath|(?:add|addition of) a fp", ldata["Effect"]):
            colour = "00ff00"
        if re.search("(?i)bridleway|upgrade(?: to)? Bw", ldata["Effect"]):
            colour = "00aa00"
        if re.search("BOAT|Byway Open to All Traffic", ldata["Effect"]) or re.search("BOAT|Byway Open to [Aa]ll Traffic", ldata["Description"]):
            colour = "ff0000"
        ldata["colour"] = colour
                                
        if ldata["Start"] != "Not Mapped":
            lonstart, latstart = scraperwiki.geo.osgb_to_lonlat(str(ldata["Start"]))
            lonend, latend = scraperwiki.geo.osgb_to_lonlat(str(ldata["End"]))
            latlng = [(latstart+latend)/2, (lonstart+lonend)/2]
        else:
            latlng = None

        date = ldata.get("Date of Receipt")
        scraperwiki.datastore.save(unique_keys=["Application Number", "Path"], data=ldata, latlng=latlng, date=date, silent=False)
                                
        result.append(ldata)
    return result

Main()
import scraperwiki
import lxml.html
import lxml.etree
import urlparse
import datetime
import re

# Register of modification orders, mostly to enable off-road traffic

url = "http://www.derbyshire.gov.uk/leisure/countryside/Access_recreation/rights_of_way/register_of_application/register.asp"


# Other registers that need scraping:
#  http://www.derbyshire.gov.uk/leisure/countryside/Access_recreation/rights_of_way/path_closure_register/search_the_register/register_all.asp
#  http://www.derbyshire.gov.uk/leisure/countryside/Access_recreation/rights_of_way/declaration_register/default.asp
#  http://www.planning-inspectorate.gov.uk/pins/row_order_advertising/councils/2010/Derbyshire_County_Council.htm

# Also, every path and byway appears to have a unique ID.  These need to be obtained somehow.


def Main():
    doc = lxml.html.parse(url)
    root = doc.getroot()
    rows = root.cssselect("table#AutoNumber1 tr")

    headings = [ td.text  for td in rows[0].cssselect("td strong") ]
    print headings
    assert headings == ['Application Number', 'Date of Receipt', 'Description', 'Stage', 'Parish'], lxml.etree.tostring(rows[0])
    for i in range(1, len(rows)):
        row = rows[i]
        #print lxml.etree.tostring(row)
        data = dict(zip(headings, row.cssselect("td")))

        alink = data["Application Number"].cssselect("a")[0]
        data["Application Number"] = alink.text.strip()
        data["link"] = urlparse.urljoin(url, alink.get("href"))

        print i, data["link"]
        ldate = data["Date of Receipt"].text.strip()
        if ldate:
            data["Date of Receipt"] = datetime.date(int(ldate[6:10]), int(ldate[3:5]), int(ldate[0:2]))
        else:
            print "Missing date", lxml.etree.tostring(row)
            del data["Date of Receipt"]
            
        data["Description"] = data["Description"].text.strip()
        data["Stage"] = data["Stage"].text.strip()
        data["Parish"] = data["Parish"].text.strip()
        
        FurtherData(data)
        

def FurtherData(data):
    doc = lxml.html.parse(data["link"])
    root = doc.getroot()
    rows = root.cssselect("table#AutoNumber4 tr")
    headings = [ td.text  for td in rows[0].cssselect("td strong") ]
    assert 3 <= len(rows) <= 10
    assert headings == ['Effect', 'District', 'Parish', 'Path', 'Start', 'End'], lxml.etree.tostring(rows[0])

    result = [ ]
    for row in rows[1:-1]:
        tds = row.cssselect("td")
        rowtexts = [ td.text.strip()  for td in tds ]
        fdata = dict(zip(headings, rowtexts))
        ldata = data.copy()
    
        #assert fdata["Parish"] == ldata["Parish"], (fdata, ldata)
        ldata["Parish"] = fdata["Parish"] # we can get multiple parishes in the same application
        ldata["Effect"] = fdata["Effect"]
        ldata["District"] = fdata["District"]
        ldata["Path"] = fdata["Path"]
        ldata["Start"] = fdata["Start"]
        ldata["End"] = fdata["End"]

        colour = "ffffff"
        if re.search("(?i)footpath|(?:add|addition of) a fp", ldata["Effect"]):
            colour = "00ff00"
        if re.search("(?i)bridleway|upgrade(?: to)? Bw", ldata["Effect"]):
            colour = "00aa00"
        if re.search("BOAT|Byway Open to All Traffic", ldata["Effect"]) or re.search("BOAT|Byway Open to [Aa]ll Traffic", ldata["Description"]):
            colour = "ff0000"
        ldata["colour"] = colour
                                
        if ldata["Start"] != "Not Mapped":
            lonstart, latstart = scraperwiki.geo.osgb_to_lonlat(str(ldata["Start"]))
            lonend, latend = scraperwiki.geo.osgb_to_lonlat(str(ldata["End"]))
            latlng = [(latstart+latend)/2, (lonstart+lonend)/2]
        else:
            latlng = None

        date = ldata.get("Date of Receipt")
        scraperwiki.datastore.save(unique_keys=["Application Number", "Path"], data=ldata, latlng=latlng, date=date, silent=False)
                                
        result.append(ldata)
    return result

Main()
import scraperwiki
import lxml.html
import lxml.etree
import urlparse
import datetime
import re

# Register of modification orders, mostly to enable off-road traffic

url = "http://www.derbyshire.gov.uk/leisure/countryside/Access_recreation/rights_of_way/register_of_application/register.asp"


# Other registers that need scraping:
#  http://www.derbyshire.gov.uk/leisure/countryside/Access_recreation/rights_of_way/path_closure_register/search_the_register/register_all.asp
#  http://www.derbyshire.gov.uk/leisure/countryside/Access_recreation/rights_of_way/declaration_register/default.asp
#  http://www.planning-inspectorate.gov.uk/pins/row_order_advertising/councils/2010/Derbyshire_County_Council.htm

# Also, every path and byway appears to have a unique ID.  These need to be obtained somehow.


def Main():
    doc = lxml.html.parse(url)
    root = doc.getroot()
    rows = root.cssselect("table#AutoNumber1 tr")

    headings = [ td.text  for td in rows[0].cssselect("td strong") ]
    print headings
    assert headings == ['Application Number', 'Date of Receipt', 'Description', 'Stage', 'Parish'], lxml.etree.tostring(rows[0])
    for i in range(1, len(rows)):
        row = rows[i]
        #print lxml.etree.tostring(row)
        data = dict(zip(headings, row.cssselect("td")))

        alink = data["Application Number"].cssselect("a")[0]
        data["Application Number"] = alink.text.strip()
        data["link"] = urlparse.urljoin(url, alink.get("href"))

        print i, data["link"]
        ldate = data["Date of Receipt"].text.strip()
        if ldate:
            data["Date of Receipt"] = datetime.date(int(ldate[6:10]), int(ldate[3:5]), int(ldate[0:2]))
        else:
            print "Missing date", lxml.etree.tostring(row)
            del data["Date of Receipt"]
            
        data["Description"] = data["Description"].text.strip()
        data["Stage"] = data["Stage"].text.strip()
        data["Parish"] = data["Parish"].text.strip()
        
        FurtherData(data)
        

def FurtherData(data):
    doc = lxml.html.parse(data["link"])
    root = doc.getroot()
    rows = root.cssselect("table#AutoNumber4 tr")
    headings = [ td.text  for td in rows[0].cssselect("td strong") ]
    assert 3 <= len(rows) <= 10
    assert headings == ['Effect', 'District', 'Parish', 'Path', 'Start', 'End'], lxml.etree.tostring(rows[0])

    result = [ ]
    for row in rows[1:-1]:
        tds = row.cssselect("td")
        rowtexts = [ td.text.strip()  for td in tds ]
        fdata = dict(zip(headings, rowtexts))
        ldata = data.copy()
    
        #assert fdata["Parish"] == ldata["Parish"], (fdata, ldata)
        ldata["Parish"] = fdata["Parish"] # we can get multiple parishes in the same application
        ldata["Effect"] = fdata["Effect"]
        ldata["District"] = fdata["District"]
        ldata["Path"] = fdata["Path"]
        ldata["Start"] = fdata["Start"]
        ldata["End"] = fdata["End"]

        colour = "ffffff"
        if re.search("(?i)footpath|(?:add|addition of) a fp", ldata["Effect"]):
            colour = "00ff00"
        if re.search("(?i)bridleway|upgrade(?: to)? Bw", ldata["Effect"]):
            colour = "00aa00"
        if re.search("BOAT|Byway Open to All Traffic", ldata["Effect"]) or re.search("BOAT|Byway Open to [Aa]ll Traffic", ldata["Description"]):
            colour = "ff0000"
        ldata["colour"] = colour
                                
        if ldata["Start"] != "Not Mapped":
            lonstart, latstart = scraperwiki.geo.osgb_to_lonlat(str(ldata["Start"]))
            lonend, latend = scraperwiki.geo.osgb_to_lonlat(str(ldata["End"]))
            latlng = [(latstart+latend)/2, (lonstart+lonend)/2]
        else:
            latlng = None

        date = ldata.get("Date of Receipt")
        scraperwiki.datastore.save(unique_keys=["Application Number", "Path"], data=ldata, latlng=latlng, date=date, silent=False)
                                
        result.append(ldata)
    return result

Main()
import scraperwiki
import lxml.html
import lxml.etree
import urlparse
import datetime
import re

# Register of modification orders, mostly to enable off-road traffic

url = "http://www.derbyshire.gov.uk/leisure/countryside/Access_recreation/rights_of_way/register_of_application/register.asp"


# Other registers that need scraping:
#  http://www.derbyshire.gov.uk/leisure/countryside/Access_recreation/rights_of_way/path_closure_register/search_the_register/register_all.asp
#  http://www.derbyshire.gov.uk/leisure/countryside/Access_recreation/rights_of_way/declaration_register/default.asp
#  http://www.planning-inspectorate.gov.uk/pins/row_order_advertising/councils/2010/Derbyshire_County_Council.htm

# Also, every path and byway appears to have a unique ID.  These need to be obtained somehow.


def Main():
    doc = lxml.html.parse(url)
    root = doc.getroot()
    rows = root.cssselect("table#AutoNumber1 tr")

    headings = [ td.text  for td in rows[0].cssselect("td strong") ]
    print headings
    assert headings == ['Application Number', 'Date of Receipt', 'Description', 'Stage', 'Parish'], lxml.etree.tostring(rows[0])
    for i in range(1, len(rows)):
        row = rows[i]
        #print lxml.etree.tostring(row)
        data = dict(zip(headings, row.cssselect("td")))

        alink = data["Application Number"].cssselect("a")[0]
        data["Application Number"] = alink.text.strip()
        data["link"] = urlparse.urljoin(url, alink.get("href"))

        print i, data["link"]
        ldate = data["Date of Receipt"].text.strip()
        if ldate:
            data["Date of Receipt"] = datetime.date(int(ldate[6:10]), int(ldate[3:5]), int(ldate[0:2]))
        else:
            print "Missing date", lxml.etree.tostring(row)
            del data["Date of Receipt"]
            
        data["Description"] = data["Description"].text.strip()
        data["Stage"] = data["Stage"].text.strip()
        data["Parish"] = data["Parish"].text.strip()
        
        FurtherData(data)
        

def FurtherData(data):
    doc = lxml.html.parse(data["link"])
    root = doc.getroot()
    rows = root.cssselect("table#AutoNumber4 tr")
    headings = [ td.text  for td in rows[0].cssselect("td strong") ]
    assert 3 <= len(rows) <= 10
    assert headings == ['Effect', 'District', 'Parish', 'Path', 'Start', 'End'], lxml.etree.tostring(rows[0])

    result = [ ]
    for row in rows[1:-1]:
        tds = row.cssselect("td")
        rowtexts = [ td.text.strip()  for td in tds ]
        fdata = dict(zip(headings, rowtexts))
        ldata = data.copy()
    
        #assert fdata["Parish"] == ldata["Parish"], (fdata, ldata)
        ldata["Parish"] = fdata["Parish"] # we can get multiple parishes in the same application
        ldata["Effect"] = fdata["Effect"]
        ldata["District"] = fdata["District"]
        ldata["Path"] = fdata["Path"]
        ldata["Start"] = fdata["Start"]
        ldata["End"] = fdata["End"]

        colour = "ffffff"
        if re.search("(?i)footpath|(?:add|addition of) a fp", ldata["Effect"]):
            colour = "00ff00"
        if re.search("(?i)bridleway|upgrade(?: to)? Bw", ldata["Effect"]):
            colour = "00aa00"
        if re.search("BOAT|Byway Open to All Traffic", ldata["Effect"]) or re.search("BOAT|Byway Open to [Aa]ll Traffic", ldata["Description"]):
            colour = "ff0000"
        ldata["colour"] = colour
                                
        if ldata["Start"] != "Not Mapped":
            lonstart, latstart = scraperwiki.geo.osgb_to_lonlat(str(ldata["Start"]))
            lonend, latend = scraperwiki.geo.osgb_to_lonlat(str(ldata["End"]))
            latlng = [(latstart+latend)/2, (lonstart+lonend)/2]
        else:
            latlng = None

        date = ldata.get("Date of Receipt")
        scraperwiki.datastore.save(unique_keys=["Application Number", "Path"], data=ldata, latlng=latlng, date=date, silent=False)
                                
        result.append(ldata)
    return result

Main()
