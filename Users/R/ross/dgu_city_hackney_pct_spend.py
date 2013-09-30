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

dataset = 'financial-transactions-data-city_and_hackney_pct'
url = 'http://www.elc.nhs.uk/about-us/finance/transparency-spend/city-and-hackney/'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)


# Check all the links for those ending with .csv
for obj in page.cssselect('a.oAssetAttachmentTitle'):
    href = obj.get('href')
    text = obj.text_content()

    if not text:
        continue

    full_url = urlparse.urljoin(url, href)
    dguclient.save_resource_row(dataset, text, full_url, source=url)



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

dataset = 'financial-transactions-data-city_and_hackney_pct'
url = 'http://www.elc.nhs.uk/about-us/finance/transparency-spend/city-and-hackney/'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)


# Check all the links for those ending with .csv
for obj in page.cssselect('a.oAssetAttachmentTitle'):
    href = obj.get('href')
    text = obj.text_content()

    if not text:
        continue

    full_url = urlparse.urljoin(url, href)
    dguclient.save_resource_row(dataset, text, full_url, source=url)



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

dataset = 'financial-transactions-data-city_and_hackney_pct'
url = 'http://www.elc.nhs.uk/about-us/finance/transparency-spend/city-and-hackney/'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)


# Check all the links for those ending with .csv
for obj in page.cssselect('a.oAssetAttachmentTitle'):
    href = obj.get('href')
    text = obj.text_content()

    if not text:
        continue

    full_url = urlparse.urljoin(url, href)
    dguclient.save_resource_row(dataset, text, full_url, source=url)



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

dataset = 'financial-transactions-data-city_and_hackney_pct'
url = 'http://www.elc.nhs.uk/about-us/finance/transparency-spend/city-and-hackney/'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)


# Check all the links for those ending with .csv
for obj in page.cssselect('a.oAssetAttachmentTitle'):
    href = obj.get('href')
    text = obj.text_content()

    if not text:
        continue

    full_url = urlparse.urljoin(url, href)
    dguclient.save_resource_row(dataset, text, full_url, source=url)



