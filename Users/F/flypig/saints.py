###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Artist', 'Album', 'Released', 'Sales (m)'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find("table", { "class" : "data" })
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Artist'] = table_cells[0].text
            record['Album'] = table_cells[1].text
            record['Released'] = table_cells[2].text
            record['Sales (m)'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Artist"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    next_link = soup.find("a", { "class" : "next" })
    print next_link
    if next_link:
        next_url = base_url + next_link['href']
        print next_url
        scrape_and_look_for_next_link(next_url)


def scrape_saint_data(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)

    if html.startswith('<script language="JavaScript">'):
        found = re.search('href=\".*\"', soup.contents[0].contents[0].string).span()
        url = soup.contents[0].contents[0].string[found[0]+6:found[1]-1]
        print url
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)

    title = soup.find("h1").contents[0].string
    if re.search('Saints.SQPN.com', title):
        title = soup.find("h2").contents[0].contents[0]
    print title

    # Now the data
    names = soup.findAll("ins")
    for name in names:
        if name.find("a"):
            name = name.find("a")
        print name.contents[0]
        next = name
        while next.nextSibling==None:
            next = next.parent
        print next
        while type(next.nextSibling).__name__ == 'NavigableString':
            next = next.nextSibling
        print next.contents[0]


# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://saints.sqpn.com/saints-a/'
html = scraperwiki.scrape(base_url)
soup = BeautifulSoup(html)

links = soup.findAll("a")
link = links[71]
#for link in links:
if 1:
    if link['href'].startswith('http://'):
        print link['href']
        scrape_saint_data(link['href'])
    else:
        print base_url + link['href']
        scrape_saint_data(base_url + link['href'])


###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Artist', 'Album', 'Released', 'Sales (m)'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find("table", { "class" : "data" })
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Artist'] = table_cells[0].text
            record['Album'] = table_cells[1].text
            record['Released'] = table_cells[2].text
            record['Sales (m)'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Artist"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    next_link = soup.find("a", { "class" : "next" })
    print next_link
    if next_link:
        next_url = base_url + next_link['href']
        print next_url
        scrape_and_look_for_next_link(next_url)


def scrape_saint_data(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)

    if html.startswith('<script language="JavaScript">'):
        found = re.search('href=\".*\"', soup.contents[0].contents[0].string).span()
        url = soup.contents[0].contents[0].string[found[0]+6:found[1]-1]
        print url
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)

    title = soup.find("h1").contents[0].string
    if re.search('Saints.SQPN.com', title):
        title = soup.find("h2").contents[0].contents[0]
    print title

    # Now the data
    names = soup.findAll("ins")
    for name in names:
        if name.find("a"):
            name = name.find("a")
        print name.contents[0]
        next = name
        while next.nextSibling==None:
            next = next.parent
        print next
        while type(next.nextSibling).__name__ == 'NavigableString':
            next = next.nextSibling
        print next.contents[0]


# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://saints.sqpn.com/saints-a/'
html = scraperwiki.scrape(base_url)
soup = BeautifulSoup(html)

links = soup.findAll("a")
link = links[71]
#for link in links:
if 1:
    if link['href'].startswith('http://'):
        print link['href']
        scrape_saint_data(link['href'])
    else:
        print base_url + link['href']
        scrape_saint_data(base_url + link['href'])


