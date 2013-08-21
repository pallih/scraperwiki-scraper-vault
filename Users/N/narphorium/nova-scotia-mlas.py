###############################################################################
# Nova Scotia MLA 
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

def unescape_entities(text):
    return BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)

def scrape_mla(url, record):
    soup = BeautifulSoup(scraperwiki.scrape(url), fromEncoding='UTF-8', smartQuotesTo=None)
    content = soup.find("div", {'id':'content'})
    sidebar = soup.find("div", {'class':'sidebar'})
    img = sidebar.find("img")
    record["Image"] = "http://www.gov.ns.ca/legislature" + img["src"].strip()[5:] if img else ""
    record["Biography"] = ""
    record["Email"] = ""
    for link in sidebar.findAll("a"):
        if link.text.strip() == "Caucus Biography":
            record["Biography"] = "http://www.gov.ns.ca/legislature/MEMBERS" + link["href"][2:].strip() if link["href"].startswith("../") else link["href"].strip()
    address_text = sidebar.find("dl", {"class":"address"}).text.strip()
    m1 = re.search("Phone:\s+(\(\d{3}\)\s+\d{3}-\d{4})", address_text)
    record["Telephone"] = m1.group(1) if m1 else ""
    m2 = re.search("Fax:\s+(\(\d{3}\)\s+\d{3}-\d{4})", address_text)
    record["Fax"] = m2.group(1) if m2 else ""

def reorder_name(name):
    name = name.replace("&nbsp;", " ")
    name_parts = name.split(",")
    if len(name_parts) > 1:
        return name_parts[1].strip() + ' ' + name_parts[0].strip()
    else:
        return name

party_names = {
    "" : "",
    "PC"  : "Progressive Conservative Party",
    "Liberal"   : "Liberal Party",
    "NDP" : "New Democratic Party",
    "Independent"   : "Independent"     
}

# retrieve a page
starting_url = "http://nslegislature.ca/index.php/people/members/sort/name/"
soup = BeautifulSoup(scraperwiki.scrape(starting_url))

table = soup.find("div", {'id' : 'content'}).find("table", {"class" : "status"})
for row in table.find("tbody").findAll("tr")[1:]:
    cols = row.findAll("td")
    record = {}
    record["Name"] = reorder_name(cols[0].text.strip())
    record["Party"] = party_names[cols[1].text.strip()]
    record["Constituency"] = cols[2].text.replace("&nbsp;"," ").strip()
    scrape_mla(cols[0].find("a")["href"].strip(), record)
    scraperwiki.sqlite.save(["Name"], record)
