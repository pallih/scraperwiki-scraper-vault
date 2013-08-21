import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

url = 'http://www.ase.gr/content/en/MarketData/Stocks/Prices/Share_SearchResults.asp'

def get_company_list():
    root = lxml.html.parse(url).getroot()
    ASE =(root.find("body/table")
    .findall("tr")[8]
    .findall("td")[1]
    .find("table/tr")
    .findall("td")[1]
    .findall("table")[1]
    .findall("td")[0]
    .findall("table")[2])
    #print lxml.html.tostring(ASE)

    ASE=ASE[2:]

    for row in ASE:
        company = {}
        company["symbol"]=row.findall("td")[0].find("a").find("font").text
        company["link"]="http://www.ase.gr"+row.findall("td")[1].find("a").get("href")
        company["CID"]=row.findall("td")[1].find("a").get("href")[56:]
        company["name"]=row.findall("td")[1].find("a").find("font").text
        scraperwiki.sqlite.save(['symbol','name', 'link','CID'], company)

get_company_list()



