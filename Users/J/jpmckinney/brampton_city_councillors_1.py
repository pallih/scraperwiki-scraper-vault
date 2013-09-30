import scraperwiki
import json
import re

from BeautifulSoup import BeautifulSoup

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DELETE FROM `swdata`')

url = "http://www.brampton.ca/en/City-Hall/CouncilOffice/Pages/Welcome.aspx"
s = BeautifulSoup(scraperwiki.scrape(url))
cards = s.findAll("div", {"class":"councillorCard"})

postal = "City of Brampton\n2 Wellington St. West\nBrampton, ON\nL6Y 4R2"

for card in cards:

    record = {}
    record["source_url"] = url
    record["elected_office"] = "Councillor"
    name = card.find("div", {"class":"councillorInfo"}).text
    name = re.findall('[A-Z][^A-Z]*',name)
    record["name"] =  name[2].strip()+" "+name[3]
    record["email"] = card.find("div", "emailInfo").text

    tx = card.find("div", "wardInfo")

    offices = [{
        "tel": tx.contents[2],
        "type": "constituency",
        "postal": postal
    }]
    record["offices"] = json.dumps(offices)

    w = tx.contents[0].split(" ")
    wards = [w[1], w[3]]

    for i in wards:
        record["district_name"] = "Ward " + i
        scraperwiki.sqlite.save([], record)


# mayor
url = "http://www.brampton.ca/EN/City-Hall/Office-Mayor/Pages/Welcome.aspx"
s = BeautifulSoup(scraperwiki.scrape(url))
c = s.find('div', {"class":"address"}) 
pic = s.find('img',{"class":"mayorsPic"})


record = {}
record["source_url"] = url
record["elected_office"] = "Mayor"
record["boundary_url"] = "/boundaries/census-subdivisions/3521010/"
record["name"] = pic.get('alt','').replace("Mayor","").strip()
record["email"] = c.find("a").text
tel_search = re.search('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',c.text)
 
offices = [{
        
    "tel" : tel_search.string[tel_search.start() : tel_search.end()], 
    "type": "constituency",
    "postal": postal
}]
record["offices"] = json.dumps(offices)



scraperwiki.sqlite.save([], record)import scraperwiki
import json
import re

from BeautifulSoup import BeautifulSoup

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DELETE FROM `swdata`')

url = "http://www.brampton.ca/en/City-Hall/CouncilOffice/Pages/Welcome.aspx"
s = BeautifulSoup(scraperwiki.scrape(url))
cards = s.findAll("div", {"class":"councillorCard"})

postal = "City of Brampton\n2 Wellington St. West\nBrampton, ON\nL6Y 4R2"

for card in cards:

    record = {}
    record["source_url"] = url
    record["elected_office"] = "Councillor"
    name = card.find("div", {"class":"councillorInfo"}).text
    name = re.findall('[A-Z][^A-Z]*',name)
    record["name"] =  name[2].strip()+" "+name[3]
    record["email"] = card.find("div", "emailInfo").text

    tx = card.find("div", "wardInfo")

    offices = [{
        "tel": tx.contents[2],
        "type": "constituency",
        "postal": postal
    }]
    record["offices"] = json.dumps(offices)

    w = tx.contents[0].split(" ")
    wards = [w[1], w[3]]

    for i in wards:
        record["district_name"] = "Ward " + i
        scraperwiki.sqlite.save([], record)


# mayor
url = "http://www.brampton.ca/EN/City-Hall/Office-Mayor/Pages/Welcome.aspx"
s = BeautifulSoup(scraperwiki.scrape(url))
c = s.find('div', {"class":"address"}) 
pic = s.find('img',{"class":"mayorsPic"})


record = {}
record["source_url"] = url
record["elected_office"] = "Mayor"
record["boundary_url"] = "/boundaries/census-subdivisions/3521010/"
record["name"] = pic.get('alt','').replace("Mayor","").strip()
record["email"] = c.find("a").text
tel_search = re.search('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',c.text)
 
offices = [{
        
    "tel" : tel_search.string[tel_search.start() : tel_search.end()], 
    "type": "constituency",
    "postal": postal
}]
record["offices"] = json.dumps(offices)



scraperwiki.sqlite.save([], record)