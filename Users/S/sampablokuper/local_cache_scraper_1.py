# Sam Kuper's Python fork of Russell Trafford's PHP "Local Cache Scraper": https://scraperwiki.com/scrapers/local_cache_scraper/
# Allows a scraper to have a local cache to prevent unnecessary scraping during development.

import scraperwiki
import calendar
import datetime
from BeautifulSoup import UnicodeDammit

def decode_html(html_string):
    # See http://stackoverflow.com/a/16427392/82216
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError(
            "Failed to detect encoding, tried [%s]",
            ', '.join(converted.triedEncodings))
    return converted.unicode

def get_source_politely(url, update_flag = False):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS sources (url TEXT PRIMARY KEY, timestamp DATETIME, source_dump TEXT)")
    result = scraperwiki.sqlite.execute("SELECT url, timestamp, source_dump FROM sources WHERE url = '" + url + "'")
    if len(result["data"]) == 0 or update_flag == True:
        # Important to apply decode_html at this point to avoid SQLite's default conversion, which seems to produce results that UnicodeDammit can't happily swallow.
        source = decode_html(scraperwiki.scrape(url))
        scraperwiki.sqlite.save(unique_keys=["url"], data={"url":url, "timestamp":calendar.timegm(datetime.datetime.utcnow().utctimetuple()), "source_dump":source}, table_name="sources")
        return source
    else:
        print "Using local cache for " + url + " as cached data exists from " + datetime.datetime.fromtimestamp(result["data"][0][1]).strftime('%Y-%m-%d %H:%M:%S') + " UTC."
        return result["data"][0][2]

# **************************************
# Sample Code Example
# **************************************

source = get_source_politely("https://www.scraperwiki.com", True)
print source
source = get_source_politely("https://www.scraperwiki.com")
print source
# Sam Kuper's Python fork of Russell Trafford's PHP "Local Cache Scraper": https://scraperwiki.com/scrapers/local_cache_scraper/
# Allows a scraper to have a local cache to prevent unnecessary scraping during development.

import scraperwiki
import calendar
import datetime
from BeautifulSoup import UnicodeDammit

def decode_html(html_string):
    # See http://stackoverflow.com/a/16427392/82216
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError(
            "Failed to detect encoding, tried [%s]",
            ', '.join(converted.triedEncodings))
    return converted.unicode

def get_source_politely(url, update_flag = False):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS sources (url TEXT PRIMARY KEY, timestamp DATETIME, source_dump TEXT)")
    result = scraperwiki.sqlite.execute("SELECT url, timestamp, source_dump FROM sources WHERE url = '" + url + "'")
    if len(result["data"]) == 0 or update_flag == True:
        # Important to apply decode_html at this point to avoid SQLite's default conversion, which seems to produce results that UnicodeDammit can't happily swallow.
        source = decode_html(scraperwiki.scrape(url))
        scraperwiki.sqlite.save(unique_keys=["url"], data={"url":url, "timestamp":calendar.timegm(datetime.datetime.utcnow().utctimetuple()), "source_dump":source}, table_name="sources")
        return source
    else:
        print "Using local cache for " + url + " as cached data exists from " + datetime.datetime.fromtimestamp(result["data"][0][1]).strftime('%Y-%m-%d %H:%M:%S') + " UTC."
        return result["data"][0][2]

# **************************************
# Sample Code Example
# **************************************

source = get_source_politely("https://www.scraperwiki.com", True)
print source
source = get_source_politely("https://www.scraperwiki.com")
print source
