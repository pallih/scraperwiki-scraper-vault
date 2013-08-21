# Taken from example at http://python-yql.org/

import scraperwiki
import yql
y = yql.Public()


query = 'select * from flickr.photos.search where text="Eiffel" limit 40';
result = y.execute(query)

for row in result.rows:
    print row
    scraperwiki.sqlite.save(unique_keys=['id'], data=row)
