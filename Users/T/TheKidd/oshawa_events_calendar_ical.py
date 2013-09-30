import scraperwiki
from icalendar import Calendar, Event, UTC, vDate, vDatetime
import datetime
from pytz import timezone

sourcescraper = 'oshawa_events_calendar'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select("* from oshawa_events_calendar.swdata")

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'PUBLISH')
cal.add('X-WR-CALNAME', 'Oshawa Events Calendar')
cal.add('X-WR-TIMEZONE', 'America/Toronto')
cal.add('X-ORIGINAL-URL', 'http://scraperwikiviews.com/run/oshawa_events_calendar_ical/')

for ev in data:
    #print ev

    event = Event()
    event.add('summary', ev['name'].replace(",","\,"))
    event.add('location', ev['location'].replace(",","\,"))
    event.add('description', ev['description'].replace(",","\,"))

    days = ev['date'].split(" - ")
    if len(days) == 2:
        startdt = datetime.datetime.strptime(days[0], "%B %d, %Y")
        enddt = datetime.datetime.strptime(days[1], "%B %d, %Y")
    else:
        startdt = enddt = datetime.datetime.strptime(ev['date'], "%B %d, %Y")

    event.add('dtstart;VALUE=DATE', vDate(startdt).ical())
    event.add('dtend;VALUE=DATE', vDate(enddt).ical())
    
    event.add('dtstamp;VALUE=DATE-TIME', vDatetime(startdt).ical())
    event.add('uid', ev['name']+"/@uoit-guidebook.com")
    event.add('class', 'PUBLIC')

    cal.add_component(event)
print cal.as_string()import scraperwiki
from icalendar import Calendar, Event, UTC, vDate, vDatetime
import datetime
from pytz import timezone

sourcescraper = 'oshawa_events_calendar'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select("* from oshawa_events_calendar.swdata")

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'PUBLISH')
cal.add('X-WR-CALNAME', 'Oshawa Events Calendar')
cal.add('X-WR-TIMEZONE', 'America/Toronto')
cal.add('X-ORIGINAL-URL', 'http://scraperwikiviews.com/run/oshawa_events_calendar_ical/')

for ev in data:
    #print ev

    event = Event()
    event.add('summary', ev['name'].replace(",","\,"))
    event.add('location', ev['location'].replace(",","\,"))
    event.add('description', ev['description'].replace(",","\,"))

    days = ev['date'].split(" - ")
    if len(days) == 2:
        startdt = datetime.datetime.strptime(days[0], "%B %d, %Y")
        enddt = datetime.datetime.strptime(days[1], "%B %d, %Y")
    else:
        startdt = enddt = datetime.datetime.strptime(ev['date'], "%B %d, %Y")

    event.add('dtstart;VALUE=DATE', vDate(startdt).ical())
    event.add('dtend;VALUE=DATE', vDate(enddt).ical())
    
    event.add('dtstamp;VALUE=DATE-TIME', vDatetime(startdt).ical())
    event.add('uid', ev['name']+"/@uoit-guidebook.com")
    event.add('class', 'PUBLIC')

    cal.add_component(event)
print cal.as_string()