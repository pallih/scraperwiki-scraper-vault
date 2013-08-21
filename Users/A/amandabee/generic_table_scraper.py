import scraperwiki
from bs4 import BeautifulSoup

import string
import urlparse


url = "http://usatoday30.usatoday.com/news/nation/ems-day1-method.htm"

def get_soup(url):
    soup = BeautifulSoup(scraperwiki.scrape(url))
    return soup

# Get a little bit of information about the tables on the page
def table_info(soup):
    tables = soup.find_all('table')
    print 'Tables: ', len(tables)
    for table in tables:
        print table.attrs,
        rows = table.find_all('tr')
        print 'Rows: ', len(rows)
        get_column_names(table)
        #for row in rows:
            #cells = row.find_all('td')
            # print 'Cells: ', len(cells)

# def count_columns(soup)

def get_column_names(table):
    print "trying"
    headers = table.find_all('thead')
    print len(headers)
    if len(headers) == 0:
        header = table.find('tr')
        for cell in header.find_all('td'):
            print cell.get_text()
    elif len(headers) > 1:
        print 'Table has multiple headers:', len(headers)
    else:
        for cell in headers:
            print cell.get_text()

         



table_info(get_soup(url))