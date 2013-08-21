import scraperwiki
import urllib
import urllib2
import urlparse
import lxml.etree, lxml.html
import re
import HTMLParser
from datetime import datetime, timedelta

scraperwiki.sqlite.attach("iswc_2011_program_schedule_1", "schedule");
#kr = scraperwiki.sqlite.select("* from schedule.swdata where title like '%Reasoners'");
#print kr[0]['start_time']

# Research track.
html = scraperwiki.scrape("http://iswc2011.semanticweb.org/program/research-papers/")

root = lxml.html.fromstring(html)
num = 0;

for div in root.cssselect(".floatbox .csc-default"):
    divId = div.get('id')
    h2 = div.cssselect("tr h2")
    if len(h2) > 0:
        num = num + 1;
        innerBlockNum = 0
        time = h2[0].text_content()
        h1 = div.cssselect("h1")
        session_name = h1[0].text_content()
        rows = div.cssselect("tr")
        session_chair = rows[1].text_content().replace('Session Chair: ', '').replace('Chair: ','')
        session_uri = 'http://data.semanticweb.org/conference/iswc/2011/sessions/research/' + str(num)
        del rows[0]
        del rows[0]
        
        # Get the room and time information
        sessionData = scraperwiki.sqlite.select("* from schedule.swdata where id like '%" + divId + "'")
        sstart, send = map(lambda x: datetime.strptime(x, r'%d.%m.%Y %H:%M'),
                           [sessionData[0]['start_time'], sessionData[0]['end_time']])
        sessionTimeD = send - sstart
        timePerTalk = sessionTimeD / len(rows)
        print sessionTimeD, timePerTalk

        
        for i,row in enumerate(rows):
            authors = row.cssselect('td')[0].text_content()
            a = row.cssselect("td a")
            paper_name = a[0].text_content()
            paper_url = 'http://iswc2011.semanticweb.org/' + a[0].get('href')
            
            start_time = sstart + timePerTalk * i
            end_time = sstart + timePerTalk * (i+1)
            assert end_time > start_time
            assert end_time <= send
            start_time, end_time = map(lambda x: x.strftime(r'%d.%m.%Y %H:%M'),
                                       [start_time, end_time])
            

            # Save research paper to the database.
            data = {}
            data['session_name'] = sessionData[0]['title']
            data['start_time'] = start_time
            data['end_time'] = end_time
            data['room'] = sessionData[0]['room']
            data['track'] = sessionData[0]['track']
            data['chair'] = session_chair
            data['session_uri'] = session_uri
            data['authors'] = authors
            data['title'] = paper_name
            data['id'] = paper_url
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)