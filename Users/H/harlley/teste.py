import scraperwiki
from cStringIO import StringIO
from csv import reader

lines = reader(StringIO(scraperwiki.scrape('http://dl.dropbox.com/u/96987/votos_m.csv')))

headings = lines.next()

for line in lines:
    scraperwiki.datastore.save(headings, dict(zip(headings, line)))