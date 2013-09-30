import scraperwiki

import urllib
import urlparse

import requests

# Current experience shows that using the ETag is unreliable for processing...
ETAG_BASED_CACHING = False

# lastBuildDate also appears to be a good expiration source
LAST_BUILD_DATE_HACK = True

tables = scraperwiki.sqlite.show_tables()

#BASE - setup as WordPress for now

feeds = [
    {"baseURL":"http://podcastle.org/feed/"},
    {"baseURL":"http://escapepod.org/feed/"},
    {"baseURL":"http://actualplay.roleplayingpublicradio.com/feed/"},
    {"baseURL":"http://slangdesign.com/rppr/feed/"}
]

# Prepare DB table w/ all feeds being processed
scraperwiki.sqlite.execute("DROP TABLE IF EXISTS feeds_processed")
scraperwiki.sqlite.commit()
scraperwiki.sqlite.save(unique_keys = ['baseURL'], data = feeds, table_name = 'feeds_processed')

# Cleanse out any entries from the store if any are missing from the feeds_processed list
if 'feed_data' in tables:
    scraperwiki.sqlite.execute("DELETE from feed_data WHERE baseURL NOT IN feeds_processed")
if 'url_result_data' in tables:
    scraperwiki.sqlite.execute("DELETE from url_result_data WHERE baseURL NOT IN feeds_processed")
if 'rss_root' in tables:
    scraperwiki.sqlite.execute("DELETE from rss_root WHERE baseURL NOT IN feeds_processed")
if 'rss_item' in tables:
    scraperwiki.sqlite.execute("DELETE from rss_item WHERE baseURL NOT IN feeds_processed")

scraperwiki.sqlite.commit()

from lxml import etree
import dateutil.parser

def processData(baseURL, url, tree):
    # TODO: Determine if all we did was replace existing data this round to abort early
    # Collect all entries
    entries = []
    for entry in tree.findall('.//item'):
        # Collect ID
        id = entry.find('guid') # optional
        if id is None:
            id = entry.find('link') # mandatory
            id = 'link:' + id.text
        else:
            id = 'guid:' + id.text
        # Collect date - we require, but RSS makes optional
        date = entry.find('pubDate')
        if date is None:
            scraperwiki.util.log("*** URL: %s reports items without pubDate - considering failure" % baseURL)
            return False

        date = dateutil.parser.parse(date.text)
        data = etree.tostring(entry)
        entries.append({"baseURL":baseURL, "id":id, "date":date,"data":data})

    scraperwiki.sqlite.save(unique_keys = ["baseURL", "id"], data = entries, table_name = "rss_item")

    if baseURL == url:
        # Strip and preserve the root data
        etree.strip_elements(tree, 'item')
        data = etree.tostring(tree)
        entry = {"baseURL":baseURL, "data":data}
        scraperwiki.sqlite.save(unique_keys = ["baseURL"], data = [entry], table_name = "rss_root")

    return True

def getCacheEntry(url):
    # Returns whether or not we've already processed the item, if so, do not process again
    if 'url_result_data' in tables:
        result = scraperwiki.sqlite.select("* FROM url_result_data WHERE url = ?", url)
        if len(result) > 0:
            return result[0]

def processSegment(baseURL, url):
    # Check for cache identifier
    cache_item = getCacheEntry(url)

    headers = {}

    if cache_item is not None:
        # Send along etag / modified header to avoid re-processing
        if ETAG_BASED_CACHING and 'ETag' in cache_item:
            headers["If-None-Match"] = cache_item.get("ETag")
        elif 'Last-Modified' in cache_item:
            headers["If-Modified-Since"] = cache_item.get("Last-Modified")

    response = requests.get(url, headers = headers)

    if response.status_code == 304:
        # Already processed! we're good
        scraperwiki.utils.log("URL '%s' reported 304 - done w/ this url but try others" % url)
        return True

    if response.status_code != 200:
        # Failed
        scraperwiki.utils.log("URL '%s' reported failure '%s'" % (url, response))
        # All failures result in no more processing
        return False

    response_headers = response.headers
    print "Working with:", response_headers

    parser = etree.XMLParser(ns_clean = True, strip_cdata = False)
    tree = etree.fromstring(response.content, parser)
    if not processData(baseURL, url, tree):
        return False

    # Store new ETag / last modified info if present
    if 'ETag' in response_headers or 'Last-Modified' in response_headers or LAST_BUILD_DATE_HACK:
        # Check info
        item = { "baseURL": baseURL, "url": url, "ETag": None, "Last-Modified": None }
        if 'ETag' in response_headers:
            item["ETag"] = response_headers['ETag']
        if 'Last-Modified' in response_headers:
            item["Last-Modified"] = response_headers.get('Last-Modified')
        elif LAST_BUILD_DATE_HACK:
            lastBuildDate = tree.find("channel/lastBuildDate")
            if lastBuildDate is not None:
                item["Last-Modified"] = lastBuildDate.text
        scraperwiki.sqlite.save(unique_keys = ['url'], data = item, table_name = "url_result_data")

    return True

def processFeed(feed):
    url = feed.get("baseURL")
    parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(parts[4]))

    index = 0
    while True:
        index = index + 1
        if index != 1:
            query["paged"] = index

        parts[4] = urllib.urlencode(query)
        if not processSegment(url, urlparse.urlunparse(parts)):
            break

for feed in feeds:
    processFeed(feed)
print "DONE PROCESSING"
import scraperwiki

import urllib
import urlparse

import requests

# Current experience shows that using the ETag is unreliable for processing...
ETAG_BASED_CACHING = False

# lastBuildDate also appears to be a good expiration source
LAST_BUILD_DATE_HACK = True

tables = scraperwiki.sqlite.show_tables()

#BASE - setup as WordPress for now

feeds = [
    {"baseURL":"http://podcastle.org/feed/"},
    {"baseURL":"http://escapepod.org/feed/"},
    {"baseURL":"http://actualplay.roleplayingpublicradio.com/feed/"},
    {"baseURL":"http://slangdesign.com/rppr/feed/"}
]

# Prepare DB table w/ all feeds being processed
scraperwiki.sqlite.execute("DROP TABLE IF EXISTS feeds_processed")
scraperwiki.sqlite.commit()
scraperwiki.sqlite.save(unique_keys = ['baseURL'], data = feeds, table_name = 'feeds_processed')

# Cleanse out any entries from the store if any are missing from the feeds_processed list
if 'feed_data' in tables:
    scraperwiki.sqlite.execute("DELETE from feed_data WHERE baseURL NOT IN feeds_processed")
if 'url_result_data' in tables:
    scraperwiki.sqlite.execute("DELETE from url_result_data WHERE baseURL NOT IN feeds_processed")
if 'rss_root' in tables:
    scraperwiki.sqlite.execute("DELETE from rss_root WHERE baseURL NOT IN feeds_processed")
if 'rss_item' in tables:
    scraperwiki.sqlite.execute("DELETE from rss_item WHERE baseURL NOT IN feeds_processed")

scraperwiki.sqlite.commit()

from lxml import etree
import dateutil.parser

def processData(baseURL, url, tree):
    # TODO: Determine if all we did was replace existing data this round to abort early
    # Collect all entries
    entries = []
    for entry in tree.findall('.//item'):
        # Collect ID
        id = entry.find('guid') # optional
        if id is None:
            id = entry.find('link') # mandatory
            id = 'link:' + id.text
        else:
            id = 'guid:' + id.text
        # Collect date - we require, but RSS makes optional
        date = entry.find('pubDate')
        if date is None:
            scraperwiki.util.log("*** URL: %s reports items without pubDate - considering failure" % baseURL)
            return False

        date = dateutil.parser.parse(date.text)
        data = etree.tostring(entry)
        entries.append({"baseURL":baseURL, "id":id, "date":date,"data":data})

    scraperwiki.sqlite.save(unique_keys = ["baseURL", "id"], data = entries, table_name = "rss_item")

    if baseURL == url:
        # Strip and preserve the root data
        etree.strip_elements(tree, 'item')
        data = etree.tostring(tree)
        entry = {"baseURL":baseURL, "data":data}
        scraperwiki.sqlite.save(unique_keys = ["baseURL"], data = [entry], table_name = "rss_root")

    return True

def getCacheEntry(url):
    # Returns whether or not we've already processed the item, if so, do not process again
    if 'url_result_data' in tables:
        result = scraperwiki.sqlite.select("* FROM url_result_data WHERE url = ?", url)
        if len(result) > 0:
            return result[0]

def processSegment(baseURL, url):
    # Check for cache identifier
    cache_item = getCacheEntry(url)

    headers = {}

    if cache_item is not None:
        # Send along etag / modified header to avoid re-processing
        if ETAG_BASED_CACHING and 'ETag' in cache_item:
            headers["If-None-Match"] = cache_item.get("ETag")
        elif 'Last-Modified' in cache_item:
            headers["If-Modified-Since"] = cache_item.get("Last-Modified")

    response = requests.get(url, headers = headers)

    if response.status_code == 304:
        # Already processed! we're good
        scraperwiki.utils.log("URL '%s' reported 304 - done w/ this url but try others" % url)
        return True

    if response.status_code != 200:
        # Failed
        scraperwiki.utils.log("URL '%s' reported failure '%s'" % (url, response))
        # All failures result in no more processing
        return False

    response_headers = response.headers
    print "Working with:", response_headers

    parser = etree.XMLParser(ns_clean = True, strip_cdata = False)
    tree = etree.fromstring(response.content, parser)
    if not processData(baseURL, url, tree):
        return False

    # Store new ETag / last modified info if present
    if 'ETag' in response_headers or 'Last-Modified' in response_headers or LAST_BUILD_DATE_HACK:
        # Check info
        item = { "baseURL": baseURL, "url": url, "ETag": None, "Last-Modified": None }
        if 'ETag' in response_headers:
            item["ETag"] = response_headers['ETag']
        if 'Last-Modified' in response_headers:
            item["Last-Modified"] = response_headers.get('Last-Modified')
        elif LAST_BUILD_DATE_HACK:
            lastBuildDate = tree.find("channel/lastBuildDate")
            if lastBuildDate is not None:
                item["Last-Modified"] = lastBuildDate.text
        scraperwiki.sqlite.save(unique_keys = ['url'], data = item, table_name = "url_result_data")

    return True

def processFeed(feed):
    url = feed.get("baseURL")
    parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(parts[4]))

    index = 0
    while True:
        index = index + 1
        if index != 1:
            query["paged"] = index

        parts[4] = urllib.urlencode(query)
        if not processSegment(url, urlparse.urlunparse(parts)):
            break

for feed in feeds:
    processFeed(feed)
print "DONE PROCESSING"
