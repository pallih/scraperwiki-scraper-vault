sourcescraper = 'frikanalen_on_twitter_1'
import scraperwiki
scraperwiki.sqlite.attach(sourcescraper)

import cgi, os           
param_hash = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
search = param_hash.get('search', '')
print search
if search:
    search = 'AND text LIKE "%{}%" '.format(search)
data = scraperwiki.sqlite.select(           
    '''* FROM {}.swdata
    WHERE text not like 'RT %'
    {}
    ORDER BY date desc LIMIT 10'''.format(sourcescraper, search)
)
print """skriv ?search=rogaland for å finna alle tweets med det i
"""

for d in data:
    print d['from_user'], d['text'], d['id']