from BeautifulSoup import BeautifulSoup
import scraperwiki, re

BASE_URL = 'http://app01.ottawa.ca'
STARTING_URL = BASE_URL + '/postingplans/searchResults.jsf?lang=en&action=as&wardSearch=true&ward='

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Application Number', 'Application Link', 'Addresses', 'Primary Address', 'Application Type', 'Review Status', 'Status Date', 'Date Received', 'Ward', 'Description', 'File Lead Name', 'File Lead Telephone'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
     datatable = soup.find("tbody")
     rows = datatable.findAll("tr")
     for row in rows:
         # Set up our data record - we'll need it later
         record = {}
         table_cells = row.findAll("td")
         if table_cells: 
             link = table_cells[0].find('a');
             record['Application Number'] = link.text
             record['Application Link']   = BASE_URL + '/postingplans/' + link['href']
             record['Application Type']   = table_cells[1].text
             record['Review Status']      = table_cells[2].text
             record['Status Date']        = table_cells[3].text

             # fetch each 'Application Link' page and scrape further details
             record = scrape_application(record['Application Link'], record)

             # Print out the data we've gathered
             print record, '------------'

             # Finally, save the record to the datastore
             latlng_tmp = None
             if len(record['Addresses']) > 0:
                 record['Primary_Address'] = record['Addresses'][0]['address']
                 latlng_tmp = record['Addresses'][0]['latlng']
             scraperwiki.datastore.save(["Application Number"],record, latlng=latlng_tmp)

def scrape_application(app_url, record):
    html = scraperwiki.scrape(app_url)
    soup = BeautifulSoup(html) 

    items = soup.findAll("div", { "class": "appDetailValue" } )

    for item in items:
        print item.findNext('div', {'class' : 'label'}).text

    

    # 0 - Return to search results
    # 1 - Application Number
    record['Date Received'] = items[2].findNext('div', {"class" : "appDetailValue" }).text

    # Address, including lat/long
    latlng_re = re.compile(r"LAT=([-\d\.]+)&LON=([-\d\.]+)")
    addr_info = items[3].findNext('div', {"class" : "appDetailValue" })
    if addr_info:
        record['Addresses'] = []
        addr_items = addr_info.findAll('a')
        for addr_a in addr_items:
            # <a href="http://apps104.ottawa.ca/emap?emapver=lite&LAT=45.323884&LON=-75.952962&featname=870+Huntmar+Drive&amp;lang=en"
            match = latlng_re.search(addr_a['href'])
            latlng = None
            if match:
                latlng = [ float(match.group(1)), float(match.group(2)) ]
            record['Addresses'].append( { "address": addr_a.text, "latlng": latlng } )
            

    # TODO: parse ward
    record['Ward'] = items[4].findNext('div', {"class" : "appDetailValue" }).text
    # 5 - Application
    # 6 - Review Status
    # 7 - Status Date
    record['Description'] = items[8].findNext('div', {"class" : "appDetailValue" }).text
    # 9 - Supporting Documents heading
    # 10 - useless comment
    # 11 - disclaimer
    # 12 - actual supporting document links  (TODO: want this)
    # 13 - adobe d/l link
    # 14 - file lead header
    record['File Lead Name'] = items[15].findNext('div', {"class" : "appDetailValue" }).text
    record['File Lead Telephone'] = items[16].findNext('div', {"class" : "appDetailValue" }).text

    return record

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_all(url):
    next_url = url
    while next_url:
        print "Fetching " + next_url
        html = scraperwiki.scrape(next_url)
        soup = BeautifulSoup(html)
        scrape_table(soup)

        text_next = soup.find(text=re.compile("^Next"))

        if text_next:
            next_url = BASE_URL + text_next.parent['href']
        else:
            next_url = None

scrape_all(STARTING_URL)from BeautifulSoup import BeautifulSoup
import scraperwiki, re

BASE_URL = 'http://app01.ottawa.ca'
STARTING_URL = BASE_URL + '/postingplans/searchResults.jsf?lang=en&action=as&wardSearch=true&ward='

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Application Number', 'Application Link', 'Addresses', 'Primary Address', 'Application Type', 'Review Status', 'Status Date', 'Date Received', 'Ward', 'Description', 'File Lead Name', 'File Lead Telephone'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
     datatable = soup.find("tbody")
     rows = datatable.findAll("tr")
     for row in rows:
         # Set up our data record - we'll need it later
         record = {}
         table_cells = row.findAll("td")
         if table_cells: 
             link = table_cells[0].find('a');
             record['Application Number'] = link.text
             record['Application Link']   = BASE_URL + '/postingplans/' + link['href']
             record['Application Type']   = table_cells[1].text
             record['Review Status']      = table_cells[2].text
             record['Status Date']        = table_cells[3].text

             # fetch each 'Application Link' page and scrape further details
             record = scrape_application(record['Application Link'], record)

             # Print out the data we've gathered
             print record, '------------'

             # Finally, save the record to the datastore
             latlng_tmp = None
             if len(record['Addresses']) > 0:
                 record['Primary_Address'] = record['Addresses'][0]['address']
                 latlng_tmp = record['Addresses'][0]['latlng']
             scraperwiki.datastore.save(["Application Number"],record, latlng=latlng_tmp)

def scrape_application(app_url, record):
    html = scraperwiki.scrape(app_url)
    soup = BeautifulSoup(html) 

    items = soup.findAll("div", { "class": "appDetailValue" } )

    for item in items:
        print item.findNext('div', {'class' : 'label'}).text

    

    # 0 - Return to search results
    # 1 - Application Number
    record['Date Received'] = items[2].findNext('div', {"class" : "appDetailValue" }).text

    # Address, including lat/long
    latlng_re = re.compile(r"LAT=([-\d\.]+)&LON=([-\d\.]+)")
    addr_info = items[3].findNext('div', {"class" : "appDetailValue" })
    if addr_info:
        record['Addresses'] = []
        addr_items = addr_info.findAll('a')
        for addr_a in addr_items:
            # <a href="http://apps104.ottawa.ca/emap?emapver=lite&LAT=45.323884&LON=-75.952962&featname=870+Huntmar+Drive&amp;lang=en"
            match = latlng_re.search(addr_a['href'])
            latlng = None
            if match:
                latlng = [ float(match.group(1)), float(match.group(2)) ]
            record['Addresses'].append( { "address": addr_a.text, "latlng": latlng } )
            

    # TODO: parse ward
    record['Ward'] = items[4].findNext('div', {"class" : "appDetailValue" }).text
    # 5 - Application
    # 6 - Review Status
    # 7 - Status Date
    record['Description'] = items[8].findNext('div', {"class" : "appDetailValue" }).text
    # 9 - Supporting Documents heading
    # 10 - useless comment
    # 11 - disclaimer
    # 12 - actual supporting document links  (TODO: want this)
    # 13 - adobe d/l link
    # 14 - file lead header
    record['File Lead Name'] = items[15].findNext('div', {"class" : "appDetailValue" }).text
    record['File Lead Telephone'] = items[16].findNext('div', {"class" : "appDetailValue" }).text

    return record

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_all(url):
    next_url = url
    while next_url:
        print "Fetching " + next_url
        html = scraperwiki.scrape(next_url)
        soup = BeautifulSoup(html)
        scrape_table(soup)

        text_next = soup.find(text=re.compile("^Next"))

        if text_next:
            next_url = BASE_URL + text_next.parent['href']
        else:
            next_url = None

scrape_all(STARTING_URL)