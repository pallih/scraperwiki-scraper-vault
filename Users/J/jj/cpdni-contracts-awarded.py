# CPDNI Contracts Awarded Scraper 2010-2011
# Broken, only noticed after running it that they change the format and data month to month, easier to do manually than to work around

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

scraperwiki.metadata.save('data_columns', ['Start Date', 'Winning Supplier', 'Supplier Address', 'Contract Title', 'Contract Value', 'Contract Shared'])

def scrape_for_links(url):
    print "get the links from "+url
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    main = soup.find("div", {"id" : "main"}) 
    next_link = main.findAll("a")
    for a in next_link:
        data_url = base_url + a['href']
        scrape_for_data(data_url)

def scrape_for_data(url):
    print "get the data from "+url
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    tds = soup.find("table", { "id" : "data1" } )
    rows = tds.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['Start Date'] = table_cells[0].text
            record['Winning Supplier'] = table_cells[1].text
            record['Supplier Address'] = table_cells[2].text
            record['Contract Title'] = table_cells[3].text
            record['Contract Value'] = re.sub(',', '', (re.sub("&#163;", '', (re.sub(".\d\d$", '', table_cells[4].text)))))            
#            record['Contract Value'] = table_cells[4].text
            record['Contract Shared'] = "U" 
            print record
            scraperwiki.datastore.save(["Winning Supplier"], record)

# Start
base_url = 'http://www.dfpni.gov.uk/'
start_path = 'index/procurement-2/cpd/cpd-suppliers/cpd_contracts_awarded_2010_-_2011.htm'
scrape_for_links(base_url + start_path)
