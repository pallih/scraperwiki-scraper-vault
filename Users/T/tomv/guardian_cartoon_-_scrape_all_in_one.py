import scraperwiki

"""
Inspired by the XKCD Google Calendar widget by Michael Bolin
http://www.bolinfest.com/calendars/

All code by Tom Viner except were stated below
"""
import sys
import re
import time
import datetime
import feedparser

def escapeIcal(ical):
    """
    This function taken from http://www.bolinfest.com/calendars/xkcd.py
    """
    # TODO(bolinfest): figure out how newlines are escaped
    return ical.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,')

def remove_tags(html):
    return re.sub(r'(?:\s*<[^>]+>\s*)+', ' - ', html).strip(' -')

# This template taken from http://www.bolinfest.com/calendars/xkcd.ics
VCAL_TEMPLATE = """\
BEGIN:VCALENDAR
X-WR-CALNAME;VALUE=TEXT:guardiancartoons
VERSION:2.0
CALSCALE:GREGORIAN
%s
END:VCALENDAR\
"""

VEVENT_TEMPLATE = """\
BEGIN:VEVENT
DTSTART;VALUE=DATE:%(start_date)sT00:00:00Z
DTEND;VALUE=DATE:%(end_date)s
SUMMARY:%(title)s
X-GOOGLE-CALENDAR-CONTENT-TITLE:%(title)s
X-GOOGLE-CALENDAR-CONTENT-ICON:http://www.guardian.co.uk/favicon.ico
X-GOOGLE-CALENDAR-CONTENT-URL:http://www.google.com/ig/modules/imagelink.xml
X-GOOGLE-CALENDAR-CONTENT-TYPE:application/x-google-gadgets+xml
X-GOOGLE-CALENDAR-CONTENT-WIDTH:%(width)s
X-GOOGLE-CALENDAR-CONTENT-HEIGHT:%(height)s
X-GOOGLE-CALENDAR-CONTENT-GADGET-PREF;NAME=linkUrl:%(link)s
X-GOOGLE-CALENDAR-CONTENT-GADGET-PREF;NAME=width:%(width)s
X-GOOGLE-CALENDAR-CONTENT-GADGET-PREF;NAME=height:%(height)s
X-GOOGLE-CALENDAR-CONTENT-GADGET-PREF;NAME=imageUrl:%(image)s
X-GOOGLE-CALENDAR-CONTENT-GADGET-PREF;NAME=tooltip:%(description)s
END:VEVENT\
"""

FEED_URL = "http://www.guardian.co.uk/cartoons/archive/rss"
ONE_DAY = datetime.timedelta(days=1)
SOME_HOURS = datetime.timedelta(hours=5)

vevents = []

d = feedparser.parse(scraperwiki.scrape(FEED_URL))
for item in d['items']:
    data = {}
    img = max(item['media_content'], key=lambda img:int(img['width']))
    data['width'] = img['width']
    data['height'] = img['height']
    data['image'] = img['url']
    data['link'] = item['link']
    data['description'] = escapeIcal(remove_tags(item['summary']))
    data['title'] = escapeIcal(item['title'])
    #data['xxx'] = item['xxx']
    t = item['updated_parsed']
    dstart = datetime.datetime(*t[:6]) + SOME_HOURS
    dend = dstart + ONE_DAY
    data['start_date'] = dstart.strftime('%Y%m%d')
    data['end_date'] = dend.strftime('%Y%m%d')
    vevents.append(VEVENT_TEMPLATE % data)

ical = VCAL_TEMPLATE % '\n'.join(vevents)
scraperwiki.utils.httpresponseheader('Content-Type', 'text/calendar')
print ical.encode('utf-8')
