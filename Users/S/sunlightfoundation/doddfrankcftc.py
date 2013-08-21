# -*- coding: utf-8 -*-
"""
Scrapes the website of the CFTC for meetings related to the
implementation of Dodd-Frank. It outputs data in a format that is more
easily consumable for our Dodd-Frank Tracker[1]. The data provided here
is still pretty raw, but easily consumable by other tools.

[1] http://reporting.sunlightfoundation.com/doddfrank/
"""

import sys
import re
import time
import datetime
import resource

import requests
import lxml.html
import lxml.etree
import scraperwiki

from pprint import pprint
from copy import deepcopy
from dateutil.parser import parse as dateparse


FullListUrl = 'http://www.cftc.gov/LawRegulation/DoddFrankAct/ExternalMeetings/ExternalMeetingsAll/index.htm'
RecentListUrl = 'http://www.cftc.gov/LawRegulation/DoddFrankAct/ExternalMeetings/MeetingsAddedinLast7Days/index.htm'


class MalformattedMeetingPage(Exception):
    def __init__(self, *args, **kwargs):
        self.context = kwargs.get('context')
        del kwargs['context']
        super(MalformattedMeetingPage, self).__init__(*args, **kwargs)


def slurp(url, params={}, method='GET', retries=2):
    response = requests.request(method, url, data=params, allow_redirects=True)
    print u'{0} {1}'.format(response.status_code, url)
    assert response.status_code == 200, 'Unable to retrieve {0}, method {1}, status {2}'.format(url, method, response.status_code)
    if response.content == '':
        if retries > 0:
            time.sleep(1)
            return slurp(url, params, method, retries-1)
        else:
            raise Exception(u'Empty response from server for {0}'.format(url))

    try:
        return lxml.html.fromstring(response.content)
    except lxml.etree.XMLSyntaxError as e:
        raise MalformattedMeetingPage(context=locals(), 
                                      msg=u'Caught {0} for page {1}'.format(e, url))


def scrape(index_url):
    meetings = []
    
    page = slurp(index_url)
    meeting_urls = list(parse_index(page))

    last_meeting_page = scraperwiki.sqlite.get_var('last_meeting_page', None)
    #if last_meeting_page is not None:
    #    split_pos = meeting_urls.index(last_meeting_page)
    #    if split_pos > 0:
    #        meeting_urls = meeting_urls[split_pos:]

    try:
        for url in meeting_urls:
            try:
                meeting_page = slurp(url)
                data = parse_meeting_page(url, meeting_page)
                data['url'] = deepcopy(url)
                meetings.append(data)
                scraperwiki.sqlite.save_var('last_meeting_page', url)

            except MalformattedMeetingPage as e:
                log_error(url, e)

            except Exception as e:
                log_error(url, e)

    except scraperwiki.CPUTimeExceededError:
        res = resource.getrusage(resource.RUSAGE_SELF)
        print 'Maximum resident size: {0}'.format(res.ru_maxrss)
        print 'CPU user time: {0}'.format(res.ru_utime)
        print 'CPU system time: {0}'.format(res.ru_stime)

    return meetings


def log_error(url, exception):
    print >>sys.stderr, str(exception)
    scraperwiki.sqlite.save(table_name='errors',
                            unique_keys=['url'],
                            data={'url': url,
                                  'description': str(exception),
                                  'context': str(getattr(exception, 'context', '')),
                                  'timestamp': datetime.datetime.now()
                                 })


def save(meetings):
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

        for o in m['organizations']:
            organization_rows.append({
                'url': m['url'],
                'org': o
            })

        for a in m['visitors']:
            attendee_rows.append({
                'url': m['url'],
                'attendee_name': a['name'],
                'attendee_org': a['org'] or '',
            })

        for staff_name in m['cftc_staff']:
            attendee_rows.append({
                'url': m['url'],
                'attendee_name': staff_name,
                'attendee_org': 'CFTC',
            })

    scraperwiki.sqlite.save(table_name="meetings",
                            unique_keys=['meeting_time',
                                         'description',
                                         'topic',
                                         'url'],
                            data=meeting_rows)

    scraperwiki.sqlite.save(table_name="attendees",
                            unique_keys=['url',
                                         'attendee_name',
                                         'attendee_org'],
                            data=attendee_rows)

    scraperwiki.sqlite.save(table_name="organizations",
                            unique_keys=['url',
                                         'org'],
                            data=organization_rows)



def parse_index(page):
    rows = page.cssselect('div.row')
    for row in rows:
        url = row.cssselect('a')[0].attrib['href']
        while url.startswith('/'):
            url = url[1:]
        url = 'http://www.cftc.gov/{0}'.format(url)
        yield (url).replace('../', '')


def strip_whitespace(s, also=u''):
    return s.strip(u' \t\u00a0' + also)


def has_line_breaks(div):
    return len(div.cssselect('br')) > 0


def parse_meeting_page(url, doc):
    m = re.search(r'(?P<date>\d\d?\/\d\d?\/\d{4}) (?P<time>\d\d?:\d\d (?:A|P)M)', doc.text_content())
    meeting_time = dateparse(' '.join(m.groups()))

    (when_div, rulemaking_div, cftc_staff_div,
     visitors_div, organizations_div) = doc.cssselect('div.column-coltwo')

    rulemaking = data_from_row(rulemaking_div)

    try:
        if has_line_breaks(cftc_staff_div):
            cftc_staff_strlist = data_from_row(cftc_staff_div)
            cftc_staff = parse_visitors(cftc_staff_strlist)
        else:
            cftc_staff = parse_inline_visitors_with_regex(cftc_staff_div)
        cftc_staff = [staff['name'] for staff in cftc_staff]
    except MalformattedMeetingPage as e:
        log_error(url, e)

    try:
        if has_line_breaks(visitors_div):
            visitors_strlist = data_from_row(visitors_div)
            visitors = parse_visitors(visitors_strlist)
        else:
            visitors = parse_inline_visitors_with_regex(visitors_div)
    except MalformattedMeetingPage as e:
        log_error(url, e)

    if has_line_breaks(organizations_div):
        organizations = data_from_row(organizations_div)
        organizations = parse_organizations(organizations)
    else:
        organizations = parse_inline_organizations(organizations_div)
    organizations = [strip_whitespace(o, also=u'"') for o in organizations]

    # The grammar for visitor lists is undecidable. The logic we use can sometimes
    # mis-interpret organization names as visitor names if there is only one visitor.
    # E.g. http://www.cftc.gov/LawRegulation/DoddFrankAct/ExternalMeetings/dfmeeting_061912_1720
    #if len(visitors) == 2 and visitors[1]['name'] in organizations:
    #    visitors[0]['org'] = visitors[1]['name']
    #    visitors = [visitors[0]]

    #if len(organizations) == 1:
    #    for visitor in visitors:
    #        if visitor['org'] is None:
    #            visitor['org'] = organizations[0]

    visitors = []
    cftc_staff = []

    description = " ".join([li.text_content() for li in doc.cssselect('div.row ul.text')]).strip()
    return {'rulemaking': rulemaking,
            'cftc_staff': cftc_staff,
            'visitors': visitors,
            'organizations': organizations,
            'description': description,
            'meeting_time': meeting_time,
            }


def split_and_strip(s, sep):
    return [p.strip() for p in sep.split(s)]


CompanySuffixPattern1 = re.compile(r'[,]? (LLC|LLP|MLP|Corp(?:oration)?|Inc(?:orporated)|\bN\.?A\.?\b)[.]?', re.IGNORECASE)
def parse_inline_organizations(organizations_div):
    organizations = organizations_div.text_content()
    organizations = CompanySuffixPattern1.sub(r'', organizations)
    separators = re.compile(ur"(?:\band the\b|\band\b|;|,)", re.IGNORECASE)
    organizations_list = separators.split(organizations)
    return [o for o in (o.strip()
                        for o in organizations_list)
            if re.match(r'^\(.+\)$', o) is None]


def parse_inline_visitors(visitors_elem):
    visitors = visitors_elem.text_content()
    print u'Using parse_inline_visitors for {0!r}'.format(visitors)
    separator = None
    separator_candidates = [u';', u',', u' and ']
    for sep in separator_candidates:
        if sep in visitors:
            separator = sep
            break
    if separator == None:
        # In this case there was no line break because there was only one person listed.
        return parse_visitors(data_from_row(visitors_elem))

    separator_pattern = re.compile(ur'(?:SEP| and )'.replace('SEP', separator))
    names = split_and_strip(visitors, separator_pattern)
    names = [(n[4:] if n.startswith('and ') else n).strip('.')
             for n in names]
    return [{'name': n, 'org': None} for n in names]
    
    
PersonNamePattern = re.compile(ur'(?:(?:(?P<name1>.*?)\s*\((?P<org1>.*?)\)\s*[,;]?\s*)|(?:(?P<name2>.*?)\s*,\s*(?P<org2>.*?)\s*;\s*)|(?:(?P<name3>.*?)\s*[-\u2013]\s*(?P<org3>.*?)\s*[,;]?\s*)|(?:\s*(?P<name4>.+?)\s*(?:,|,? and |;|\.|$)))')
def parse_person_names(text):
    person_list = []
    matches = PersonNamePattern.finditer(text)
    for match in matches:
        m = match.groupdict()
        for n in (1, 2, 3):
            name = m['name' + str(n)]
            org = m['org' + str(n)]
            if name and org:
                person_list.append((name, org))
        if m['name4']:
            person_list.append((m['name4'], None))
    return person_list


def parse_inline_visitors_with_regex(visitors_elem):
    word_count = lambda n: len(re.split(r'\s+', n))
    visitors = visitors_elem.text_content()
    print u'Using parse_inline_visitors_with_regex for {0!r}'.format(visitors)
    visitors = re.compile(ur'^[\w\s]+:').sub('', visitors).strip(' \xa0.')
    matches = PersonNamePattern.finditer(visitors)
    visitor_list = []
    for match in matches:
        m = match.groupdict()
        for n in ['1', '2', '3']:
            if m['org' + n] and m['name' + n]:
                visitor_list.append({'name': m['name' + n],
                                     'org': m['org' + n]})
        if m['name4']:
            if word_count(m['name4']) < 2:
                raise MalformattedMeetingPage(u'Name too short: {0}'.format(m['name4']).encode('utf-8'), context=locals())
            if word_count(m['name4']) > 4:
                raise MalformattedMeetingPage(u'Name has too many words: {0}'.format(m['name4']).encode('utf-8'), context=locals())

            visitor_list.append({'name': m['name4'], 'org': None})

    return visitor_list

def parse_visitors(visitors):
    visitor_orgs = []
    for visitor in visitors:
        regex = re.compile(ur'\((?P<org>.*?)\)')
        m = regex.search(visitor)
        if m:
            name = regex.sub(u'', visitor).strip()
            org = m.groups('org')[0]
            visitor_orgs.append({'name': name, 'org': org, })
            continue

        regex = re.compile(ur', (?P<org>.*)$')
        m = regex.search(visitor)
        if m:
            name = regex.sub('', visitor).strip()
            org = m.groups('org')[0]
            visitor_orgs.append({'name': name, 'org': org, })
            continue

        regex = re.compile(ur' Staff$', re.I)
        m = regex.search(visitor)
        if m:
            org = regex.sub('', visitor).strip()
            visitor_orgs.append({'name': 'Staff', 'org': org, })
            continue

        regex = re.compile(ur' [–\u2013] ')
        m = regex.search(visitor)
        if m:
            name, org = regex.split(visitor)
            visitor_orgs.append({'name': name.strip(), 'org': org.strip(), })
            continue

        # There's some preposterously bad formatting:
        # http://www.cftc.gov/LawRegulation/DoddFrankAct/ExternalMeetings/dfmeeting_041012_1560
        regex = re.compile(ur'[\xa0]')
        m = regex.search(visitor)
        if m:
            name, org = regex.split(visitor)
            name = name.strip()
            org = org.strip()
            if len(name) > 3 and len(org) > 3:
                visitor_orgs.append({'name': name.strip(), 'org': org.strip(), })
                continue

        regex = re.compile(ur'-')
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
    organizations = [x.strip() for x in organizations if x.find('including:') == -1]
    return organizations


def data_from_row(row):
    col = row.cssselect('div.column-coltwo')[0]
    return list(col.itertext())



if __name__ == '__main__':
    pprint(scrape(sys.argv[1] if len(sys.argv) > 1 else FullListUrl))

if __name__ == "scraper":
    save(scrape(FullListUrl))



