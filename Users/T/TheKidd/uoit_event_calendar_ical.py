import scraperwiki
from icalendar import Calendar, Event, UTC, vDatetime
import datetime
from pytz import timezone

args = scraperwiki.utils.GET()

sourcescraper = 'uoit_event_calendar'
scraperwiki.sqlite.attach(sourcescraper)

if args.has_key('cat'):
    data = scraperwiki.sqlite.select("* from uoit_event_calendar.swdata WHERE category='%s'" % args['cat'])
else:
    data = scraperwiki.sqlite.select("* from uoit_event_calendar.swdata")

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'PUBLISH')
cal.add('X-WR-CALNAME', 'UOIT Events Calendar')
cal.add('X-WR-TIMEZONE', 'America/Toronto')
cal.add('X-ORIGINAL-URL', 'http://scraperwikiviews.com/run/uoit_events_calendar_ical/')
for ev in data:
    #print ev
    times = ev['time'].replace(".","").split(" to ")

    event = Event()
    event.add('summary', ev['name'].replace(",","\,"))
    event.add('location', ev['location'].replace(",","\,"))

    #use different parsing strings depending on if times contain minutes
    starttime = " ".join([ev['date'], times[0]])
    startdt = datetime.datetime.strptime(starttime, "%A, %B %d, %Y %I" + (":%M %p" if ":" in starttime else " %p"))
    event.add('dtstart;VALUE=DATE-TIME', vDatetime(startdt).ical())
    
    endtime = " ".join([ev['date'], times[1]])
    enddt = datetime.datetime.strptime(endtime, "%A, %B %d, %Y %I" + (":%M %p" if ":" in endtime else " %p"))
    event.add('dtend;VALUE=DATE-TIME', vDatetime(enddt).ical())
    
    event.add('dtstamp;VALUE=DATE-TIME', vDatetime(startdt).ical())
    event.add('uid', str(ev['id'])+"/@uoit-guidebook.com")
    event.add('class', 'PUBLIC')

    cal.add_component(event)

scraperwiki.utils.httpresponseheader("Content-Type", "text/calendar")
scraperwiki.utils.httpresponseheader("Content-Disposition", "inline; filename=uoit-events.ics")
print cal.as_string()