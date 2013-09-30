###############################################################################
# Manitoba MLA Scaper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

def reorder_name(name):
    name = name.replace("&nbsp;", " ")
    name_parts = name.split(",")
    if len(name_parts) > 1:
        return name_parts[1].strip() + ' ' + name_parts[0].strip().title()
    else:
        return name

# retrieve a page
starting_url = "http://www.gov.mb.ca/legislature/members/alphabetical.html"
soup = BeautifulSoup(scraperwiki.scrape(starting_url))

# use BeautifulSoup to get all <td> tags
table = soup.findAll("table")[1]
for row in table.findAll("tr")[1:]:
    cols = row.findAll("td")
    record = {}
    record["Name"] = reorder_name(cols[0].text.strip())
    record["Constituency"] = cols[1].text.replace("&nbsp;", " ").strip().title()
    record["Party"] = cols[2].text.strip()
    #record["Telephone"] = cols[3].text.strip()
    #record["Fax"] = cols[4].text.strip()
    #record["Email"] = cols[5].text.replace("&nbsp;", " ").strip()
    # save records to the datastore
    scraperwiki.sqlite.save(["Name"], record) 
    ###############################################################################
# Manitoba MLA Scaper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

def reorder_name(name):
    name = name.replace("&nbsp;", " ")
    name_parts = name.split(",")
    if len(name_parts) > 1:
        return name_parts[1].strip() + ' ' + name_parts[0].strip().title()
    else:
        return name

# retrieve a page
starting_url = "http://www.gov.mb.ca/legislature/members/alphabetical.html"
soup = BeautifulSoup(scraperwiki.scrape(starting_url))

# use BeautifulSoup to get all <td> tags
table = soup.findAll("table")[1]
for row in table.findAll("tr")[1:]:
    cols = row.findAll("td")
    record = {}
    record["Name"] = reorder_name(cols[0].text.strip())
    record["Constituency"] = cols[1].text.replace("&nbsp;", " ").strip().title()
    record["Party"] = cols[2].text.strip()
    #record["Telephone"] = cols[3].text.strip()
    #record["Fax"] = cols[4].text.strip()
    #record["Email"] = cols[5].text.replace("&nbsp;", " ").strip()
    # save records to the datastore
    scraperwiki.sqlite.save(["Name"], record) 
    