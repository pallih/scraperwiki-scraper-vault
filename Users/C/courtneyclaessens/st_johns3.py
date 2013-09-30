import scraperwiki
import re 
from bs4 import BeautifulSoup

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')

url = 'http://www.stjohns.ca/city-hall/about-city-hall/council'
soup = BeautifulSoup(scraperwiki.scrape(url))
base = 'http://www.stjohns.ca/'

rows = soup.findAll("div", "views-row")
for row in rows:
    fields = row.findAll(class_="field-content")
    record = {}
    record["source_url"] = url
    if "Ward" in fields[0].string:
        record["district_name"] = fields[0].string
    record["photo_url"] = fields[1].find_next("img")["src"]
    record["elected_office"] = fields[2].string.split()[0]
    if record["elected_office"] == 'Deputy-Mayor':
        record["elected_office"] = 'Deputy Mayor'
    record["name"] = " ".join(fields[2].string.split()[1:])
    # offices.tel fields[3].string
    record["email"] = fields[4].find_next("a")["href"].replace("mailto:", "").strip()
    record["url"] = "http://www.stjohns.ca" + fields[2].find_next("a")["href"]
    if "district_name" not in record:
        record["boundary_url"] = "/boundaries/census-subdivisions/1001519/"

    scraperwiki.sqlite.save(["name"], record)

import scraperwiki
import re 
from bs4 import BeautifulSoup

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')

url = 'http://www.stjohns.ca/city-hall/about-city-hall/council'
soup = BeautifulSoup(scraperwiki.scrape(url))
base = 'http://www.stjohns.ca/'

rows = soup.findAll("div", "views-row")
for row in rows:
    fields = row.findAll(class_="field-content")
    record = {}
    record["source_url"] = url
    if "Ward" in fields[0].string:
        record["district_name"] = fields[0].string
    record["photo_url"] = fields[1].find_next("img")["src"]
    record["elected_office"] = fields[2].string.split()[0]
    if record["elected_office"] == 'Deputy-Mayor':
        record["elected_office"] = 'Deputy Mayor'
    record["name"] = " ".join(fields[2].string.split()[1:])
    # offices.tel fields[3].string
    record["email"] = fields[4].find_next("a")["href"].replace("mailto:", "").strip()
    record["url"] = "http://www.stjohns.ca" + fields[2].find_next("a")["href"]
    if "district_name" not in record:
        record["boundary_url"] = "/boundaries/census-subdivisions/1001519/"

    scraperwiki.sqlite.save(["name"], record)

