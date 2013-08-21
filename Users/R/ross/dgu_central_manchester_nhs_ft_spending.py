import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time

dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'spend_over_25000_in_central_manchester_university_hospitals_nhs_foundation_trust'
url = 'http://www.cmft.nhs.uk/your-trust/freedom-of-information/what-we-spend-and-how-we-spend-it.aspx'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)


# Check all the links for those ending with .csv
for obj in page.cssselect('ul li a'):
    href = obj.get('href')
    text = obj.text_content()

    if not (href.lower().endswith('.csv') or href.lower().endswith('.xls')):
        continue
    
    if text.strip() == 'contracts':
        continue

    full_url = urlparse.urljoin(url, href)
    print full_url, text
    fmt = href[-3:].upper()

    dguclient.save_resource_row(dataset, text, full_url, fmt=fmt, source=url)



import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time

dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'spend_over_25000_in_central_manchester_university_hospitals_nhs_foundation_trust'
url = 'http://www.cmft.nhs.uk/your-trust/freedom-of-information/what-we-spend-and-how-we-spend-it.aspx'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)


# Check all the links for those ending with .csv
for obj in page.cssselect('ul li a'):
    href = obj.get('href')
    text = obj.text_content()

    if not (href.lower().endswith('.csv') or href.lower().endswith('.xls')):
        continue
    
    if text.strip() == 'contracts':
        continue

    full_url = urlparse.urljoin(url, href)
    print full_url, text
    fmt = href[-3:].upper()

    dguclient.save_resource_row(dataset, text, full_url, fmt=fmt, source=url)



