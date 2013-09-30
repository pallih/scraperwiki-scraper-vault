#!/usr/bin/env python
import scraperwiki

import urllib2
from bs4 import BeautifulSoup
import string
import urlparse
import re
from datetime import datetime
import csv


def get_soup(url):
    ## strip the unicode spaces here.
    html = urllib2.urlopen(url).read()
    html = re.sub(u'\xa0', ' ', html)
    html = re.sub(u'\xc2', ' ', html)
    soup = BeautifulSoup(html)
    return soup


def date_format(datestring):
    # Assumes dates in the format July 7th, 2013
    try:
        datestrings = datestring.split()
        # Add 2013 to dates w/no year
        if len(datestrings) == 2:
            datestrings.append('2013')
        newstring = datestrings[0], \
                    re.sub('[snthrd, ]', '', datestrings[1]), \
                    datestrings[2]
        newerstring = " ".join(newstring)
        # print newerstring
        better_date = datetime.strptime(newerstring, '%B %d %Y')
        return better_date
    except Exception, e:
        # print datestring
        print 'Funky date: ', datestrings, e


def scrape_toc(soup):
    ## need to rework this so it writes once. 
    fieldorder = ['tocShortcode', 'tocFullname', 'tocBoro', 'tocTime']
    table = soup.find('table', {'class': 'table-classes'})
    for itemAnchor in table.find_all('a'):
        tocShortcode = itemAnchor['href']
        tocFullname = itemAnchor.text
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 3:
            tocBoro = cells[1].get_text()
            tocTime = cells[2].get_text()
            unique_keys = ['tocShortcode']
            data = {
                'tocShortcode': tocShortcode,
                'tocFullname': tocFullname,
                'tocBoro': tocBoro,
                'tocTime': tocTime
            }
        scraperwiki.sqlite.save(unique_keys, data, table_name="toc")


def scrape_classes(soup):
    fieldorder = ['i', 'site', 'site_time', 'better_meeting', 'better_date', \
                  'site_addy', 'meeting', 'date_of_class', 'topic']
    i = 0
    tables = soup.find_all('table', {'class': 'individual'})
    for table in tables:
        site = table.find_previous('h3').get_text()
        site_time = table.find_previous('h5').get_text()
        better_site_time = re.sub(' - Starting Up Again on 9-20-12', '', \
                                    site_time)
        addy = table.find_previous('h5').find_next('p').get_text()
        addy = re.sub('\s+', ' ', addy)
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            try:
                meeting = cells[0].get_text()
                better_mtg = re.sub('[a-zA-Z# ]', '', cells[0].get_text())
                date_of_class = cells[1].get_text()
                better_date = date_format(date_of_class)
                topic = re.sub('\s+', ' ', cells[2].get_text())
                data = {
                    'i': i,
                    'site': site,
                    'site_time': better_site_time,
                    'site_addy': addy,
                    'meeting': meeting,
                    'sortable_meeting_no': better_mtg,
                    'date_of_class': date_of_class,
                    'sortable_date': better_date,
                    'topic': topic
                }
                unique_keys = ['i']
                i += 1
                scraperwiki.sqlite.save(unique_keys, data, table_name="allclasses")
            except Exception, e:
                print site, len(cells), e




### Drop the tables ###
scraperwiki.sqlite.execute('DROP TABLE IF EXISTS allclasses')
#scraperwiki.sqlite.execute('DROP TABLE IF EXISTS  toc')
#scraperwiki.sqlite.execute('DROP TABLE  IF EXISTS classdata')

scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `allclasses` (`i` INTEGER PRIMARY KEY ASC, `site` TEXT, `site_addy` TEXT, `site_time` TEXT, `sortable_date` TEXT, `sortable_meeting_no` INTEGER, `topic` TEXT, `meeting` TEXT, `date_of_class` TEXT);")

### Get new data ### 
soup = get_soup("http://yougottabelieve.org/get-learning/class-details/")
#tocList = scrape_toc(soup)
classList = scrape_classes(soup)


# Saving data:
# unique_keys = [ 'id' ]
# data = { 'id':12, 'name':'violet', 'age':7 }
# scraperwiki.sql.save(unique_keys, data)
#!/usr/bin/env python
import scraperwiki

import urllib2
from bs4 import BeautifulSoup
import string
import urlparse
import re
from datetime import datetime
import csv


def get_soup(url):
    ## strip the unicode spaces here.
    html = urllib2.urlopen(url).read()
    html = re.sub(u'\xa0', ' ', html)
    html = re.sub(u'\xc2', ' ', html)
    soup = BeautifulSoup(html)
    return soup


def date_format(datestring):
    # Assumes dates in the format July 7th, 2013
    try:
        datestrings = datestring.split()
        # Add 2013 to dates w/no year
        if len(datestrings) == 2:
            datestrings.append('2013')
        newstring = datestrings[0], \
                    re.sub('[snthrd, ]', '', datestrings[1]), \
                    datestrings[2]
        newerstring = " ".join(newstring)
        # print newerstring
        better_date = datetime.strptime(newerstring, '%B %d %Y')
        return better_date
    except Exception, e:
        # print datestring
        print 'Funky date: ', datestrings, e


def scrape_toc(soup):
    ## need to rework this so it writes once. 
    fieldorder = ['tocShortcode', 'tocFullname', 'tocBoro', 'tocTime']
    table = soup.find('table', {'class': 'table-classes'})
    for itemAnchor in table.find_all('a'):
        tocShortcode = itemAnchor['href']
        tocFullname = itemAnchor.text
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 3:
            tocBoro = cells[1].get_text()
            tocTime = cells[2].get_text()
            unique_keys = ['tocShortcode']
            data = {
                'tocShortcode': tocShortcode,
                'tocFullname': tocFullname,
                'tocBoro': tocBoro,
                'tocTime': tocTime
            }
        scraperwiki.sqlite.save(unique_keys, data, table_name="toc")


def scrape_classes(soup):
    fieldorder = ['i', 'site', 'site_time', 'better_meeting', 'better_date', \
                  'site_addy', 'meeting', 'date_of_class', 'topic']
    i = 0
    tables = soup.find_all('table', {'class': 'individual'})
    for table in tables:
        site = table.find_previous('h3').get_text()
        site_time = table.find_previous('h5').get_text()
        better_site_time = re.sub(' - Starting Up Again on 9-20-12', '', \
                                    site_time)
        addy = table.find_previous('h5').find_next('p').get_text()
        addy = re.sub('\s+', ' ', addy)
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            try:
                meeting = cells[0].get_text()
                better_mtg = re.sub('[a-zA-Z# ]', '', cells[0].get_text())
                date_of_class = cells[1].get_text()
                better_date = date_format(date_of_class)
                topic = re.sub('\s+', ' ', cells[2].get_text())
                data = {
                    'i': i,
                    'site': site,
                    'site_time': better_site_time,
                    'site_addy': addy,
                    'meeting': meeting,
                    'sortable_meeting_no': better_mtg,
                    'date_of_class': date_of_class,
                    'sortable_date': better_date,
                    'topic': topic
                }
                unique_keys = ['i']
                i += 1
                scraperwiki.sqlite.save(unique_keys, data, table_name="allclasses")
            except Exception, e:
                print site, len(cells), e




### Drop the tables ###
scraperwiki.sqlite.execute('DROP TABLE IF EXISTS allclasses')
#scraperwiki.sqlite.execute('DROP TABLE IF EXISTS  toc')
#scraperwiki.sqlite.execute('DROP TABLE  IF EXISTS classdata')

scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `allclasses` (`i` INTEGER PRIMARY KEY ASC, `site` TEXT, `site_addy` TEXT, `site_time` TEXT, `sortable_date` TEXT, `sortable_meeting_no` INTEGER, `topic` TEXT, `meeting` TEXT, `date_of_class` TEXT);")

### Get new data ### 
soup = get_soup("http://yougottabelieve.org/get-learning/class-details/")
#tocList = scrape_toc(soup)
classList = scrape_classes(soup)


# Saving data:
# unique_keys = [ 'id' ]
# data = { 'id':12, 'name':'violet', 'age':7 }
# scraperwiki.sql.save(unique_keys, data)
