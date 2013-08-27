from lxml.html import fromstring
import scraperwiki
import urlparse
import os
import cgi
import json

def get_ons_resources_for_url(root):

    html = scraperwiki.scrape(root)
    page = fromstring(html)

    results = []
    outerdivs = page.cssselect('.table-info')
    for odiv in outerdivs:
        url, title, description = None, None, None

        # URL
        dldiv = odiv.cssselect('.download-options ul li a')[0]
        url = urlparse.urljoin(root, dldiv.get('href'))

        dlinfo = odiv.cssselect('.download-info')[0]
        title = dlinfo.cssselect('h3')[0].text_content()

        description = dlinfo.cssselect('div')[2].text_content()
        description = description.strip()[len('Description: '):]

        _, extension = os.path.splitext(url)
        if extension.lower() in ['.xls', '.csv']:
            results.append(dict(title=title, url=url, description=description))
    return results


scraperwiki.utils.httpresponseheader("Content-Type", "application/json")

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
url = paramdict.get('url')
if not url:
    print json.dumps({'error': 'No URL was specified for this request'})
try:
    results = get_ons_resources_for_url(url)
    sort = paramdict.get('sort', 'title')
    results = sorted(results, key=lambda k: k[sort]) 
except Exception as e:
    print json.dumps({'error': 'An error occurred fetching the data %s' % str(e)})
print json.dumps(results)
from lxml.html import fromstring
import scraperwiki
import urlparse
import os
import cgi
import json

def get_ons_resources_for_url(root):

    html = scraperwiki.scrape(root)
    page = fromstring(html)

    results = []
    outerdivs = page.cssselect('.table-info')
    for odiv in outerdivs:
        url, title, description = None, None, None

        # URL
        dldiv = odiv.cssselect('.download-options ul li a')[0]
        url = urlparse.urljoin(root, dldiv.get('href'))

        dlinfo = odiv.cssselect('.download-info')[0]
        title = dlinfo.cssselect('h3')[0].text_content()

        description = dlinfo.cssselect('div')[2].text_content()
        description = description.strip()[len('Description: '):]

        _, extension = os.path.splitext(url)
        if extension.lower() in ['.xls', '.csv']:
            results.append(dict(title=title, url=url, description=description))
    return results


scraperwiki.utils.httpresponseheader("Content-Type", "application/json")

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
url = paramdict.get('url')
if not url:
    print json.dumps({'error': 'No URL was specified for this request'})
try:
    results = get_ons_resources_for_url(url)
    sort = paramdict.get('sort', 'title')
    results = sorted(results, key=lambda k: k[sort]) 
except Exception as e:
    print json.dumps({'error': 'An error occurred fetching the data %s' % str(e)})
print json.dumps(results)
from lxml.html import fromstring
import scraperwiki
import urlparse
import os
import cgi
import json

def get_ons_resources_for_url(root):

    html = scraperwiki.scrape(root)
    page = fromstring(html)

    results = []
    outerdivs = page.cssselect('.table-info')
    for odiv in outerdivs:
        url, title, description = None, None, None

        # URL
        dldiv = odiv.cssselect('.download-options ul li a')[0]
        url = urlparse.urljoin(root, dldiv.get('href'))

        dlinfo = odiv.cssselect('.download-info')[0]
        title = dlinfo.cssselect('h3')[0].text_content()

        description = dlinfo.cssselect('div')[2].text_content()
        description = description.strip()[len('Description: '):]

        _, extension = os.path.splitext(url)
        if extension.lower() in ['.xls', '.csv']:
            results.append(dict(title=title, url=url, description=description))
    return results


scraperwiki.utils.httpresponseheader("Content-Type", "application/json")

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
url = paramdict.get('url')
if not url:
    print json.dumps({'error': 'No URL was specified for this request'})
try:
    results = get_ons_resources_for_url(url)
    sort = paramdict.get('sort', 'title')
    results = sorted(results, key=lambda k: k[sort]) 
except Exception as e:
    print json.dumps({'error': 'An error occurred fetching the data %s' % str(e)})
print json.dumps(results)
