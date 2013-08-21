###############################################################################
# Grande Prairie Mayor and Council Scraper
###############################################################################

import scraperwiki
import re
import json
from BeautifulSoup import BeautifulSoup

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')

def scrape_councillor(tr, record):
    tds = tr.findAll("td");
    expression = re.compile(r'(\S+),\s+(\S+)')
    record["boundary_url"] = "/boundaries/census-subdivisions/4819012/"
    record["name"] = expression.sub(r'\2 \1', tds[0].findNext("a").text);
    record["elected_office"] = tds[1].string;
    record["offices"] = json.dumps([{'tel': tds[3].string}])
    record["email"] = tds[4].findNext("a")["href"].replace("mailto:","")
    firstName, lastName = record["name"].lower().split(' ', 1)

    for link in photolinks:
        #if not link.string:
         #   continue
        if link.string and firstName in link.string.lower() and lastName in link.string.lower():
            record["source_url"] = base + link["href"]
            soup = BeautifulSoup(scraperwiki.scrape(base+link["href"]))
            for img in soup.findAll("img"):
                if firstName in img["alt"].lower() and lastName in img["alt"].lower():
                    record["photo_url"] = base+img["src"]
    
    scraperwiki.sqlite.save(["name"], record)
    return

photo_url = 'http://www.cityofgp.com/index.aspx?page=719'
soup = BeautifulSoup(scraperwiki.scrape(photo_url))
photolinks = soup.findAll("a");
        
# retrieve a page
starting_url = 'http://www.cityofgp.com/index.aspx?page=718'
soup = BeautifulSoup(scraperwiki.scrape(starting_url))
base = 'http://www.cityofgp.com/';

for tr in soup.findAll("tr"):
    if "listtable_header" in str(tr):
        continue
    record = {}
    scrape_councillor(tr, record);  
