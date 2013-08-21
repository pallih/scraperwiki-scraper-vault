import scraperwiki
from itertools import islice, chain
import os
# os.getenv("QUERY_STRING")

def batch(iterable, size):
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, size)
        yield chain([batchiter.next()], batchiter)

scraperwiki.utils.httpresponseheader('Content-Type', 'text/calendar; charset="UTF-8"' )

sourcescraper = "uk-parliament-calendar-ical-feed"

scraperwiki.sqlite.attach("uk-parliament-calendar-ical-feed", "datasource")
data = scraperwiki.sqlite.execute('select * from datasource.swdata where date > "2011-12-01" order by date')

keys = data['keys']

print "BEGIN:VCALENDAR"
print "METHOD:PUBLISH"
print "VERSION:2.0"
print "X-WR-CALNAME:UK Parliament"
print "X-WR-CALDESC:UK Parliament Calendar"
print "PRODID:-//Apple Inc.//iCal 5.0.1//EN"
print "X-WR-TIMEZONE:Europe/London"

for datarows in batch(data['data'], 100):
    for datarow in datarows:
        row = dict( zip( keys, datarow ) )
        print "BEGIN:VEVENT"
        print "UID:%s" % row.get('guid')
        if row.get('date'):
            if row.get('starttime'): 
                print "DTSTAMP:%s" % row.get('date').replace("-","") + "T" + row.get('starttime').replace(":","") + "Z"
                print "DTSTART:%s" % row.get('date').replace("-","") + "T" + row.get('starttime').replace(":","") + "Z"
                print "DTEND:%s" % row.get('date').replace("-","") + "T" + row.get('starttime').replace(":","") + "Z"
            else:
                print "DTSTAMP:%s" % row.get('date').replace("-","") + "T000000Z"
                print "DTSTART:%s" % row.get('date').replace("-","") + "T000000Z"
                print "DTEND:%s" % row.get('date').replace("-","") + "T000000Z"
        else:
            print "DTSTAMP:%s" % "00000000T000000Z"
        print "X-TITLE:%s" % row.get('title')
        print "X-UK-PARLIAMENT-COMMITTEE:%s" % row.get('committee')
        print "X-UK-PARLIAMENT-EVENT-ID:%s" % row.get('event-id')
        # print "X-UK-PARLIAMENT-WITNESSES:%s" % row.get('witnesses')
        print "X-UK-PARLIAMENT-LINK:%s" % row.get('link')
        if row.get('subject'):
            print "SUMMARY:%s" % row.get('subject').replace("\n", " ").replace("\r", " ")
            print "DESCRIPTION:%s" % row.get('subject').replace("\n", " ").replace("\r", " ")
        elif row.get('title'):
            print "SUMMARY:%s" % row.get('title').replace("\n", " ").replace("\r", " ")
            print "DESCRIPTION:%s" % ""
        if row.get('location'):
            print "LOCATION:%s" % row.get('location') + " [" + row.get('house') + "]"
        else:
            print "LOCATION:%s" % row.get('chamber')
        
        print "END:VEVENT"
    
print "END:VCALENDAR"
