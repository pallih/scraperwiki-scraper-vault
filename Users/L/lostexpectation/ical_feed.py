from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "uk-parliament-calendar-ical-feed"

keys = scraperwiki.sqlite.attach(sourcescraper)

print "BEGIN:VCALENDAR"
print "METHOD:PUBLISH"
print "VERSION:2.0"
print "X-WR-CALNAME:UK Parliament"
print "X-WR-CALDESC:UK Parliament Calendar"
print "PRODID:-//Apple Inc.//iCal 4.0.3//EN"
print "X-WR-TIMEZONE:Europe/London"

for row in getData(sourcescraper):
    
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
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "uk-parliament-calendar-ical-feed"

keys = scraperwiki.sqlite.attach(sourcescraper)

print "BEGIN:VCALENDAR"
print "METHOD:PUBLISH"
print "VERSION:2.0"
print "X-WR-CALNAME:UK Parliament"
print "X-WR-CALDESC:UK Parliament Calendar"
print "PRODID:-//Apple Inc.//iCal 4.0.3//EN"
print "X-WR-TIMEZONE:Europe/London"

for row in getData(sourcescraper):
    
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
