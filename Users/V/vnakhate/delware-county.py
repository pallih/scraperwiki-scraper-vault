import scraperwiki

# Blank Python


import scraperwiki
import json

from BeautifulSoup import BeautifulSoup


#scraperwiki.sqlite.execute('DROP TABLE `swdata`')


url = "http://www.brampton.ca/en/City-Hall/CouncilOffice/Pages/Welcome.aspx"
s = BeautifulSoup(scraperwiki.scrape(url))

c = s.find("div", id="Content")
t = c.findAll("table")[0]
tds = t.findAll("td")

for i in range(1, len(tds) + 1):

    # skip every 3rd td
    if not i % 3: continue
    td = tds[i - 1]

    record = {}
    record["source_url"] = url
    record["elected_office"] = "Councillor"
    record["name"] = td.find("div", "councillorInfo").find("a").contents[2]
    record["email"] = td.find("div", "emailInfo").text

    tx = td.find("div", "wardInfo")
    record["district_name"] = tx.contents[0]

    offices = [{
        "tel": tx.contents[2],
        "type": "constituency",
        "postal": "City of Brampton\n2 Wellington St. West\nBrampton, ON\nL6Y 4R2"
    }]
    record["offices"] = json.dumps(offices)

    print record
    scraperwiki.sqlite.save(['name'], record)



import scraperwiki

# Blank Python


import scraperwiki
import json

from BeautifulSoup import BeautifulSoup


#scraperwiki.sqlite.execute('DROP TABLE `swdata`')


url = "http://www.brampton.ca/en/City-Hall/CouncilOffice/Pages/Welcome.aspx"
s = BeautifulSoup(scraperwiki.scrape(url))

c = s.find("div", id="Content")
t = c.findAll("table")[0]
tds = t.findAll("td")

for i in range(1, len(tds) + 1):

    # skip every 3rd td
    if not i % 3: continue
    td = tds[i - 1]

    record = {}
    record["source_url"] = url
    record["elected_office"] = "Councillor"
    record["name"] = td.find("div", "councillorInfo").find("a").contents[2]
    record["email"] = td.find("div", "emailInfo").text

    tx = td.find("div", "wardInfo")
    record["district_name"] = tx.contents[0]

    offices = [{
        "tel": tx.contents[2],
        "type": "constituency",
        "postal": "City of Brampton\n2 Wellington St. West\nBrampton, ON\nL6Y 4R2"
    }]
    record["offices"] = json.dumps(offices)

    print record
    scraperwiki.sqlite.save(['name'], record)



