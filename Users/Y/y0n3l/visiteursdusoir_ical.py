#!/usr/bin/python
# -*- coding: utf-8 -*-
import scraperwiki
import dateutil.parser
import sys
from datetime import datetime, date, timedelta
from icalendar import Calendar, Event, UTC, vDatetime

scraperwiki.utils.httpresponseheader('Content-Type', 'text/calendar;charset=utf-8')
sourcescraper = 'visiteursdusoir'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('* from visiteursdusoir.swdata')
cal = Calendar()
# TODO: VERSION property should display first according to http://icalvalid.cloudapp.net/ iCal validator
# TODO: need a newer icalendar module (http://pypi.python.org/pypi/icalendar/3.0)
cal.add('version', '2.0')
cal.add('prodid', '-//ScraperWiki MB//visiteursdusoir//FR')
cal.add('X-WR-CALNAME', 'Les Visiteurs du Soir')
cal.add('X-WR-TIMEZONE', 'Europe/Paris')
cal.add('X-ORIGINAL-URL', 'https://scraperwiki.com/scrapers/visiteursdusoir/')

for ev in data:
    event = Event()
    event.add('summary', "%s *movie*" % ev['title'])
    description = "%s - %s %s (%s)\n\n%s" % (ev['director'], ev['country'], ev['duration'], ev['year'], ev['synopsis'])
    event.add('description', description)
    event.add('location', u'Pré des arts, Valbonne, France')
    event.add('geo', (43.641385,7.006245))
    event.add('url', ev['url'])
    #event.add('url', ev['allocine'])
    #event.add('X-GOOGLE-CALENDAR-CONTENT-URL', ev['poster'])
    #event.add('X-GOOGLE-CALENDAR-CONTENT-TYPE', 'image/png')
    start = datetime.strptime(ev['schedule'], '%Y-%m-%dT%H:%M:%S')
    #start =  datetime(year=start.year, month=start.month, day=start.day, hour=start.hour, minute=start.minute, tzinfo=UTC)
    event['DTSTART']= start.strftime('%Y%m%dT%H%M%S')
    #event.add('dtstart', start)
    if ev['duration']!='' and ('h' in ev['duration']):
        durationTokens = ev['duration'].split('h')
        durationMin = 0
        if durationTokens[1]!='':
            durationMin = int(durationTokens[1])
        duration = timedelta(hours=int(durationTokens[0]), minutes=durationMin)
        end = start + duration
        event['DTEND']= end.strftime('%Y%m%dT%H%M%S')
        #event.add('dtend', start+duration)
    else:
        end = start+timedelta(hours=1, minutes=30)
        #event.add('dtend', start+timedelta(hours=1, minutes=30))
        event['DTEND']= end.strftime('%Y%m%dT%H%M%S')
    #event.add('duration', timedelta(hours=2))
    #event.add('dtend', dateutil.parser.parse(ev['schedule']).date()+datetime.timedelta(hours=2))
    event.add('class', 'PUBLIC')
    cal.add_component(event)

sys.stdout.write(cal.to_ical())
