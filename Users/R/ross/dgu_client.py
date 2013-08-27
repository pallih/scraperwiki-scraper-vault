import scraperwiki
import ckanclient
import requests
import datetime
import json
import time

class CkanError(Exception): pass

def _get_client():
    """ Returns a ckanclient instance pointing at DGU """
    return ckanclient.CkanClient(base_location='http://data.gov.uk/api')

def get_resources_for_dataset(package_name):
    """ Returns a list of dicts containing all of the resources for 
        the named package. """
    c = _get_client()
    try:
        pkg = c.package_entity_get(package_name)
    except ckanclient.CkanApiNotFoundError as e:
        raise CkanError(str(e))
    return pkg['resources']

def get_dataset_names_for_publisher(publisher_name):
    """ Returns a list of strings, where those strings are the names
        for the packages within this publisher"""
    c = _get_client()
    try:
        publisher = c.group_entity_get(publisher_name)
    except ckanclient.CkanApiNotFoundError as e:
        raise CkanError(str(e))
    return publisher['packages']


def save_resource_row(dataset, text, full_url, fmt='CSV', source=''):

    if len(scraperwiki.sqlite.show_tables()) > 0:
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

    if status_code == '200':
        size = headers.get('content-length', 0)
    else:
        size = 0 # We want the size of the content, not the redirect.

    scraperwiki.sqlite.save(['url'], 
        dict(url=full_url, label=text, dataset=dataset, scrape_time=datetime.datetime.now(), 
             headers=json.dumps(headers), error=error, status_code=status_code, format=fmt,
             size=size, source=source), 
        table_name="data")
import scraperwiki
import ckanclient
import requests
import datetime
import json
import time

class CkanError(Exception): pass

def _get_client():
    """ Returns a ckanclient instance pointing at DGU """
    return ckanclient.CkanClient(base_location='http://data.gov.uk/api')

def get_resources_for_dataset(package_name):
    """ Returns a list of dicts containing all of the resources for 
        the named package. """
    c = _get_client()
    try:
        pkg = c.package_entity_get(package_name)
    except ckanclient.CkanApiNotFoundError as e:
        raise CkanError(str(e))
    return pkg['resources']

def get_dataset_names_for_publisher(publisher_name):
    """ Returns a list of strings, where those strings are the names
        for the packages within this publisher"""
    c = _get_client()
    try:
        publisher = c.group_entity_get(publisher_name)
    except ckanclient.CkanApiNotFoundError as e:
        raise CkanError(str(e))
    return publisher['packages']


def save_resource_row(dataset, text, full_url, fmt='CSV', source=''):

    if len(scraperwiki.sqlite.show_tables()) > 0:
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

    if status_code == '200':
        size = headers.get('content-length', 0)
    else:
        size = 0 # We want the size of the content, not the redirect.

    scraperwiki.sqlite.save(['url'], 
        dict(url=full_url, label=text, dataset=dataset, scrape_time=datetime.datetime.now(), 
             headers=json.dumps(headers), error=error, status_code=status_code, format=fmt,
             size=size, source=source), 
        table_name="data")
import scraperwiki
import ckanclient
import requests
import datetime
import json
import time

class CkanError(Exception): pass

def _get_client():
    """ Returns a ckanclient instance pointing at DGU """
    return ckanclient.CkanClient(base_location='http://data.gov.uk/api')

def get_resources_for_dataset(package_name):
    """ Returns a list of dicts containing all of the resources for 
        the named package. """
    c = _get_client()
    try:
        pkg = c.package_entity_get(package_name)
    except ckanclient.CkanApiNotFoundError as e:
        raise CkanError(str(e))
    return pkg['resources']

def get_dataset_names_for_publisher(publisher_name):
    """ Returns a list of strings, where those strings are the names
        for the packages within this publisher"""
    c = _get_client()
    try:
        publisher = c.group_entity_get(publisher_name)
    except ckanclient.CkanApiNotFoundError as e:
        raise CkanError(str(e))
    return publisher['packages']


def save_resource_row(dataset, text, full_url, fmt='CSV', source=''):

    if len(scraperwiki.sqlite.show_tables()) > 0:
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

    if status_code == '200':
        size = headers.get('content-length', 0)
    else:
        size = 0 # We want the size of the content, not the redirect.

    scraperwiki.sqlite.save(['url'], 
        dict(url=full_url, label=text, dataset=dataset, scrape_time=datetime.datetime.now(), 
             headers=json.dumps(headers), error=error, status_code=status_code, format=fmt,
             size=size, source=source), 
        table_name="data")
