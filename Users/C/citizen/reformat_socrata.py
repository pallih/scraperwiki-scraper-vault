import scraperwiki           
import json
from pprint import pformat

sourcescraper = 'chicago_socrata'

base_api = 'https://data.cityofchicago.org/api/views/{}/rows.{}'

scraperwiki.sqlite.attach(sourcescraper)


data = scraperwiki.sqlite.select(           
    '''* from chicago''')

for ds in data:
    ds['id'] = ds['socrata_id']
    del ds['socrata_id']

    ds['notes'] = ds['description']
    del ds['description']
    if ds['tags'] is not None:
        ds['tags'] = ds['tags'].split(', ')
    ds['title'] = ds['name']

    ds['res_url'] = []

    for i in ['csv', 'json', 'pdf', 'rdf', 'rss', 'xls', 'xlsx', 'xml']:
         ds['res_url'].append(base_api.format(ds['id'], i))

    ds['source'] = 'City of Chicago'
    ds['format'] = ['CSV', 'JSON']


print json.dumps(data)import scraperwiki           
import json
from pprint import pformat

sourcescraper = 'chicago_socrata'

base_api = 'https://data.cityofchicago.org/api/views/{}/rows.{}'

scraperwiki.sqlite.attach(sourcescraper)


data = scraperwiki.sqlite.select(           
    '''* from chicago''')

for ds in data:
    ds['id'] = ds['socrata_id']
    del ds['socrata_id']

    ds['notes'] = ds['description']
    del ds['description']
    if ds['tags'] is not None:
        ds['tags'] = ds['tags'].split(', ')
    ds['title'] = ds['name']

    ds['res_url'] = []

    for i in ['csv', 'json', 'pdf', 'rdf', 'rss', 'xls', 'xlsx', 'xml']:
         ds['res_url'].append(base_api.format(ds['id'], i))

    ds['source'] = 'City of Chicago'
    ds['format'] = ['CSV', 'JSON']


print json.dumps(data)