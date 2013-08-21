import scraperwiki
from string import Template
import re
from math import ceil
from BeautifulSoup import BeautifulSoup

start_page = scraperwiki.sqlite.get_var("current_page", 1) 
page = start_page 
num_pages = 1
max_pages = 100

html = scraperwiki.scrape("http://www.ic.gc.ca/eic/site/company-entreprises.nsf/eng/h_gu00029.html")
soup = BeautifulSoup(html)

for top_category_list in soup.findAll("ul")[3:]:
    for top_category in top_category_list.findAll("li"):
        top_category_url = "http://www.ic.gc.ca/eic/site/company-entreprises.nsf/eng/" + top_category.find("a")["href"]
        html2 = scraperwiki.scrape(top_category_url)
        soup2 = BeautifulSoup(html2)

        for category in soup2.findAll("ul")[3].findAll("li"):
            links = category.findAll("a")
            naics_code = links[0].text.replace("NAICS","").strip()
            naics_name = links[1].text.strip()

            html3 = scraperwiki.scrape(links[1]["href"])
            soup3 = BeautifulSoup(html3, fromEncoding="iso-8859-1")
            
            r = 0
            for row in soup3.findAll("table")[1].findAll("tr")[1:]:
                columns = row.findAll("td")
                if r % 2 == 0:
                    record = {"NAICS":naics_code, "NAICS_Name":naics_name, "Name":row.text.strip()}
                else:
                    m = re.search('estblmntNo=(\d+)', row.find("a")["href"])
                    record["ID"] = m.group(1)
                    if record.has_key('ID'):
                        #print record
                        # save records to the datastore
                        scraperwiki.sqlite.save(["ID"], record) 
                r += 1

        