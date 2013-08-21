from datetime import datetime
import json
import sys
import traceback

from dateutil.parser import parse

import scraperwiki

FOIA_CATEGORY = 'FOIA'
DATA_CHICAGO_URL = 'http://data.cityofchicago.org/api/views?category=' + FOIA_CATEGORY
MAPPED_KEYS = { 'due_date': 'date_due',
                '_due_date_': 'date_due',
                'date_recieved': 'date_received',
                'received_date': 'date_received',
                'date_requested': 'date_received',
                '_requestor_name': 'requestor_name',
                'description_of_request': 'description',
                'description_of_request_-_statements_of_financial_interests': 'description',
                'description_of_request_-_other': 'description',
                'description_of_request_-_lobbyists_filings': 'description',
                'description_of_request_': 'description',
                'brief_description_of_records_sought': 'description',
                'institution': 'organization',
               }
TIMESTAMP_KEYS = ['date_due', 'date_received', 'created_at', 'updated_at']

def map_key(k):
    """Map a key to its normalized version."""
    return MAPPED_KEYS.get(k, k)

data = scraperwiki.scrape(DATA_CHICAGO_URL)
jsondata = json.loads(data)

views = [(view['id'], (view['name'].partition('FOIA Request Log - ')[2] or view['name'])) for view in jsondata]

for id, name in views:
    view_url = 'http://data.cityofchicago.org/api/views/%s/rows.json' % id
    
    data = scraperwiki.scrape(view_url)
    jsondata = json.loads(data)
    
    columns = [map_key(column['name'].lower().replace(' ', '_')) for column in jsondata['meta']['view']['columns']]
    columns.insert(0, 'dataset')
    
    for row in jsondata['data']:
        try:
            row.insert(0, name)
            
            record = dict(zip(columns, row))

            if 'requestor_name' not in record:
                record['requestor_name'] = ' '.join(filter(None, [record.get('requestor_first_name'), record.get('requestor_middle_initial'), record.get('requestor_last_name')]))
            
            if record['meta'] == '{\n}':
                del record['meta']

            for key in TIMESTAMP_KEYS:
                if key in record and record[key]:
                    try:
                        record[key] = datetime.fromtimestamp(record[key])
                    except:
                        try:
                            record[key] = parse(record[key])
                        except:
                            print 'Failed to parse date: ', record[key]
            
            scraperwiki.sqlite.save(['id'], record)
        except Exception, e:
            traceback.print_exc()
            print 'Failed to process row: ', row
