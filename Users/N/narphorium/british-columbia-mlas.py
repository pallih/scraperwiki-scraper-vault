##############################################################################
# British Columbia MLA Scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup, Tag

def scrape_mla(url):
    record = {}
    record["URL"] = url
    try:
        soup = BeautifulSoup(scraperwiki.scrape(record["URL"]))
        table1 = soup.find("table", { "width" : "440" })
        paragraphs = table1.findAll("p")
        record["Name"] = paragraphs[0].text.replace("MLA:","").replace("&nbsp;"," ").strip()
        record["Riding"] = paragraphs[1].text.strip()
        record["Role"] = paragraphs[2].text.strip() if not re.search("Elected:", paragraphs[2].text) else ""
        img = table1.find("img")
        record["Image"] = record["URL"][0:record["URL"].rindex("/")+1] + img["src"].strip() if img else ""
        table2 = soup.find("table", { "width" : "466" })
        record["Email"] = ""
        record["Website"] = ""
        if table2:
            links = table2.findAll("a")
            record["Email"] = links[0].text.strip() if len(links) > 0 else ""
            record["Website"] = "http://" + links[1].text.strip() if len(links) > 1 else ""
    except:
        record = None
    return record

# retrieve a page
starting_url = 'http://www.leg.bc.ca/mla/3-1-6.htm'
soup = BeautifulSoup(scraperwiki.scrape(starting_url))

# use BeautifulSoup to get all <td> tags
#header = soup.find(text="Alphabetical List by MLA Name:")
table = soup.find("table", { "align" : "center" })
for link in table.findAll("a"):
    record = scrape_mla("http://www.leg.bc.ca/mla/" + link['href'])
    # save records to the datastore
    if record:
        scraperwiki.sqlite.save(["Name"], record)
    ##############################################################################
# British Columbia MLA Scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup, Tag

def scrape_mla(url):
    record = {}
    record["URL"] = url
    try:
        soup = BeautifulSoup(scraperwiki.scrape(record["URL"]))
        table1 = soup.find("table", { "width" : "440" })
        paragraphs = table1.findAll("p")
        record["Name"] = paragraphs[0].text.replace("MLA:","").replace("&nbsp;"," ").strip()
        record["Riding"] = paragraphs[1].text.strip()
        record["Role"] = paragraphs[2].text.strip() if not re.search("Elected:", paragraphs[2].text) else ""
        img = table1.find("img")
        record["Image"] = record["URL"][0:record["URL"].rindex("/")+1] + img["src"].strip() if img else ""
        table2 = soup.find("table", { "width" : "466" })
        record["Email"] = ""
        record["Website"] = ""
        if table2:
            links = table2.findAll("a")
            record["Email"] = links[0].text.strip() if len(links) > 0 else ""
            record["Website"] = "http://" + links[1].text.strip() if len(links) > 1 else ""
    except:
        record = None
    return record

# retrieve a page
starting_url = 'http://www.leg.bc.ca/mla/3-1-6.htm'
soup = BeautifulSoup(scraperwiki.scrape(starting_url))

# use BeautifulSoup to get all <td> tags
#header = soup.find(text="Alphabetical List by MLA Name:")
table = soup.find("table", { "align" : "center" })
for link in table.findAll("a"):
    record = scrape_mla("http://www.leg.bc.ca/mla/" + link['href'])
    # save records to the datastore
    if record:
        scraperwiki.sqlite.save(["Name"], record)
    