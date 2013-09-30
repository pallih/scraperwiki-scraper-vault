import scraperwiki
import re
import dateutil.parser
from datetime import date
from icalendar import Calendar, Event, UTC, vDatetime
import sys

def sqlite_api(scrapername, sql):
    # returns a list/dict of data from the named scraper
    if scrapername and sql:
        import requests, json
        api_base = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite'
        params = {'format': 'jsondict', 'name': scrapername, 'query': sql}
        j = requests.get(api_base, params=params, verify=False).content
        if j:
            return json.loads(j)
        else:
            raise Exception("sqlite_api() could not decode the ScraperWiki API's JSON response")
    else:
        raise Exception("sqlite_api() takes two arguments: a scraper name and a SQLite query")

events = sqlite_api('liverpool_cruise_call_schedule', 'select * from schedule order by start asc')

if 'error' in events:
    raise Exception("ScraperWiki API error: " + events['error'])
else:
    scraperwiki.utils.httpresponseheader('Content-Type', 'text/calendar')
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('prodid', '-//ScraperWiki//Liverpool Cruise Call Schedule//EN')
    cal.add('X-WR-CALNAME', 'Liverpool Cruise Call Schedule')
    cal.add('X-WR-TIMEZONE', 'Europe/London')
    cal.add('METHOD', 'REQUEST')
    cal.add('ORGANIZER', 'liverpool-cruise-call-schedule@scraperwiki.com')
    
    for e in events:
        event = Event()
        event.add('class', 'PUBLIC')
        title = e['vessel']
        if e['cruise_line']:
            title += ' (' + e['cruise_line'] + ' cruise line)'
        title += ' calls at Liverpool'
        if e['category']:
            title += ' for ' + e['category'].lower()
        event.add('summary', title)
        event.add('location', 'Liverpool')
        event.add('dtstart', dateutil.parser.parse(e['start']))
        event.add('dtend', dateutil.parser.parse(e['end']))
        event['uid'] = str(date.strftime(dateutil.parser.parse(e['start']), '%Y%m%d%H%M%S')) + '/liverpool-cruise-call-schedule@scraperwiki.com'
        cal.add_component(event)
    
    # use sys.stdout because print would end file with a \n
    # which is invalid and causes iCal (Mac) to barf
    sys.stdout.write(cal.to_ical())
import scraperwiki
import re
import dateutil.parser
from datetime import date
from icalendar import Calendar, Event, UTC, vDatetime
import sys

def sqlite_api(scrapername, sql):
    # returns a list/dict of data from the named scraper
    if scrapername and sql:
        import requests, json
        api_base = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite'
        params = {'format': 'jsondict', 'name': scrapername, 'query': sql}
        j = requests.get(api_base, params=params, verify=False).content
        if j:
            return json.loads(j)
        else:
            raise Exception("sqlite_api() could not decode the ScraperWiki API's JSON response")
    else:
        raise Exception("sqlite_api() takes two arguments: a scraper name and a SQLite query")

events = sqlite_api('liverpool_cruise_call_schedule', 'select * from schedule order by start asc')

if 'error' in events:
    raise Exception("ScraperWiki API error: " + events['error'])
else:
    scraperwiki.utils.httpresponseheader('Content-Type', 'text/calendar')
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('prodid', '-//ScraperWiki//Liverpool Cruise Call Schedule//EN')
    cal.add('X-WR-CALNAME', 'Liverpool Cruise Call Schedule')
    cal.add('X-WR-TIMEZONE', 'Europe/London')
    cal.add('METHOD', 'REQUEST')
    cal.add('ORGANIZER', 'liverpool-cruise-call-schedule@scraperwiki.com')
    
    for e in events:
        event = Event()
        event.add('class', 'PUBLIC')
        title = e['vessel']
        if e['cruise_line']:
            title += ' (' + e['cruise_line'] + ' cruise line)'
        title += ' calls at Liverpool'
        if e['category']:
            title += ' for ' + e['category'].lower()
        event.add('summary', title)
        event.add('location', 'Liverpool')
        event.add('dtstart', dateutil.parser.parse(e['start']))
        event.add('dtend', dateutil.parser.parse(e['end']))
        event['uid'] = str(date.strftime(dateutil.parser.parse(e['start']), '%Y%m%d%H%M%S')) + '/liverpool-cruise-call-schedule@scraperwiki.com'
        cal.add_component(event)
    
    # use sys.stdout because print would end file with a \n
    # which is invalid and causes iCal (Mac) to barf
    sys.stdout.write(cal.to_ical())
