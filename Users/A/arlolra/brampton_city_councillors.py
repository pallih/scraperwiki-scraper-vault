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
    record["name"] = card.find("div", {"class":"councillorInfo"}).text.replace("City Councillor","")
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
        print record
        scraperwiki.sqlite.save([], record)


# mayor
url = "http://www.brampton.ca/EN/City-Hall/Office-Mayor/Pages/Welcome.aspx"
s = BeautifulSoup(scraperwiki.scrape(url))

c = s.find("div", "address").replace("<br /"," ")

pic = s.find('img',{"class":"mayorsPic"})


record = {}
record["source_url"] = url
record["elected_office"] = "Mayor"
record["boundary_url"] = "/boundaries/census-subdivisions/3521010/"
record["name"] = pic.get('alt','').replace("Mayor","")
record["email"] = c.find("a").text
tel_search = re.search('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',c)
 
offices = [{
        
    "tel" : tel_search.string[tel_search.start() : tel_search.end()], 
    "type": "constituency",
    "postal": postal
}]
record["offices"] = json.dumps(offices)


print record
scraperwiki.sqlite.save([], record)