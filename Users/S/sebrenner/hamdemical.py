import scraperwiki
from icalendar import Calendar, Event, UTC, vDate, vDatetime
import datetime
from pytz import timezone

sourcescraper = 'hamdem_ical_feed'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select("* from hamdem_ical_feed.swdata")

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'PUBLISH')
cal.add('X-WR-CALNAME', 'Hamilton County Democratic Party Events')
cal.add('X-WR-TIMEZONE', 'America/Detroit')
cal.add('X-ORIGINAL-URL', 'http://scraperwikiviews.com/run/hamdemical/')

for row_num, ev in enumerate(data):

    event = Event()
    event.add('summary', ev['eventName'].replace(",","\,"))
    event.add('description', ev['eventDescription'].replace(",","\,").replace(";","\;"))
    # 2011-08-05 18:30:00

    event.add('dtstart;VALUE=DATE-TIME', datetime.datetime.strptime(ev['eventStart'], "%Y-%m-%dT%H:%M:%S"))
    event.add(  'dtend;VALUE=DATE-TIME', datetime.datetime.strptime(ev['eventEnd'],   "%Y-%m-%dT%H:%M:%S"))

    event.add('dtstamp;VALUE=DATE-TIME', vDatetime(datetime.datetime.now()).ical())
    
    event.add('uid', ev['eventURI'][-4:] + "@events.hamiltoncountydems.org")
    event.add('class', 'PUBLIC')

    cal.add_component(event)

scraperwiki.utils.httpresponseheader("Content-Type", "text/calendar")
scraperwiki.utils.httpresponseheader("Content-Disposition", "inline; filename=ham-dem-events.ics")
print cal.as_string()