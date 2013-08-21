# -*- coding: utf-8 -*-
###############################################################################
# Quebec MLA Scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')

def clean_up_name(name):
    name = name.replace("&nbsp;", " ").strip()
    last_name, first_name = [n.strip() for n in name.split(",")]
    return {
        "last_name": last_name,
        "first_name": first_name
    }

# retrieve a page
starting_url = 'http://www.assnat.qc.ca/en/deputes/index.html'
soup = BeautifulSoup(scraperwiki.scrape(starting_url))

# use BeautifulSoup to get all <td> tags
table = soup.find("table", { "id" : "ListeDeputes" })
base_record = {
    "elected_office": "MNA",
    "source_url": starting_url
}

for row in table.find("tbody").findAll("tr"):
    record = base_record.copy()
    columns = row.findAll('td')
    
    record.update( # get name, last_name and first_name
        clean_up_name(columns[0].text)
    )
    record["url"] = "http://www.assnat.qc.ca" + columns[0].find("a")["href"].strip()
    record["district_name"] = columns[1].text.strip()

    party_name = columns[2].text.strip()
    if party_name == u'Ind\xe9pendante':
        party_name = u"Indépendant"

    record["party_name"] = party_name
    email_link = columns[3].find("a")
    if email_link:
        record["email"] = columns[3].find("a")["href"].replace("mailto:","").strip()
    
    # save records to the datastore
    scraperwiki.sqlite.save(["district_name"], record)
