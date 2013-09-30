# Designed to be able to be the base for 
# extracting entries from any Socrata site

import lxml.html
import scraperwiki

sites = dict(
    #data_gov='http://explore.data.gov/catalog/raw/',
    #new_york='http://nycopendata.socrata.com/browse',
    #baltimore='http://data.baltimorecity.gov/browse',
    #kenya='http://opendata.go.ke/browse',
    chicago='http://data.cityofchicago.org/browse',
    )

def GET(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

def find_last_page(page):
    elems = page.cssselect('a.lastLink')
    last = elems[0].attrib['href']
    last = last.rsplit('=')[-1]
    last = int(last)
    return last

def process_page(url):
    print 'EXTRACTING FROM', url
    page = GET(url)
    base = url.replace('//', '!!').split('/')[0].replace('!!', '//')

    for row in page.cssselect('tr.local'):
        socrata_id = row.attrib['data-viewid']
        description = row.cssselect('div.description')[0].text
        try:
            _name= row.cssselect('a.name')[0]
        except IndexError:
            _name = row.cssselect('a.nameLink')[0]


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
            scraperwiki.sqlite.save(['socrata_id'], entries, table_name=name)
            scraperwiki.sqlite.save(['socrata_id', 'tag'], tags, table_name='tags')


go(sites)# Designed to be able to be the base for 
# extracting entries from any Socrata site

import lxml.html
import scraperwiki

sites = dict(
    #data_gov='http://explore.data.gov/catalog/raw/',
    #new_york='http://nycopendata.socrata.com/browse',
    #baltimore='http://data.baltimorecity.gov/browse',
    #kenya='http://opendata.go.ke/browse',
    chicago='http://data.cityofchicago.org/browse',
    )

def GET(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

def find_last_page(page):
    elems = page.cssselect('a.lastLink')
    last = elems[0].attrib['href']
    last = last.rsplit('=')[-1]
    last = int(last)
    return last

def process_page(url):
    print 'EXTRACTING FROM', url
    page = GET(url)
    base = url.replace('//', '!!').split('/')[0].replace('!!', '//')

    for row in page.cssselect('tr.local'):
        socrata_id = row.attrib['data-viewid']
        description = row.cssselect('div.description')[0].text
        try:
            _name= row.cssselect('a.name')[0]
        except IndexError:
            _name = row.cssselect('a.nameLink')[0]


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
            scraperwiki.sqlite.save(['socrata_id'], entries, table_name=name)
            scraperwiki.sqlite.save(['socrata_id', 'tag'], tags, table_name='tags')


go(sites)