import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time

dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'financial-transactions-data-derbyshire-mental-health-services-trust'
url = 'http://www.derbyshirementalhealthservices.nhs.uk/about-us/foi/transparency-spending/'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)

table_exists = len(scraperwiki.sqlite.show_tables()) > 0


# Check all the links for those ending with .csv
for obj in page.cssselect('.oLinkAssetXls'):
    href = obj.get('href')
    text = obj.text_content() # title is inconsistent

    if not text:
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

dataset = 'financial-transactions-data-derbyshire-mental-health-services-trust'
url = 'http://www.derbyshirementalhealthservices.nhs.uk/about-us/foi/transparency-spending/'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)

table_exists = len(scraperwiki.sqlite.show_tables()) > 0


# Check all the links for those ending with .csv
for obj in page.cssselect('.oLinkAssetXls'):
    href = obj.get('href')
    text = obj.text_content() # title is inconsistent

    if not text:
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

dataset = 'financial-transactions-data-derbyshire-mental-health-services-trust'
url = 'http://www.derbyshirementalhealthservices.nhs.uk/about-us/foi/transparency-spending/'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)

table_exists = len(scraperwiki.sqlite.show_tables()) > 0


# Check all the links for those ending with .csv
for obj in page.cssselect('.oLinkAssetXls'):
    href = obj.get('href')
    text = obj.text_content() # title is inconsistent

    if not text:
        continue

    full_url = urlparse.urljoin(url, href)
    dguclient.save_resource_row(dataset, text, full_url, source=url)




