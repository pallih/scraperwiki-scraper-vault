# MPSEB: Import data
# ------------------

# MPSEB publishes [Daily Power Reports](http://www.mp.gov.in/energy/mpseb/DPR/daily-dpr.htm).
# This program extracts these and saves them as CSV files

import re
import scraperwiki
from lxml import etree

def get_dpr_exec_summary(url):
    # The DRP URL looks like this:  http://www.mp.gov.in/energy/mpseb/DPR/dpr-100211.htm
    # Exec summary is on 1st sheet: http://www.mp.gov.in/energy/mpseb/DPR/dpr-100211_files/sheet001.htm
    exec_summary_url = url.replace('.htm', '_files/sheet001.htm')
    date = '20' + url[-6:-4] + '-' + url[-8:-6] + '-' + url[-10:-8]
    print exec_summary_url
    html = scraperwiki.scrape(exec_summary_url)
    tree = etree.HTML(html)
    out = []
    for tr in tree.xpath('.//tr'):
        row = [td.text for td in tr.xpath('.//td')]
        # Just pick up the rows that have a "MAX." in the second column, and are at least 6 cells wide
        # This appears to be the structure for data that has a MIN and a MAX
        if len(row) >= 6 and row[2] == 'MAX.':
            key = re.sub(r'\s+', ' ', row[1]).lower()
            scraperwiki.datastore.save(unique_keys=['date','sheet','key'], data={
                'date':date,
                'sheet':'1',
                'key': key,
                'min': re.sub(r'[^0-9]', '', row[3]),
                'max': re.sub(r'[^0-9]', '', row[6]),
            })

def get_dpr():
    url = 'http://www.mp.gov.in/energy/mpseb/DPR/daily-dpr.htm'
    print url
    html = scraperwiki.scrape(url)
    tree = etree.HTML(html)
    # Currently, all links at this URL are a DPR, so just crawl them
    for a in tree.xpath('.//a'):
        dpr_url = 'http://www.mp.gov.in/energy/mpseb/DPR/' + a.get('href')
        # Don't re-crawl
        if not scraperwiki.metadata.get(dpr_url):
            try:
                get_dpr_exec_summary(dpr_url)
                scraperwiki.metadata.save(dpr_url, True)
            except Exception, e:
                print dpr_url, e

get_dpr()
# MPSEB: Import data
# ------------------

# MPSEB publishes [Daily Power Reports](http://www.mp.gov.in/energy/mpseb/DPR/daily-dpr.htm).
# This program extracts these and saves them as CSV files

import re
import scraperwiki
from lxml import etree

def get_dpr_exec_summary(url):
    # The DRP URL looks like this:  http://www.mp.gov.in/energy/mpseb/DPR/dpr-100211.htm
    # Exec summary is on 1st sheet: http://www.mp.gov.in/energy/mpseb/DPR/dpr-100211_files/sheet001.htm
    exec_summary_url = url.replace('.htm', '_files/sheet001.htm')
    date = '20' + url[-6:-4] + '-' + url[-8:-6] + '-' + url[-10:-8]
    print exec_summary_url
    html = scraperwiki.scrape(exec_summary_url)
    tree = etree.HTML(html)
    out = []
    for tr in tree.xpath('.//tr'):
        row = [td.text for td in tr.xpath('.//td')]
        # Just pick up the rows that have a "MAX." in the second column, and are at least 6 cells wide
        # This appears to be the structure for data that has a MIN and a MAX
        if len(row) >= 6 and row[2] == 'MAX.':
            key = re.sub(r'\s+', ' ', row[1]).lower()
            scraperwiki.datastore.save(unique_keys=['date','sheet','key'], data={
                'date':date,
                'sheet':'1',
                'key': key,
                'min': re.sub(r'[^0-9]', '', row[3]),
                'max': re.sub(r'[^0-9]', '', row[6]),
            })

def get_dpr():
    url = 'http://www.mp.gov.in/energy/mpseb/DPR/daily-dpr.htm'
    print url
    html = scraperwiki.scrape(url)
    tree = etree.HTML(html)
    # Currently, all links at this URL are a DPR, so just crawl them
    for a in tree.xpath('.//a'):
        dpr_url = 'http://www.mp.gov.in/energy/mpseb/DPR/' + a.get('href')
        # Don't re-crawl
        if not scraperwiki.metadata.get(dpr_url):
            try:
                get_dpr_exec_summary(dpr_url)
                scraperwiki.metadata.save(dpr_url, True)
            except Exception, e:
                print dpr_url, e

get_dpr()
