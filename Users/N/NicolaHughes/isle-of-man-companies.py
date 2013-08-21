# Using OpenCorporates.com

import scraperwiki
from bs4 import BeautifulSoup

url = "http://opencorporates.com/companies/im?current_status=Live&page="

for n in range(6,980):
    html = scraperwiki.scrape(url + str(n))
    soup = BeautifulSoup(html)
    li_list = soup.find_all("li")
    for li in li_list[:30]:
        link = li.find("a")["href"]
        scraperwiki.sqlite.save(["url"], data={"url": link}, table_name="data")

