import scraperwiki
from icalendar import Calendar, Event, UTC, vDatetime
import datetime
from pytz import timezone

sourcescraper = 'uoit_student_center_calendar'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select("* from uoit_student_center_calendar.swdata")

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'PUBLISH')
cal.add('X-WR-CALNAME', 'UOIT Student Center Calendar')
cal.add('X-WR-TIMEZONE', 'America/Toronto')
cal.add('X-ORIGINAL-URL', 'http://scraperwikiviews.com/run/uoit_student_center_calendar_ical/')

for ev in data:
    #print ev

    event = Event()
    event.add('summary', ev['name'].replace(",","\,"))
    event.add('location', ev['location'].replace(",","\,"))

    startday = ev['from'].rpartition(" ")[0]
    startdt = datetime.datetime.strptime(ev['from'], "%b %d, %Y %I:%M%p")
    event.add('dtstart;VALUE=DATE-TIME', vDatetime(startdt).ical())
    
    #use different parsing strings depending on if no date
    enddt = datetime.datetime.strptime(ev['to'] if " " in ev['to'] else " ".join([startday,ev['to']]), "%b %d, %Y %I:%M%p")
    event.add('dtend;VALUE=DATE-TIME', vDatetime(enddt).ical())
    
    event.add('dtstamp;VALUE=DATE-TIME', vDatetime(startdt).ical())
    event.add('uid', str(ev['id'])+"/@uoit-guidebook.com")
    event.add('class', 'PUBLIC')

    cal.add_component(event)
print cal.as_string()import scraperwiki
from icalendar import Calendar, Event, UTC, vDatetime
import datetime
from pytz import timezone

sourcescraper = 'uoit_student_center_calendar'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select("* from uoit_student_center_calendar.swdata")

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'PUBLISH')
cal.add('X-WR-CALNAME', 'UOIT Student Center Calendar')
cal.add('X-WR-TIMEZONE', 'America/Toronto')
cal.add('X-ORIGINAL-URL', 'http://scraperwikiviews.com/run/uoit_student_center_calendar_ical/')

for ev in data:
    #print ev

    event = Event()
    event.add('summary', ev['name'].replace(",","\,"))
    event.add('location', ev['location'].replace(",","\,"))

    startday = ev['from'].rpartition(" ")[0]
    startdt = datetime.datetime.strptime(ev['from'], "%b %d, %Y %I:%M%p")
    event.add('dtstart;VALUE=DATE-TIME', vDatetime(startdt).ical())
    
    #use different parsing strings depending on if no date
    enddt = datetime.datetime.strptime(ev['to'] if " " in ev['to'] else " ".join([startday,ev['to']]), "%b %d, %Y %I:%M%p")
    event.add('dtend;VALUE=DATE-TIME', vDatetime(enddt).ical())
    
    event.add('dtstamp;VALUE=DATE-TIME', vDatetime(startdt).ical())
    event.add('uid', str(ev['id'])+"/@uoit-guidebook.com")
    event.add('class', 'PUBLIC')

    cal.add_component(event)
print cal.as_string()