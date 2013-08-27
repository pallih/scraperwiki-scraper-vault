import scraperwiki
import hashlib
import time
from urlparse import urljoin
from lxml.html import fromstring

url = "http://www.ons.gov.uk/ons/datasets-and-tables/index.html?newquery=*&newoffset=&pageSize=1000&content-type=Dataset&content-type-orig=%22Dataset%22+OR+content-type_original%3A%22Reference+table%22&sortBy=pubdate&sortDirection=DESCENDING&applyFilters=true"


def get_links(id, url):
    time.sleep(0.75)
    page = fromstring(scraperwiki.scrape(url))
    links = page.cssselect('.data a')
    resources = []
    for link in links:
        href = urljoin(url, link.get('href'))
        if href.endswith('.html'):
            continue
        resources.append({'dataset':id, 'url': href, 'type': link.get('class') , 'title': link.text_content()})
    scraperwiki.sqlite.save(['dataset', 'url'], resources, table_name='resources')
        

def get_datasets():
    page = fromstring(scraperwiki.scrape(url))
    table = page.cssselect('table.results-listing')[0]
    for row in table.cssselect('tr')[1:]:
        tds = row.cssselect('td')

        lnk = tds[0].cssselect('a')[0]
        ds_url = urljoin(url, lnk.get('href'))
        name = lnk.text_content()
        description = tds[0].cssselect('.resultsDescription')[0].text_content()
        date = tds[1].text_content()
        id = hashlib.md5(ds_url).hexdigest()
        dataset = {'id': id, 'url':ds_url, 'name': name, 'description': description, 'release_date':date}
        get_links(id, ds_url)
        scraperwiki.sqlite.save(['id'],dataset , table_name='datasets')

get_datasets()import scraperwiki
import hashlib
import time
from urlparse import urljoin
from lxml.html import fromstring

url = "http://www.ons.gov.uk/ons/datasets-and-tables/index.html?newquery=*&newoffset=&pageSize=1000&content-type=Dataset&content-type-orig=%22Dataset%22+OR+content-type_original%3A%22Reference+table%22&sortBy=pubdate&sortDirection=DESCENDING&applyFilters=true"


def get_links(id, url):
    time.sleep(0.75)
    page = fromstring(scraperwiki.scrape(url))
    links = page.cssselect('.data a')
    resources = []
    for link in links:
        href = urljoin(url, link.get('href'))
        if href.endswith('.html'):
            continue
        resources.append({'dataset':id, 'url': href, 'type': link.get('class') , 'title': link.text_content()})
    scraperwiki.sqlite.save(['dataset', 'url'], resources, table_name='resources')
        

def get_datasets():
    page = fromstring(scraperwiki.scrape(url))
    table = page.cssselect('table.results-listing')[0]
    for row in table.cssselect('tr')[1:]:
        tds = row.cssselect('td')

        lnk = tds[0].cssselect('a')[0]
        ds_url = urljoin(url, lnk.get('href'))
        name = lnk.text_content()
        description = tds[0].cssselect('.resultsDescription')[0].text_content()
        date = tds[1].text_content()
        id = hashlib.md5(ds_url).hexdigest()
        dataset = {'id': id, 'url':ds_url, 'name': name, 'description': description, 'release_date':date}
        get_links(id, ds_url)
        scraperwiki.sqlite.save(['id'],dataset , table_name='datasets')

get_datasets()import scraperwiki
import hashlib
import time
from urlparse import urljoin
from lxml.html import fromstring

url = "http://www.ons.gov.uk/ons/datasets-and-tables/index.html?newquery=*&newoffset=&pageSize=1000&content-type=Dataset&content-type-orig=%22Dataset%22+OR+content-type_original%3A%22Reference+table%22&sortBy=pubdate&sortDirection=DESCENDING&applyFilters=true"


def get_links(id, url):
    time.sleep(0.75)
    page = fromstring(scraperwiki.scrape(url))
    links = page.cssselect('.data a')
    resources = []
    for link in links:
        href = urljoin(url, link.get('href'))
        if href.endswith('.html'):
            continue
        resources.append({'dataset':id, 'url': href, 'type': link.get('class') , 'title': link.text_content()})
    scraperwiki.sqlite.save(['dataset', 'url'], resources, table_name='resources')
        

def get_datasets():
    page = fromstring(scraperwiki.scrape(url))
    table = page.cssselect('table.results-listing')[0]
    for row in table.cssselect('tr')[1:]:
        tds = row.cssselect('td')

        lnk = tds[0].cssselect('a')[0]
        ds_url = urljoin(url, lnk.get('href'))
        name = lnk.text_content()
        description = tds[0].cssselect('.resultsDescription')[0].text_content()
        date = tds[1].text_content()
        id = hashlib.md5(ds_url).hexdigest()
        dataset = {'id': id, 'url':ds_url, 'name': name, 'description': description, 'release_date':date}
        get_links(id, ds_url)
        scraperwiki.sqlite.save(['id'],dataset , table_name='datasets')

get_datasets()