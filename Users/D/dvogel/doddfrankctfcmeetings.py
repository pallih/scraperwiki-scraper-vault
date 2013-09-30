# -*- coding: utf-8 -*-

import sys
import re
import time

import requests
import lxml.html
if __name__ == "scraper":
    import scraperwiki

from pprint import pprint
from dateutil.parser import parse as dateparse


FullListUrl = 'http://www.cftc.gov/LawRegulation/DoddFrankAct/ExternalMeetings/index.htm'
RecentListUrl = 'http://www.cftc.gov/LawRegulation/DoddFrankAct/ExternalMeetings/MeetingsAddedinLast7Days/index.htm'


def slurp(url, params={}, method='GET'):
    response = requests.request(method, url, data=params)
    assert response.status_code == 200, 'Unable to retrieve {0}, method {1}, status {2}'.format(url, method, response.status_code)
    return lxml.html.fromstring(response.content)


def scrape(index_url):
    meetings = []

    page = slurp(index_url)
    meeting_urls = parse_index(page)
    for url in meeting_urls:
        meeting_page = slurp(url)
        data = parse_meeting_page(meeting_page)
        data['url'] = url
        meetings.append(data)

    return meetings


def save(meetings):
    organization_names = set()
    meeting_rows = []
    attendee_rows = []
    organization_rows = []
    for m in meetings:
        meeting_rows.append({
            'meeting_time': m['meeting_time'].isoformat(),
            'description': m['description'],
            'topic': '; '.join(m['rulemaking']),
            'url': m['url']
        })

        for a in m['visitors']:
            attendee_rows.append({
                'meeting_time': m['meeting_time'].isoformat(),
                'description': m['description'],
                'topic': '; '.join(m['rulemaking']),
                'url': m['url'],

                'attendee_name': a['name'],
                'attendee_org': a['org'] or '',
            })
            if a['org']:
                organization_names.add(a['org'])

        for staff_name in m['cftc_staff']:
            attendee_rows.append({
                'meeting_time': m['meeting_time'].isoformat(),
                'description': m['description'],
                'topic': '; '.join(m['rulemaking']),
                'url': m['url'],

                'attendee_name': staff_name,
                'attendee_org': 'CFTC',
            })

        for org_name in organization_names:
            organization_rows.append({
                'meeting_time': m['meeting_time'].isoformat(),
                'description': m['description'],
                'topic': '; '.join(m['rulemaking']),
                'url': m['url'],

                'org': org_name,
            })

    scraperwiki.sqlite.save(table_name="meetings",
                            unique_keys=['meeting_time',
                                         'description',
                                         'topic',
                                         'url'],
                            data=meeting_rows)

    scraperwiki.sqlite.save(table_name="attendees",
                            unique_keys=['meeting_time',
                                         'description',
                                         'topic',
                                         'url',
                                         'attendee_name',
                                         'attendee_org'],
                            data=attendee_rows)

    scraperwiki.sqlite.save(table_name="organizations",
                            unique_keys=['meeting_time',
                                         'description',
                                         'topic',
                                         'url',
                                         'org'],
                            data=organization_rows)



def parse_index(page):
    rows = page.cssselect('div.row')
    for row in rows:
        url = row.cssselect('a')[0].attrib['href']
        print url
        yield ('http://www.cftc.gov/%s' % url).replace('../', '')


def parse_meeting_page(doc):
    m = re.search(r'(?P<date>\d\d?\/\d\d?\/\d{4}) (?P<time>\d\d?:\d\d (?:A|P)M)', doc.text_content())
    meeting_time = dateparse(' '.join(m.groups()))

    rows = doc.cssselect('div.row')
    rulemaking, cftc_staff, visitors, organizations = [data_from_row(row) for row in rows[:-1]]
    visitors = parse_visitors(visitors)
    organizations = parse_organizations(organizations)
    description = rows[-1].text_content().strip()
    return {'rulemaking': rulemaking,
            'cftc_staff': cftc_staff,
            'visitors': visitors,
            'organizations': organizations,
            'description': description, 
            'meeting_time': meeting_time,
            }


def parse_visitors(visitors):
    visitor_orgs = []
    for visitor in visitors:
        regex = re.compile(r'\((?P<org>.*?)\)')
        m = regex.search(visitor)
        if m:
            name = regex.sub('', visitor).strip()
            org = m.groups('org')[0]
            visitor_orgs.append({'name': name, 'org': org, })
            continue

        regex = re.compile(r', (?P<org>.*)$')
        m = regex.search(visitor)
        if m:
            name = regex.sub('', visitor).strip()
            org = m.groups('org')[0]
            visitor_orgs.append({'name': name, 'org': org, })
            continue

        regex = re.compile(r' Staff$', re.I)
        m = regex.search(visitor)
        if m:
            org = regex.sub('', visitor).strip()
            visitor_orgs.append({'name': 'Staff', 'org': org, })
            continue

        regex = re.compile(r' – ')
        m = regex.search(visitor)
        if m:
            name, org = regex.split(visitor)
            visitor_orgs.append({'name': name.strip(), 'org': org.strip(), })
            continue

        regex = re.compile(r'-')
        m = regex.search(visitor)
        if m:
            try:
                name, org = regex.split(visitor)
            except ValueError:
                visitor_orgs.append({'name': visitor, 'org': None, })
                continue
            visitor_orgs.append({'name': name.strip(), 'org': org.strip(), })
            continue

        visitor_orgs.append({'name': visitor, 'org': None, })

    if 'Staff' in [x['name'] for x in visitor_orgs]:
        org = [x['org'] for x in visitor_orgs if x['name'] == 'Staff'][0]
        name = [x['name'] for x in visitor_orgs if x['org'] == None][0]
        visitor_orgs = [{'name': name, 'org': org, }, ]

    return visitor_orgs


def parse_organizations(organizations):
    organizations = [x for x in organizations if x.find('including:') == -1]
    return organizations


def data_from_row(row):
    col = row.cssselect('div.column-coltwo')[0]
    return list(col.itertext())



if __name__ == '__main__':
    pprint(scrape(sys.argv[1] if len(sys.argv) > 1 else RecentListUrl))

if __name__ == "scraper":
    save(scrape(RecentListUrl))

# -*- coding: utf-8 -*-

import sys
import re
import time

import requests
import lxml.html
if __name__ == "scraper":
    import scraperwiki

from pprint import pprint
from dateutil.parser import parse as dateparse


FullListUrl = 'http://www.cftc.gov/LawRegulation/DoddFrankAct/ExternalMeetings/index.htm'
RecentListUrl = 'http://www.cftc.gov/LawRegulation/DoddFrankAct/ExternalMeetings/MeetingsAddedinLast7Days/index.htm'


def slurp(url, params={}, method='GET'):
    response = requests.request(method, url, data=params)
    assert response.status_code == 200, 'Unable to retrieve {0}, method {1}, status {2}'.format(url, method, response.status_code)
    return lxml.html.fromstring(response.content)


def scrape(index_url):
    meetings = []

    page = slurp(index_url)
    meeting_urls = parse_index(page)
    for url in meeting_urls:
        meeting_page = slurp(url)
        data = parse_meeting_page(meeting_page)
        data['url'] = url
        meetings.append(data)

    return meetings


def save(meetings):
    organization_names = set()
    meeting_rows = []
    attendee_rows = []
    organization_rows = []
    for m in meetings:
        meeting_rows.append({
            'meeting_time': m['meeting_time'].isoformat(),
            'description': m['description'],
            'topic': '; '.join(m['rulemaking']),
            'url': m['url']
        })

        for a in m['visitors']:
            attendee_rows.append({
                'meeting_time': m['meeting_time'].isoformat(),
                'description': m['description'],
                'topic': '; '.join(m['rulemaking']),
                'url': m['url'],

                'attendee_name': a['name'],
                'attendee_org': a['org'] or '',
            })
            if a['org']:
                organization_names.add(a['org'])

        for staff_name in m['cftc_staff']:
            attendee_rows.append({
                'meeting_time': m['meeting_time'].isoformat(),
                'description': m['description'],
                'topic': '; '.join(m['rulemaking']),
                'url': m['url'],

                'attendee_name': staff_name,
                'attendee_org': 'CFTC',
            })

        for org_name in organization_names:
            organization_rows.append({
                'meeting_time': m['meeting_time'].isoformat(),
                'description': m['description'],
                'topic': '; '.join(m['rulemaking']),
                'url': m['url'],

                'org': org_name,
            })

    scraperwiki.sqlite.save(table_name="meetings",
                            unique_keys=['meeting_time',
                                         'description',
                                         'topic',
                                         'url'],
                            data=meeting_rows)

    scraperwiki.sqlite.save(table_name="attendees",
                            unique_keys=['meeting_time',
                                         'description',
                                         'topic',
                                         'url',
                                         'attendee_name',
                                         'attendee_org'],
                            data=attendee_rows)

    scraperwiki.sqlite.save(table_name="organizations",
                            unique_keys=['meeting_time',
                                         'description',
                                         'topic',
                                         'url',
                                         'org'],
                            data=organization_rows)



def parse_index(page):
    rows = page.cssselect('div.row')
    for row in rows:
        url = row.cssselect('a')[0].attrib['href']
        print url
        yield ('http://www.cftc.gov/%s' % url).replace('../', '')


def parse_meeting_page(doc):
    m = re.search(r'(?P<date>\d\d?\/\d\d?\/\d{4}) (?P<time>\d\d?:\d\d (?:A|P)M)', doc.text_content())
    meeting_time = dateparse(' '.join(m.groups()))

    rows = doc.cssselect('div.row')
    rulemaking, cftc_staff, visitors, organizations = [data_from_row(row) for row in rows[:-1]]
    visitors = parse_visitors(visitors)
    organizations = parse_organizations(organizations)
    description = rows[-1].text_content().strip()
    return {'rulemaking': rulemaking,
            'cftc_staff': cftc_staff,
            'visitors': visitors,
            'organizations': organizations,
            'description': description, 
            'meeting_time': meeting_time,
            }


def parse_visitors(visitors):
    visitor_orgs = []
    for visitor in visitors:
        regex = re.compile(r'\((?P<org>.*?)\)')
        m = regex.search(visitor)
        if m:
            name = regex.sub('', visitor).strip()
            org = m.groups('org')[0]
            visitor_orgs.append({'name': name, 'org': org, })
            continue

        regex = re.compile(r', (?P<org>.*)$')
        m = regex.search(visitor)
        if m:
            name = regex.sub('', visitor).strip()
            org = m.groups('org')[0]
            visitor_orgs.append({'name': name, 'org': org, })
            continue

        regex = re.compile(r' Staff$', re.I)
        m = regex.search(visitor)
        if m:
            org = regex.sub('', visitor).strip()
            visitor_orgs.append({'name': 'Staff', 'org': org, })
            continue

        regex = re.compile(r' – ')
        m = regex.search(visitor)
        if m:
            name, org = regex.split(visitor)
            visitor_orgs.append({'name': name.strip(), 'org': org.strip(), })
            continue

        regex = re.compile(r'-')
        m = regex.search(visitor)
        if m:
            try:
                name, org = regex.split(visitor)
            except ValueError:
                visitor_orgs.append({'name': visitor, 'org': None, })
                continue
            visitor_orgs.append({'name': name.strip(), 'org': org.strip(), })
            continue

        visitor_orgs.append({'name': visitor, 'org': None, })

    if 'Staff' in [x['name'] for x in visitor_orgs]:
        org = [x['org'] for x in visitor_orgs if x['name'] == 'Staff'][0]
        name = [x['name'] for x in visitor_orgs if x['org'] == None][0]
        visitor_orgs = [{'name': name, 'org': org, }, ]

    return visitor_orgs


def parse_organizations(organizations):
    organizations = [x for x in organizations if x.find('including:') == -1]
    return organizations


def data_from_row(row):
    col = row.cssselect('div.column-coltwo')[0]
    return list(col.itertext())



if __name__ == '__main__':
    pprint(scrape(sys.argv[1] if len(sys.argv) > 1 else RecentListUrl))

if __name__ == "scraper":
    save(scrape(RecentListUrl))

