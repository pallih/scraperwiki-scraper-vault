import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("workshop_2_1")

scrapings = scraperwiki.sqlite.select("* from 'workshop_2_1'.swdata")

#how do I go fetch the URL from this?

for scraping in scrapings:
    url = scraping["URL"]
    print url

    soup = BeautifulSoup(scraping["HTML"])
    title = soup.find("div", "fieldset-title corners-top").get_text().replace("English", "").strip()
    print title

