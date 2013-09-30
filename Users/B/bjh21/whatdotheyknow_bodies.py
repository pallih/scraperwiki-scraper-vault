import scraperwiki
import csv

# Dummy URL load to give ScraperWiki something to screenshot.
scraperwiki.scrape("http://www.whatdotheyknow.com/body/list/all")

data = scraperwiki.scrape('http://www.whatdotheyknow.com/body/all-authorities.csv')
scraperwiki.sqlite.execute('DELETE FROM swdata')
scraperwiki.sqlite.execute('DELETE FROM tags')
rdr = csv.DictReader(data.splitlines())

tags = []
bodies = []
for row in rdr:
    for tag in row['Tags'].split():
        (tagname, _, value) = tag.partition(':')
        tags += [{ 'Tag': tagname, 'Value': value, 'URL name': row['URL name'] }]
    del row['Tags']
    bodies.append(row)

scraperwiki.sqlite.save(['URL name'], bodies)
scraperwiki.sqlite.save(['Tag', 'Value', 'URL name'], tags,
            table_name = 'tags')

scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS body_byurl ON swdata(`URL name`)')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS body_byname ON swdata(`Name`)')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS tag_bytag ON tags(`Tag`)')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS tag_byurl ON tags(`URL name`)')
scraperwiki.sqlite.execute('ANALYZE')
scraperwiki.sqlite.commit()

import scraperwiki
import csv

# Dummy URL load to give ScraperWiki something to screenshot.
scraperwiki.scrape("http://www.whatdotheyknow.com/body/list/all")

data = scraperwiki.scrape('http://www.whatdotheyknow.com/body/all-authorities.csv')
scraperwiki.sqlite.execute('DELETE FROM swdata')
scraperwiki.sqlite.execute('DELETE FROM tags')
rdr = csv.DictReader(data.splitlines())

tags = []
bodies = []
for row in rdr:
    for tag in row['Tags'].split():
        (tagname, _, value) = tag.partition(':')
        tags += [{ 'Tag': tagname, 'Value': value, 'URL name': row['URL name'] }]
    del row['Tags']
    bodies.append(row)

scraperwiki.sqlite.save(['URL name'], bodies)
scraperwiki.sqlite.save(['Tag', 'Value', 'URL name'], tags,
            table_name = 'tags')

scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS body_byurl ON swdata(`URL name`)')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS body_byname ON swdata(`Name`)')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS tag_bytag ON tags(`Tag`)')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS tag_byurl ON tags(`URL name`)')
scraperwiki.sqlite.execute('ANALYZE')
scraperwiki.sqlite.commit()

