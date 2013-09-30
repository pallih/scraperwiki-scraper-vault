import datetime
import time
import scraperwiki
import re

stime = int(time.time() * 1000)
stzone = time.timezone
sdate = datetime.datetime.now()
sdate_split = str(sdate.year) + str(sdate.month) + str(sdate.day)

record = {}
record['stime'] = stime
record['sdate'] = sdate
record['sdate_split'] = sdate_split
record['stzone'] = stzone

    
#print record
if record.has_key('sdate'):
        # save records to the datastore
        scraperwiki.sqlite.save(['sdate'],record)



import datetime
import time
import scraperwiki
import re

stime = int(time.time() * 1000)
stzone = time.timezone
sdate = datetime.datetime.now()
sdate_split = str(sdate.year) + str(sdate.month) + str(sdate.day)

record = {}
record['stime'] = stime
record['sdate'] = sdate
record['sdate_split'] = sdate_split
record['stzone'] = stzone

    
#print record
if record.has_key('sdate'):
        # save records to the datastore
        scraperwiki.sqlite.save(['sdate'],record)



