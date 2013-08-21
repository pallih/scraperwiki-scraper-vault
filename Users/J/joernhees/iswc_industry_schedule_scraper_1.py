import scraperwiki
import urllib
import urllib2
import urlparse
import lxml.etree, lxml.html
import re
import HTMLParser
from datetime import datetime, timedelta


# Industry track.
html = scraperwiki.scrape("http://iswc2011.semanticweb.org/program/industry-track/")
scraperwiki.sqlite.attach("iswc_2011_program_schedule_1", "schedule");

root = lxml.html.fromstring(html)
num = 0;

tr = root.cssselect("#c1465 tr")
rows = tr[2:8] + tr[9:15]
i=0
for row in rows:
    num = num + 1
    td = row.cssselect('td')
    paper_name = td[1].text_content()
    authors = td[0].text_content()

    if td[1].cssselect('a') > 0:
        paper_url = 'http://iswc2011.semanticweb.org/' + td[1].cssselect('a')[0].get('href').lstrip('../')
    else:
        paper_url = ''
    if num < 7:
        session_uri = 'http://data.semanticweb.org/conference/iswc/2011/sessions/industry/1'
        startTime = '25.10.2011 14:00'
        endTime = '25.10.2011 16:00'
        talks = 6
    else:
        if num == 7: i = 0 # reset counter for time offsets in the session
        session_uri = 'http://data.semanticweb.org/conference/iswc/2011/sessions/industry/2'
        startTime = '25.10.2011 16:30'
        endTime = '25.10.2011 18:00'
        talks = 6
    
    # Get the room and time information
    sstart, send = map(lambda x: datetime.strptime(x, r'%d.%m.%Y %H:%M'),
                       [startTime, endTime])
    sessionTimeD = send - sstart
    timePerTalk = sessionTimeD / talks
    print sessionTimeD, timePerTalk
    start_time = sstart + timePerTalk * i
    end_time = sstart + timePerTalk * (i+1)
    assert end_time > start_time
    assert end_time <= send
    start_time, end_time = map(lambda x: x.strftime(r'%d.%m.%Y %H:%M'),
                               [start_time, end_time])
    
    i+=1
    
    # Save research paper to the database.
    data = {}
    data['session_name'] = "Industry Track"
    data['start_time'] = start_time
    data['end_time'] = end_time
    data['room'] = "Liszt"
    data['track'] = "Industry"
    data['session_uri'] = session_uri
    data['authors'] = authors
    data['title'] = paper_name
    data['id'] = paper_url
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

