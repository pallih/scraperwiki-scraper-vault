import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("defence-contracts-all")

scrapings = scraperwiki.sqlite.select("* from 'defence-contracts-all'.swdata")

for scraping in scrapings:
    url = scraping["URL"]
    #print url

    soup = BeautifulSoup(scraping["HTML"])

    title = soup.find("div", "fieldset-title corners-top").get_text().replace("English", "").strip()
    #print title

links = soup.find("div","notice-header-details").get_text
print links
import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("defence-contracts-all")

scrapings = scraperwiki.sqlite.select("* from 'defence-contracts-all'.swdata")

for scraping in scrapings:
    url = scraping["URL"]
    #print url

    soup = BeautifulSoup(scraping["HTML"])

    title = soup.find("div", "fieldset-title corners-top").get_text().replace("English", "").strip()
    #print title

links = soup.find("div","notice-header-details").get_text
print links
