# Blank Python
import scraperwiki, re

def ical_date(d):
    return re.sub(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})[-+](\d{2}):(\d{2})', r'\1\2\3T\4\5\6', d)

sourcescraper = 'alfresco_devcon_hcalendar_event_parser'
tzid=";TZID=US/Pacific"
#tzid=""

scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select("* from `events`")

scraperwiki.utils.httpresponseheader("Content-Type", "text/plain")

print """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//wabson/devcon//NONSGML v1.0//EN
X-WR-CALNAME;VALUE=TEXT:San Jose Sessions"""

tz = """BEGIN:VTIMEZONE
TZID:US/Pacific
LAST-MODIFIED:20060110T171418Z
BEGIN:STANDARD
DTSTART:20121030T080000
TZOFFSETTO:-0800
TZOFFSETFROM:+0000
TZNAME:PST
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:20130402T020000
TZOFFSETTO:-0700
TZOFFSETFROM:-0800
TZNAME:PDT
END:DAYLIGHT
END:VTIMEZONE"""

print tz

for row in data:
    print "BEGIN:VEVENT"
    print "UID:devcon.alfresco.com" + row['url']
    print "DTSTAMP%s:" % (tzid) + ical_date(row['start_time'])
    print "DTSTART%s:" % (tzid) + ical_date(row['start_time'])
    print "DTEND%s:" % (tzid) + ical_date(row['end_time'])
    print "LOCATION:" + row['event_location']
    print "SUMMARY:" + re.sub(r'\s+', ' ', row['event_name']).replace(',', '\,')
    print "DESCRIPTION: Full session information - http://devcon.alfresco.com%s" % (row['url'])
    print "END:VEVENT"

print "END:VCALENDAR"
# Blank Python
import scraperwiki, re

def ical_date(d):
    return re.sub(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})[-+](\d{2}):(\d{2})', r'\1\2\3T\4\5\6', d)

sourcescraper = 'alfresco_devcon_hcalendar_event_parser'
tzid=";TZID=US/Pacific"
#tzid=""

scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select("* from `events`")

scraperwiki.utils.httpresponseheader("Content-Type", "text/plain")

print """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//wabson/devcon//NONSGML v1.0//EN
X-WR-CALNAME;VALUE=TEXT:San Jose Sessions"""

tz = """BEGIN:VTIMEZONE
TZID:US/Pacific
LAST-MODIFIED:20060110T171418Z
BEGIN:STANDARD
DTSTART:20121030T080000
TZOFFSETTO:-0800
TZOFFSETFROM:+0000
TZNAME:PST
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:20130402T020000
TZOFFSETTO:-0700
TZOFFSETFROM:-0800
TZNAME:PDT
END:DAYLIGHT
END:VTIMEZONE"""

print tz

for row in data:
    print "BEGIN:VEVENT"
    print "UID:devcon.alfresco.com" + row['url']
    print "DTSTAMP%s:" % (tzid) + ical_date(row['start_time'])
    print "DTSTART%s:" % (tzid) + ical_date(row['start_time'])
    print "DTEND%s:" % (tzid) + ical_date(row['end_time'])
    print "LOCATION:" + row['event_location']
    print "SUMMARY:" + re.sub(r'\s+', ' ', row['event_name']).replace(',', '\,')
    print "DESCRIPTION: Full session information - http://devcon.alfresco.com%s" % (row['url'])
    print "END:VEVENT"

print "END:VCALENDAR"
