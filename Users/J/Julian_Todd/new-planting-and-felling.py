import lxml.html
import scraperwiki
import urllib

# more to do:
#  find out how to iterate back through the database
print dir(scraperwiki.geo)



url = "https://www.eforestry.gov.uk/glade/public_register_prePublicRegisterCases.do?d-448625-p=2&consId=10"
html = urllib.urlopen(url).read()
print html
root = lxml.html.fromstring(html)
print lxml.html.tostring(root)

headers = [ a.text  for a in root.cssselect("table#wgsrow thead a") ]

for row in root.cssselect("table#wgsrow tbody tr"):
    values = [ td.text.strip()  for td in row.cssselect("td") ]
    values[0] = row.cssselect("td a")[0].text.strip()
    print values
    data = dict(zip(headers, values))

    
    lonlat = scraperwiki.geo.osgb_to_lonlat(data["Grid Ref"])
    wlonlat = scraperwiki.geo.turn_osgb36_into_wgs84(lonlat[0], lonlat[1], 200)

    scraperwiki.datastore.save(unique_keys=["Ref"], data=data, latlng=[wlonlat[1], wlonlat[0]])



import lxml.html
import scraperwiki
import urllib

# more to do:
#  find out how to iterate back through the database
print dir(scraperwiki.geo)



url = "https://www.eforestry.gov.uk/glade/public_register_prePublicRegisterCases.do?d-448625-p=2&consId=10"
html = urllib.urlopen(url).read()
print html
root = lxml.html.fromstring(html)
print lxml.html.tostring(root)

headers = [ a.text  for a in root.cssselect("table#wgsrow thead a") ]

for row in root.cssselect("table#wgsrow tbody tr"):
    values = [ td.text.strip()  for td in row.cssselect("td") ]
    values[0] = row.cssselect("td a")[0].text.strip()
    print values
    data = dict(zip(headers, values))

    
    lonlat = scraperwiki.geo.osgb_to_lonlat(data["Grid Ref"])
    wlonlat = scraperwiki.geo.turn_osgb36_into_wgs84(lonlat[0], lonlat[1], 200)

    scraperwiki.datastore.save(unique_keys=["Ref"], data=data, latlng=[wlonlat[1], wlonlat[0]])



import lxml.html
import scraperwiki
import urllib

# more to do:
#  find out how to iterate back through the database
print dir(scraperwiki.geo)



url = "https://www.eforestry.gov.uk/glade/public_register_prePublicRegisterCases.do?d-448625-p=2&consId=10"
html = urllib.urlopen(url).read()
print html
root = lxml.html.fromstring(html)
print lxml.html.tostring(root)

headers = [ a.text  for a in root.cssselect("table#wgsrow thead a") ]

for row in root.cssselect("table#wgsrow tbody tr"):
    values = [ td.text.strip()  for td in row.cssselect("td") ]
    values[0] = row.cssselect("td a")[0].text.strip()
    print values
    data = dict(zip(headers, values))

    
    lonlat = scraperwiki.geo.osgb_to_lonlat(data["Grid Ref"])
    wlonlat = scraperwiki.geo.turn_osgb36_into_wgs84(lonlat[0], lonlat[1], 200)

    scraperwiki.datastore.save(unique_keys=["Ref"], data=data, latlng=[wlonlat[1], wlonlat[0]])



import lxml.html
import scraperwiki
import urllib

# more to do:
#  find out how to iterate back through the database
print dir(scraperwiki.geo)



url = "https://www.eforestry.gov.uk/glade/public_register_prePublicRegisterCases.do?d-448625-p=2&consId=10"
html = urllib.urlopen(url).read()
print html
root = lxml.html.fromstring(html)
print lxml.html.tostring(root)

headers = [ a.text  for a in root.cssselect("table#wgsrow thead a") ]

for row in root.cssselect("table#wgsrow tbody tr"):
    values = [ td.text.strip()  for td in row.cssselect("td") ]
    values[0] = row.cssselect("td a")[0].text.strip()
    print values
    data = dict(zip(headers, values))

    
    lonlat = scraperwiki.geo.osgb_to_lonlat(data["Grid Ref"])
    wlonlat = scraperwiki.geo.turn_osgb36_into_wgs84(lonlat[0], lonlat[1], 200)

    scraperwiki.datastore.save(unique_keys=["Ref"], data=data, latlng=[wlonlat[1], wlonlat[0]])



import lxml.html
import scraperwiki
import urllib

# more to do:
#  find out how to iterate back through the database
print dir(scraperwiki.geo)



url = "https://www.eforestry.gov.uk/glade/public_register_prePublicRegisterCases.do?d-448625-p=2&consId=10"
html = urllib.urlopen(url).read()
print html
root = lxml.html.fromstring(html)
print lxml.html.tostring(root)

headers = [ a.text  for a in root.cssselect("table#wgsrow thead a") ]

for row in root.cssselect("table#wgsrow tbody tr"):
    values = [ td.text.strip()  for td in row.cssselect("td") ]
    values[0] = row.cssselect("td a")[0].text.strip()
    print values
    data = dict(zip(headers, values))

    
    lonlat = scraperwiki.geo.osgb_to_lonlat(data["Grid Ref"])
    wlonlat = scraperwiki.geo.turn_osgb36_into_wgs84(lonlat[0], lonlat[1], 200)

    scraperwiki.datastore.save(unique_keys=["Ref"], data=data, latlng=[wlonlat[1], wlonlat[0]])



import lxml.html
import scraperwiki
import urllib

# more to do:
#  find out how to iterate back through the database
print dir(scraperwiki.geo)



url = "https://www.eforestry.gov.uk/glade/public_register_prePublicRegisterCases.do?d-448625-p=2&consId=10"
html = urllib.urlopen(url).read()
print html
root = lxml.html.fromstring(html)
print lxml.html.tostring(root)

headers = [ a.text  for a in root.cssselect("table#wgsrow thead a") ]

for row in root.cssselect("table#wgsrow tbody tr"):
    values = [ td.text.strip()  for td in row.cssselect("td") ]
    values[0] = row.cssselect("td a")[0].text.strip()
    print values
    data = dict(zip(headers, values))

    
    lonlat = scraperwiki.geo.osgb_to_lonlat(data["Grid Ref"])
    wlonlat = scraperwiki.geo.turn_osgb36_into_wgs84(lonlat[0], lonlat[1], 200)

    scraperwiki.datastore.save(unique_keys=["Ref"], data=data, latlng=[wlonlat[1], wlonlat[0]])



import lxml.html
import scraperwiki
import urllib

# more to do:
#  find out how to iterate back through the database
print dir(scraperwiki.geo)



url = "https://www.eforestry.gov.uk/glade/public_register_prePublicRegisterCases.do?d-448625-p=2&consId=10"
html = urllib.urlopen(url).read()
print html
root = lxml.html.fromstring(html)
print lxml.html.tostring(root)

headers = [ a.text  for a in root.cssselect("table#wgsrow thead a") ]

for row in root.cssselect("table#wgsrow tbody tr"):
    values = [ td.text.strip()  for td in row.cssselect("td") ]
    values[0] = row.cssselect("td a")[0].text.strip()
    print values
    data = dict(zip(headers, values))

    
    lonlat = scraperwiki.geo.osgb_to_lonlat(data["Grid Ref"])
    wlonlat = scraperwiki.geo.turn_osgb36_into_wgs84(lonlat[0], lonlat[1], 200)

    scraperwiki.datastore.save(unique_keys=["Ref"], data=data, latlng=[wlonlat[1], wlonlat[0]])



