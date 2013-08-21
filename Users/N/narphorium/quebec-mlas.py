###############################################################################
# Quebec MLA Scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def reorder_name(name):
    name = name.replace("&nbsp;", " ")
    name_parts = name.split(",")
    return name_parts[1].strip() + ' ' + name_parts[0].strip()

# retrieve a page
starting_url = 'http://www.assnat.qc.ca/en/deputes/index.html'
soup = BeautifulSoup(scraperwiki.scrape(starting_url))

# use BeautifulSoup to get all <td> tags
table = soup.find("table", { "id" : "ListeDeputes" })
for row in table.find("tbody").findAll("tr"):
    record = {}
    columns = row.findAll('td')
    record["Name"] = reorder_name(columns[0].text.replace("&nbsp;"," ").strip())
    record["URL"] = "http://www.assnat.qc.ca" + columns[0].find("a")["href"].strip()
    record["Riding"] = columns[1].text.strip()
    record["Party"] = columns[2].text.strip()
    email_link = columns[3].find("a")
    if email_link:
        record["Email"] = columns[3].find("a")["href"].replace("mailto:","").strip()
    
    # save records to the datastore
    scraperwiki.sqlite.save(["Name"], record) 
    