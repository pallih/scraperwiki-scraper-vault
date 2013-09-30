import scraperwiki
from bs4 import BeautifulSoup

url = "http://old.iatistandard.org/codelists/organisation_identifier_bilateral"
html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)
table = soup.find("tbody")

for td in table.find_all("tr"): 
    code = td.find("td", "column-1").get_text()
    country = td.find("td", "column-2").get_text()
    abbrev = td.find("td", "column-3").get_text()
    name = td.find("td", "column-4").get_text()
    organisation = "bilateral" 
    data = {"Code": code, "Country": country, "Abbreviation": abbrev, "Name": name, "Organisation_type": organisation}
    scraperwiki.sqlite.save(["Name", "Code"], data)import scraperwiki
from bs4 import BeautifulSoup

url = "http://old.iatistandard.org/codelists/organisation_identifier_bilateral"
html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)
table = soup.find("tbody")

for td in table.find_all("tr"): 
    code = td.find("td", "column-1").get_text()
    country = td.find("td", "column-2").get_text()
    abbrev = td.find("td", "column-3").get_text()
    name = td.find("td", "column-4").get_text()
    organisation = "bilateral" 
    data = {"Code": code, "Country": country, "Abbreviation": abbrev, "Name": name, "Organisation_type": organisation}
    scraperwiki.sqlite.save(["Name", "Code"], data)