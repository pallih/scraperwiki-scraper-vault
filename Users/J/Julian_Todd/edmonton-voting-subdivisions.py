import lxml.etree
import urllib
import re
import json
import scraperwiki


def GetData():
    url = "http://datafeed.edmonton.ca/v1/coe/VotingSubdivisions?$filter=&format=xml"
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data
    
for data in GetData():
    addr = "%s, Edmonton, Canada" % data["address"]
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(addr)).read()
    v = json.loads(a)
    coords = v['Placemark'][0]["Point"]["coordinates"]
    latlng = [coords[1], coords[0]]
    print latlng, v
    scraperwiki.datastore.save(unique_keys=["descname"], data=data, latlng=latlng)
    
import lxml.etree
import urllib
import re
import json
import scraperwiki


def GetData():
    url = "http://datafeed.edmonton.ca/v1/coe/VotingSubdivisions?$filter=&format=xml"
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data
    
for data in GetData():
    addr = "%s, Edmonton, Canada" % data["address"]
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(addr)).read()
    v = json.loads(a)
    coords = v['Placemark'][0]["Point"]["coordinates"]
    latlng = [coords[1], coords[0]]
    print latlng, v
    scraperwiki.datastore.save(unique_keys=["descname"], data=data, latlng=latlng)
    
import lxml.etree
import urllib
import re
import json
import scraperwiki


def GetData():
    url = "http://datafeed.edmonton.ca/v1/coe/VotingSubdivisions?$filter=&format=xml"
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data
    
for data in GetData():
    addr = "%s, Edmonton, Canada" % data["address"]
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(addr)).read()
    v = json.loads(a)
    coords = v['Placemark'][0]["Point"]["coordinates"]
    latlng = [coords[1], coords[0]]
    print latlng, v
    scraperwiki.datastore.save(unique_keys=["descname"], data=data, latlng=latlng)
    
import lxml.etree
import urllib
import re
import json
import scraperwiki


def GetData():
    url = "http://datafeed.edmonton.ca/v1/coe/VotingSubdivisions?$filter=&format=xml"
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data
    
for data in GetData():
    addr = "%s, Edmonton, Canada" % data["address"]
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(addr)).read()
    v = json.loads(a)
    coords = v['Placemark'][0]["Point"]["coordinates"]
    latlng = [coords[1], coords[0]]
    print latlng, v
    scraperwiki.datastore.save(unique_keys=["descname"], data=data, latlng=latlng)
    
import lxml.etree
import urllib
import re
import json
import scraperwiki


def GetData():
    url = "http://datafeed.edmonton.ca/v1/coe/VotingSubdivisions?$filter=&format=xml"
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data
    
for data in GetData():
    addr = "%s, Edmonton, Canada" % data["address"]
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(addr)).read()
    v = json.loads(a)
    coords = v['Placemark'][0]["Point"]["coordinates"]
    latlng = [coords[1], coords[0]]
    print latlng, v
    scraperwiki.datastore.save(unique_keys=["descname"], data=data, latlng=latlng)
    
import lxml.etree
import urllib
import re
import json
import scraperwiki


def GetData():
    url = "http://datafeed.edmonton.ca/v1/coe/VotingSubdivisions?$filter=&format=xml"
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data
    
for data in GetData():
    addr = "%s, Edmonton, Canada" % data["address"]
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(addr)).read()
    v = json.loads(a)
    coords = v['Placemark'][0]["Point"]["coordinates"]
    latlng = [coords[1], coords[0]]
    print latlng, v
    scraperwiki.datastore.save(unique_keys=["descname"], data=data, latlng=latlng)
    
import lxml.etree
import urllib
import re
import json
import scraperwiki


def GetData():
    url = "http://datafeed.edmonton.ca/v1/coe/VotingSubdivisions?$filter=&format=xml"
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data
    
for data in GetData():
    addr = "%s, Edmonton, Canada" % data["address"]
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(addr)).read()
    v = json.loads(a)
    coords = v['Placemark'][0]["Point"]["coordinates"]
    latlng = [coords[1], coords[0]]
    print latlng, v
    scraperwiki.datastore.save(unique_keys=["descname"], data=data, latlng=latlng)
    
import lxml.etree
import urllib
import re
import json
import scraperwiki


def GetData():
    url = "http://datafeed.edmonton.ca/v1/coe/VotingSubdivisions?$filter=&format=xml"
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data
    
for data in GetData():
    addr = "%s, Edmonton, Canada" % data["address"]
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(addr)).read()
    v = json.loads(a)
    coords = v['Placemark'][0]["Point"]["coordinates"]
    latlng = [coords[1], coords[0]]
    print latlng, v
    scraperwiki.datastore.save(unique_keys=["descname"], data=data, latlng=latlng)
    
import lxml.etree
import urllib
import re
import json
import scraperwiki


def GetData():
    url = "http://datafeed.edmonton.ca/v1/coe/VotingSubdivisions?$filter=&format=xml"
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data
    
for data in GetData():
    addr = "%s, Edmonton, Canada" % data["address"]
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(addr)).read()
    v = json.loads(a)
    coords = v['Placemark'][0]["Point"]["coordinates"]
    latlng = [coords[1], coords[0]]
    print latlng, v
    scraperwiki.datastore.save(unique_keys=["descname"], data=data, latlng=latlng)
    
import lxml.etree
import urllib
import re
import json
import scraperwiki


def GetData():
    url = "http://datafeed.edmonton.ca/v1/coe/VotingSubdivisions?$filter=&format=xml"
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data
    
for data in GetData():
    addr = "%s, Edmonton, Canada" % data["address"]
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(addr)).read()
    v = json.loads(a)
    coords = v['Placemark'][0]["Point"]["coordinates"]
    latlng = [coords[1], coords[0]]
    print latlng, v
    scraperwiki.datastore.save(unique_keys=["descname"], data=data, latlng=latlng)
    
import lxml.etree
import urllib
import re
import json
import scraperwiki


def GetData():
    url = "http://datafeed.edmonton.ca/v1/coe/VotingSubdivisions?$filter=&format=xml"
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data
    
for data in GetData():
    addr = "%s, Edmonton, Canada" % data["address"]
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(addr)).read()
    v = json.loads(a)
    coords = v['Placemark'][0]["Point"]["coordinates"]
    latlng = [coords[1], coords[0]]
    print latlng, v
    scraperwiki.datastore.save(unique_keys=["descname"], data=data, latlng=latlng)
    
import lxml.etree
import urllib
import re
import json
import scraperwiki


def GetData():
    url = "http://datafeed.edmonton.ca/v1/coe/VotingSubdivisions?$filter=&format=xml"
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data
    
for data in GetData():
    addr = "%s, Edmonton, Canada" % data["address"]
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(addr)).read()
    v = json.loads(a)
    coords = v['Placemark'][0]["Point"]["coordinates"]
    latlng = [coords[1], coords[0]]
    print latlng, v
    scraperwiki.datastore.save(unique_keys=["descname"], data=data, latlng=latlng)
    
import lxml.etree
import urllib
import re
import json
import scraperwiki


def GetData():
    url = "http://datafeed.edmonton.ca/v1/coe/VotingSubdivisions?$filter=&format=xml"
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data
    
for data in GetData():
    addr = "%s, Edmonton, Canada" % data["address"]
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(addr)).read()
    v = json.loads(a)
    coords = v['Placemark'][0]["Point"]["coordinates"]
    latlng = [coords[1], coords[0]]
    print latlng, v
    scraperwiki.datastore.save(unique_keys=["descname"], data=data, latlng=latlng)
    
