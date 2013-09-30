###############################################################################
# Strathcona County Mayor and Council Scraper
###############################################################################

import scraperwiki
import re
import json
from BeautifulSoup import BeautifulSoup

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')

def scrape_councillor(link, record):
    record["name"] = None
    record["url"]  = link
    record["source_url"] = "http://www.strathcona.ab.ca/local_government/mayor-councillors.aspx"
    match = re.search("Mayor.+?([A-Z](\w+\-?){2,})", link)
    if match != None:
            name = match.group(1)
            name = name.replace("-", " ")
            record["name"] = name
            record["elected_office"] = "Mayor"
            record["boundary_url"] = "/boundaries/census-subdivisions/4811052/"

    linksoup = BeautifulSoup(scraperwiki.scrape(link))
    lines = linksoup.prettify();
    lines = lines.split("\n");
    for img in linksoup.findAll("img"):
        if "photo of" in img["alt"].lower() or "ph" in img["src"].lower():
            record["photo_url"] = base+img["src"]; 
    for idx, line in enumerate(lines):
        
        
        match = re.search("Ward\s+(\d+).+Councillor\s+([A-Z](\w+\s+){2,})", line)
        if match != None:
            record["name"] = match.group(2).strip()
            record["district_id"] = match.group(1);
            record["elected_office"] = "Councillor";
        match = re.search("mailto:([^\"]+)", line); 
        if match != None:
            record["email"] = match.group(1);
    if record["name"] != None:
        scraperwiki.sqlite.save(["name"], record)

        
# retrieve a page
starting_url = 'http://www.strathcona.ab.ca/local_government/Councillors/ward-1.aspx'
soup = BeautifulSoup(scraperwiki.scrape(starting_url))
base = 'http://www.strathcona.ab.ca';

for link in soup.findAll("a"):

    if "Mayor " not in str(link) and "Councillor " not in str(link):
        continue
    record = {}
    scrape_councillor(base+str(link['href']), record);  
###############################################################################
# Strathcona County Mayor and Council Scraper
###############################################################################

import scraperwiki
import re
import json
from BeautifulSoup import BeautifulSoup

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')

def scrape_councillor(link, record):
    record["name"] = None
    record["url"]  = link
    record["source_url"] = "http://www.strathcona.ab.ca/local_government/mayor-councillors.aspx"
    match = re.search("Mayor.+?([A-Z](\w+\-?){2,})", link)
    if match != None:
            name = match.group(1)
            name = name.replace("-", " ")
            record["name"] = name
            record["elected_office"] = "Mayor"
            record["boundary_url"] = "/boundaries/census-subdivisions/4811052/"

    linksoup = BeautifulSoup(scraperwiki.scrape(link))
    lines = linksoup.prettify();
    lines = lines.split("\n");
    for img in linksoup.findAll("img"):
        if "photo of" in img["alt"].lower() or "ph" in img["src"].lower():
            record["photo_url"] = base+img["src"]; 
    for idx, line in enumerate(lines):
        
        
        match = re.search("Ward\s+(\d+).+Councillor\s+([A-Z](\w+\s+){2,})", line)
        if match != None:
            record["name"] = match.group(2).strip()
            record["district_id"] = match.group(1);
            record["elected_office"] = "Councillor";
        match = re.search("mailto:([^\"]+)", line); 
        if match != None:
            record["email"] = match.group(1);
    if record["name"] != None:
        scraperwiki.sqlite.save(["name"], record)

        
# retrieve a page
starting_url = 'http://www.strathcona.ab.ca/local_government/Councillors/ward-1.aspx'
soup = BeautifulSoup(scraperwiki.scrape(starting_url))
base = 'http://www.strathcona.ab.ca';

for link in soup.findAll("a"):

    if "Mayor " not in str(link) and "Councillor " not in str(link):
        continue
    record = {}
    scrape_councillor(base+str(link['href']), record);  
