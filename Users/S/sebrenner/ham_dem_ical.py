import scraperwiki
from icalendar import Calendar, Event, UTC, vDate, vDatetime
import datetime
from pytz import timezone


sourcescraper = 'HamDemScraper'
scraperwiki.sqlite.attach(sourcescraper)


data = scraperwiki.sqlite.select("* from HamDemScraper.swdata")

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'PUBLISH')
cal.add('X-WR-CALNAME', 'Hamilton County Democratic Party Events')
cal.add('X-WR-TIMEZONE', 'America/Detroit')
cal.add('X-ORIGINAL-URL', 'http://scraperwikiviews.com/run/torontoca_events_calendar_ical/')

for row_num, ev in enumerate(data):

    event = Event()
    event.add('summary', ev['name'].replace(",","\,"))
    event.add('description', ev['description'].replace(",","\,").replace(";","\;"))

    startdt = enddt = datetime.datetime.strptime(ev['date'], "%Y-%m-%d")

    event.add('dtstart;VALUE=DATE', vDate(startdt).ical())
    event.add('DURATION', "PT1H0M0S")  

    event.add('dtstamp;VALUE=DATE-TIME', vDatetime(startdt).ical())
    event.add('uid', str(row_num)+"@toronto-events")
    event.add('class', 'PUBLIC')

    cal.add_component(event)

scraperwiki.utils.httpresponseheader("Content-Type", "text/calendar")
scraperwiki.utils.httpresponseheader("Content-Disposition", "inline; filename=ham_dems.ics")
print cal.as_string()import scraperwiki
from icalendar import Calendar, Event, UTC, vDate, vDatetime
import datetime
from pytz import timezone


sourcescraper = 'HamDemScraper'
scraperwiki.sqlite.attach(sourcescraper)


data = scraperwiki.sqlite.select("* from HamDemScraper.swdata")

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'PUBLISH')
cal.add('X-WR-CALNAME', 'Hamilton County Democratic Party Events')
cal.add('X-WR-TIMEZONE', 'America/Detroit')
cal.add('X-ORIGINAL-URL', 'http://scraperwikiviews.com/run/torontoca_events_calendar_ical/')

for row_num, ev in enumerate(data):

    event = Event()
    event.add('summary', ev['name'].replace(",","\,"))
    event.add('description', ev['description'].replace(",","\,").replace(";","\;"))

    startdt = enddt = datetime.datetime.strptime(ev['date'], "%Y-%m-%d")

    event.add('dtstart;VALUE=DATE', vDate(startdt).ical())
    event.add('DURATION', "PT1H0M0S")  

    event.add('dtstamp;VALUE=DATE-TIME', vDatetime(startdt).ical())
    event.add('uid', str(row_num)+"@toronto-events")
    event.add('class', 'PUBLIC')

    cal.add_component(event)

scraperwiki.utils.httpresponseheader("Content-Type", "text/calendar")
scraperwiki.utils.httpresponseheader("Content-Disposition", "inline; filename=ham_dems.ics")
print cal.as_string()