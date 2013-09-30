import scraperwiki
import re
from bs4 import BeautifulSoup

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')

url = 'http://www.city.sault-ste-marie.on.ca/Open_Page.aspx?ID=174&deptid=1'
soup = BeautifulSoup(scraperwiki.scrape(url))
base = 'http://www.city.sault-ste-marie.on.ca/'

#mayor
fields = soup.findAll(size="1")

record = {}
record["source_url"] = url
record["photo_url"] = "http://www.city.sault-ste-marie.on.ca" + fields[1].find_next("img")["src"]
record["district_name"] = " ".join(fields[0].contents[:1])
if "Mayor" in record["district_name"]:
    record["elected_office"] = "Mayor"
    record["boundary_url"] = "/boundaries/census-subdivisions/3557061/"
record["name"] = fields[1].find_next("strong").string
record["email"] = fields[2].find_next("a")["href"].replace("mailto:","")

scraperwiki.sqlite.save([], record)

#councillors - start at 4th tds in list
c = soup.find("div", id="litcontentDiv")
t = c.findAll("tbody")[0]
tds = t.findAll("td")

for i in range(1, len(tds))[3:]:

    # skip every 3rd tds
    if not i % 3: continue
    td = tds[i]

    record = {}
    record["source_url"] = url
    record["photo_url"] = "http://www.city.sault-ste-marie.on.ca" + td.find_next("img")["src"]
    record["district_name"] = td.find_next("img")["alt"].split("-")[1].strip()
    record["elected_office"] = "Councillor"
    record["name"] = td.find_next("img")["alt"].split("-")[2].strip()
    record["email"] = td.find_next("a")["href"].replace("mailto:","")
    if '@' in record["email"]:
        record["email"] = re.sub(r'\?.+', '', record["email"])
    else:
        record.pop("email", None)
        
    scraperwiki.sqlite.save([], record)

import scraperwiki
import re
from bs4 import BeautifulSoup

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')

url = 'http://www.city.sault-ste-marie.on.ca/Open_Page.aspx?ID=174&deptid=1'
soup = BeautifulSoup(scraperwiki.scrape(url))
base = 'http://www.city.sault-ste-marie.on.ca/'

#mayor
fields = soup.findAll(size="1")

record = {}
record["source_url"] = url
record["photo_url"] = "http://www.city.sault-ste-marie.on.ca" + fields[1].find_next("img")["src"]
record["district_name"] = " ".join(fields[0].contents[:1])
if "Mayor" in record["district_name"]:
    record["elected_office"] = "Mayor"
    record["boundary_url"] = "/boundaries/census-subdivisions/3557061/"
record["name"] = fields[1].find_next("strong").string
record["email"] = fields[2].find_next("a")["href"].replace("mailto:","")

scraperwiki.sqlite.save([], record)

#councillors - start at 4th tds in list
c = soup.find("div", id="litcontentDiv")
t = c.findAll("tbody")[0]
tds = t.findAll("td")

for i in range(1, len(tds))[3:]:

    # skip every 3rd tds
    if not i % 3: continue
    td = tds[i]

    record = {}
    record["source_url"] = url
    record["photo_url"] = "http://www.city.sault-ste-marie.on.ca" + td.find_next("img")["src"]
    record["district_name"] = td.find_next("img")["alt"].split("-")[1].strip()
    record["elected_office"] = "Councillor"
    record["name"] = td.find_next("img")["alt"].split("-")[2].strip()
    record["email"] = td.find_next("a")["href"].replace("mailto:","")
    if '@' in record["email"]:
        record["email"] = re.sub(r'\?.+', '', record["email"])
    else:
        record.pop("email", None)
        
    scraperwiki.sqlite.save([], record)

