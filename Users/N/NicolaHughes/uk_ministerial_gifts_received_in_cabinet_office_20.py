import scraperwiki
import urllib
import csv
import re

url = "http://download.cabinetoffice.gov.uk/transparency/gifts-received-2009-10.csv"
f = urllib.urlopen(url)
lines = f.readlines()
clist = list(csv.reader(lines))
header = clist.pop(0)   # set 'header' to be the first row of the CSV file
dept = ''
rownumber = 1
cheader = []

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
longmonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def convertdate(d):
    md = re.match("(\w+) (\d+)$", d)
    if md == None:
        return d
    if md.group(1) in months:
        imonth = months.index(md.group(1)) + 1
    else:
        imonth = longmonths.index(md.group(1)) + 1
    return '%s-%02d'%(md.group(2), imonth) 

for x in header:
    cheader.append(x.strip())

for row in clist:
    rownumber += 1
    if row[0] != '':
        dept = row[0]
    else:
        row[0] = dept
    if row[1].strip() != 'NIL RETURN':
            data = dict(zip(cheader, row)) # and use 'dict' to create a dictionary for each row
            data['Row Number'] = rownumber
            data['URL'] = url
            data['Date'] = convertdate(data['Date']) 
            if data['Value'] != 'Over Limit':
                data['Value'] = int(data['Value'][1:])
            print data
            scraperwiki.datastore.save(unique_keys=["Row Number", "URL"], data=data)




