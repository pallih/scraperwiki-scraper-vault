import urllib
import csv
import datetime
import re
import scraperwiki

chunk = 100
startoffset = 0000
endoffset = 70000

fcols = "%2C".join([ "col%d" % c  for c in range(19) ])
fquery = "select+%s+from+273326" % fcols

numerickeys = ['Coalition forces killed', 'Enemy kia', 'Civilian wia', 'Enemy wia', 'Civilian kia', 'Iraq forces killed', 
               'Coalition forces wounded', 'Total deaths', 'Enemy detained' ]
def cleanup(data):
    for key in numerickeys:
        data[key] = int(data[key])
    data["Longitude"] = float(data["Longitude"])
    data["Latitude"] = float(data["Latitude"])
    mdate = re.match("(\d\d)/(\d\d)/(\d\d\d\d) (\d\d):(\d\d)$", data['Date and time'])

    # should fix the \\n and convert to linefeeds here data["\\n"]

    data['Date and time'] = datetime.datetime(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)), int(mdate.group(4)), int(mdate.group(5)))
    data['Date'] =datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))


    # carriage returns \r are found in the data.
    # prob way of handing it with a dialect but can't see how
def cleanup_r(fin):
    while True:
        line = fin.readline()
        if not line:
            break
        yield re.sub("\r", "NEWLINE", line)


for offset in range(startoffset, endoffset, chunk):  # total is 52071
    url = "http://www.google.com/fusiontables/exporttable?query=%s+offset+%d+limit+%d" % (fquery, offset, chunk)
    print "Fetching %d" % offset
    fin = urllib.urlopen(url, "rU")
    cfin = csv.reader(cleanup_r(fin))

    header = cfin.next()
    for i, row in enumerate(cfin):
        data = dict(zip(header, row))
        data["rownumber"] = i+offset
        cleanup(data)
        scraperwiki.sqlite.save(unique_keys=["Report key"], data=data, verbose=0)
    scraperwiki.sqlite.commit()
    print "got", i+1
    if i+1 < chunk:
        break

import urllib
import csv
import datetime
import re
import scraperwiki

chunk = 100
startoffset = 0000
endoffset = 70000

fcols = "%2C".join([ "col%d" % c  for c in range(19) ])
fquery = "select+%s+from+273326" % fcols

numerickeys = ['Coalition forces killed', 'Enemy kia', 'Civilian wia', 'Enemy wia', 'Civilian kia', 'Iraq forces killed', 
               'Coalition forces wounded', 'Total deaths', 'Enemy detained' ]
def cleanup(data):
    for key in numerickeys:
        data[key] = int(data[key])
    data["Longitude"] = float(data["Longitude"])
    data["Latitude"] = float(data["Latitude"])
    mdate = re.match("(\d\d)/(\d\d)/(\d\d\d\d) (\d\d):(\d\d)$", data['Date and time'])

    # should fix the \\n and convert to linefeeds here data["\\n"]

    data['Date and time'] = datetime.datetime(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)), int(mdate.group(4)), int(mdate.group(5)))
    data['Date'] =datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))


    # carriage returns \r are found in the data.
    # prob way of handing it with a dialect but can't see how
def cleanup_r(fin):
    while True:
        line = fin.readline()
        if not line:
            break
        yield re.sub("\r", "NEWLINE", line)


for offset in range(startoffset, endoffset, chunk):  # total is 52071
    url = "http://www.google.com/fusiontables/exporttable?query=%s+offset+%d+limit+%d" % (fquery, offset, chunk)
    print "Fetching %d" % offset
    fin = urllib.urlopen(url, "rU")
    cfin = csv.reader(cleanup_r(fin))

    header = cfin.next()
    for i, row in enumerate(cfin):
        data = dict(zip(header, row))
        data["rownumber"] = i+offset
        cleanup(data)
        scraperwiki.sqlite.save(unique_keys=["Report key"], data=data, verbose=0)
    scraperwiki.sqlite.commit()
    print "got", i+1
    if i+1 < chunk:
        break

