###############################################################################
# Saskatchewan MLA Scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def getName(node):
    links = node.findAll("a")
    [link.extract() for link in links]
    return node.text.strip()

def getLink(node):
    link = node.find("a")
    if link:
        return link["href"]
    else:
        return ""

# retrieve a page
starting_url = "http://www.legassembly.sk.ca/members/mla_list.htm"
content = scraperwiki.scrape(starting_url)
content = content.replace('&nbsp;',' ')
soup = BeautifulSoup(content, fromEncoding='iso-8859-1', smartQuotesTo=None)

# use BeautifulSoup to get all <td> tags
table = soup.findAll("table")[4]
for row in table.findAll("tr", recursive=False)[2:]:
    record = {}
    cols = row.findAll("td", recursive=False)
    record["Name"] = getName(cols[0])
    record["Party"] = cols[1].text.strip()
    record["Website"] = getLink(cols[2])
    record["Constituency"] = getName(cols[2])
    record["Phone"] = cols[4].text.strip()
    record["Fax"] = cols[5].text.strip()
    # save records to the datastore
    scraperwiki.sqlite.save(["Name"], record) 
    