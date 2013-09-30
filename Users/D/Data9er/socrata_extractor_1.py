# Designed to be able to be the base for 
# extracting entries from any Socrata site

from lxml import html
from scraperwiki import scrape, sqlite

sites = dict(
    socrata_com='http://opendata.socrata.com'
    )

def GET(url):
    return html.parse(url)

def find_last_page(page):
    elems = page.getroot().cssselect('a.lastLink')
    last = elems[0].attrib['href']
    last = last.rsplit('=')[-1]
    last = int(last)
    print last
    return last

def process_page(url):
    print 'EXTRACTING FROM', url
    page = GET(url)
    base = url.replace('//', '!!').split('/')[0].replace('!!', '//')

    for row in page.getroot().cssselect('tr.local'):
        socrata_id = row.attrib['data-viewid']
        description = row.cssselect('div.description')[0].text
        _name= row.cssselect('a.name')[0]
        name, url = _name.text, base + _name.attrib['href']
        try:
            category = row.cssselect('span.category')[0].text
        except IndexError:
            category = None
        try:
            tags = row.cssselect('span.tags')[0].text.strip().split(', ')
        except IndexError:
            tags = []
        yield dict(socrata_id=socrata_id,
                   description=description,
                   name=name,
                   url=url,
                   category=category,
                   tags=tags)

def go(sites=sites):
    for name, url in sites.iteritems():
        root = GET(url)
        for i in range(1, find_last_page(root)+1):
            entries = []
            tags = []
            for entry in process_page(url + '?&page=' + str(i)):
                print entry
                _tags = [dict(socrata_id=entry['socrata_id'], tag=tag) for tag in entry['tags']]
                if _tags:
                    tags.extend(_tags)
                    entry['tags'] = ', '.join(entry['tags'])
                else:
                    entry['tags'] = None
                entries.append(entry)
            sqlite.save(['socrata_id'], entries, table_name=name)
            sqlite.save(['socrata_id', 'tag'], tags, table_name='tags')

go(sites)# Designed to be able to be the base for 
# extracting entries from any Socrata site

from lxml import html
from scraperwiki import scrape, sqlite

sites = dict(
    socrata_com='http://opendata.socrata.com'
    )

def GET(url):
    return html.parse(url)

def find_last_page(page):
    elems = page.getroot().cssselect('a.lastLink')
    last = elems[0].attrib['href']
    last = last.rsplit('=')[-1]
    last = int(last)
    print last
    return last

def process_page(url):
    print 'EXTRACTING FROM', url
    page = GET(url)
    base = url.replace('//', '!!').split('/')[0].replace('!!', '//')

    for row in page.getroot().cssselect('tr.local'):
        socrata_id = row.attrib['data-viewid']
        description = row.cssselect('div.description')[0].text
        _name= row.cssselect('a.name')[0]
        name, url = _name.text, base + _name.attrib['href']
        try:
            category = row.cssselect('span.category')[0].text
        except IndexError:
            category = None
        try:
            tags = row.cssselect('span.tags')[0].text.strip().split(', ')
        except IndexError:
            tags = []
        yield dict(socrata_id=socrata_id,
                   description=description,
                   name=name,
                   url=url,
                   category=category,
                   tags=tags)

def go(sites=sites):
    for name, url in sites.iteritems():
        root = GET(url)
        for i in range(1, find_last_page(root)+1):
            entries = []
            tags = []
            for entry in process_page(url + '?&page=' + str(i)):
                print entry
                _tags = [dict(socrata_id=entry['socrata_id'], tag=tag) for tag in entry['tags']]
                if _tags:
                    tags.extend(_tags)
                    entry['tags'] = ', '.join(entry['tags'])
                else:
                    entry['tags'] = None
                entries.append(entry)
            sqlite.save(['socrata_id'], entries, table_name=name)
            sqlite.save(['socrata_id', 'tag'], tags, table_name='tags')

go(sites)