import datetime

import dateutil.parser
from icalendar import Calendar, Event
from pytz import timezone

import scraperwiki

sourcescraper = 'chicago_public_schools_student_days_off'
track = "Track R"
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select('''* from swdata where track = ? OR track = "All Tracks" ORDER BY date''', track)
cal = Calendar()
cal.add('prodid', "-//Geoffrey Hing//Chicago Public Schools: Student days off (%s)//EN" % (track))
cal.add('version', '2.0')
cal.add('x-wr-calname', "Chicago Public Schools: Student days off (%s)" % (track))
cal.add('x-wr-caldesc', "Days off from Chicago Public Shools %s schools" % (track))
cal.add('x-wr-timezone', 'America/Chicago')

one_day = datetime.timedelta(days=1)

for row in data:   
    date = dateutil.parser.parse(row['date']).date()
    start = date
    end = start + one_day
    event = Event()
    event.add('summary', 'No Class: %s' % row['description'])
    event.add('dtstart', date)
    event.add('dtend', date)
    cal.add_component(event)

scraperwiki.utils.httpresponseheader("Content-Type", "text/calendar")
scraperwiki.utils.httpresponseheader("Content-Disposition", "inline; filename=cps-student_days_off-track_r.ics")
print cal.to_ical()
import datetime

import dateutil.parser
from icalendar import Calendar, Event
from pytz import timezone

import scraperwiki

sourcescraper = 'chicago_public_schools_student_days_off'
track = "Track R"
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select('''* from swdata where track = ? OR track = "All Tracks" ORDER BY date''', track)
cal = Calendar()
cal.add('prodid', "-//Geoffrey Hing//Chicago Public Schools: Student days off (%s)//EN" % (track))
cal.add('version', '2.0')
cal.add('x-wr-calname', "Chicago Public Schools: Student days off (%s)" % (track))
cal.add('x-wr-caldesc', "Days off from Chicago Public Shools %s schools" % (track))
cal.add('x-wr-timezone', 'America/Chicago')

one_day = datetime.timedelta(days=1)

for row in data:   
    date = dateutil.parser.parse(row['date']).date()
    start = date
    end = start + one_day
    event = Event()
    event.add('summary', 'No Class: %s' % row['description'])
    event.add('dtstart', date)
    event.add('dtend', date)
    cal.add_component(event)

scraperwiki.utils.httpresponseheader("Content-Type", "text/calendar")
scraperwiki.utils.httpresponseheader("Content-Disposition", "inline; filename=cps-student_days_off-track_r.ics")
print cal.to_ical()
