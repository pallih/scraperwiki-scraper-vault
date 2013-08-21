import lxml.html           
import scraperwiki
from itertools import islice, chain

def batch(iterable, size):
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, size)
        yield chain([batchiter.next()], batchiter)


html = scraperwiki.scrape('http://drupal.org/project/usage')
page = lxml.html.fromstring(html)

table = page.cssselect('#project-usage-all-projects')[0]
for row in table.cssselect('tbody tr'):
    data = {}
    data['pid']      = row[0].text_content()
    data['name']     = row[1].text_content()
    data['current']  = row[2].text_content()
    data['previous'] = row[3].text_content()
    data['oldest']   = row[4].text_content()
    scraperwiki.sqlite.save( ['pid'], data)