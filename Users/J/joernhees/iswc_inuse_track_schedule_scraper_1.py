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
html = scraperwiki.scrape("http://iswc2011.semanticweb.org/program/semantic-web-in-use/")

root = lxml.html.fromstring(html)
num = 0;

for div in root.cssselect(".floatbox .csc-default"):
    divId = div.get('id')
    if divId == "c1350": divId = "1350"
    if divId == "c1352": divId = "1352"
    
    h2 = div.cssselect("tr h2")
    if len(h2) > 0:
        num = num + 1;
        innerBlockNum = 0
        time = h2[0].text_content()
        h1 = div.cssselect("h1")
        session_name = h1[0].text_content()
        print session_name
        rows = div.cssselect("tr")
        session_chair = rows[2].text_content().replace('Session Chair: ', '').replace('Chair: ','')
        print session_chair
        session_uri = 'http://data.semanticweb.org/conference/iswc/2011/sessions/inuse/' + str(num)
        del rows[0]
        del rows[0]
        del rows[0]
        
        # Get the room and time information
        sessionData = scraperwiki.sqlite.select("* from schedule.swdata where id like '%" + divId + "'")

        
        for i,row in enumerate(rows):
            sessionData = scraperwiki.sqlite.select("* from schedule.swdata where id like '%" + divId + "'")
            sstart, send = map(lambda x: datetime.strptime(x, r'%d.%m.%Y %H:%M'),
                               [sessionData[0]['start_time'], sessionData[0]['end_time']])

            start_time, end_time = map(lambda x: (sstart.strftime(r'%d.%m.%Y ') + x).strip(),
                                       row.cssselect('td')[0].text_content().strip().split('-')[:])
            authors = row.cssselect('td b')[0].text_content().rstrip('.')
            print authors
            a = row.cssselect("td a")
            paper_name = a[0].text_content()
            paper_url = 'http://iswc2011.semanticweb.org/' + a[0].get('href')
            
            

            # Save research paper to the database.
            data = {}
            data['session_name'] = session_name
            data['start_time'] = start_time
            data['end_time'] = end_time
            data['room'] = sessionData[0]['room']
            data['track'] = sessionData[0]['track']
            data['chair'] = session_chair
            data['session_uri'] = session_uri
            data['authors'] = authors
            data['title'] = paper_name
            data['id'] = paper_url
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)import scraperwiki
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
html = scraperwiki.scrape("http://iswc2011.semanticweb.org/program/semantic-web-in-use/")

root = lxml.html.fromstring(html)
num = 0;

for div in root.cssselect(".floatbox .csc-default"):
    divId = div.get('id')
    if divId == "c1350": divId = "1350"
    if divId == "c1352": divId = "1352"
    
    h2 = div.cssselect("tr h2")
    if len(h2) > 0:
        num = num + 1;
        innerBlockNum = 0
        time = h2[0].text_content()
        h1 = div.cssselect("h1")
        session_name = h1[0].text_content()
        print session_name
        rows = div.cssselect("tr")
        session_chair = rows[2].text_content().replace('Session Chair: ', '').replace('Chair: ','')
        print session_chair
        session_uri = 'http://data.semanticweb.org/conference/iswc/2011/sessions/inuse/' + str(num)
        del rows[0]
        del rows[0]
        del rows[0]
        
        # Get the room and time information
        sessionData = scraperwiki.sqlite.select("* from schedule.swdata where id like '%" + divId + "'")

        
        for i,row in enumerate(rows):
            sessionData = scraperwiki.sqlite.select("* from schedule.swdata where id like '%" + divId + "'")
            sstart, send = map(lambda x: datetime.strptime(x, r'%d.%m.%Y %H:%M'),
                               [sessionData[0]['start_time'], sessionData[0]['end_time']])

            start_time, end_time = map(lambda x: (sstart.strftime(r'%d.%m.%Y ') + x).strip(),
                                       row.cssselect('td')[0].text_content().strip().split('-')[:])
            authors = row.cssselect('td b')[0].text_content().rstrip('.')
            print authors
            a = row.cssselect("td a")
            paper_name = a[0].text_content()
            paper_url = 'http://iswc2011.semanticweb.org/' + a[0].get('href')
            
            

            # Save research paper to the database.
            data = {}
            data['session_name'] = session_name
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