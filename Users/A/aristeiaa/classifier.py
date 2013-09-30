import scraperwiki

import yql
y = yql.Public()
query = 'select * from flickr.photos.search where text="panda" limit 3';
result = y.execute(query)
print resultimport scraperwiki

import yql
y = yql.Public()
query = 'select * from flickr.photos.search where text="panda" limit 3';
result = y.execute(query)
print result