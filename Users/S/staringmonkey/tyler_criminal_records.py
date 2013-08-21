#!/usr/bin/env python

from datetime import date, datetime, timedelta
from httplib import BadStatusLine, HTTPResponse
import re
import string
import sys
from traceback import print_exc

from lxml.etree import tostring
from lxml.html.soupparser import fromstring
import requests
import scraperwiki

def monkey_patch(self):
    """
    This is the part where we monkey patch httplib to deal with the server returning empty status lines! Fun!
    """
    _MAXLINE = 65536
    line = unicode(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
    if len(line) > _MAXLINE:
        raise LineTooLong("status line")
    if self.debuglevel > 0:
        print("reply:", repr(line))
    if not line:
        # Presumably, the server closed the connection before
        # sending a valid response.
        #raise BadStatusLine(line)
        # HA!
        line = 'HTTP/1.0 200 OK'
    try:
        version, status, reason = line.split(None, 2)
    except ValueError:
        try:
            version, status = line.split(None, 1)
            reason = ""
        except ValueError:
            # empty version will cause next test to fail.
            version = ""
    if not version.startswith("HTTP/"):
        self.close()
        raise BadStatusLine(line)

    # The status code is a three-digit number
    try:
        status = int(status)
        if status < 100 or status > 999:
            raise BadStatusLine(line)
    except ValueError:
        raise BadStatusLine(line)
    return version, status, reason

HTTPResponse._read_status = monkey_patch

last_run = datetime.strptime(scraperwiki.sqlite.get_var('last_run', '2011-12-20'), '%Y-%m-%d')

# Always go back ten days since we don't know how quickly updates come in
start_date = (last_run - timedelta(days=10)).strftime('%m/%d/%Y')
print 'Scraping cases on or after: %s' % start_date

for letter in string.lowercase:
    print 'Starting letter: %s' % letter
    index = 1

    while True:
        print 'Page index: %i' % index
        page = scraperwiki.scrape('http://judicial.smith-county.com/JudicialSearch/Scripts/UVlink.dll/smith_2/WEBSERV/CriminalSearch', { 'key': letter, 'startdate': start_date, 'startindex': index })

        if 'Sorry' in page:
            break

        root = fromstring(page)

        try:
            main_table = root.cssselect('body > div > table')[0]
        except IndexError:
            print 'Unparseable result, wtf?'
            break

        count = 0

        # Root tag gets included without the "div >" part
        for table in main_table.cssselect('div > table'):
            try:
                case = {}
                trs = table.cssselect('tr')
                
                tds = trs[0].cssselect('td')
                case['view_url'] = tds[1].cssselect('a')[0].get('href')
                case['cause_number'] = tds[1].text_content()
                try:
                    case['date_filed'] = datetime.strptime(tds[3].text_content(), '%m/%d/%Y').date()
                except ValueError:
                    pass
                offense = tds[5].text_content()

                crime_date_match = re.match('(\d{2}/\d{2}/\d{2})-(.*)$', offense)

                if crime_date_match:
                    try:
                        case['crime_date'] = datetime.strptime(crime_date_match.group(1), '%m/%d/%y').date()
                    except ValueError:
                        pass
                    case['offense'] = crime_date_match.group(2)
                else:
                    case['offense'] = offense
            
                tds = trs[1].cssselect('td')
                case['defendant_name'], defendant_birthdate = tds[1].text_content().split(' - ')
                try:
                    case['defendant_birthdate'] = datetime.strptime(defendant_birthdate, '%m/%d/%Y').date()
                except ValueError:
                    pass
                case['court'] = tds[3].text_content()
                
                tds = trs[2].cssselect('td')
                case['disposed'] = tds[3].text_content()
                case['degree'] = tds[5].text_content()
    
                tds = trs[3].cssselect('td')
                case['warrant_status'] = tds[3].text_content()
                case['attorney'] = tds[5].text_content()

                scraperwiki.sqlite.save(unique_keys=['cause_number'], data=case)
                count += 1
            except:
                print_exc()

        if 'View the remaining selections' not in page:
            break

        index += 10

today = date.today()
scraperwiki.sqlite.save_var('last_run', today.strftime('%Y-%m-%d'))