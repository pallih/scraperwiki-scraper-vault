import urllib
import csv
import scraperwiki
import datetime
import re

url = "http://www.iraqbodycount.org/database/download/ibc-individuals"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
def convertdate(d):
    md = re.match("(\d+) (\w+) (\d+)$", d)
    imonth = months.index(md.group(2)) + 1
    return datetime.date(int(md.group(3)), imonth, int(md.group(1))) 

def cleanup(data):
    data["IBC code part1"], data["IBC code part2"] = data["IBC code"].split("-", 1)
    data["Latest Date"] = convertdate(data["Latest Date"])
    data["Earliest Date"] = convertdate(data["Earliest Date"])

fin = urllib.urlopen(url)
for i in range(26):
    fin.readline()

cfin = csv.reader(fin)
header = cfin.next()
assert header == ['IBC code', 'Name or Identifying Details', 'Age', 'Sex', 'Marital Status', 'Parental Status', 
                  'Earliest Date', 'Latest Date', 'Location'], header

for i, row in enumerate(cfin):
    if i <= 0:
        continue
    if (i % 100) == 99:
        scraperwiki.sqlite.commit()
        print "Fetched to", i
    data = dict(zip(header, row))
    data["rownumber"] = i
    cleanup(data)
    scraperwiki.sqlite.save(unique_keys=["IBC code"], data=data, verbose=0)
scraperwiki.sqlite.commit()



import urllib
import csv
import scraperwiki
import datetime
import re

url = "http://www.iraqbodycount.org/database/download/ibc-individuals"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
def convertdate(d):
    md = re.match("(\d+) (\w+) (\d+)$", d)
    imonth = months.index(md.group(2)) + 1
    return datetime.date(int(md.group(3)), imonth, int(md.group(1))) 

def cleanup(data):
    data["IBC code part1"], data["IBC code part2"] = data["IBC code"].split("-", 1)
    data["Latest Date"] = convertdate(data["Latest Date"])
    data["Earliest Date"] = convertdate(data["Earliest Date"])

fin = urllib.urlopen(url)
for i in range(26):
    fin.readline()

cfin = csv.reader(fin)
header = cfin.next()
assert header == ['IBC code', 'Name or Identifying Details', 'Age', 'Sex', 'Marital Status', 'Parental Status', 
                  'Earliest Date', 'Latest Date', 'Location'], header

for i, row in enumerate(cfin):
    if i <= 0:
        continue
    if (i % 100) == 99:
        scraperwiki.sqlite.commit()
        print "Fetched to", i
    data = dict(zip(header, row))
    data["rownumber"] = i
    cleanup(data)
    scraperwiki.sqlite.save(unique_keys=["IBC code"], data=data, verbose=0)
scraperwiki.sqlite.commit()



