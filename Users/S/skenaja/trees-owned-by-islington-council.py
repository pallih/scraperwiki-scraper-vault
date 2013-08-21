#############################################################################
# Comma Separated Value (CSV) files are a common way to back up
# large amounts of consistent data.  
# Usually there is one record on each line, fields separated by commas.
#############################################################################
import scraperwiki
import csv
from scraperwiki import datastore
import urllib

# CSV file sent to WDTK - list of Islington Council owned trees
url = "http://www.whatdotheyknow.com/request/48611/response/125279/attach/3/Trees%20LBI%20Owned.csv.txt"
f = urllib.urlopen(url)
lines = f.readlines()

#DEBUG:
#for line in lines:
#   print line

clist = list(csv.reader(lines))

#DEBUG:
#print clist

header = clist.pop(0)   # set 'header' to be the first row of the CSV file

for row in clist[1::1]:  # move to 2nd row after
    data = dict(zip(header, row)) # and use 'dict' to create a dictionary for each row

    #save to datastore
    datastore.save(unique_keys=['OBJECTID'], data=data, latlng=(scraperwiki.geo.os_easting_northing_to_latlng(float(data['X']), float(data['Y']))))


