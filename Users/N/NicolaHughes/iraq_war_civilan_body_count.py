import urllib
import csv
import scraperwiki
import datetime
import re

url = "http://www.iraqbodycount.org/database/download/ibc-incidents"


months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def convertdate(d):
    md = re.match("(\d+) (\w+) (\d+)$", d)
    if not md:
        print 'Failed to convert d'
        raise AttributeError(d + ' is not a valid date')
    imonth = months.index(md.group(2)) + 1
    return datetime.date(int(md.group(3)), imonth, int(md.group(1))) 
    
def cleanup(data):
    data["End Date"] = convertdate(data["End Date"])
    data["Start Date"] = convertdate(data["Start Date"])
    data['Reported Maximum'] = int(data['Reported Maximum'])
    data['Reported Minimum'] = int(data['Reported Minimum'])
    mtime = re.match("(?:(\d+):(\d+)\s*)?(AM|PM)?(?: onwards)?$", data['Time'].strip("-"))
    if mtime:  # sometimes you get ranges
        assert mtime, data
        if mtime.group(3):
            data["AMPM"] = mtime.group(2)
    # put 24 hour clock
    # data["Time"] to deal with, but often empty



fin = urllib.urlopen(url)
for i in range(11):
    fin.readline()

cfin = csv.reader(fin)
header = cfin.next()
print header
assert header == ['IBC code', 'Start Date', 'End Date', 'Time', 'Location', 'Target', 'Weapons', 
                  'Reported Minimum', 'Reported Maximum', 'Sources'], header

for i, row in enumerate(cfin):
    data = dict(zip(header, row))
    cleanup(data)
    scraperwiki.sqlite.save(unique_keys=["IBC code"], data=data, verbose=0)
scraperwiki.sqlite.commit()


import urllib
import csv
import scraperwiki
import datetime
import re

url = "http://www.iraqbodycount.org/database/download/ibc-incidents"


months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def convertdate(d):
    md = re.match("(\d+) (\w+) (\d+)$", d)
    if not md:
        print 'Failed to convert d'
        raise AttributeError(d + ' is not a valid date')
    imonth = months.index(md.group(2)) + 1
    return datetime.date(int(md.group(3)), imonth, int(md.group(1))) 
    
def cleanup(data):
    data["End Date"] = convertdate(data["End Date"])
    data["Start Date"] = convertdate(data["Start Date"])
    data['Reported Maximum'] = int(data['Reported Maximum'])
    data['Reported Minimum'] = int(data['Reported Minimum'])
    mtime = re.match("(?:(\d+):(\d+)\s*)?(AM|PM)?(?: onwards)?$", data['Time'].strip("-"))
    if mtime:  # sometimes you get ranges
        assert mtime, data
        if mtime.group(3):
            data["AMPM"] = mtime.group(2)
    # put 24 hour clock
    # data["Time"] to deal with, but often empty



fin = urllib.urlopen(url)
for i in range(11):
    fin.readline()

cfin = csv.reader(fin)
header = cfin.next()
print header
assert header == ['IBC code', 'Start Date', 'End Date', 'Time', 'Location', 'Target', 'Weapons', 
                  'Reported Minimum', 'Reported Maximum', 'Sources'], header

for i, row in enumerate(cfin):
    data = dict(zip(header, row))
    cleanup(data)
    scraperwiki.sqlite.save(unique_keys=["IBC code"], data=data, verbose=0)
scraperwiki.sqlite.commit()


