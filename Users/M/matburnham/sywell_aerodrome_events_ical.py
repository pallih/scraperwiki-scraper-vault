# should validate at http://icalvalid.cloudapp.net/
import dateutil.parser
import datetime
import scraperwiki
import sys
from icalendar import Calendar, Event, UTC, vDatetime

scraperwiki.utils.httpresponseheader('Content-Type', 'text/calendar')
sourcescraper = 'sywell_aerodrome_events'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('* from sywell_aerodrome_events.swdata')

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//ScraperWiki MB//Sywell Aerodrome Events//EN')
cal.add('X-WR-CALNAME', 'Sywell Aerodrome Events')
cal.add('X-WR-TIMEZONE', 'Europe/London')
cal.add('X-ORIGINAL-URL', 'https://scraperwiki.com/scrapers/sywell_aerodrome_events/')

for ev in data:
    event = Event()
    event.add('summary', ev['summary'])
    event.add('location', 'Sywell Aerodrome')
    event.add('dtstart', dateutil.parser.parse(ev['start_date']).date())
    # Add an extra day as RFC2445 appears to suggest that is the correct way,
    # and that's the way Google Calendar treats it
    event.add('dtend', dateutil.parser.parse(ev['end_date']).date()+datetime.timedelta(days=1))
    event.add('class', 'PUBLIC')

    cal.add_component(event)

sys.stdout.write(cal.to_ical())

# should validate at http://icalvalid.cloudapp.net/
import dateutil.parser
import datetime
import scraperwiki
import sys
from icalendar import Calendar, Event, UTC, vDatetime

scraperwiki.utils.httpresponseheader('Content-Type', 'text/calendar')
sourcescraper = 'sywell_aerodrome_events'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('* from sywell_aerodrome_events.swdata')

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//ScraperWiki MB//Sywell Aerodrome Events//EN')
cal.add('X-WR-CALNAME', 'Sywell Aerodrome Events')
cal.add('X-WR-TIMEZONE', 'Europe/London')
cal.add('X-ORIGINAL-URL', 'https://scraperwiki.com/scrapers/sywell_aerodrome_events/')

for ev in data:
    event = Event()
    event.add('summary', ev['summary'])
    event.add('location', 'Sywell Aerodrome')
    event.add('dtstart', dateutil.parser.parse(ev['start_date']).date())
    # Add an extra day as RFC2445 appears to suggest that is the correct way,
    # and that's the way Google Calendar treats it
    event.add('dtend', dateutil.parser.parse(ev['end_date']).date()+datetime.timedelta(days=1))
    event.add('class', 'PUBLIC')

    cal.add_component(event)

sys.stdout.write(cal.to_ical())

