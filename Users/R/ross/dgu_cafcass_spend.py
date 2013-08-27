import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time

dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'financial-transactions-data-cafcass'
url = 'http://www.cafcass.gov.uk/about_cafcass/procurement/transparency_of_contracts/spend_information.aspx'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)

table_exists = len(scraperwiki.sqlite.show_tables()) > 0


# Check all the links for those ending with .csv
for obj in page.cssselect('a'):
    href = obj.get('href')
    text = obj.get('title')

    if not text or not href.lower().endswith('.xls'):
        continue

    fu = urlparse.urljoin(url, href)
    filename = fu.rpartition('/')[2]    
    full_url = 'http://www.cafcass.gov.uk/docs/' + filename

    dguclient.save_resource_row(dataset, text, full_url, fmt='XLS', source=url)




import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time

dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'financial-transactions-data-cafcass'
url = 'http://www.cafcass.gov.uk/about_cafcass/procurement/transparency_of_contracts/spend_information.aspx'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)

table_exists = len(scraperwiki.sqlite.show_tables()) > 0


# Check all the links for those ending with .csv
for obj in page.cssselect('a'):
    href = obj.get('href')
    text = obj.get('title')

    if not text or not href.lower().endswith('.xls'):
        continue

    fu = urlparse.urljoin(url, href)
    filename = fu.rpartition('/')[2]    
    full_url = 'http://www.cafcass.gov.uk/docs/' + filename

    dguclient.save_resource_row(dataset, text, full_url, fmt='XLS', source=url)




import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time

dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'financial-transactions-data-cafcass'
url = 'http://www.cafcass.gov.uk/about_cafcass/procurement/transparency_of_contracts/spend_information.aspx'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)

table_exists = len(scraperwiki.sqlite.show_tables()) > 0


# Check all the links for those ending with .csv
for obj in page.cssselect('a'):
    href = obj.get('href')
    text = obj.get('title')

    if not text or not href.lower().endswith('.xls'):
        continue

    fu = urlparse.urljoin(url, href)
    filename = fu.rpartition('/')[2]    
    full_url = 'http://www.cafcass.gov.uk/docs/' + filename

    dguclient.save_resource_row(dataset, text, full_url, fmt='XLS', source=url)




