import calendar
import datetime
import re
import scraperwiki
import xlrd
from BeautifulSoup import BeautifulSoup

path = {
    'analytical_series': 'http://www.rba.gov.au/statistics/xls/cpi-analytical-series.xls',
    'release_index': 'http://www.abs.gov.au/AUSSTATS/abs@.nsf/second+level+view?ReadForm&prodno=6401.0&tabname=Past%20Future%20Issues',
    'latest_prefix': 'http://www.abs.gov.au/AUSSTATS/abs@.nsf/Latestproducts/6401.0Main%20Features6',
    'latest_suffix': '?opendocument&prodno=6401.0',
}

regex = {
    'latest': '<a [^>]*>Consumer Price Index, Australia (\w{3}) (\d{4}) <b>\(Latest\)</b></a>',
}

def float_or_none(s):
    if s: return float(s)
    else: return None

def expand_table(table):
    l = []
    for year in table:
        for quarter in xrange(1, 5):
            month = quarter * 3
            day = calendar.monthrange(year, month)[1]
            date = datetime.date(year, month, day)
            value = table[year][quarter-1]
            if value is not None:
                l.append((date,value))
    return l

def get_cpi_table():
    d = {}
    release_index = scraperwiki.scrape(path['release_index'])
    latest = re.search(regex['latest'], release_index).groups()
    html = scraperwiki.scrape(path['latest_prefix'] + latest[0] + '%20' + latest[1] + path['latest_suffix'])
    soup = BeautifulSoup(html)
    tables = soup.findAll('table')
    for table in tables:
        rows = table.findAll('tr')
        if 'LONGER TERM SERIES' in rows[0].text:
            for row in rows[5:-1]:
                fields = [field.text.strip() for field in row.findAll('td')]
                year = int(fields.pop(0))
                d[year] = map(float_or_none, fields)
    return expand_table(d)

def get_quarterly_percentage_change():
    d = {}
    xls = scraperwiki.scrape(path['analytical_series'])
    book = xlrd.open_workbook(file_contents=xls)
    sheet = book.sheet_by_index(0)
    for row in xrange(sheet.nrows):
        date_cell = sheet.cell(row, 0)
        value_cell = sheet.cell(row, 5)
        if date_cell.ctype  != xlrd.XL_CELL_DATE or \
           value_cell.ctype != xlrd.XL_CELL_NUMBER:
            continue
        year, month = xlrd.xldate_as_tuple(date_cell.value, book.datemode)[:2]
        quarter = month/3
        value = value_cell.value
        if year not in d:
            d[year] = [None]*4
        d[year][quarter-1] = value
    return expand_table(d)

def merge_tables(*tables):
    d = {}
    for i,table in enumerate(tables):
        for date,value in table:
            if date not in d:
                d[date] = [None]*len(tables)
            d[date][i] = value
    l = d.items()
    l.sort()
    return l

def fill_cpi(table):
    n = 0
    while table[n][1][0] is None:
        n = n + 1
    for i in xrange(n-1, -1, -1):
        cpi,change = table[i+1][1]
        table[i][1][0] = cpi / (1 + change/100)

table = merge_tables(get_cpi_table(), get_quarterly_percentage_change())
fill_cpi(table)
for date,(cpi,change) in table:
    scraperwiki.datastore.save(['date'], {'date':date, 'cpi':round(cpi,1), 'change':change})

import calendar
import datetime
import re
import scraperwiki
import xlrd
from BeautifulSoup import BeautifulSoup

path = {
    'analytical_series': 'http://www.rba.gov.au/statistics/xls/cpi-analytical-series.xls',
    'release_index': 'http://www.abs.gov.au/AUSSTATS/abs@.nsf/second+level+view?ReadForm&prodno=6401.0&tabname=Past%20Future%20Issues',
    'latest_prefix': 'http://www.abs.gov.au/AUSSTATS/abs@.nsf/Latestproducts/6401.0Main%20Features6',
    'latest_suffix': '?opendocument&prodno=6401.0',
}

regex = {
    'latest': '<a [^>]*>Consumer Price Index, Australia (\w{3}) (\d{4}) <b>\(Latest\)</b></a>',
}

def float_or_none(s):
    if s: return float(s)
    else: return None

def expand_table(table):
    l = []
    for year in table:
        for quarter in xrange(1, 5):
            month = quarter * 3
            day = calendar.monthrange(year, month)[1]
            date = datetime.date(year, month, day)
            value = table[year][quarter-1]
            if value is not None:
                l.append((date,value))
    return l

def get_cpi_table():
    d = {}
    release_index = scraperwiki.scrape(path['release_index'])
    latest = re.search(regex['latest'], release_index).groups()
    html = scraperwiki.scrape(path['latest_prefix'] + latest[0] + '%20' + latest[1] + path['latest_suffix'])
    soup = BeautifulSoup(html)
    tables = soup.findAll('table')
    for table in tables:
        rows = table.findAll('tr')
        if 'LONGER TERM SERIES' in rows[0].text:
            for row in rows[5:-1]:
                fields = [field.text.strip() for field in row.findAll('td')]
                year = int(fields.pop(0))
                d[year] = map(float_or_none, fields)
    return expand_table(d)

def get_quarterly_percentage_change():
    d = {}
    xls = scraperwiki.scrape(path['analytical_series'])
    book = xlrd.open_workbook(file_contents=xls)
    sheet = book.sheet_by_index(0)
    for row in xrange(sheet.nrows):
        date_cell = sheet.cell(row, 0)
        value_cell = sheet.cell(row, 5)
        if date_cell.ctype  != xlrd.XL_CELL_DATE or \
           value_cell.ctype != xlrd.XL_CELL_NUMBER:
            continue
        year, month = xlrd.xldate_as_tuple(date_cell.value, book.datemode)[:2]
        quarter = month/3
        value = value_cell.value
        if year not in d:
            d[year] = [None]*4
        d[year][quarter-1] = value
    return expand_table(d)

def merge_tables(*tables):
    d = {}
    for i,table in enumerate(tables):
        for date,value in table:
            if date not in d:
                d[date] = [None]*len(tables)
            d[date][i] = value
    l = d.items()
    l.sort()
    return l

def fill_cpi(table):
    n = 0
    while table[n][1][0] is None:
        n = n + 1
    for i in xrange(n-1, -1, -1):
        cpi,change = table[i+1][1]
        table[i][1][0] = cpi / (1 + change/100)

table = merge_tables(get_cpi_table(), get_quarterly_percentage_change())
fill_cpi(table)
for date,(cpi,change) in table:
    scraperwiki.datastore.save(['date'], {'date':date, 'cpi':round(cpi,1), 'change':change})

