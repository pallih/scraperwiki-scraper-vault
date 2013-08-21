###############################################################################
# Ottawa City Council Scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup, Tag

def scrape_councillor(url, record):
    record["URL"] = url
    soup = BeautifulSoup(scraperwiki.scrape(record["URL"]))
    table1 = soup.find("table")
    table2 = table1.find("table")
    table3 = table2.find("table")
    img = table2.find("img")
    if img:
        record["Image"] = "http://www.ottawa.ca/city_hall/mayor_council/councillors/" + img["src"].strip()
    for m in table3.findAll("i"):
        prop = m.text.strip()
        p = m.parent.parent
        m.extract()
        #v = m.parent.nextSibling.nextSibling
        #value = v.text.strip() if isinstance(v, Tag) else v.strip()
        value = p.text.strip()
        record[prop] = value

def parse_ward(ward_name):
    ward = {}
    matches = re.search("^Ward (\d+) - (.+)$", ward_name, re.MULTILINE)
    ward["Number"] = matches.group(1).strip()
    ward["Name"] = matches.group(2).strip()
    return ward

# retrieve a page
starting_url = 'http://www.ottawa.ca/city_hall/mayor_council/councillors/index_en.html'
soup = BeautifulSoup(scraperwiki.scrape(starting_url))

# use BeautifulSoup to get all <td> tags
columns = soup.findAll("td", { "valign" : "top"}) 
for column in columns:
    links = column.findAll("a", { "target" : "_top" })
    if len(links) > 0:
        name = links[0].text.replace("Councillor", "").strip()
        ward_data = parse_ward(links[1].text.replace("&#8211;", "-").strip())
        record = { "Name" : name, "Ward Number" : ward_data.group(1).strip() , "Ward Name" : ward_data.group(2).strip() }
        scrape_councillor("http://www.ottawa.ca" + links[0]['href'], record)
        print record
        # save records to the datastore
        #scraperwiki.datastore.save(["Name"], record)
    