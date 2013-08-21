from BeautifulSoup import BeautifulSoup
import scraperwiki, re, sqlite3

import time
from datetime import datetime

BASE_URL = 'http://app01.ottawa.ca'
STARTING_URL = BASE_URL + '/postingplans/searchResults.jsf?lang=en&action=as&wardSearch=true&ward='

START = datetime.now()

print START
print datetime.fromtimestamp(int(time.mktime(START.utctimetuple())))

LATLNG_RE = re.compile(r"LAT=([-\d\.]+)&LON=([-\d\.]+)")
ATTR_RE = re.compile('^main:content:supportingDocLink')
WARD_RE = re.compile('^Ward (\d+)')

class Status:
    def __init__(self):
        self.exceptions = {}
        self.scraped = []


status = Status()


def timeInt(t):
    return int(time.mktime(t.utctimetuple()))


# scrape_table function: gets passed a page of search results to scrape
def scrape_table(soup, hashes):
    global status
    datatable = soup.find("tbody")
    rows = datatable.findAll("tr")

    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        addresses = []
        documents = []
        table_cells = row.findAll("td")
        if table_cells: 
            link = table_cells[0].find('a');

            h = hash(link.text.strip()) + hash(table_cells[2].text.strip()) + hash(table_cells[3].text.strip())
            h = hex(h)
            if h in hashes:
                continue

            record["Status_Hash"] = h

            print "Scraping %s" % link.text
            status.scraped.append(link.text)

            # fetch each 'Application Link' page and scrape further details
            scrape_application(BASE_URL + '/postingplans/' + link['href'], record, addresses, documents)

            # Finally, save the record to the datastore
            try:
                scraperwiki.sqlite.execute("UPDATE Applications SET Current=0 WHERE Application_Number=?", record['Application_Number']) 
                record['Current'] = 1;
                scraperwiki.sqlite.save(["Application_Number", "Date_Status"], record, table_name="Applications")
                scraperwiki.sqlite.save(["Application_Number"], addresses, table_name="Locations")
                scraperwiki.sqlite.save(["Application_Number"], documents, table_name="Documents")
            except sqlite3.Error as e:
                status.exceptions[link.text] = e
                


# scrape_application: scrape an application page
def scrape_application(app_url, record, addresses, docs):
    html = scraperwiki.scrape(app_url)
    soup = BeautifulSoup(html) 

    items = soup.findAll("div", { "class": "appDetailValue" } )

    #for item in items:
    #    print item.text

    record['Application_URI'] = app_url
    record['Last_Scrape'] = timeInt(START)

    # 0 - Application Numberrecord
    record['Application_Number'] = items[0].text

    print "Scraping: ", items[0].text
    
    # 1 - Date rcvd
    record['Date_Received'] = timeInt(datetime.strptime(items[1].text, "%B %d, %Y"))

    # 2 - Addresses - See below
    # 3 - Ward
    m = WARD_RE.search(items[3].text)
    if m:
        record['Ward'] = int(m.group(1))

    # 4 - Application type
    record['Application_Type'] = items[4].text

    # 5 - Review status
    record['Review_Status'] = items[5].text

    # 6 - Status date
    record['Date_Status'] = timeInt(datetime.strptime(items[6].text, "%B %d, %Y"))

    # 7 - Description
    record['Description'] = items[7].text

    # 9 - File lead
    record['File_Lead'] = items[9].text.replace('&nbsp;', '')

    # 9 - File lead phone number
    # 10 - Comments link

    #print(record)
    

    # Address, including lat/longrecord
    addr_info = items[2].findAll('a', {"target" : "_emap" })
    if addr_info:
        for addr_a in addr_info:
            # <a href="http://apps104.ottawa.ca/emap?emapver=lite&LAT=45.323884&LON=-75.952962&featname=870+Huntmar+Drive&amp;lang=en"
            match = LATLNG_RE.search(addr_a['href'])
            if match:
                lat = float(match.group(1))
                lng = float(match.group(2))
                addresses.append( { "Application_Number": items[0].text, 'Last_Scrape' : timeInt(START), "Address": addr_a.text, "Lat" : lat, "Long": lng } )
            
    #print(addresses)

    
    # Document links
    for lnk_a in soup.findAll("a", {"target" : "_ottext", "name" : ATTR_RE}):
        docs.append( { "Application_Number": items[0].text, 'Last_Scrape' : START, "URI" : lnk_a['href'], 'Title' : lnk_a.findNext('img')['title'] })

    #print docs


# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_all(url, hashes):
    global status
    next_url = url
    page = 1
    while next_url:
        print "Fetching index page %s (%ss) - %s" % (page, time.clock(), next_url)
        html = scraperwiki.scrape(next_url)
        soup = BeautifulSoup(html)
        scrape_table(soup, hashes)

        text_next = soup.find(text=re.compile("^Next"))

        if text_next:
            next_url = BASE_URL + text_next.parent['href']
            page += 1
        else:
            next_url = None

    print "Completed. CPU time: %s. Scraped: %s. Errors: %s." % (time.clock(), len(status.scraped), len(status.exceptions))


hashes = set()
try:
    for d in scraperwiki.sqlite.select("Status_Hash, Application_Number FROM Applications"):
        hashes.add(d['Status_Hash'])
except scraperwiki.sqlite.SqliteError as e:
    scraperwiki.sqlite.execute("CREATE TABLE Applications (Current INTEGER, Application_Number STRING)")
    pass

scrape_all(STARTING_URL, hashes)