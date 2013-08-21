"""
Australian stock exchange

This scraper retrieves stock symbols, company links and names of all the companies listed on the Australian stock exchange.

"""

import lxml.html
import scraperwiki

# The list of companies is divided across sector pages. 
# So first let's fetch the sectors' URL codes and names and store them in a dictionary.

url_sectors = "http://www.asx.com.au/asx/markets/equityPrices.do"
root = lxml.html.fromstring(scraperwiki.scrape(url_sectors))
ASX_sectors = {} 

options = root.cssselect("option")

for i in options[1:]:
    ASX_sectors[i.text_content()]=i.get("value")

# Now let's get the list of companies and their individual pages and symbols across each sector
    
LINK = "http://www.asx.com.au/asx/research/companyInfo.do?by=asxCode&asxCode={0!s}"

def get_companies_list(url):
    root = lxml.html.fromstring(scraperwiki.scrape(url))

    options = root.cssselect("option")
    
    company = {}

    for row in options:
        parts = row.text_content().rpartition(")")
        company["symbol"] = parts[2][1:]
        company["name"] = parts[0][1:]
        company["link"] = LINK.format(company["symbol"])
        scraperwiki.sqlite.save(["symbol", "name", "link"], company)

for i in ASX_sectors:
    url = "http://www.asx.com.au/asx/markets/equityPrices.do?by=industryGroup&industryGroup=%s" %(ASX_sectors[i])
    get_companies_list(url)


# row returns Element object

# row.text_content() returns:
#(AAQ HOLDINGS LTD) AAQ
