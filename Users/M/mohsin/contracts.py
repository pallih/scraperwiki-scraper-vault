import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("dod-contracts-html")

scrapings = scraperwiki.sqlite.select("* from `dod-contracts-html`.swdata")

for scraping in scrapings: 
    html = scraping["html"]
    soup = BeautifulSoup(html)
    title = soup.find("div", "fieldset-title corners-top")
    title = title.get_text().replace("English", "").strip()
    refnum = soup.find("div", "clearfix")
    refnum = refnum.get_text().replace("Reference number:", "").strip()
    print refnum




