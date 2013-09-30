"""
Scrapes the website of the FDIC for meetings related to the
implementation of Dodd-Frank. It outputs data in a format that is more
easily consumable for our Dodd-Frank Tracker[1]. The data provided here
is still pretty raw, but easily consumable by other tools.

[1] http://reporting.sunlightfoundation.com/doddfrank/
"""

import csv
import re
import urllib2
import scraperwiki

from dateutil.parser import parse as dateparse

def scrape():
    meetings = scrape_csv_file()
    save_meetings(meetings)


def scrape_csv_file():
    url = 'http://www.fdic.gov/regulations/meetings/vlog.csv'
    reader = csv.DictReader(urllib2.urlopen(url))
    return [{
        'staff': parse_staff(row['Person Visited']),
        'meeting_time': dateparse(row['Date']),
        'disclosure_time': dateparse(row['Creation Date']),
        'organizations': parse_organizations(row['Affiliation']),
        'visitors': parse_visitors(row['Visitor']),
        'material_provided': row['Material Provided'],
        'description': row['Issues Discussed'].replace(':', '; ')
    }
    for row in reader
    if row['Status'].strip() == 'PUBLISH']

def reversed_name(last_first):
    if ',' in last_first:
        name_parts = reversed([w.strip() for w in last_first.split(',')])
        first_last = ' '.join(name_parts)
        return first_last
    else:
        return last_first
    
def parse_staff(staff):
    return [{'name': reversed_name(last_first),
             'org': 'FDIC'}
            for last_first in staff.split(':')]

def parse_visitors(visitors):
    visitors = [x.strip() for x in visitors.split(':')
                    if x != 'Multiple, Visitors'
                    and x != 'Multiple , Visitors']
    visitor_orgs = []
    for visitor in visitors:
        regex = re.compile(r'\((?P<org>.*?)\)')
        m = regex.search(visitor)
        if m:
            name = regex.sub('', visitor).strip()
            org = m.groups('org')[0]
            visitor_orgs.append({'name': reversed_name(name),
                                 'org': org, })
        else:
            visitor_orgs.append({'name': reversed_name(visitor),
                                 'org': None, })
    return visitor_orgs

def parse_organizations(organizations):
    organizations = re.sub(r', (Inc|LLP|LLC)', r' \1', organizations)
    organizations = re.split(r'(?:;|,|/)', organizations)
    return [x.strip() for x in organizations]


def save_meetings(meetings):
    meeting_records = []
    organization_records = []
    attendee_records = []

    for meeting in meetings:
        meeting_records.append({
            'Date': meeting['meeting_time'],
            'Topics': meeting['description'],
            'Disclosed': meeting['disclosure_time']
        })

        unique_org_names = set()

        for org in meeting['organizations']:
            unique_org_names.add(org)
        
        for staff in meeting['staff']:
            attendee_records.append({
                'Date': meeting['meeting_time'],
                'Topics': meeting['description'],
                'Disclosed': meeting['disclosure_time'],
                'Attendee': staff['name'],
                'Org': staff['org']
            })
            unique_org_names.add(staff['org'])

        for visitor in meeting['visitors']:
            attendee_records.append({
                'Date': meeting['meeting_time'],
                'Topics': meeting['description'],
                'Disclosed': meeting['disclosure_time'],
                'Attendee': visitor['name'],
                'Org': visitor['org'] or ''
            })
            if visitor['org']:
                unique_org_names.add(visitor['org'])

        for org in unique_org_names:
            organization_records.append({
                'Date': meeting['meeting_time'],
                'Topics': meeting['description'],
                'Disclosed': meeting['disclosure_time'],
                'Org': org
            })

    scraperwiki.sqlite.save(table_name="meetings",
                            unique_keys=['Date',
                                         'Topics',
                                         'Disclosed'],
                            data=meeting_records)

    scraperwiki.sqlite.save(table_name="attendees",
                            unique_keys=['Date',
                                         'Topics',
                                         'Disclosed',
                                         'Attendee'],
                            data=attendee_records)

    scraperwiki.sqlite.save(table_name="organizations",
                            unique_keys=['Date',
                                         'Topics',
                                         'Disclosed',
                                         'Org'],
                            data=organization_records)
    
if __name__ == "__main__":
    scrape()

if __name__ == "scraper":
    scrape()

"""
Scrapes the website of the FDIC for meetings related to the
implementation of Dodd-Frank. It outputs data in a format that is more
easily consumable for our Dodd-Frank Tracker[1]. The data provided here
is still pretty raw, but easily consumable by other tools.

[1] http://reporting.sunlightfoundation.com/doddfrank/
"""

import csv
import re
import urllib2
import scraperwiki

from dateutil.parser import parse as dateparse

def scrape():
    meetings = scrape_csv_file()
    save_meetings(meetings)


def scrape_csv_file():
    url = 'http://www.fdic.gov/regulations/meetings/vlog.csv'
    reader = csv.DictReader(urllib2.urlopen(url))
    return [{
        'staff': parse_staff(row['Person Visited']),
        'meeting_time': dateparse(row['Date']),
        'disclosure_time': dateparse(row['Creation Date']),
        'organizations': parse_organizations(row['Affiliation']),
        'visitors': parse_visitors(row['Visitor']),
        'material_provided': row['Material Provided'],
        'description': row['Issues Discussed'].replace(':', '; ')
    }
    for row in reader
    if row['Status'].strip() == 'PUBLISH']

def reversed_name(last_first):
    if ',' in last_first:
        name_parts = reversed([w.strip() for w in last_first.split(',')])
        first_last = ' '.join(name_parts)
        return first_last
    else:
        return last_first
    
def parse_staff(staff):
    return [{'name': reversed_name(last_first),
             'org': 'FDIC'}
            for last_first in staff.split(':')]

def parse_visitors(visitors):
    visitors = [x.strip() for x in visitors.split(':')
                    if x != 'Multiple, Visitors'
                    and x != 'Multiple , Visitors']
    visitor_orgs = []
    for visitor in visitors:
        regex = re.compile(r'\((?P<org>.*?)\)')
        m = regex.search(visitor)
        if m:
            name = regex.sub('', visitor).strip()
            org = m.groups('org')[0]
            visitor_orgs.append({'name': reversed_name(name),
                                 'org': org, })
        else:
            visitor_orgs.append({'name': reversed_name(visitor),
                                 'org': None, })
    return visitor_orgs

def parse_organizations(organizations):
    organizations = re.sub(r', (Inc|LLP|LLC)', r' \1', organizations)
    organizations = re.split(r'(?:;|,|/)', organizations)
    return [x.strip() for x in organizations]


def save_meetings(meetings):
    meeting_records = []
    organization_records = []
    attendee_records = []

    for meeting in meetings:
        meeting_records.append({
            'Date': meeting['meeting_time'],
            'Topics': meeting['description'],
            'Disclosed': meeting['disclosure_time']
        })

        unique_org_names = set()

        for org in meeting['organizations']:
            unique_org_names.add(org)
        
        for staff in meeting['staff']:
            attendee_records.append({
                'Date': meeting['meeting_time'],
                'Topics': meeting['description'],
                'Disclosed': meeting['disclosure_time'],
                'Attendee': staff['name'],
                'Org': staff['org']
            })
            unique_org_names.add(staff['org'])

        for visitor in meeting['visitors']:
            attendee_records.append({
                'Date': meeting['meeting_time'],
                'Topics': meeting['description'],
                'Disclosed': meeting['disclosure_time'],
                'Attendee': visitor['name'],
                'Org': visitor['org'] or ''
            })
            if visitor['org']:
                unique_org_names.add(visitor['org'])

        for org in unique_org_names:
            organization_records.append({
                'Date': meeting['meeting_time'],
                'Topics': meeting['description'],
                'Disclosed': meeting['disclosure_time'],
                'Org': org
            })

    scraperwiki.sqlite.save(table_name="meetings",
                            unique_keys=['Date',
                                         'Topics',
                                         'Disclosed'],
                            data=meeting_records)

    scraperwiki.sqlite.save(table_name="attendees",
                            unique_keys=['Date',
                                         'Topics',
                                         'Disclosed',
                                         'Attendee'],
                            data=attendee_records)

    scraperwiki.sqlite.save(table_name="organizations",
                            unique_keys=['Date',
                                         'Topics',
                                         'Disclosed',
                                         'Org'],
                            data=organization_records)
    
if __name__ == "__main__":
    scrape()

if __name__ == "scraper":
    scrape()

