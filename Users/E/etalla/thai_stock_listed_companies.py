## Retrieves the names and stock symbols of all the companies listed on Thai Stock Exchange in the Agro and Food Industry.

import scraperwiki
import lxml.html

root = scraperwiki.scrape("http://www.set.or.th/listedcompany/static/listedCompanies_en_US.xls")
root = lxml.html.fromstring(root)

companies = root.cssselect("tr")
company = {}

for row in companies:
    details = row.cssselect("td")
    for line in details:
        if line.text_content() == "Agro & Food Industry":
            company["symbol"] = row[0].text_content().strip()
            company["name"]= row[1].text_content().strip()
            scraperwiki.sqlite.save(["symbol", "name"], company)
            
## Retrieves the names and stock symbols of all the companies listed on Thai Stock Exchange in the Agro and Food Industry.

import scraperwiki
import lxml.html

root = scraperwiki.scrape("http://www.set.or.th/listedcompany/static/listedCompanies_en_US.xls")
root = lxml.html.fromstring(root)

companies = root.cssselect("tr")
company = {}

for row in companies:
    details = row.cssselect("td")
    for line in details:
        if line.text_content() == "Agro & Food Industry":
            company["symbol"] = row[0].text_content().strip()
            company["name"]= row[1].text_content().strip()
            scraperwiki.sqlite.save(["symbol", "name"], company)
            
