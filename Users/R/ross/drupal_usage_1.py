import re
import lxml.html           
import scraperwiki
from itertools import islice, chain

def batch(iterable, size):
    # This is just a utility function so we can grab a part of the iterator
    # at a time, rather than saving a single row to the database, we'll save lots
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, size)
        yield chain([batchiter.next()], batchiter)

print 'Fetching page'
html = scraperwiki.scrape('http://drupal.org/project/usage')
print "HTML is %d in size" % (len(html),)

page = lxml.html.fromstring(html)

# Make sure we remove any ,
to_num = lambda x: int(re.subn(',', '', x)[0])

table = page.cssselect('#project-usage-all-projects')[0]
for rows in batch(table.cssselect('tbody tr'), 50):
    lst = []
    for row in rows:
        data = {}
        data['id']      = int(row[0].text_content())
        data['name']     = row[1].text_content()
        data['current']  = to_num(row[2].text_content())
        data['previous'] = to_num(row[3].text_content())
        data['oldest']   = to_num(row[4].text_content())
        lst.append(data)
    scraperwiki.sqlite.save( ['id'], lst)import re
import lxml.html           
import scraperwiki
from itertools import islice, chain

def batch(iterable, size):
    # This is just a utility function so we can grab a part of the iterator
    # at a time, rather than saving a single row to the database, we'll save lots
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, size)
        yield chain([batchiter.next()], batchiter)

print 'Fetching page'
html = scraperwiki.scrape('http://drupal.org/project/usage')
print "HTML is %d in size" % (len(html),)

page = lxml.html.fromstring(html)

# Make sure we remove any ,
to_num = lambda x: int(re.subn(',', '', x)[0])

table = page.cssselect('#project-usage-all-projects')[0]
for rows in batch(table.cssselect('tbody tr'), 50):
    lst = []
    for row in rows:
        data = {}
        data['id']      = int(row[0].text_content())
        data['name']     = row[1].text_content()
        data['current']  = to_num(row[2].text_content())
        data['previous'] = to_num(row[3].text_content())
        data['oldest']   = to_num(row[4].text_content())
        lst.append(data)
    scraperwiki.sqlite.save( ['id'], lst)import re
import lxml.html           
import scraperwiki
from itertools import islice, chain

def batch(iterable, size):
    # This is just a utility function so we can grab a part of the iterator
    # at a time, rather than saving a single row to the database, we'll save lots
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, size)
        yield chain([batchiter.next()], batchiter)

print 'Fetching page'
html = scraperwiki.scrape('http://drupal.org/project/usage')
print "HTML is %d in size" % (len(html),)

page = lxml.html.fromstring(html)

# Make sure we remove any ,
to_num = lambda x: int(re.subn(',', '', x)[0])

table = page.cssselect('#project-usage-all-projects')[0]
for rows in batch(table.cssselect('tbody tr'), 50):
    lst = []
    for row in rows:
        data = {}
        data['id']      = int(row[0].text_content())
        data['name']     = row[1].text_content()
        data['current']  = to_num(row[2].text_content())
        data['previous'] = to_num(row[3].text_content())
        data['oldest']   = to_num(row[4].text_content())
        lst.append(data)
    scraperwiki.sqlite.save( ['id'], lst)