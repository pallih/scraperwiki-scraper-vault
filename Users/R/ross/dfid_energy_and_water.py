"""
Simple scraper for looking for resources on a single page for a single
dataset.  
"""

import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time
dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'dfid-energy-and-water-consumption'
url = 'http://www.ecodriver.uk.com/eCMS/viewfiles.asp?folder=DFID'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)

table_exists = len(scraperwiki.sqlite.show_tables()) > 0

def save_row(text, full_url):
    if table_exists:
        if scraperwiki.sqlite.select("* from data where url=?", full_url):
            return

    headers = {}
    error = ''
    status_code = ''

    try:
        time.sleep(3)  # Let's be nice.
        response = requests.head(full_url)
        headers = response.headers
        status_code = '%s' % response.status_code
    except Exception as e:
        error = str(e)

    size = headers.get('content-length', 0)

    scraperwiki.sqlite.save(['url'], 
        dict(url=full_url, label=text, dataset=dataset, scrape_time=datetime.datetime.now(), 
             headers=json.dumps(headers), error=error, status_code=status_code, format="CSV",
             size=size), 
        table_name="data")


# Check all the links for those ending with .csv
for obj in page.cssselect('a'):
    href = obj.get('href')
    text = obj.text_content()

    if not href.lower().endswith('.csv') or not text:
        continue

    full_url = urlparse.urljoin(url, href)
    dguclient.save_resource_row(dataset, text, full_url,source=url)




"""
Simple scraper for looking for resources on a single page for a single
dataset.  
"""

import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time
dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'dfid-energy-and-water-consumption'
url = 'http://www.ecodriver.uk.com/eCMS/viewfiles.asp?folder=DFID'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)

table_exists = len(scraperwiki.sqlite.show_tables()) > 0

def save_row(text, full_url):
    if table_exists:
        if scraperwiki.sqlite.select("* from data where url=?", full_url):
            return

    headers = {}
    error = ''
    status_code = ''

    try:
        time.sleep(3)  # Let's be nice.
        response = requests.head(full_url)
        headers = response.headers
        status_code = '%s' % response.status_code
    except Exception as e:
        error = str(e)

    size = headers.get('content-length', 0)

    scraperwiki.sqlite.save(['url'], 
        dict(url=full_url, label=text, dataset=dataset, scrape_time=datetime.datetime.now(), 
             headers=json.dumps(headers), error=error, status_code=status_code, format="CSV",
             size=size), 
        table_name="data")


# Check all the links for those ending with .csv
for obj in page.cssselect('a'):
    href = obj.get('href')
    text = obj.text_content()

    if not href.lower().endswith('.csv') or not text:
        continue

    full_url = urlparse.urljoin(url, href)
    dguclient.save_resource_row(dataset, text, full_url,source=url)




"""
Simple scraper for looking for resources on a single page for a single
dataset.  
"""

import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time
dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'dfid-energy-and-water-consumption'
url = 'http://www.ecodriver.uk.com/eCMS/viewfiles.asp?folder=DFID'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)

table_exists = len(scraperwiki.sqlite.show_tables()) > 0

def save_row(text, full_url):
    if table_exists:
        if scraperwiki.sqlite.select("* from data where url=?", full_url):
            return

    headers = {}
    error = ''
    status_code = ''

    try:
        time.sleep(3)  # Let's be nice.
        response = requests.head(full_url)
        headers = response.headers
        status_code = '%s' % response.status_code
    except Exception as e:
        error = str(e)

    size = headers.get('content-length', 0)

    scraperwiki.sqlite.save(['url'], 
        dict(url=full_url, label=text, dataset=dataset, scrape_time=datetime.datetime.now(), 
             headers=json.dumps(headers), error=error, status_code=status_code, format="CSV",
             size=size), 
        table_name="data")


# Check all the links for those ending with .csv
for obj in page.cssselect('a'):
    href = obj.get('href')
    text = obj.text_content()

    if not href.lower().endswith('.csv') or not text:
        continue

    full_url = urlparse.urljoin(url, href)
    dguclient.save_resource_row(dataset, text, full_url,source=url)




