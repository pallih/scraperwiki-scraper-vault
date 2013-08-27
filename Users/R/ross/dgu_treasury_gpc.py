import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time

dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'government-procurement-card-spend'
url = 'http://www.hm-treasury.gov.uk/about_transparency_gpc_spend.htm'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)


# Check all the links for those ending with .csv
for obj in page.cssselect('a'):
    href = obj.get('href')
    text = obj.text_content()

    if not text or not href.lower().endswith('.csv'):
        continue

    full_url = urlparse.urljoin(url, href)
    dguclient.save_resource_row(dataset, text, full_url, source=url)



import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time

dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'government-procurement-card-spend'
url = 'http://www.hm-treasury.gov.uk/about_transparency_gpc_spend.htm'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)


# Check all the links for those ending with .csv
for obj in page.cssselect('a'):
    href = obj.get('href')
    text = obj.text_content()

    if not text or not href.lower().endswith('.csv'):
        continue

    full_url = urlparse.urljoin(url, href)
    dguclient.save_resource_row(dataset, text, full_url, source=url)



import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time

dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'government-procurement-card-spend'
url = 'http://www.hm-treasury.gov.uk/about_transparency_gpc_spend.htm'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)


# Check all the links for those ending with .csv
for obj in page.cssselect('a'):
    href = obj.get('href')
    text = obj.text_content()

    if not text or not href.lower().endswith('.csv'):
        continue

    full_url = urlparse.urljoin(url, href)
    dguclient.save_resource_row(dataset, text, full_url, source=url)



