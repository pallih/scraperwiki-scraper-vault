# David Jones, ScraperWiki Limited

import scraperwiki

import cgi
import json
import os
import sys

# To bootstrap the schema.
scraperwiki.sqlite.save(['counter'], dict(counter='dummy',value=0))

def get(counter):
    """Get the value of a counter."""
    value = scraperwiki.sqlite.execute("select value from swdata where counter=?", counter)
    if value['data']:
        value = value['data'][0][0]
    else:
        value = 0
    return value

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

counter = paramdict.get('view', paramdict.get('increment', ''))
if not counter:
    sys.exit(0)

value = get(counter)
if 'view' in paramdict:
    scraperwiki.utils.httpresponseheader('Content-Type', 'text/json')
    print json.dumps(dict(value=value))
    sys.exit(0)

if 'increment' in paramdict:
    value += 1
    scraperwiki.sqlite.save(['counter'], dict(counter=counter, value=value))
