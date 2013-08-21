import scraperwiki
import urllib
url = 'http://www.ncua.gov/DataApps/Documents/CUDirectory2010.txt'

f = urllib.urlopen(url)
lines = f.readlines()
#for line in lines:
#    print line

import csv
clist = list(csv.reader(lines))
#print clist #  gives: [['Name', 'Phone_number'], ['Smith, John', '99999'], etc

header = clist.pop(0)   # set 'header' to be the first row of the CSV file
for row in clist:
    record = dict(zip(header, row)) # and use 'dict' to create a dictionary for each row
    scraperwiki.sqlite.save(["CHART"], record) # save the records one by one
