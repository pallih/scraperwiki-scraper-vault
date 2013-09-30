import scraperwiki
from icalendar import Calendar, Event, UTC, vDate, vDatetime
import datetime
from pytz import timezone

sourcescraper = 'torontoca_events_calendar'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select("* from torontoca_events_calendar.swdata")

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'PUBLISH')
cal.add('X-WR-CALNAME', 'Toronto Events Calendar')
cal.add('X-WR-TIMEZONE', 'America/Toronto')
cal.add('X-ORIGINAL-URL', 'http://scraperwikiviews.com/run/torontoca_events_calendar_ical/')

for row_num, ev in enumerate(data):

    event = Event()
    event.add('summary', ev['name'].replace(",","\,"))
    event.add('description', ev['description'].replace(",","\,").replace(";","\;"))

    startdt = enddt = datetime.datetime.strptime(ev['date'], "%Y-%m-%d")

    event.add('dtstart;VALUE=DATE', vDate(startdt).ical())
    event.add('dtend;VALUE=DATE', vDate(enddt).ical())
    
    event.add('dtstamp;VALUE=DATE-TIME', vDatetime(startdt).ical())
    event.add('uid', str(row_num)+"@toronto-events")
    event.add('class', 'PUBLIC')

    cal.add_component(event)

scraperwiki.utils.httpresponseheader("Content-Type", "text/calendar")
scraperwiki.utils.httpresponseheader("Content-Disposition", "inline; filename=toronto-events.ics")
print cal.as_string()import scraperwiki
from icalendar import Calendar, Event, UTC, vDate, vDatetime
import datetime
from pytz import timezone

sourcescraper = 'torontoca_events_calendar'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select("* from torontoca_events_calendar.swdata")

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'PUBLISH')
cal.add('X-WR-CALNAME', 'Toronto Events Calendar')
cal.add('X-WR-TIMEZONE', 'America/Toronto')
cal.add('X-ORIGINAL-URL', 'http://scraperwikiviews.com/run/torontoca_events_calendar_ical/')

for row_num, ev in enumerate(data):

    event = Event()
    event.add('summary', ev['name'].replace(",","\,"))
    event.add('description', ev['description'].replace(",","\,").replace(";","\;"))

    startdt = enddt = datetime.datetime.strptime(ev['date'], "%Y-%m-%d")

    event.add('dtstart;VALUE=DATE', vDate(startdt).ical())
    event.add('dtend;VALUE=DATE', vDate(enddt).ical())
    
    event.add('dtstamp;VALUE=DATE-TIME', vDatetime(startdt).ical())
    event.add('uid', str(row_num)+"@toronto-events")
    event.add('class', 'PUBLIC')

    cal.add_component(event)

scraperwiki.utils.httpresponseheader("Content-Type", "text/calendar")
scraperwiki.utils.httpresponseheader("Content-Disposition", "inline; filename=toronto-events.ics")
print cal.as_string()