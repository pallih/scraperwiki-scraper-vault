# Scrapes all of the US locations out of the Dairy Queen web site.


# Load the list of locations for the current page in the current state
def processState(baseUrl, pageNum):
    url = baseUrl + '?page=' + str(pageNum)
    print(url)
    # retrieve HTML
    html = scraperwiki.scrape(url)
    # strip out addresses
    root = lxml.html.fromstring(html)
    scrapeAddress(root)
    # look for next page
    nextLink = root.cssselect("a.next_page")
    if (nextLink):
        pageNum = pageNum + 1
        processState(baseUrl, pageNum)
    else:
        print('Done with this state')


# Parse the address fields out of the HTML
def scrapeAddress(root):
    cards = root.cssselect('div.vcard')
    for card in cards:
        a = card.cssselect('a')[0]
        hrefval = a.get("href")
        dqStoreId = hrefval.split("/")[3]
        name = a.text
        adr = card.cssselect('div div')
        street = adr[2].text
        adr = card.cssselect('div span')
        city = adr[1].text
        state = adr[2].text
        zip = adr[3].text
        scraperwiki.sqlite.execute("DELETE from 'locations' where store_id = ?", (dqStoreId))
        scraperwiki.sqlite.execute("INSERT into 'locations' values(?,?,?,?,?,?)", (dqStoreId, name, street, city, state, zip))


# Import required libraries
import scraperwiki
import lxml.html
import urlparse

# Create destination DB table
address_fields = ["store_id INTEGER PRIMARY KEY","name TEXT", "street TEXT", "city TEXT", "state TEXT", "zip TEXT"]
scraperwiki.sqlite.execute("create table if not exists locations (%s)" \
  % ",".join(address_fields))

# List of all US state abbreviations used by DQ
states = [ "al", "ak", "az", "ar", "ca", "co", "ct", "dc", "de", "fl", "ga", "hi", "ia", "id", "il", "in", "ks", "ky", "la", "ma", "me", "md", "mi", "mn", "mo", "ms", "mt", "nc", "nd", "ne", "nh", "nj", "nm", "nv", "ny", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "va", "vt", "wa", "wi", "wv", "wy" ]

# Iterate over all states
for abrv in states:
    pageOneUrl = 'http://www.dairyqueen.com/us-en/stores/' + abrv + '/'
    processState(pageOneUrl, 1)

# Commit DB changes
scraperwiki.sqlite.commit()



