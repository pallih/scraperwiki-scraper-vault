# Scrapes all of the US locations out of the Carinos web site.


# Load the list of locations for the current page in the current state
def processState(url):
    print(url)
    # retrieve HTML
    html = scraperwiki.scrape(url)
    # strip out addresses
    root = lxml.html.fromstring(html)
    scrapeAddress(root)


# Parse the address fields out of the HTML
def scrapeAddress(root):
    addrs = root.cssselect('span.address')
    titles = root.cssselect('a.title')
    length = len(addrs)
    for t, a in zip(titles, addrs):
        storeTitle = t.text
        print(storeTitle)
        storeAddress = a.text
        print(storeAddress)
        #scraperwiki.sqlite.execute("DELETE from 'locations' where store_id = ?", (dqStoreId))
        scraperwiki.sqlite.execute("INSERT into 'locations' values(?,?)", (storeTitle, storeAddress))


# Import required libraries
import scraperwiki
import lxml.html
import urlparse

# Create destination DB table
scraperwiki.sqlite.execute("drop table if exists locations")
address_fields = ["store_title TEXT","address TEXT"]
scraperwiki.sqlite.execute("create table if not exists locations (%s)" \
  % ",".join(address_fields))

# List of all US state abbreviations (including DC, not including territories)
# for testing
#states = ["nc"]
# full list
states = [ "al", "ak", "az", "ar", "ca", "co", "ct", "dc", "de", "fl", "ga", "hi", "ia", "id", "il", "in", "ks", "ky", "la", "ma", "me", "md", "mi", "mn", "mo", "ms", "mt", "nc", "nd", "ne", "nh", "nj", "nm", "nv", "ny", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "va", "vt", "wa", "wi", "wv", "wy" ]

# Iterate over all states
for abrv in states:
    url = 'http://www.carinos.com/location/home/ziplookup/' + abrv
    processState(url)

# Commit DB changes
scraperwiki.sqlite.commit()

# Scrapes all of the US locations out of the Carinos web site.


# Load the list of locations for the current page in the current state
def processState(url):
    print(url)
    # retrieve HTML
    html = scraperwiki.scrape(url)
    # strip out addresses
    root = lxml.html.fromstring(html)
    scrapeAddress(root)


# Parse the address fields out of the HTML
def scrapeAddress(root):
    addrs = root.cssselect('span.address')
    titles = root.cssselect('a.title')
    length = len(addrs)
    for t, a in zip(titles, addrs):
        storeTitle = t.text
        print(storeTitle)
        storeAddress = a.text
        print(storeAddress)
        #scraperwiki.sqlite.execute("DELETE from 'locations' where store_id = ?", (dqStoreId))
        scraperwiki.sqlite.execute("INSERT into 'locations' values(?,?)", (storeTitle, storeAddress))


# Import required libraries
import scraperwiki
import lxml.html
import urlparse

# Create destination DB table
scraperwiki.sqlite.execute("drop table if exists locations")
address_fields = ["store_title TEXT","address TEXT"]
scraperwiki.sqlite.execute("create table if not exists locations (%s)" \
  % ",".join(address_fields))

# List of all US state abbreviations (including DC, not including territories)
# for testing
#states = ["nc"]
# full list
states = [ "al", "ak", "az", "ar", "ca", "co", "ct", "dc", "de", "fl", "ga", "hi", "ia", "id", "il", "in", "ks", "ky", "la", "ma", "me", "md", "mi", "mn", "mo", "ms", "mt", "nc", "nd", "ne", "nh", "nj", "nm", "nv", "ny", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "va", "vt", "wa", "wi", "wv", "wy" ]

# Iterate over all states
for abrv in states:
    url = 'http://www.carinos.com/location/home/ziplookup/' + abrv
    processState(url)

# Commit DB changes
scraperwiki.sqlite.commit()

