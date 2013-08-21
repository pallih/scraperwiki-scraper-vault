import urllib
import csv
import scraperwiki

description = "London cycle hire locations coloured according to their capacity"
# as seen in http://www.guardian.co.uk/technology/blog/2010/jun/15/london-datastore-tfl-data-free

def Main():
    url = "http://data.london.gov.uk/datafiles/transport/tfl-cycle-hire-locations.csv"
    f = urllib.urlopen(url)
    lines = f.readlines()
    
    clist = list(csv.reader(lines))
    header = clist.pop(0)   # take off the first row
    assert header == ['Name', 'Postcode_District', 'TfL_Ref', 'Capacity', 'Lat', 'Long', 'Easting', 'Northing'], header
    capacities = [ ]
    for row in clist:
        data = dict(zip(header, row))

        latlng = [float(data.pop("Lat")), float(data.pop("Long"))]
        easting, northing = float(data.pop("Easting")), float(data.pop("Northing"))
        enlatlng = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
    
        data["Name"] = data["Name"].replace("\xa0", " ").strip()  # problematic \xa0
        data["Postcode_District"] = data["Postcode_District"].replace("\xa0", " ").strip()  # problematic \xa0
        data["TfL_Ref"] = data["TfL_Ref"].replace("\xa0", " ").strip()  # problematic \xa0
        data["Capacity"] = int(data["Capacity"])
        
        capacities.append(data["Capacity"])

        # build the bicycle chart icon, coloured according to capacity
        colour = "4fd"
        if data["Capacity"] > 20:
            colour = "0e0"
        if data["Capacity"] > 30:
            colour = "ee0"
        chartimg = "http://chart.apis.google.com/chart?chst=d_map_pin_icon&chld=bicycle|%s" % colour
        data["chart"] = { "chartimg":chartimg, 'Size': [21,34], 'Pixel': [-10,-34] }

        scraperwiki.datastore.save(unique_keys=["TfL_Ref"], data=data, latlng=latlng)  # enlatlng is a few metres out


Main()

import urllib
import csv
import scraperwiki

description = "London cycle hire locations coloured according to their capacity"
# as seen in http://www.guardian.co.uk/technology/blog/2010/jun/15/london-datastore-tfl-data-free

def Main():
    url = "http://data.london.gov.uk/datafiles/transport/tfl-cycle-hire-locations.csv"
    f = urllib.urlopen(url)
    lines = f.readlines()
    
    clist = list(csv.reader(lines))
    header = clist.pop(0)   # take off the first row
    assert header == ['Name', 'Postcode_District', 'TfL_Ref', 'Capacity', 'Lat', 'Long', 'Easting', 'Northing'], header
    capacities = [ ]
    for row in clist:
        data = dict(zip(header, row))

        latlng = [float(data.pop("Lat")), float(data.pop("Long"))]
        easting, northing = float(data.pop("Easting")), float(data.pop("Northing"))
        enlatlng = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
    
        data["Name"] = data["Name"].replace("\xa0", " ").strip()  # problematic \xa0
        data["Postcode_District"] = data["Postcode_District"].replace("\xa0", " ").strip()  # problematic \xa0
        data["TfL_Ref"] = data["TfL_Ref"].replace("\xa0", " ").strip()  # problematic \xa0
        data["Capacity"] = int(data["Capacity"])
        
        capacities.append(data["Capacity"])

        # build the bicycle chart icon, coloured according to capacity
        colour = "4fd"
        if data["Capacity"] > 20:
            colour = "0e0"
        if data["Capacity"] > 30:
            colour = "ee0"
        chartimg = "http://chart.apis.google.com/chart?chst=d_map_pin_icon&chld=bicycle|%s" % colour
        data["chart"] = { "chartimg":chartimg, 'Size': [21,34], 'Pixel': [-10,-34] }

        scraperwiki.datastore.save(unique_keys=["TfL_Ref"], data=data, latlng=latlng)  # enlatlng is a few metres out


Main()

import urllib
import csv
import scraperwiki

description = "London cycle hire locations coloured according to their capacity"
# as seen in http://www.guardian.co.uk/technology/blog/2010/jun/15/london-datastore-tfl-data-free

def Main():
    url = "http://data.london.gov.uk/datafiles/transport/tfl-cycle-hire-locations.csv"
    f = urllib.urlopen(url)
    lines = f.readlines()
    
    clist = list(csv.reader(lines))
    header = clist.pop(0)   # take off the first row
    assert header == ['Name', 'Postcode_District', 'TfL_Ref', 'Capacity', 'Lat', 'Long', 'Easting', 'Northing'], header
    capacities = [ ]
    for row in clist:
        data = dict(zip(header, row))

        latlng = [float(data.pop("Lat")), float(data.pop("Long"))]
        easting, northing = float(data.pop("Easting")), float(data.pop("Northing"))
        enlatlng = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
    
        data["Name"] = data["Name"].replace("\xa0", " ").strip()  # problematic \xa0
        data["Postcode_District"] = data["Postcode_District"].replace("\xa0", " ").strip()  # problematic \xa0
        data["TfL_Ref"] = data["TfL_Ref"].replace("\xa0", " ").strip()  # problematic \xa0
        data["Capacity"] = int(data["Capacity"])
        
        capacities.append(data["Capacity"])

        # build the bicycle chart icon, coloured according to capacity
        colour = "4fd"
        if data["Capacity"] > 20:
            colour = "0e0"
        if data["Capacity"] > 30:
            colour = "ee0"
        chartimg = "http://chart.apis.google.com/chart?chst=d_map_pin_icon&chld=bicycle|%s" % colour
        data["chart"] = { "chartimg":chartimg, 'Size': [21,34], 'Pixel': [-10,-34] }

        scraperwiki.datastore.save(unique_keys=["TfL_Ref"], data=data, latlng=latlng)  # enlatlng is a few metres out


Main()

import urllib
import csv
import scraperwiki

description = "London cycle hire locations coloured according to their capacity"
# as seen in http://www.guardian.co.uk/technology/blog/2010/jun/15/london-datastore-tfl-data-free

def Main():
    url = "http://data.london.gov.uk/datafiles/transport/tfl-cycle-hire-locations.csv"
    f = urllib.urlopen(url)
    lines = f.readlines()
    
    clist = list(csv.reader(lines))
    header = clist.pop(0)   # take off the first row
    assert header == ['Name', 'Postcode_District', 'TfL_Ref', 'Capacity', 'Lat', 'Long', 'Easting', 'Northing'], header
    capacities = [ ]
    for row in clist:
        data = dict(zip(header, row))

        latlng = [float(data.pop("Lat")), float(data.pop("Long"))]
        easting, northing = float(data.pop("Easting")), float(data.pop("Northing"))
        enlatlng = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
    
        data["Name"] = data["Name"].replace("\xa0", " ").strip()  # problematic \xa0
        data["Postcode_District"] = data["Postcode_District"].replace("\xa0", " ").strip()  # problematic \xa0
        data["TfL_Ref"] = data["TfL_Ref"].replace("\xa0", " ").strip()  # problematic \xa0
        data["Capacity"] = int(data["Capacity"])
        
        capacities.append(data["Capacity"])

        # build the bicycle chart icon, coloured according to capacity
        colour = "4fd"
        if data["Capacity"] > 20:
            colour = "0e0"
        if data["Capacity"] > 30:
            colour = "ee0"
        chartimg = "http://chart.apis.google.com/chart?chst=d_map_pin_icon&chld=bicycle|%s" % colour
        data["chart"] = { "chartimg":chartimg, 'Size': [21,34], 'Pixel': [-10,-34] }

        scraperwiki.datastore.save(unique_keys=["TfL_Ref"], data=data, latlng=latlng)  # enlatlng is a few metres out


Main()

import urllib
import csv
import scraperwiki

description = "London cycle hire locations coloured according to their capacity"
# as seen in http://www.guardian.co.uk/technology/blog/2010/jun/15/london-datastore-tfl-data-free

def Main():
    url = "http://data.london.gov.uk/datafiles/transport/tfl-cycle-hire-locations.csv"
    f = urllib.urlopen(url)
    lines = f.readlines()
    
    clist = list(csv.reader(lines))
    header = clist.pop(0)   # take off the first row
    assert header == ['Name', 'Postcode_District', 'TfL_Ref', 'Capacity', 'Lat', 'Long', 'Easting', 'Northing'], header
    capacities = [ ]
    for row in clist:
        data = dict(zip(header, row))

        latlng = [float(data.pop("Lat")), float(data.pop("Long"))]
        easting, northing = float(data.pop("Easting")), float(data.pop("Northing"))
        enlatlng = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
    
        data["Name"] = data["Name"].replace("\xa0", " ").strip()  # problematic \xa0
        data["Postcode_District"] = data["Postcode_District"].replace("\xa0", " ").strip()  # problematic \xa0
        data["TfL_Ref"] = data["TfL_Ref"].replace("\xa0", " ").strip()  # problematic \xa0
        data["Capacity"] = int(data["Capacity"])
        
        capacities.append(data["Capacity"])

        # build the bicycle chart icon, coloured according to capacity
        colour = "4fd"
        if data["Capacity"] > 20:
            colour = "0e0"
        if data["Capacity"] > 30:
            colour = "ee0"
        chartimg = "http://chart.apis.google.com/chart?chst=d_map_pin_icon&chld=bicycle|%s" % colour
        data["chart"] = { "chartimg":chartimg, 'Size': [21,34], 'Pixel': [-10,-34] }

        scraperwiki.datastore.save(unique_keys=["TfL_Ref"], data=data, latlng=latlng)  # enlatlng is a few metres out


Main()

