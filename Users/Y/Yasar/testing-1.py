#############################################################################
# Comma Separated Value (CSV) files are a common way to back up 
# large amounts of consistent data.  
# Usually there is one record on each line, fields separated by commas.
#############################################################################
import urllib

# Here is an example CSV file
url = "http://scraperwiki.com/scrapers/export/tutorial-csv/"
f = urllib.urlopen(url)
lines = f.readlines()
for line in lines:
    print line

#----------------------------------------------------------------------
# Reading the data is more complicated than just splitting it up by commas 
# [e.g. line.split(",") in Python, because the fields themselves can
# contain commas, e.g. "Smith, John"
# Fortunately the csv.reader() function solves this problem.
# UNCOMMENT THE NEXT THREE LINES.
#----------------------------------------------------------------------

import csv
clist = list(csv.reader(lines))
print clist #  gives: [['Name', 'Phone_number'], ['Smith, John', '99999'], etc

#----------------------------------------------------------------------
# A useful trick....
# In many CSV files the first line is the names of the columns.  
# Often you will want to use this to make a dictionary object, like:
#  { "Name" : "Smith, John", "Phone number" : 99999 }
# You can make dictionaries easily, using the dict and zip functions.
# UNCOMMENT THE NEXT THREE LINES.
#----------------------------------------------------------------------
header = clist.pop(0)   # set 'header' to be the first row of the CSV file
for row in clist:
    print dict(zip(header, row)) # and use 'dict' to create a dictionary for each row









# ignore this bit, which generates the data
#
#def AddSomeData():
#    import scraperwiki
#    scraperwiki.datastore.save(unique_keys=["Name"], data={"Name":"Smith, John", "Phone number":99999}) 
#    for n in range(4, 15):
#        scraperwiki.datastore.save(unique_keys=["Name"], data={"Name":"Suzie %d" % n, "Phone number":10000+n})
#AddSomeData()
