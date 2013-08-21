# should validate at http://icalvalid.cloudapp.net/
import dateutil.parser
import datetime, time
import scraperwiki
import sys
from icalendar import Calendar, Event, UTC, vDatetime, vRecur
from icalendar.cal import Component
import cgi, os

def getCourses(coursedata):
    courses=coursedata.split(',')
    coursedata = ""
    donefirst = False
    for course in courses:
        if (donefirst):
            coursedata = coursedata + ","
        coursedata = coursedata + '"' + course + '"'
        donefirst = True
    return coursedata

try:
    args = cgi.parse_qs(os.getenv("QUERY_STRING"))
except AttributeError:
    print "No courses defined"
    sys.exit()
    pass

scraperwiki.utils.httpresponseheader('Content-Type', 'text/calendar')
sourcescraper = 'course_listings'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('* from swdata WHERE course_code IN (' + getCourses(args['courses'][0]) + ')')

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//ScraperWiki MB//SOAS Course Listings//EN')
cal.add('X-WR-CALNAME', 'SOAS Course Listings')
cal.add('X-WR-TIMEZONE', 'Europe/London')
cal.add('X-ORIGINAL-URL', 'https://scraperwiki.com/scrapers/course_listings/')

for ev in data:

# if it's in the request...

    day_adder = { "Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4 }
    dates = []
    if (ev['term'] == "Term 1"):
        dates = [
        { "start_date": "2012-10-01", "end_date": "2012-10-30" },
        { "start_date": "2012-11-12", "end_date": "2012-12-11" }
        ]
    if (ev['term'] == "Term 1 (from week 2 of teaching)"):
        dates = [
        { "start_date" : "2012-10-08", "end_date" : "2012-10-30" },
        { "start_date" : "2012-11-12", "end_date" : "2012-12-11" }
        ]
    if (ev['term'] == "Term 1 (weeks 1-5 of teaching)"):
        dates = [
        { "start_date" : "2012-10-01", "end_date" : "2012-10-30" }
        ]
    if (ev['term'] == "Term 1, Week 1"):
        dates = [
        { "start_date" : "2012-10-01", "end_date" : "2012-10-08" }
        ]
    if (ev['term'] == "Term 1, Week 5"):
        dates = [
        { "start_date" : "2012-10-01", "end_date" : "2012-10-30" }
        ]
    if (ev['term'] == "Term 1, Week 6 of teaching"):
        dates = [
        { "start_date" : "2012-11-12", "end_date" : "2012-11-18" }
        ]
    """
        elif (ev['term'] == "Term 2"):
            dates = [
            { "start_date" : "2012-10-01", "end_date" : "2012-10-30" },
            { "start_date" : "2012-11-12", "end_date" : "2012-12-11" }
            ]
        elif (ev['term'] == "Term 3 (Week 2 Confirmed)"):
            dates = [
            { "start_date" : "2012-10-01", "end_date" : "2012-10-30" },
            { "start_date" : "2012-11-12", "end_date" : "2012-12-11" }
            ]
    """
    
    #Not implemented:
    #Full Year
    #Full Year (from week 2)
    # should probably do this better in terms of recurring events
    for date in dates:
        day = ev['day']
        try:
            d = datetime.timedelta(days=day_adder[day])
        except KeyError:
            d = datetime.timedelta(days=0)

        start_date = datetime.datetime.strptime((date["start_date"]), "%Y-%m-%d")+d
        end_date = datetime.datetime.strptime((date["end_date"]), "%Y-%m-%d")+d
        
        start_hour = datetime.timedelta(hours=ev['start_time'])
        duration = datetime.timedelta(hours=int(ev['duration']))

        start_date_time = (start_date+start_hour)
        end_date_time = (start_date_time+duration)

        event = Event()
        event.add('summary', ev['title'])
        event.add('location', ev['location'])
    
        
        recur = vRecur(FREQ='weekly', UNTIL=end_date)
        event.add('rrule', recur)
    
        event.add('dtstart',start_date_time)
        # Add an extra day as RFC2445 appears to suggest that is the correct way,
        # and that's the way Google Calendar treats it
        event.add('dtend', end_date_time)
        event.add('class', 'PUBLIC')
    
        cal.add_component(event)

sys.stdout.write(cal.to_ical())
