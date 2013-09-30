#############################################################################
# Comma Separated Value (CSV) files are a common way to back up 
# large amounts of consistent data.  
# Usually there is one record on each line, fields separated by commas.
#############################################################################
import scraperwiki
import csv
from scraperwiki import datastore
import urllib

# Here is an example CSV file
url = "http://www.whatdotheyknow.com/request/49424/response/121792/attach/3/Footbridges%20FOI.csv.txt"
f = urllib.urlopen(url)
lines = f.readlines()

#DEBUG:
#for line in lines:
#   print line

clist = list(csv.reader(lines))

#DEBUG:
#print clist

header = clist.pop(15)   # set 'header' to be the first row of the CSV file

for row in clist[16:-5:1]:  # move to 2nd row after
    data = dict(zip(header, row)) # and use 'dict' to create a dictionary for each row

    #TODO: ignore the last 5 blank lines - seems to be done automatically...

    #TODO: strip whitespace from the strings in the dict 

    #save to datastore
    datastore.save(unique_keys=['Structure Key '], data=data, latlng=(scraperwiki.geo.os_easting_northing_to_latlng(float(data['Eastings ']), float(data['Northings ']))))

#############################################################################
# Comma Separated Value (CSV) files are a common way to back up 
# large amounts of consistent data.  
# Usually there is one record on each line, fields separated by commas.
#############################################################################
import scraperwiki
import csv
from scraperwiki import datastore
import urllib

# Here is an example CSV file
url = "http://www.whatdotheyknow.com/request/49424/response/121792/attach/3/Footbridges%20FOI.csv.txt"
f = urllib.urlopen(url)
lines = f.readlines()

#DEBUG:
#for line in lines:
#   print line

clist = list(csv.reader(lines))

#DEBUG:
#print clist

header = clist.pop(15)   # set 'header' to be the first row of the CSV file

for row in clist[16:-5:1]:  # move to 2nd row after
    data = dict(zip(header, row)) # and use 'dict' to create a dictionary for each row

    #TODO: ignore the last 5 blank lines - seems to be done automatically...

    #TODO: strip whitespace from the strings in the dict 

    #save to datastore
    datastore.save(unique_keys=['Structure Key '], data=data, latlng=(scraperwiki.geo.os_easting_northing_to_latlng(float(data['Eastings ']), float(data['Northings ']))))

