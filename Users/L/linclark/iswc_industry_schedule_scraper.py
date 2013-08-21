import scraperwiki
import urllib
import urllib2
import urlparse
import lxml.etree, lxml.html
import re
import HTMLParser

# Industry track.
html = scraperwiki.scrape("http://iswc2011.semanticweb.org/program/industry-track/")

root = lxml.html.fromstring(html)
num = 0;

tr = root.cssselect("#c1465 tr")
rows = tr[2:8] + tr[9:15]
for row in rows:
    num = num + 1
    td = row.cssselect('td')
    paper_name = td[1].text_content()
    if td[1].get('href') > 0:
        paper_url = 'http://iswc2011.semanticweb.org/' + td[1].get('href').lstrip('../')
    else:
        paper_url = ''
    if num < 7:
        session_uri = 'http://data.semanticweb.org/conference/iswc/2011/sessions/industry/1'
        startTime = '14:00'
        endTime = '16:00'
    else:
        session_uri = 'http://data.semanticweb.org/conference/iswc/2011/sessions/industry/2'
        startTime = '16:30'
        endTime = '18:00'

    # Save research paper to the database.
    data = {}
    data['session_start'] = startTime
    data['session_end'] = endTime
    data['session_day'] = 'Tuesday'
    data['session_room'] = 'Liszt'
    data['session_uri'] = session_uri
    data['paper_name'] = paper_name
    data['paper_url'] = paper_url
    scraperwiki.sqlite.save(unique_keys=['paper_name'], data=data)