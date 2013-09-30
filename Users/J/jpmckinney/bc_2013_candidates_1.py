import scraperwiki
import csv
import json
import re

SOURCE_URL = 'https://docs.google.com/spreadsheet/pub?key=0Ah9_k4AYPzqCdHIxTFdPVkEtYVd3dXd6Y2c0X3FJT3c&single=true&gid=0&output=csv'
ELECTED_OFFICE = 'MLA'

def transform_key(k):
    k = k.lower().strip()
    k = re.sub(r'[^a-z0-9_ ]', '', k)
    k = k.replace(' ', '_')
    return ALTERNATE_FIELD_NAMES.get(k, k)

STANDARD_KEYS = set(('name', 'district_name', 'elected_office', 'source_url',
            'first_name', 'last_name', 'party_name', 'email', 'url', 'personal_url',
            'photo_url', 'gender', 'incumbent'))

ALTERNATE_FIELD_NAMES = {
    'full_name': 'name',
    'postal_address': 'postal'
}


def process_row(source):
    row = {
        'offices': [],
        'extra': {},
        'source_url': SOURCE_URL,
        'elected_office': ELECTED_OFFICE
    }
    for k, v in source.items():
        v = v.strip()
        if not v:
            continue
        office_match = re.search(r'^Office (\d): ', k)
        if office_match:
            office_num = int(office_match.group(1))
            while office_num > len(row['offices']):
                row['offices'].append({})
            k = transform_key(k[10:])
            row['offices'][office_num - 1][k] = v
            continue
        k = transform_key(k)
        if k in STANDARD_KEYS:
            row[k] = v
        else:
            row['extra'][k] = v

    row['offices'] = json.dumps(row['offices'])
    row['extra'] = json.dumps(row['extra'])

    unique_keys = set(('name', 'district_name', 'party_name')).intersection(set(row.keys()))

    scraperwiki.sqlite.save(list(unique_keys), data=row)

def main():
    data = scraperwiki.scrape(SOURCE_URL)
    reader = csv.DictReader(data.splitlines(True))
    for row in reader:
        process_row(row)

scraperwiki.sqlite.execute('DROP TABLE IF EXISTS swdata;')
main()




            

import scraperwiki
import csv
import json
import re

SOURCE_URL = 'https://docs.google.com/spreadsheet/pub?key=0Ah9_k4AYPzqCdHIxTFdPVkEtYVd3dXd6Y2c0X3FJT3c&single=true&gid=0&output=csv'
ELECTED_OFFICE = 'MLA'

def transform_key(k):
    k = k.lower().strip()
    k = re.sub(r'[^a-z0-9_ ]', '', k)
    k = k.replace(' ', '_')
    return ALTERNATE_FIELD_NAMES.get(k, k)

STANDARD_KEYS = set(('name', 'district_name', 'elected_office', 'source_url',
            'first_name', 'last_name', 'party_name', 'email', 'url', 'personal_url',
            'photo_url', 'gender', 'incumbent'))

ALTERNATE_FIELD_NAMES = {
    'full_name': 'name',
    'postal_address': 'postal'
}


def process_row(source):
    row = {
        'offices': [],
        'extra': {},
        'source_url': SOURCE_URL,
        'elected_office': ELECTED_OFFICE
    }
    for k, v in source.items():
        v = v.strip()
        if not v:
            continue
        office_match = re.search(r'^Office (\d): ', k)
        if office_match:
            office_num = int(office_match.group(1))
            while office_num > len(row['offices']):
                row['offices'].append({})
            k = transform_key(k[10:])
            row['offices'][office_num - 1][k] = v
            continue
        k = transform_key(k)
        if k in STANDARD_KEYS:
            row[k] = v
        else:
            row['extra'][k] = v

    row['offices'] = json.dumps(row['offices'])
    row['extra'] = json.dumps(row['extra'])

    unique_keys = set(('name', 'district_name', 'party_name')).intersection(set(row.keys()))

    scraperwiki.sqlite.save(list(unique_keys), data=row)

def main():
    data = scraperwiki.scrape(SOURCE_URL)
    reader = csv.DictReader(data.splitlines(True))
    for row in reader:
        process_row(row)

scraperwiki.sqlite.execute('DROP TABLE IF EXISTS swdata;')
main()




            

