###############################################################################
# Basic scraper
###############################################################################

import datetime
import scraperwiki
from BeautifulSoup import BeautifulSoup

BASE_URL = "http://www.cabinetoffice.gov.uk"

def scrape_page(url, unit_name):
    record = {"permalink": url, "department": unit_name}
    page = BeautifulSoup(scraperwiki.scrape(url))
    content = page.find("div", {"class":"grid-660 alpha contentblock"})
    # resource info
    for ri in content.find("div", {"class":"resource-info"}).findAll("p"):
        key, val = ri.text.split(":",1)
        if key == "Publication date":
            pub_date = val.split("/")
            record["given_on"] = datetime.date(int(pub_date[2]), int(pub_date[1]), int(pub_date[0]))
    record["title"] = content.find("h1", {"class":"title"}).text
    # TODO: text of the page?
    # Get all attached files
    files = {}
    for f in content.find("dl", {"id": "resource-library-items-wrapper"}).findAll("dt"):
        a = f.find("a")
        files[a.text] = a["href"]
    record["files"] = files
    # The raw text for further mining
    raw_text = content.text
    raw_text = raw_text[raw_text.find("</h1>")+5:]
    raw_text = raw_text[:raw_text.find('<div class="downloadfile">')]
    record["content"] = raw_text
    # Store record
    scraperwiki.sqlite.save(["permalink"], record)

# Loop over all units
page = BeautifulSoup(scraperwiki.scrape("http://www.cabinetoffice.gov.uk/resource-library/"))
unit_list = page.find("div", {"class": "grid-205"}).findAll("div", {"class": "left-news-nav"})[-1]
for unit in unit_list.findAll("li"):
    unit_name = " ".join(unit.find("a").text.split()[:-1])
    print unit_name
    unit_url = "http://www.cabinetoffice.gov.uk" + unit.find("a")["href"]
    print unit_url
    pagenum = 0
    while True: # Lots of pages just exit on first non-existent page
        print "page:", pagenum
        page = scraperwiki.scrape(unit_url+"?page=%d" % (pagenum))

        # Check if pagenum is to large and stop
        if (page.find('<li class="pager-current first">1</li>') > -1) and pagenum > 0:
            break # Pagenum is inconsistent with actual page

        bs = BeautifulSoup(page)
        items = bs.find("dl", {"class": "search-results apachesolr_search-results"})
        for i in items.findAll("dt", {"class":"title"}):
            url = BASE_URL+i.find("a")["href"]
            scrape_page(url, unit_name)
        
        if (pagenum == 0) and (page.find('<li class="pager-current first">1</li>') == -1):
            break
        pagenum += 1
        



    