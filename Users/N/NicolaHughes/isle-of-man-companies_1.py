# Using OpenCorporates.com

import scraperwiki
import json

url = "http://api.opencorporates.com/companies/search?jurisdiction_code=im&exclude_inactive=true&per_page=100&page="

for n in range(1,300):
    info = scraperwiki.scrape(url + str(n))
    search = json.loads(info)
    companies = search["results"]["companies"]
    for company in companies:
        id = company["company"]["company_number"]
        name = company["company"]["name"]
        jurisdiction = company["company"]["jurisdiction_code"]
        data = {"id":id, "name":name, "jurisdiction":jurisdiction}
        scraperwiki.sqlite.save(["id"], data)

# Using OpenCorporates.com

import scraperwiki
import json

url = "http://api.opencorporates.com/companies/search?jurisdiction_code=im&exclude_inactive=true&per_page=100&page="

for n in range(1,300):
    info = scraperwiki.scrape(url + str(n))
    search = json.loads(info)
    companies = search["results"]["companies"]
    for company in companies:
        id = company["company"]["company_number"]
        name = company["company"]["name"]
        jurisdiction = company["company"]["jurisdiction_code"]
        data = {"id":id, "name":name, "jurisdiction":jurisdiction}
        scraperwiki.sqlite.save(["id"], data)

