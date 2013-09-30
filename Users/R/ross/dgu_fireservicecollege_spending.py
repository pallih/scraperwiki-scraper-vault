import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time

dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'financial-transactions-data-fsc'
url = 'http://www.fireservicecollege.ac.uk/about-us/access-to-information/transparency-agenda.aspx'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)


# Check all the links for those ending with .csv
for obj in page.cssselect('a'):
    href = obj.get('href')
    text = obj.text_content()

    if not href or not (href.lower().endswith('.csv') or href.lower().endswith('.xls')):
        continue
    
    parts = text.split(' ')
    if len(parts) != 2:
        continue

    try:
        yr = int(parts[1])
        if yr <= 2000:
            continue
    except:
        continue

    full_url = urlparse.urljoin(url, href)
    print full_url, text
    fmt = href[-3:].upper()
    
    dguclient.save_resource_row(dataset, text, full_url, fmt=fmt, source=url)

dguclient.save_resource_row(dataset, "2009-2010", "http://www.fireservicecollege.ac.uk/media/23873/09-10%20spend%20(csv).csv", fmt="CSV", source=url)



import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time

dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'financial-transactions-data-fsc'
url = 'http://www.fireservicecollege.ac.uk/about-us/access-to-information/transparency-agenda.aspx'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)


# Check all the links for those ending with .csv
for obj in page.cssselect('a'):
    href = obj.get('href')
    text = obj.text_content()

    if not href or not (href.lower().endswith('.csv') or href.lower().endswith('.xls')):
        continue
    
    parts = text.split(' ')
    if len(parts) != 2:
        continue

    try:
        yr = int(parts[1])
        if yr <= 2000:
            continue
    except:
        continue

    full_url = urlparse.urljoin(url, href)
    print full_url, text
    fmt = href[-3:].upper()
    
    dguclient.save_resource_row(dataset, text, full_url, fmt=fmt, source=url)

dguclient.save_resource_row(dataset, "2009-2010", "http://www.fireservicecollege.ac.uk/media/23873/09-10%20spend%20(csv).csv", fmt="CSV", source=url)



import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time

dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'financial-transactions-data-fsc'
url = 'http://www.fireservicecollege.ac.uk/about-us/access-to-information/transparency-agenda.aspx'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)


# Check all the links for those ending with .csv
for obj in page.cssselect('a'):
    href = obj.get('href')
    text = obj.text_content()

    if not href or not (href.lower().endswith('.csv') or href.lower().endswith('.xls')):
        continue
    
    parts = text.split(' ')
    if len(parts) != 2:
        continue

    try:
        yr = int(parts[1])
        if yr <= 2000:
            continue
    except:
        continue

    full_url = urlparse.urljoin(url, href)
    print full_url, text
    fmt = href[-3:].upper()
    
    dguclient.save_resource_row(dataset, text, full_url, fmt=fmt, source=url)

dguclient.save_resource_row(dataset, "2009-2010", "http://www.fireservicecollege.ac.uk/media/23873/09-10%20spend%20(csv).csv", fmt="CSV", source=url)



import scraperwiki
import requests
import lxml.html
import urlparse
import datetime
import json
import time

dguclient = scraperwiki.utils.swimport('dgu_client')

dataset = 'financial-transactions-data-fsc'
url = 'http://www.fireservicecollege.ac.uk/about-us/access-to-information/transparency-agenda.aspx'

data = scraperwiki.scrape(url)
page = lxml.html.fromstring(data)


# Check all the links for those ending with .csv
for obj in page.cssselect('a'):
    href = obj.get('href')
    text = obj.text_content()

    if not href or not (href.lower().endswith('.csv') or href.lower().endswith('.xls')):
        continue
    
    parts = text.split(' ')
    if len(parts) != 2:
        continue

    try:
        yr = int(parts[1])
        if yr <= 2000:
            continue
    except:
        continue

    full_url = urlparse.urljoin(url, href)
    print full_url, text
    fmt = href[-3:].upper()
    
    dguclient.save_resource_row(dataset, text, full_url, fmt=fmt, source=url)

dguclient.save_resource_row(dataset, "2009-2010", "http://www.fireservicecollege.ac.uk/media/23873/09-10%20spend%20(csv).csv", fmt="CSV", source=url)



