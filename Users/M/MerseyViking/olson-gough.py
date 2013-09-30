import urllib2
import scraperwiki
import lxml.html
import random
import requests
import time

URL = 'http://mcassessor.maricopa.gov/Assessor/ParcelApplication/ResRental.aspx'

fields = [
    'lblParcel',
    'lblPropertyType',
    'lblSiteAddress',
    'lblLegalClass',
    'lblAccountNumber',
    'lblYearBuilt',
    'lblEntity',
    'lblOwnershipType',
    'lblOwnerName',
    'lblOwnerPhone',
    'lblOwnerAddress',
    'lblContactName',
    'lblContactPhone',
    'lblContactAddress',
    'lblAgentName',
    'lblAgentPhone',
    'lblAgentAddress',
    'lblLastUpdatedOn',
    'lblFirstRegistered'
]

batch_size = 10
retries = 3
retry_interval_range = (3, 10)


def format_field(field):
    if field.text is None:
        return ''

    text = [field.text.strip()]

    for br in field:
        if br.tail is not None:
            text.append(br.tail.strip())

    return ', '.join(text)


def parse_detail_page(parcel_id, page_dom):
    detail_table = page_dom.cssselect('div#pnlDetail table')[0]

    values = [format_field(detail_table.get_element_by_id(field)) for field in fields]
    data = dict(zip(fields, values))
    data['id'] = parcel_id
    return data


def search(city_name):
    print('Getting search page...')

    # We need a couple of hidden fields to validate the current session.
    searchpage = requests.get(URL).text

    root = lxml.html.fromstring(searchpage)
    params = {}
    params['__EVENTTARGET'] = ''
    params['__EVENTARGUMENT'] = ''
    params['btnAddress'] = 'Search'
    params['__VIEWSTATE'] = root.cssselect('#__VIEWSTATE')[0].value
    params['__EVENTVALIDATION'] = root.cssselect('#__EVENTVALIDATION')[0].value

    # The first city listed is the "Unsure?" text, so skip it.
    cities = [city.text_content() for city in root.cssselect('#ddlCity option')][1:]

    if city_name in cities:
        params['ddlCity'] = city_name

        print('Searching for parcels in {0}...'.format(city_name))

        results = requests.post(URL, data=params, headers={'Accept-Encoding': 'gzip,deflate,sdch'}).text
        table_dom = lxml.html.fromstring(results).cssselect('table#dgResults')[0]
        parcel_ids = [link[2].split('=')[1].strip() for link in lxml.html.iterlinks(table_dom)]

        print('Found {0} records'.format(len(parcel_ids)))

        # If we aborted last time, start from where we left off.
        last_index = 0
        last_id = scraperwiki.sqlite.get_var('last_id', None)

        if last_id is not None:
            last_index = parcel_ids.index(last_id)
            print('Partial scrape detected, skipping {0} records'.format(last_index + 1))

        return parcel_ids[last_index:]
    else:
        print('Cannot find {0} in {1}'.format(city_name, cities))
        return []


def scrape(ids):
    print('Scraping...')

    row_cache = []

    for parcel_id in ids:
        # We occasionally get a "URLError: <urlopen error [Errno -3] Temporary failure in name resolution>",
        # so we'll use a simple retry system with throttling.
        retry_interval = random.randint(retry_interval_range[0], retry_interval_range[1])
        detail_page = ''

        for retry in xrange(retries):
            try:
                detail_page = lxml.html.fromstring(requests.get(URL,
                                                                params={'Parcel_ID': parcel_id},
                                                                headers={'Accept-Encoding': 'gzip,deflate,sdch'}).text)
                break
            except urllib2.URLError as e:
                if retry + 1 == retries:
                    print('Unable to get page. Aborting.')
                    raise
                else:
                    print('Unable to get page. Retrying in {0} seconds.'.format(retry_interval))
                    time.sleep(retry_interval)
                    retry_interval *= 2

        row_cache.append(parse_detail_page(parcel_id, detail_page))

        if len(row_cache) == batch_size:
            scraperwiki.sqlite.save(unique_keys=['id'], data=row_cache)
            # Remember where we were in case we abort.
            scraperwiki.sqlite.save_var('last_id', parcel_id)
            del row_cache[:]


results = search('Avondale')
scrape(results)
scraperwiki.sqlite.save_var('last_id', None)import urllib2
import scraperwiki
import lxml.html
import random
import requests
import time

URL = 'http://mcassessor.maricopa.gov/Assessor/ParcelApplication/ResRental.aspx'

fields = [
    'lblParcel',
    'lblPropertyType',
    'lblSiteAddress',
    'lblLegalClass',
    'lblAccountNumber',
    'lblYearBuilt',
    'lblEntity',
    'lblOwnershipType',
    'lblOwnerName',
    'lblOwnerPhone',
    'lblOwnerAddress',
    'lblContactName',
    'lblContactPhone',
    'lblContactAddress',
    'lblAgentName',
    'lblAgentPhone',
    'lblAgentAddress',
    'lblLastUpdatedOn',
    'lblFirstRegistered'
]

batch_size = 10
retries = 3
retry_interval_range = (3, 10)


def format_field(field):
    if field.text is None:
        return ''

    text = [field.text.strip()]

    for br in field:
        if br.tail is not None:
            text.append(br.tail.strip())

    return ', '.join(text)


def parse_detail_page(parcel_id, page_dom):
    detail_table = page_dom.cssselect('div#pnlDetail table')[0]

    values = [format_field(detail_table.get_element_by_id(field)) for field in fields]
    data = dict(zip(fields, values))
    data['id'] = parcel_id
    return data


def search(city_name):
    print('Getting search page...')

    # We need a couple of hidden fields to validate the current session.
    searchpage = requests.get(URL).text

    root = lxml.html.fromstring(searchpage)
    params = {}
    params['__EVENTTARGET'] = ''
    params['__EVENTARGUMENT'] = ''
    params['btnAddress'] = 'Search'
    params['__VIEWSTATE'] = root.cssselect('#__VIEWSTATE')[0].value
    params['__EVENTVALIDATION'] = root.cssselect('#__EVENTVALIDATION')[0].value

    # The first city listed is the "Unsure?" text, so skip it.
    cities = [city.text_content() for city in root.cssselect('#ddlCity option')][1:]

    if city_name in cities:
        params['ddlCity'] = city_name

        print('Searching for parcels in {0}...'.format(city_name))

        results = requests.post(URL, data=params, headers={'Accept-Encoding': 'gzip,deflate,sdch'}).text
        table_dom = lxml.html.fromstring(results).cssselect('table#dgResults')[0]
        parcel_ids = [link[2].split('=')[1].strip() for link in lxml.html.iterlinks(table_dom)]

        print('Found {0} records'.format(len(parcel_ids)))

        # If we aborted last time, start from where we left off.
        last_index = 0
        last_id = scraperwiki.sqlite.get_var('last_id', None)

        if last_id is not None:
            last_index = parcel_ids.index(last_id)
            print('Partial scrape detected, skipping {0} records'.format(last_index + 1))

        return parcel_ids[last_index:]
    else:
        print('Cannot find {0} in {1}'.format(city_name, cities))
        return []


def scrape(ids):
    print('Scraping...')

    row_cache = []

    for parcel_id in ids:
        # We occasionally get a "URLError: <urlopen error [Errno -3] Temporary failure in name resolution>",
        # so we'll use a simple retry system with throttling.
        retry_interval = random.randint(retry_interval_range[0], retry_interval_range[1])
        detail_page = ''

        for retry in xrange(retries):
            try:
                detail_page = lxml.html.fromstring(requests.get(URL,
                                                                params={'Parcel_ID': parcel_id},
                                                                headers={'Accept-Encoding': 'gzip,deflate,sdch'}).text)
                break
            except urllib2.URLError as e:
                if retry + 1 == retries:
                    print('Unable to get page. Aborting.')
                    raise
                else:
                    print('Unable to get page. Retrying in {0} seconds.'.format(retry_interval))
                    time.sleep(retry_interval)
                    retry_interval *= 2

        row_cache.append(parse_detail_page(parcel_id, detail_page))

        if len(row_cache) == batch_size:
            scraperwiki.sqlite.save(unique_keys=['id'], data=row_cache)
            # Remember where we were in case we abort.
            scraperwiki.sqlite.save_var('last_id', parcel_id)
            del row_cache[:]


results = search('Avondale')
scrape(results)
scraperwiki.sqlite.save_var('last_id', None)