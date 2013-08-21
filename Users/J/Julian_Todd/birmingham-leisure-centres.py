import urllib
import re
import scraperwiki
import lxml
import lxml.html
import urlparse

gid = 0
idletters = "adjmptw"  # and g

def CleanupData(data):
    global gid
    assert data['adr'] == '', data
    del data['adr']
    if "country-name" in data:
        del data["country-name"]
    if not data.get('postal-code'):
        data['postal-code'] = re.search(',([\s\w]*)$', data['extended-address']).group(1).strip()

    postcode = data.get('postal-code')
    latlng = scraperwiki.geo.gb_postcode_to_latlng(postcode)
    data["shortname"] = re.sub("(?:Community|Centre|Sports|Sport|Fitness|Leisure| and| &).*$", "", data.get("name"))
    data["shortname"] = re.sub(" Swimming", "", data["shortname"]).strip()
    data["numid"] = gid
    data["id"] = "g%s%s%s" % (idletters[gid % 7], idletters[(gid/7) % 7], idletters[(gid/49) % 7])
    gid += 1
    scraperwiki.datastore.save(unique_keys=["numid", "id"], data=data, latlng=latlng)
    

def ParseIndexPage(url, root):
    print lxml.etree.tostring(root)
    for tr in root.cssselect("tr.vcard"):
        lk, addr, contact = tr.cssselect("td")
        assert lk[0].tag == "a", lxml.etree.tostring(tr)
        data = { }
        data["url"] = urlparse.urljoin(url, lk[0].attrib.get("href"))
        data["name"] = lk[0].text.strip()
        for span in addr.cssselect("span"):
            data[span.attrib.get("class")] = span.text.strip()
        data["telephone"] = contact[0].text.strip()
        print data
        CleanupData(data)
        

# link sourced from:
# http://www.birmingham.gov.uk/cs/Satellite/leisureinfo?packedargs=website%3D4&rendermode=live
def Main():
    url = "http://www.birmingham.gov.uk/cs/Satellite?pagename=BCC/Common/Wrapper/Wrapper&"+\
      "childpagename=SystemAdmin/Page"+\
      "Layout&c=Page&cid=1186481130144&searchPageId=1223115664505"+\
      "&searchForm=1&pagination=1&entityname=&entitykeywords=&entitytype=Venue&entityarea=Any"+\
      "&entityfacilities=Leisure+Centre&entityservices=Any&search=Search"

    while True:
        root = lxml.html.parse(url).getroot()
        ParseIndexPage(url, root)
        unext = [ a.attrib.get("href")  for a in root.cssselect("a")  if a.text == "Next" ]
        if not unext:
            break
        url = urlparse.urljoin(url, unext[0])

        
Main()import urllib
import re
import scraperwiki
import lxml
import lxml.html
import urlparse

gid = 0
idletters = "adjmptw"  # and g

def CleanupData(data):
    global gid
    assert data['adr'] == '', data
    del data['adr']
    if "country-name" in data:
        del data["country-name"]
    if not data.get('postal-code'):
        data['postal-code'] = re.search(',([\s\w]*)$', data['extended-address']).group(1).strip()

    postcode = data.get('postal-code')
    latlng = scraperwiki.geo.gb_postcode_to_latlng(postcode)
    data["shortname"] = re.sub("(?:Community|Centre|Sports|Sport|Fitness|Leisure| and| &).*$", "", data.get("name"))
    data["shortname"] = re.sub(" Swimming", "", data["shortname"]).strip()
    data["numid"] = gid
    data["id"] = "g%s%s%s" % (idletters[gid % 7], idletters[(gid/7) % 7], idletters[(gid/49) % 7])
    gid += 1
    scraperwiki.datastore.save(unique_keys=["numid", "id"], data=data, latlng=latlng)
    

def ParseIndexPage(url, root):
    print lxml.etree.tostring(root)
    for tr in root.cssselect("tr.vcard"):
        lk, addr, contact = tr.cssselect("td")
        assert lk[0].tag == "a", lxml.etree.tostring(tr)
        data = { }
        data["url"] = urlparse.urljoin(url, lk[0].attrib.get("href"))
        data["name"] = lk[0].text.strip()
        for span in addr.cssselect("span"):
            data[span.attrib.get("class")] = span.text.strip()
        data["telephone"] = contact[0].text.strip()
        print data
        CleanupData(data)
        

# link sourced from:
# http://www.birmingham.gov.uk/cs/Satellite/leisureinfo?packedargs=website%3D4&rendermode=live
def Main():
    url = "http://www.birmingham.gov.uk/cs/Satellite?pagename=BCC/Common/Wrapper/Wrapper&"+\
      "childpagename=SystemAdmin/Page"+\
      "Layout&c=Page&cid=1186481130144&searchPageId=1223115664505"+\
      "&searchForm=1&pagination=1&entityname=&entitykeywords=&entitytype=Venue&entityarea=Any"+\
      "&entityfacilities=Leisure+Centre&entityservices=Any&search=Search"

    while True:
        root = lxml.html.parse(url).getroot()
        ParseIndexPage(url, root)
        unext = [ a.attrib.get("href")  for a in root.cssselect("a")  if a.text == "Next" ]
        if not unext:
            break
        url = urlparse.urljoin(url, unext[0])

        
Main()import urllib
import re
import scraperwiki
import lxml
import lxml.html
import urlparse

gid = 0
idletters = "adjmptw"  # and g

def CleanupData(data):
    global gid
    assert data['adr'] == '', data
    del data['adr']
    if "country-name" in data:
        del data["country-name"]
    if not data.get('postal-code'):
        data['postal-code'] = re.search(',([\s\w]*)$', data['extended-address']).group(1).strip()

    postcode = data.get('postal-code')
    latlng = scraperwiki.geo.gb_postcode_to_latlng(postcode)
    data["shortname"] = re.sub("(?:Community|Centre|Sports|Sport|Fitness|Leisure| and| &).*$", "", data.get("name"))
    data["shortname"] = re.sub(" Swimming", "", data["shortname"]).strip()
    data["numid"] = gid
    data["id"] = "g%s%s%s" % (idletters[gid % 7], idletters[(gid/7) % 7], idletters[(gid/49) % 7])
    gid += 1
    scraperwiki.datastore.save(unique_keys=["numid", "id"], data=data, latlng=latlng)
    

def ParseIndexPage(url, root):
    print lxml.etree.tostring(root)
    for tr in root.cssselect("tr.vcard"):
        lk, addr, contact = tr.cssselect("td")
        assert lk[0].tag == "a", lxml.etree.tostring(tr)
        data = { }
        data["url"] = urlparse.urljoin(url, lk[0].attrib.get("href"))
        data["name"] = lk[0].text.strip()
        for span in addr.cssselect("span"):
            data[span.attrib.get("class")] = span.text.strip()
        data["telephone"] = contact[0].text.strip()
        print data
        CleanupData(data)
        

# link sourced from:
# http://www.birmingham.gov.uk/cs/Satellite/leisureinfo?packedargs=website%3D4&rendermode=live
def Main():
    url = "http://www.birmingham.gov.uk/cs/Satellite?pagename=BCC/Common/Wrapper/Wrapper&"+\
      "childpagename=SystemAdmin/Page"+\
      "Layout&c=Page&cid=1186481130144&searchPageId=1223115664505"+\
      "&searchForm=1&pagination=1&entityname=&entitykeywords=&entitytype=Venue&entityarea=Any"+\
      "&entityfacilities=Leisure+Centre&entityservices=Any&search=Search"

    while True:
        root = lxml.html.parse(url).getroot()
        ParseIndexPage(url, root)
        unext = [ a.attrib.get("href")  for a in root.cssselect("a")  if a.text == "Next" ]
        if not unext:
            break
        url = urlparse.urljoin(url, unext[0])

        
Main()import urllib
import re
import scraperwiki
import lxml
import lxml.html
import urlparse

gid = 0
idletters = "adjmptw"  # and g

def CleanupData(data):
    global gid
    assert data['adr'] == '', data
    del data['adr']
    if "country-name" in data:
        del data["country-name"]
    if not data.get('postal-code'):
        data['postal-code'] = re.search(',([\s\w]*)$', data['extended-address']).group(1).strip()

    postcode = data.get('postal-code')
    latlng = scraperwiki.geo.gb_postcode_to_latlng(postcode)
    data["shortname"] = re.sub("(?:Community|Centre|Sports|Sport|Fitness|Leisure| and| &).*$", "", data.get("name"))
    data["shortname"] = re.sub(" Swimming", "", data["shortname"]).strip()
    data["numid"] = gid
    data["id"] = "g%s%s%s" % (idletters[gid % 7], idletters[(gid/7) % 7], idletters[(gid/49) % 7])
    gid += 1
    scraperwiki.datastore.save(unique_keys=["numid", "id"], data=data, latlng=latlng)
    

def ParseIndexPage(url, root):
    print lxml.etree.tostring(root)
    for tr in root.cssselect("tr.vcard"):
        lk, addr, contact = tr.cssselect("td")
        assert lk[0].tag == "a", lxml.etree.tostring(tr)
        data = { }
        data["url"] = urlparse.urljoin(url, lk[0].attrib.get("href"))
        data["name"] = lk[0].text.strip()
        for span in addr.cssselect("span"):
            data[span.attrib.get("class")] = span.text.strip()
        data["telephone"] = contact[0].text.strip()
        print data
        CleanupData(data)
        

# link sourced from:
# http://www.birmingham.gov.uk/cs/Satellite/leisureinfo?packedargs=website%3D4&rendermode=live
def Main():
    url = "http://www.birmingham.gov.uk/cs/Satellite?pagename=BCC/Common/Wrapper/Wrapper&"+\
      "childpagename=SystemAdmin/Page"+\
      "Layout&c=Page&cid=1186481130144&searchPageId=1223115664505"+\
      "&searchForm=1&pagination=1&entityname=&entitykeywords=&entitytype=Venue&entityarea=Any"+\
      "&entityfacilities=Leisure+Centre&entityservices=Any&search=Search"

    while True:
        root = lxml.html.parse(url).getroot()
        ParseIndexPage(url, root)
        unext = [ a.attrib.get("href")  for a in root.cssselect("a")  if a.text == "Next" ]
        if not unext:
            break
        url = urlparse.urljoin(url, unext[0])

        
Main()