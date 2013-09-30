import scraperwiki

import re

def get_page():
    url = 'http://www.fec.gov/press/press2011/new_form1dt.shtml'
    return scraperwiki.scrape(url)


def parse_page(page):
    rows = re.findall(r'<tr.*?<\/tr>', page)
    for row in rows:
        yield parse_row(row)


def parse_row(row):
    cells = re.findall(r'<td.*?>(.*?)<\/td>', row)
    fields = ['count', 'committee_id', 'committee_type', 'committee_name', 'filing_date', ]
    data = dict(zip(fields, cells))
    for k, v in data.iteritems():
        data[k] = clean_cell(v)
    return data


def clean_cell(cell):
    return re.sub(r'<\/?(center|a|br).*?>', '', cell)

def _main():
    page = get_page()
    data = parse_page(page)
    for row in data:
        scraperwiki.sqlite.save(unique_keys=['committee_id', ], data=row)


_main()import scraperwiki

import re

def get_page():
    url = 'http://www.fec.gov/press/press2011/new_form1dt.shtml'
    return scraperwiki.scrape(url)


def parse_page(page):
    rows = re.findall(r'<tr.*?<\/tr>', page)
    for row in rows:
        yield parse_row(row)


def parse_row(row):
    cells = re.findall(r'<td.*?>(.*?)<\/td>', row)
    fields = ['count', 'committee_id', 'committee_type', 'committee_name', 'filing_date', ]
    data = dict(zip(fields, cells))
    for k, v in data.iteritems():
        data[k] = clean_cell(v)
    return data


def clean_cell(cell):
    return re.sub(r'<\/?(center|a|br).*?>', '', cell)

def _main():
    page = get_page()
    data = parse_page(page)
    for row in data:
        scraperwiki.sqlite.save(unique_keys=['committee_id', ], data=row)


_main()